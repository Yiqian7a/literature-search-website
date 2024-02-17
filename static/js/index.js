

let first_load_js = {
    "home": true,
    "details": true,
    "history": true,
}

let currentPage = null;

function get_page(PageSign, privateData='') {
    if (PageSign === 'empty'){
        if (currentPage) {eval("exit_" + currentPage + "()")}
        document.querySelector('main').innerHTML = `<h1 style="color:white; text-align: center; margin-top: 30%">即将开放，敬请期待！</h1>`
        currentPage = null;
    }
    else {
        // 发送 AJAX 请求
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/index', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({page_sign: PageSign, private_data: privateData}));

        xhr.onload = function () {
            const response = JSON.parse(xhr.responseText);
            if (response.state === 200) {
                if (currentPage) {
                    // 使用exit_xxx()函数来终止运行中js，例如setTimeInterval
                    eval("exit_" + currentPage + "()")
                }

                document.getElementById("private-css").href = "/static/css/" + PageSign + ".css"
                document.querySelector(".main").innerHTML = response.privateHTML;

                if (first_load_js[PageSign]) {
                    // 添加新js
                    const newScript = document.createElement('script')
                    newScript.src = "/static/js/" + PageSign + ".js"
                    document.body.appendChild(newScript);
                } else {
                    eval("reload_" + PageSign + "()")
                }
                currentPage = PageSign
            }
        };

        xhr.onerror = function () {
            alert("页面请求失败");
        };
    }
}

// 获取浏览器网址栏的参数
let params = window.location.search.substring(1).split("&");
let searchPara = {};
for (let i = 0; i < params.length; i++) {
    let param = params[i].split("=");
    searchPara[param[0]] = param[1];
}


get_page('home')
if (searchPara.page === 'details') {
    get_page('details', searchPara.id)
}
else if (searchPara.page === 'history') {
    get_page('history')
}
