#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/videodev2.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#define LOG(...) printf(__VA_ARGS__)

struct buffer
{
    void* start;
    unsigned int length;
}*buffers;

void process_image(buffer *);

int main()
{
    int ret;

    LOG("program start\n");
    int fd=open("/dev/video1",O_RDWR);
    LOG("open return %d\n",fd);

/*    v4l2_cropcap vc;
    vc.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
    vc.bounds.left=0;
    vc.bounds.top=0;
    vc.bounds.width=640;
    vc.bounds.height=480;
    vc.defrect.left=0;
    vc.defrect.top=0;
    vc.defrect.width=640;
    vc.defrect.height=480;
    vc.pixelaspect.denominator=1;
    vc.pixelaspect.numerator=1;
    //ioctl(23, VIDIOC_CROPCAP, {type=V4L2_BUF_TYPE_VIDEO_CAPTURE, bounds={left=0, top=0, width=640, height=480},
            //defrect={left=0, top=0, width=640, height=480}, pixelaspect=1/1});
    ret=ioctl(fd,VIDIOC_CROPCAP,&vc);
    LOG("ret=%d\n",ret);
    long ty =V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ret=ioctl (fd,VIDIOC_STREAMOFF, &ty);
    LOG("ret=%d\n",ret);
    ret=ioctl (fd,VIDIOC_STREAMON, &ty);
    LOG("ret=%d\n",ret);
    return 0;*/

    //显示设备信息
    v4l2_capability cap;
    ret=ioctl(fd,VIDIOC_QUERYCAP,&cap);
    LOG("DriverName:%s\nCard Name:%s\nBus info:%s\nDriverVersion:%u.%u.%u\n",cap.driver,cap.card,cap.bus_info,(cap.version>>16)&0xFF,(cap.version>>8)&0xFF,cap.version&0xFF);
    if (!(cap.capabilities & V4L2_CAP_VIDEO_CAPTURE)) {
        LOG("not video capture");
        return -1;
    }
    if (!(cap.capabilities & V4L2_CAP_STREAMING)) {
        LOG("does not support streaming i/o");
        return -1;
    }
    //显示设备支持的格式
    v4l2_fmtdesc fmtdesc;
    fmtdesc.index=0;
    fmtdesc.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
    printf("Supportformat:\n");
    while(ioctl(fd,VIDIOC_ENUM_FMT,&fmtdesc)!=-1)
    {
        printf("\t%d.%s\n",fmtdesc.index+1,fmtdesc.description);
        fmtdesc.index++;
    }

    //显示当前帧格式
    v4l2_format fmt;
    fmt.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ioctl(fd,VIDIOC_G_FMT,&fmt);
    printf("Currentdata format information:\n\twidth:%d\n\theight:%d\n",fmt.fmt.pix.width,fmt.fmt.pix.height);
    fmtdesc.index=0;
    fmtdesc.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
    while(ioctl(fd,VIDIOC_ENUM_FMT,&fmtdesc)!=-1)
    {
        if(fmtdesc.pixelformat& fmt.fmt.pix.pixelformat)
        {
            LOG("\tformat:%s\n",fmtdesc.description);
            break;
        }
        fmtdesc.index++;
    }

    //设置像素格式
    fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_YUYV;
    fmt.fmt.pix.height = 480;
    fmt.fmt.pix.width = 640;
    fmt.fmt.pix.field = V4L2_FIELD_INTERLACED;

    if(ioctl(fd, VIDIOC_S_FMT, &fmt) == -1)
    {
        LOG("Unable to set format\n");
        return -1;
    }

    //读取设置
    if(ioctl(fd, VIDIOC_G_FMT, &fmt) == -1)
    {
        LOG("Unable to get format\n");
        return -1;
    }
    else{
         LOG("fmt.type:\t\t%d\n",fmt.type);
         LOG("pix.pixelformat:\t%c%c%c%c\n",fmt.fmt.pix.pixelformat & 0xFF, (fmt.fmt.pix.pixelformat >> 8) & 0xFF,(fmt.fmt.pix.pixelformat >> 16) & 0xFF, (fmt.fmt.pix.pixelformat >> 24) & 0xFF);
         LOG("pix.height:\t\t%d\n",fmt.fmt.pix.height);
         LOG("pix.width:\t\t%d\n",fmt.fmt.pix.width);
         LOG("pix.field:\t\t%d\n",fmt.fmt.pix.field);
    }

    //申请一个四个帧的缓冲区
    v4l2_requestbuffers req;
    req.count=4;
    req.type=V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory=V4L2_MEMORY_MMAP;
    ioctl(fd,VIDIOC_REQBUFS,&req);

    //MMAP
    buffers =(buffer*)calloc (req.count, sizeof (*buffers));
    if (!buffers) {
        LOG("Out of memory\n");
        exit(EXIT_FAILURE);
    }
    for (unsigned int n_buffers = 0; n_buffers < req.count; ++n_buffers) {
        struct v4l2_buffer buf;
        memset(&buf,0,sizeof(buf));
        buf.type =V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory =V4L2_MEMORY_MMAP;
        buf.index =n_buffers;
        // 查询序号为n_buffers 的缓冲区，得到其起始物理地址和大小
        if (-1 == ioctl(fd, VIDIOC_QUERYBUF, &buf))
            exit(-1);
        buffers[n_buffers].length= buf.length;
        LOG("buffers[%d].length=%d\n",n_buffers,buf.length);
        // 映射内存
        buffers[n_buffers].start=mmap(NULL,buf.length,PROT_READ | PROT_WRITE ,MAP_SHARED,fd, buf.m.offset);
        if (MAP_FAILED== buffers[n_buffers].start)
            exit(-1);
    }

    //把四个缓冲区放入队列并启动数据流
    unsigned int i;
    enum v4l2_buf_type type;
    for (i = 0; i< 4; ++i)
    {
        v4l2_buffer buf;
        buf.type =V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory =V4L2_MEMORY_MMAP;
        buf.index = i;
        ret=ioctl (fd,VIDIOC_QBUF, &buf);
        LOG("ioctl1 return %d\n",ret);
    }
    type =V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ret=ioctl (fd,VIDIOC_STREAMON, &type);
    LOG("ioctl2 return %d\n",ret);
    if(ret!=0)
        return -1;

    //
    while(1){
        v4l2_buffer buf;
        buf.type =V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory =V4L2_MEMORY_MMAP;
        // 从缓冲区取出一个缓冲帧
        ioctl (fd,VIDIOC_DQBUF, &buf);
        // 图像处理
        process_image(buffers+buf.index);
        LOG("buf.index=%d\n",buf.index);
        // 将取出的缓冲帧放回缓冲区
        ioctl (fd, VIDIOC_QBUF,&buf);
        sleep(1);
    }
    close(fd);
    return 0;
}

void process_image(buffer *_buf)
{
    const unsigned char* buf=(const unsigned char*)_buf->start;
    for(int i=0;i<100;i++)
    {
        LOG("%2x",buf[i]);
    }
    LOG("\nprocess image end\n");
}
