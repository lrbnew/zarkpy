(function(){

    var namespace = 'api';
    var base_uri = '/api/';
    var apis = {
        isLogin: {url:'user/profile?action=isLogin'},
        login: {url:'user/profile?action=login&email={email}&password={password}&remember_me={remember_me}'},
        deleteUserImage: {url:'user-image?action=delete&UserImageid={UserImageid}'}
        
    };

    var isFunction = function( fn ) {
        return !!fn && typeof fn != "string" && !fn.nodeName &&
            fn.constructor != Array && /function/i.test( fn + "" );
    }
    var buildURL = function(url, params){
        var tmp = url.split("?");
        var uri = tmp[0];
        var ps = null;
        if (tmp.length > 1) ps = tmp[1].split("&");
        var pnames = uri.match(/{\w+}/g);
        if (pnames != null) {
            for (var i=0; i<pnames.length; ++i){
                var pn = pnames[i];
                var ppn = pnames[i].match(/{(\w+)}/)[1];
                if (!params[ppn]) return null;
                else uri = uri.replace(pn, params[ppn]);
            }
        }
        if (!ps) return uri;
        var re_ps = [];
        for (var i=0; i<ps.length; ++i) {
            var tmp = ps[i].match(/{(\w+)}/);
            if (tmp==null) re_ps.push(ps[i]);
            else {
                var pn = tmp[0];
                var ppn = tmp[1];
                if (typeof params[ppn] !== 'undefined')
                    re_ps.push(encodeURI(ps[i].replace(pn, params[ppn])));
            }
        }
        if (re_ps.length>0) return [uri, re_ps.join("&")].join("?");
        else return uri;
    }
    var jsc = (new Date).getTime();
    var buildTempFunction = function(cb){
        var jsonp = "jsonp" + jsc++;
        window[ jsonp ] = function(data){
            cb(data);
            // Garbage collect
            window[ jsonp ] = undefined;
            try{ delete window[ jsonp ]; } catch(e){}
        };
        return jsonp;
    }
    var sendScriptRequest = function(url){
        var head = document.getElementsByTagName("head")[0];
        var script = document.createElement("script");
        script.src = url;
        script.charset = 'utf-8';
        head.appendChild(script);
    }
    var formatParams = function(params) {
        if (isFunction(params.callback)) params.callback = buildTempFunction(params.callback);
        return params;
    }
    var send = function(url, params){
        var url = buildURL(url, params);
        if (url!=null) sendScriptRequest(url);
    }

    var cp = 'callback={callback}';
    var testing = 'test={test}';
    var successcallback = 'successcallback={successcallback}';
    for (var name in apis) {
        if (apis[name].url.search(/\?/)!=-1) apis[name].url = base_uri + apis[name].url + '&' + cp + '&' + testing;
        else apis[name].url = base_uri + apis[name].url + '?' + cp + '&' + testing;
    }

    if (!window[namespace]) window[namespace] = {};
    var api_obj = window[namespace];
    for (var name in apis) {
        api_obj[name] = (function(url){
            return function(params){
                if (params === undefined) {
                    params={};
                };
                send(url, formatParams(params));
            };
        })(apis[name].url)
    }

})()
