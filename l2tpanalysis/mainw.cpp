#include "mainw.h"
#include "ui_mainw.h"

#include <linux/if_ether.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <linux/tcp.h>
#include <netinet/in.h>

#include <QTextStream>

struct l2tphdr{
    __u8 prioritybit:1;
    __u8 offsetbit:1;
    __u8 pad0:1;
    __u8 seqbit:1;
    __u8 pad1:2;
    __u8 lenbit:1;
    __u8 typebit:1;

    __u8 version:4;
    __u8 pad2:4;

    __u16 length;
    __u16 tunnelid;
    __u16 Ns;
    __u16 Nr;

    int gel2tplen(){
        int l=2;
 /*       if(this->lenbit){
            l=ntohs(this->length);
        }
        else{
            l+=4;//tunnel id session id
            if(this->seqbit)l+=4;
            if(this->offsetbit){
                //TODO:
            }
        }*/
          if(this->lenbit){
                   l+=2;
               }

                   l+=4;//tunnel id session id
                   if(this->seqbit)l+=4;
                   if(this->offsetbit){
                       //TODO:
                   }

        return l;
    }
};

struct ppphdr{
    __u8 addr;
    __u8 ctl;
    __u16 protocol;
};



//全局变量
pcap_if_t* _interfaces;
pcap_t* _pcap;
char _errbuf[PCAP_ERRBUF_SIZE];

int _port=1701;

//---------------------

QString ip2qstr(unsigned int ip_net)
{
    unsigned char*p=(unsigned char*)&ip_net;
    return QString::asprintf("%d.%d.%d.%d",p[0],p[1],p[2],p[3]);
}
QString ipport2qstr(unsigned int ip_net,unsigned short port_net)
{
    unsigned char*p=(unsigned char*)&ip_net;
    return QString::asprintf("%d.%d.%d.%d:%d",p[0],p[1],p[2],p[3],ntohs(port_net));
}


//----------------------
QString ipv4_parse(unsigned char*partdata)//final
{
    QString str;
    QTextStream qs(&str);
    iphdr* ipp=(iphdr*)partdata;
    if(ipp->protocol==IPPROTO_UDP){
        udphdr* upp=(udphdr*)partdata+ipp->ihl*4;
        qs<<"UDP:"<<ipport2qstr(ipp->saddr,upp->source)
         <<" ----> "<<ipport2qstr(ipp->daddr,upp->dest)<<endl;
    }
    else if(ipp->protocol==IPPROTO_TCP)
    {
        tcphdr* tpp=(tcphdr*)partdata+ipp->ihl*4;
        qs<<"TCP:"<<ipport2qstr(ipp->saddr,tpp->source)
         <<" ----> "<<ipport2qstr(ipp->daddr,tpp->dest)<<endl;
    }
    else{
        qs<<"Other IP expect TCP or UDP"<<endl;
    }
    return str;
}

QString ppp_lcp_parse(unsigned char* partdata)//final
{
    QString str;
    QTextStream qs(&str);
    const char*code[]={
        "Configure-Request",
        "Configure-Ack",
        "Configure-Nak",
        "Configure-Reject",
        "Terminate-Request",
        "Terminate-Ack",
        "Code-Reject",
        "Protocol-Reject",
        "Echo-Request",
        "Echo-Reply",
        "Discard-Request"
    };
    struct lcp{
        __u8 code;
        __u8 id;
        __u16 length;
    }* p=(lcp*)partdata;
    if(p->code>=1&&p->code<=11){
        qs<<code[p->code-1]<<endl;
    }
    else{
        qs<<"Unknown Code"<<endl;
    }
    return str;
}
QString ppp_ipcp_parse(unsigned char* partdata)//final
{
    QString str;
    QTextStream qs(&str);
    const char*code[]={
        "Configure-Request",//1
        "Configure-Ack",//2
        "Configure-Nak",//3
        "Configure-Reject",//4
        "Terminate-Request",//5
        "Terminate-Ack",//6
        "Code-Reject"//7
    };
    struct ipcp{
        __u8 code;
        __u8 id;
        __u16 length;
    }* p=(ipcp*)partdata;
    if(p->code>=1&&p->code<=7){
        qs<<code[p->code-1]<<endl;
    }
    else{
        qs<<"Unknown Code"<<endl;
    }
    return str;
}
QString ppp_chap_parse(unsigned char* partdata)//final
{
    QString str;
    QTextStream qs(&str);
    const char*code[]={
        "Challenge",//1
        "Response",//2
        "Success"//3
    };
    struct chap{
        __u8 code;
        __u8 id;
        __u16 length;
    }* p=(chap*)partdata;
    if(p->code>=1&&p->code<=3){
        qs<<code[p->code-1]<<endl;
    }
    else{
        qs<<"Unknown Code"<<endl;
    }
    return str;
}


QString ppp_parse(unsigned char*partdata)
{
    QString str;
    QTextStream qs(&str);
    ppphdr* pp=(ppphdr*)partdata;
    qs<<"##PPP ";
    switch(pp->protocol){
    case 0x21C0:
        qs<<"LCP"<<endl;
        qs<<ppp_lcp_parse(partdata+4);
        break;
    case 0x23C2:
        qs<<"CHAP"<<endl;
        qs<<ppp_chap_parse(partdata+4);
        break;
    case 0x23C0:
        qs<<"PAP"<<endl;
        break;
    case 0x2180:
        qs<<"IPCP"<<endl;
        qs<<ppp_ipcp_parse(partdata+4);
        break;
    case 0x25C0:
        qs<<"LQR"<<endl;
        break;
    case 0xFD80:
        qs<<"CCP"<<endl;
        break;
    case 0x2100:
        qs<<"IPv4"<<endl;
        qs<<ipv4_parse(partdata+sizeof(ppphdr));
        break;
    default:
        qs<<"Unknown"<<QString::asprintf("%x",pp->protocol)<<endl;
        break;
    }
    return str;
}

