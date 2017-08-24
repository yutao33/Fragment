
gMap = {}

deleteList = []

api=require("disk-system:widget/system/fileService/fileManagerApi/fileManagerApi.js")

function deletefile(start){
    console.log(start);
    if(start>=deleteList.length){
        return;
    }
    var s1=start;
    var s2=start+100;
    if(s2>deleteList.length){
        s2=deleteList.length;
    }
    var list=[];
    for(var i = s1;i<s2;i++){
        list.push(deleteList[i])
    }
    api.deleteFiles(list,function back(a,b,c){
        console.log(a)
        console.log(b)
        console.log(c)
        if(b=="删除成功"){
            deletefile(s2);
        }
    },null)
}

function gotit(){
    md5list=[];
    filesll=[];
    for(var i in gMap){
        var fll = gMap[i];
        if(i.length==32 && fll.length>1){
            md5list.push(i);
            filesll.push(fll);
        }
    }
    gMap=null;
    for(var i=0;i<filesll.length;i++){
        list = filesll[i];
        var selected=-1;
        var maxlevel=0;
        for(var k=0;k<list.length;k++){
            var fn = list[k];
            var level=0;
            for(var pos=0;pos<fn.length;pos++){
                if(fn[pos]=='/'){
                    level++;
                }
            }
            if(maxlevel<level){
                maxlevel=level;
                selected=k;
            }
        }
        for(var k=0;k<list.length;k++){
            if(k!=selected){
                deleteList.push(list[k]);
            }
        }
    }
    console.log("get list");
    //deletefile(0);
}

var name = "FileSystem"
var version = 1
var request=window.indexedDB.open(name,version);
request.onerror=function(e){
    console.log(e.currentTarget.error.message);
};
request.onsuccess=function(e){
    var db=e.target.result;
    var trans = db.transaction(["fileList"], "readonly");
    var store = trans.objectStore("fileList");
    var cursor = store.openCursor();
    cursor.onsuccess = function(e){
        var res = e.target.result;
        if(res){
            //console.log(res)
            var k=res.key;
            var v=res.value;
            var md5=v.md5;
            if(v.size>1024*1024*512){
                if(gMap.hasOwnProperty(md5)){
                    gMap[md5].push(k)
                    //console.log(k)
                } else {
                    gMap[md5]=[k]
                }
            }
            res.continue();
        } else {
            gotit();
        }
    }
};
