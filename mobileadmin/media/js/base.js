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
