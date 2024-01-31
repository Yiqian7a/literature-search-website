window.onload = function() {

    console.log("li", literatureData)
    console.log("kw", keyWord)
    // 获取文献容器
    const literatureContainer = document.getElementById("literature-container");

    if (keyWord != '') {
        console.log("keyWord not null");
        // 创建正则表达式，用于匹配关键词
        var regex = new RegExp(keyWord, 'gi');
        var searchInput = document.getElementById('search-input');
        console.log(searchInput)
        searchInput.value = keyWord;
    }

    if (literatureData != '') {
        // 每页显示的文献数
        const literaturePerPage = 5;

        // 计算总页数
        const totalPages = Math.ceil(literatureData.length / literaturePerPage);

        // 初始化当前页码
        let currentPage = 1;
        // 获取翻页容器
        const paginationContainer = document.querySelector(".pagination");

        // 显示当前页的文献
        function showPage(page) {
            // 更新当前页码
            currentPage = page;

            // 计算起始索引和结束索引
            const startIndex = (page - 1) * literaturePerPage;
            const endIndex = startIndex + literaturePerPage;

            // 清空文献容器中的内容
            literatureContainer.innerHTML = "";

            // 遍历文献数据，显示当前页的文献
            for (let i = startIndex; i < endIndex && i < literatureData.length; i++) {
                const literatureItem = literatureData[i];
                const literatureElement = document.createElement("div");
                if (keyWord != '' && keyWord != null) {
                    var literatureTI = literatureItem.TI.replace(regex, '<span style="background-color: yellow;">$&</span>');
                    var literatureAU = literatureItem.AU.replace(regex, '<span style="background-color: yellow;">$&</span>')
                } else {
                    var literatureTI = literatureItem.TI
                    var literatureAU = literatureItem.AU
                }
                // console.log(literatureTI)
                literatureElement.addEventListener("click", function (event) {
                    // 判断点击的元素是否为文献标题或内容
                    if (event.target.classList.contains("literature-link")) {
                        window.location.href = "/details?doc_id=" + literatureItem.id;
                    }
                });
                literatureElement.classList.add("literature-item");
                literatureElement.innerHTML = `
                <h2 class="literature-link">&nbsp;&nbsp;${literatureTI}</a></h2>
                <p class="literature-link">作者：${literatureAU}</a></p>
                <p class="literature-link">发布日期：${literatureItem.PY} ${literatureItem.PD}</a></p>
            `;
                literatureContainer.appendChild(literatureElement);
            }

            // 更新翻页导航栏
            updatePagination();
        }

        // 更新翻页导航栏
        function updatePagination() {
            // 生成翻页链接
            let paginationHTML = "";
            for (let i = 1; i <= totalPages; i++) {
                if (i === currentPage) {
                    paginationHTML += `
                <a href="#" class="active">${i}</a>
                `;
                } else {
                    paginationHTML += `
                <a href="#" onclick="showPage(${i})">${i}</a>
            `;
                }
            }

            // 更新翻页容器中的内容
            paginationContainer.innerHTML = paginationHTML;
        }

        // 显示第一页的文献
        showPage(1);

    } else {
        const literatureElement = document.createElement("div");

        // 清空文献容器中的内容
        literatureContainer.innerHTML = "";
        literatureElement.innerHTML = `<h3>（没有找到相关文献）</h3>`;
        literatureContainer.appendChild(literatureElement);
    }


    var slider = document.querySelector('.slider');
    var currentIndex = 0;

    setInterval(function () {
        var imageWidth = document.querySelector('.slider img').clientWidth;
        currentIndex++;
        if (currentIndex >= slider.children.length) {
            currentIndex = 0;
        }
        var newPosition = -currentIndex * imageWidth;
        slider.style.transform = 'translateX(' + newPosition + 'px)';
    }, 3000);
}