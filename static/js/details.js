if (first_load_js.details) {

    function random(max) {
        return Math.floor(Math.random() * max);
    }

    let activeElement = null;
    var initialX;
    var initialY;
    var xOffset = 0;
    var yOffset = 0;

    // 拖拽开始时记录初始位置
    function dragStart(e) {
        activeElement = e.target;
        initialX = e.clientX - activeElement.getBoundingClientRect().left - xOffset;
        initialY = e.clientY - activeElement.getBoundingClientRect().top - yOffset;
    }

    function dragEnd() {
        activeElement = null;
        xOffset = 0;
        yOffset = 0;
    }

    function drag(e) {
        if (activeElement) {
            e.preventDefault();
            xOffset = e.clientX - initialX;
            yOffset = e.clientY - initialY;
            setTranslate(xOffset, yOffset, activeElement);
        }
    }

    function setTranslate(xPos, yPos, el) {
        el.style.left = xPos + 'px';
        el.style.top = yPos + 'px';
    }

    function drawTopic(data) {
        console.log(typeof data,data)
        const chartContainer = document.getElementById('topic-container');
        chartContainer.innerHTML = '';

        if (data) {
            data = data.replace(/'/g, '"');
            data = JSON.parse(data);
            // 计算data中值的和
            let sum = 0;
            for (const topic in data) {
                sum += data[topic];
            }
            // 计算每个标签的边长（按正方形算）
            const totalArea = 10000; // 容器的总面积
            for (const topic in data) {
                data[topic] = Math.sqrt(totalArea * data[topic] / sum);
            }

            const colorBoard = ['#e84e4e', '#ec7a3c', '#f3d63e', '#7de770',
                '#9beff6', '#3b8cf6', '#6d6de7'];

            // 遍历数据并渲染圆形元素
            for (const topic in data) {
                const a = data[topic];
                const circle = document.createElement('div');
                circle.className = 'topic';
                circle.innerText = topic;
                circle.style.backgroundColor = colorBoard[random(7)];
                // 设置圆的d大小
                circle.style.width = a * 2 + 'px';
                circle.style.height = a * 2 + 'px';

                circle.style.top = random(200) + 'px';
                circle.style.left = random(400) + 'px';

                circle.style.fontSize = a / 2 + 'px';

                circle.addEventListener("mousedown", dragStart);
                circle.addEventListener("mouseup", dragEnd);

                chartContainer.appendChild(circle);
            }
        }
        else {}
    }

    function reload_details() {
        history.pushState({}, '', `/index?page=details&id=${document.getElementById("id").className}`);
        document.getElementById("private-title").innerHTML = '文献搜索：'+ document.getElementById("TI").innerHTML;
        document.addEventListener("mousemove", drag);
        drawTopic(document.getElementById("topic-container").innerHTML)
        }

    function exit_details(){
        document.removeEventListener("mousemove", drag);
    }

    eval("reload_" + currentPage + "()")

    first_load_js.details = false
}
