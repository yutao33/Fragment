#!/usr/bin/node

http = require('http')

options = {
    socketPath: "/var/run/docker.sock",
    path: "/images/json?all=1",
}

var req = http.request(options, (res) => {
    res.on('data', (data) => {
        var d = data.toString();
        var obj = JSON.parse(data);
        var nodes = [];
        var m = new Map();
        for (var i in obj) {
            var d = obj[i];
            if (d.RepoTags == null) {
                d.RepoTags = "null:" + d.Id.substring(7, 15);
            }
            m.set(d.Id, [i, d.ParentId, d.RepoTags]);
            var n = `node${i}[shape=box,label="${d.RepoTags}"];`;
            nodes.push(n);
        }

        var links = [];

        m.forEach((v, k) => {
            if (v[1] != "") {
                var vv = m.get(v[1]);
                if (vv) {
                    links.push(`node${vv[0]}->node${v[0]};`);
                }
            }
        })

        str = `digraph{\n${nodes.join("\n")}\n${links.join("\n")}\n}`;


        console.log(str);
    })
})


req.on('error', (e) => {
    console.log(`problem with request: ${e.message}`);
});


req.end();