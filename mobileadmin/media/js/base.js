addEventListener("load", function() {
    setTimeout(updateLayout, 0);
}, false);

var currentWidth = 0;
function updateLayout() {
    if (window.innerWidth != currentWidth) {
        currentWidth = window.innerWidth;
        var orient = currentWidth == 320 ? "profile" : "landscape";
        document.body.setAttribute("orient", orient);
        setTimeout(function() {
            window.scrollTo(0, 1);
        }, 100);            
    }
}
setInterval(updateLayout, 400);

function $(ele) {
    return document.getElementById(ele);
}
function hasClass(ele,cls) {
    return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}
function addClass(ele,cls) {
    if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}
function removeClass(ele,cls) {
    if (hasClass(ele,cls)) {
        var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
        ele.className=ele.className.replace(reg,' ');
    }
}
function addAndRemoveClass(ele,_new,_old) {
    addClass(ele,_new);
    removeClass(ele,_old);
}
function tabSwitcher(tabLabels) {
    function toggle() {
        toActivate = this.id.substr(1);
        toDeactivate = tabLabels[toActivate];
        $(toDeactivate).removeAttribute('selected');
        $(toActivate).setAttribute('selected', 'true'); 
        addAndRemoveClass($(this.id), 'active', 'inactive');
        addAndRemoveClass($("_"+toDeactivate), 'inactive', 'active');
    }
    for (label in tabLabels) {
        $("_"+label).addEventListener("click", toggle, false);
    }
}

function getElementsByClassName(className, tag, elm){
    var testClass = new RegExp("(^|\\s)" + className + "(\\s|$)");
    var tag = tag || "*";
    var elm = elm || document;
    var elements = (tag == "*" && elm.all)? elm.all : elm.getElementsByTagName(tag);
    var returnElements = [];
    var current;
    var length = elements.length;
    for(var i=0; i<length; i++){
        current = elements[i];
        if(testClass.test(current.className)){
            returnElements.push(current);
        }   
    }
    return returnElements;
}

function createCookie(value, age, path, secure) {
    var cookie = "mobileadmin="+escape(value);
    var date = new Date();
    date.setTime(date.getTime()+(age*1000));
    cookie += "; expires="+date.toGMTString();
    cookie += "; path=/" + path;
    if (secure)
        cookie += "; secure";
    document.cookie = cookie;
}

function toggle(age, path, secure) {
    var toggle_link = $('mobileadmin_toggle');
}

var toggle_link = document.createElement('a');
toggle_link.setAttribute('href','');
var toggle_link_text = document.createTextNode("toggle")
toggle_link.appendChild(toggle_link_text);
var user_tools = getElementsByClassName('user-tools');
alert(user_tools);
user_tools[0].appendChild(toggle_link);
