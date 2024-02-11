
var sign2title = {
            "home": "主页",
            "details": "",
            "history": "历史记录"
        }

function get_page(PageSign) {
    // 发送 AJAX 请求
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/index', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(PageSign));

    xhr.onload = function () {
        const response = JSON.parse(xhr.responseText);
        if (response.state === 201) {
            document.getElementById("private-title").innerHTML = '文献搜索：' + sign2title[PageSign];
            document.getElementById("private-css").href = "/static/css/" + PageSign + ".css"
            document.getElementById("private-js").src= "/static/js/" + PageSign + ".js"
            document.querySelector(".main").innerHTML = response.privateHTML;
            window.privateData = response.data;
        }
    };

    xhr.onerror = function () {
        alert("页面请求失败");
    };
}


get_page("home")
