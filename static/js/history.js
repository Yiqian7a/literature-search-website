if (first_load_js.history) {
    function get_history() {
        fetch('/history')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log(typeof data, data);
            const historyContainer = document.getElementById("history-container");
            for (let i = 0; i <= Math.min(20, data.length); i++) {
                const historyItem = data[i];
                const historyElement = document.createElement("div");
                historyElement.classList.add("history-item");
                historyElement.innerHTML = `
                    <h2 onclick="get_page('details', '${historyItem[0]}')">&nbsp;&nbsp;${historyItem[2]}</h2>
                    <p>浏览日期：${historyItem[1]}</p>
                `;
                historyContainer.appendChild(historyElement);
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    }

    function reload_history() {
        get_history()
    }
    function exit_history(){}

    reload_history()
}
