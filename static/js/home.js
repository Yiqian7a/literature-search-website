
// 切换图片
let slider = document.querySelector('.slider');
let currentIndex = 0;

setInterval(function () {
    let imageWidth = document.querySelector('.slider img').clientWidth;
    currentIndex++;
    if (currentIndex >= slider.children.length) {
        currentIndex = 0;
    }
    let newPosition = -currentIndex * imageWidth;
    slider.style.transform = 'translateX(' + newPosition + 'px)';
}, 3000);


let literatureData = [];
let keyWord

const literatureContainer = document.getElementById('literature-container');
let loadedNum = 0;
const literaturePerPage = 5;

let randomSearch = false;
function search() {
    keyWord = document.getElementById('search-input').value
    // 发送 AJAX 请求
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/search', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(keyWord));

    xhr.onload = function () {
        const response = JSON.parse(xhr.responseText);
        if (response.state === 201) {
            if (keyWord == '') {
                if (randomSearch) {
                    // 前一次为随机推荐，继续随机
                    literatureData = literatureData.concat(response.data);
                }
                else {
                    // 第一次随机推荐或搜索后再随机推送，先清空现有的文献，恢复页面
                    literatureContainer.innerText = ''
                    literatureData = []
                    loadedNum = 0
                    literatureData = literatureData.concat(response.data);
                    randomSearch = true;
                    loadContent();
                }
            }
            else {
                // 搜索前先清空现有的文献
                literatureContainer.innerText = ''
                literatureData = response.data
                loadedNum = 0
                randomSearch = false;
                loadContent();
            }
        }
    };
    xhr.onerror = function () {
        alert("请求失败");
    };
}

async function loadContent() {
    keyWord = document.getElementById('search-input').value
    console.log("kw:", keyWord);
    const remainCount = document.getElementById('remain-count')
    let remainCounts = literatureData.length - loadedNum;
    console.log("li:",literatureData)
    console.log("1remainingCounts:", remainCounts);
    console.log('1loaded content', loadedNum)
    // 对现有的文献结果进行高亮或增添
    if (keyWord === ''){
        // 没有搜索，随机推送
        if (remainCounts <= literaturePerPage) {
            search(''); // 页面显示了所有结果，再随机推送一次
        }
        remainCount.innerHTML = '点击查看更多文献';
        remainCount.addEventListener('click', loadContent);
    }
    else {
        // 用户搜索，创建正则表达式匹配关键词，高亮搜索结果
        if (literatureData.length === 0) {
            remainCount.innerHTML = '没有找到相关文献';
            remainCount.removeEventListener('click', loadContent);
            return false; // 只是为了退出函数
        }
        else {
            // 高亮显示搜索字符
            let regex = new RegExp(keyWord, 'gi');
            for (let i = 0; i <= Math.min(literaturePerPage, remainCounts)-1; i++) {
                const literatureItem = literatureData[loadedNum + i];
                // 用标亮后的html替换原来的数据
                literatureData[loadedNum + i].TI = literatureItem.TI.replace(regex, '<span style="background-color: yellow;">$&</span>');
                literatureData[loadedNum + i].AU = literatureItem.AU.replace(regex, '<span style="background-color: yellow;">$&</span>');
            }
        }
    }

     // 每次滚动最多加载5条数据
    for (let i = 1; i <= Math.min(literaturePerPage, remainCounts); i++) {
        const literatureElement = document.createElement("div");
        const literatureItem = literatureData[loadedNum];
        literatureElement.classList.add("literature-item");
        literatureElement.innerHTML = `
            <a onclick="get_page('details', '${literatureItem.id}')"><h2>&nbsp;&nbsp;${literatureItem.TI}</h2></a>
            <p>作者：${literatureItem.AU}</a></p>
            <p>发布日期：${literatureItem.PY} ${literatureItem.PD}</a></p>
        `;
        literatureContainer.appendChild(literatureElement);
        loadedNum += 1
    }

    remainCounts = literatureData.length - loadedNum
    if (keyWord !== ''){
        if (remainCounts === 0) {
            remainCount.innerHTML = '没有更多相关文献了';
            remainCount.removeEventListener('click', loadContent);
        }
        else {
            remainCount.innerHTML = `点击查看剩下${remainCounts}条结果`;
            remainCount.addEventListener('click', loadContent);
        }
    }

    console.log("2remainingCounts:", remainCounts);
    console.log('2loaded content', loadedNum)
}

document.getElementById('search-button').addEventListener('click', search);
loadContent()