QString l2tp_avp_parse(unsigned char*partdata,int len)//final
{
    QString str;
    QTextStream qs(&str);
    const struct{
        int n;
        const char* s;
    } code[]={
    {1,"Start Control Request"},
    {2,"Start Control Reply"},
    {3,"Start Control Connected"},
    {10,"Incoming Call Request"},
    {11,"Incoming Call Reply"},
    {12,"Incoming Call Connected"},
    {14,"Call Disconnect Notification"},
    {4,"Stop Control Notification"},
    {6,"Hello"}
    };
    int num=9;
    struct avp{
        __u16 len:10;
        __u16 pad:4;
        __u16 h:1;
        __u16 m:1;
        __u16 id;
        __u16 type;
        __u16 ctltype;//only for control message
    }* p=(avp*)partdata;

    if(len>=sizeof(avp)){
    //if(len!=12){
        if(p->h==0&&p->type==0){
            int i=0;
            for(;i<num;i++){
                if(ntohs(p->ctltype)==code[i].n){
                    qs<<code[i].s<<endl;
                    break;
                }
            }
            if(i==num){
                qs<<"other control message"<<endl;
            }
        }
        else{
            qs<<"Others Unknown"<<endl;
        }
    }
    else if(len==0){
    //else{
        qs<<"Zero Length Bit message"<<endl;
    }
    else{
        qs<<"Others Unknown"<<endl;
    }
    return str;
}

QString l2tp_parse(unsigned char* partdata,int len)
{
    QString str;
    QTextStream qs(&str);
    l2tphdr* lpp=(l2tphdr*)partdata;
    int lhl=lpp->gel2tplen();

    if(lpp->typebit){
        qs<<"#L2TP Control Message"<<endl;
        qs<<l2tp_avp_parse(partdata+lhl,len-lhl);
    }
    else{
        qs<<"#L2TP Payload"<<endl;
        qs<<ppp_parse(partdata+lhl);
    }
    return str;
}

void Thread::run()
{
    pcap_pkthdr pphdr;
    while(1){
        const unsigned char*data=pcap_next(_pcap,&pphdr);
        int minlen=sizeof(ethhdr)+sizeof(iphdr)+sizeof(udphdr);
        if(data&&pphdr.caplen>=minlen){
            ethhdr* ethp=(ethhdr*)data;
            if(ntohs(ethp->h_proto)==ETH_P_IP){
                iphdr* ipp=(iphdr*)(data+sizeof(ethhdr));
                if(ipp->protocol==IPPROTO_UDP){
                    const unsigned char*pp=data+sizeof(ethhdr)+ipp->ihl*4;
                    udphdr* upp=(udphdr*)pp;
                    if(ntohs(upp->source)==_port||
                            ntohs(upp->dest)==_port){
                        QString str;
                        QTextStream qs(&str);
                        qs<<ip2qstr(ipp->saddr)<<":"<<ntohs(upp->source)
                         <<" ----> "<<ip2qstr(ipp->daddr)<<":"<<ntohs(upp->dest)<<endl;

                        unsigned char*partdata=(unsigned char*)upp+sizeof(udphdr);
                        int len=pphdr.caplen-(partdata-data);
                        qs<<l2tp_parse(partdata,len);
                        emit work_print(str);
                    }
                }
            }
        }
    }
}


//一开始获取所有网络接口
QStringList getdevs()
{
    QStringList qsl;
    pcap_if_t*inf1;
    if(pcap_findalldevs(&_interfaces,_errbuf)==0){
        inf1=_interfaces;
        int count=0;
        while(inf1){
            qsl.append(inf1->name);
            inf1=inf1->next;
            count++;
        }
        QString str;
        str.sprintf("枚举到%d个接口",count);
        QMessageBox::information(NULL,"info",str);
    }
    else{
        QMessageBox::information(NULL,"error","aren't able to pcap_findalldevs");
    }
    return qsl;
}

//打开一个接口
bool opendev(int n)
{
    pcap_if_t*inf=_interfaces;
    while(n--)inf=inf->next;
    _pcap=pcap_open_live(inf->name,65535,0,0,_errbuf);
    if(!_pcap){
        QMessageBox::information(NULL,"error","aren't able to pcap_open_live");
        qDebug()<<_errbuf;
        return false;
    }
    return true;
}


//--MainW窗口类
MainW::MainW(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainW)
{
    ui->setupUi(this);
    QStringList qsl=getdevs();
    ui->comboBox->addItems(qsl);
    if(qsl.length()>0){
        ui->buttonstart->setEnabled(true);
    }
}

MainW::~MainW()
{
    delete ui;
}


void MainW::on_buttonstart_clicked()
{
    int i=ui->comboBox->currentIndex();
    if(opendev(i)){
        workthread=new Thread();
        connect(workthread,SIGNAL(work_print(QString)),this,SLOT(on_work_print(QString)));
        workthread->start();
        ui->buttonstart->setEnabled(false);
        ui->buttonstop->setEnabled(true);
    }
}

void MainW::on_buttonstop_clicked()
{
    ui->buttonstart->setEnabled(true);
    ui->buttonstop->setEnabled(false);
    workthread->terminate();
    workthread->wait();
    workthread=NULL;
    ui->plainTextEdit->clear();
}

void MainW::on_work_print(QString s)
{
    qDebug()<<s;
    ui->plainTextEdit->appendPlainText(s);
}
