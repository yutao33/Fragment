function getGrayData(d){
    var len=d.length/4;
    var arr=new Int32Array(len);
    for(var i=0;i<len;i++){
        var r=d[i*4];
        var g=d[i*4+1];
        var b=d[i*4+2];
        var gray = (r*19595 + g*38469 + b*7472) >> 16;
        arr[i]=gray;
    }
    return arr;
}

function getonepage(ds){
    var tbody=document.getElementsByTagName('tbody')
    var tbody1=tbody[1]
    var trs = tbody1.children

    var len = (trs.length-2)/2;
    for(var i=0;i<len;i++){
        var k = i*2+1;
        var question = trs[k].children;
        var type = question[0].innerText;
        var qimg = question[1].getElementsByTagName('img')[0];
        ct.drawImage(qimg,0,0);
        var imgdata = ct.getImageData(0,0,targetwidth,targetheight)
        var data = getGrayData(imgdata.data)
        var fonts = trs[k+1].getElementsByTagName('font');
        var answer = fonts[0].innerText;
        answer =  answer.trim(' ');
        ds.push({type:type,data:data,answer:answer})
    }
}

var targetheight=16
var targetwidth=500

var canvas = document.createElement('canvas')
canvas.height=targetheight
canvas.width=targetwidth
var banner = document.getElementById('banner')
banner.append(canvas)

var ct = canvas.getContext('2d')

var ds=[]
var page=1

function menuClick(v_url,iniframe,iframeHight){
    updateDiv(v_url,"nrzs",function(){
        setTimeout(function(){
            console.log('11')
        },0)
    },iniframe,iframeHight);
}




