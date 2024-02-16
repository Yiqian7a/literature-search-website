
    let sign2title = {
        "home": "主页",
        "details": "",
        "history": "历史记录"
    }

    let first_load_js = {
        "home": true,
        "details": true,
        "history": true
    }

    let currentPage = null;

    function get_page(PageSign, privateData='') {
        // 发送 AJAX 请求
        let xhr = new XMLHttpRequest();
        xhr.open('POST', '/index', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({page_sign:PageSign, private_data:privateData}));

        xhr.onload = function () {
            const response = JSON.parse(xhr.responseText);
            if (response.state === 201) {
                if (currentPage){
                    // 使用exit_xxx()函数来终止运行中js，例如setTimeInterval
                    eval("exit_" + currentPage + "()")
                }

                document.getElementById("private-title").innerHTML = '文献搜索：' + sign2title[PageSign];
                document.getElementById("private-css").href = "/static/css/" + PageSign + ".css"
                document.querySelector(".main").innerHTML = response.privateHTML;

                if (first_load_js[PageSign]){
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
    get_page('home')