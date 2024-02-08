
function search() {
    const searchInput = document.getElementById('search-input').value;
    window.location.href = '/index?search_key=' + encodeURIComponent(searchInput);
}

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
    xhr.send(JSON.stringify({PageSign: PageSign}));

    xhr.onload = function () {
        const response = JSON.parse(xhr.responseText);
        console.log(sign2title[PageSign]);
        if (response.state === 201) {
            document.getElementById("private-title").innerHTML = '文献搜索：' + sign2title[PageSign];
            document.getElementById("private-css").href = "/static/css/" + PageSign + ".css"
            document.getElementById("private-js").src= "/static/js/" + PageSign + ".js"
            document.querySelector(".main").innerHTML = "templates/" + PageSign + ".html"
            window.privateData = response.data;
            console.log(window.privateData);
        }
    };

    xhr.onerror = function () {
        alert("请求失败");
    };
}

get_page("home")
