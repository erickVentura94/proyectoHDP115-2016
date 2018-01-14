var sse3 = function () {
    var speed = 8;
    return {
        initMenu: function () {
            var m = document.getElementById('sses3');
            if (!m) return;
            m.style.width = m.getElementsByTagName("ul")[0].offsetWidth + 1 + "px";
            var lis = m.getElementsByTagName('li');
            var a = m.getElementsByTagName("a");
            var url = document.location.href.toLowerCase();
            var k = -1;
            var nLength = -1;
            var slip = [];

            for (i = 0; i < a.length; i++) {
                if (url.indexOf(a[i].href.toLowerCase()) != -1 && a[i].href.length > nLength) {
                    k = i;
                    nLength = a[i].href.length;
                }
            }
            if (k == -1 && /:\/\/(?:www\.)?[^.\/]+?\.[^.\/]+\/?$/.test) {
                for (var i = 0; i < a.length; i++) {
                    if (a[i].getAttribute("maptopuredomain") == "true") {
                        k = i;
                        break;
                    }
                }
                if (k == -1 && a[0].getAttribute("maptopuredomain") != "false")
                    k = 0;
            }

            for (var i = 0; i < lis.length; i++) {

                slip[i] = document.createElement('div');
                slip[i].className = 'slip';
                slip[i].style.width = lis[i].offsetWidth + "px";
                slip[i].style.height = lis[i].offsetHeight + "px";
                slip[i].style.left = lis[i].offsetWidth + 1 + "px"; // +1 to eliminate an gap color in IE5 or No DOCTYPE
                lis[i].appendChild(slip[i]);

                lis[i].onmouseover = function () {
                    clearInterval(this.t);
                    sse3.move(this, 0);
                };
                lis[i].onmouseout = function () {
                    clearInterval(this.t);
                    sse3.move(this, 1);
                }
            }
            if (k > -1) {
                slip[k].style.display = 'none';
                lis[k].className = 'current';
            }
        },
        move: function (li, direction) {
            var tabs = li.childNodes;
            var slipobj = tabs[tabs.length - 1];
            if (direction == 0) {
                li.t = setInterval(function () { if (slipobj.offsetLeft <= 0) { clearInterval(li.t); } else { sse3.moveLeft(slipobj); } }, 15);
            }
            else {
                li.t = setInterval(function () { if (slipobj.offsetLeft >= slipobj.offsetWidth) { clearInterval(li.t); } else { sse3.moveRight(slipobj); } }, 15);
            }
        },
        moveLeft: function (obj) {
            if (obj.offsetLeft < 3) {
                obj.style.left = "0px";
            }
            else {
                obj.style.left = obj.offsetLeft-Math.ceil(obj.offsetLeft / speed) + "px";
            }
        },
        moveRight: function (obj) {
            obj.style.left = obj.offsetLeft + 3 + "px";
        }
    };
} ();

if (window.addEventListener) {
    window.addEventListener("load", sse3.initMenu, false);
}
else if (window.attachEvent) {
    window.attachEvent("onload", sse3.initMenu);
}
else {
    window["onload"] = sse3.initMenu;
}