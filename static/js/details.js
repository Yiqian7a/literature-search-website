if (first_load_js.details) {
    first_load_js.details = false

    function reload_details() {
        history.pushState({}, '', `/index?page=details&id=${document.getElementById("id").className}`);
        const title = document.getElementById("TI").innerHTML;
        document.getElementById("private-title").innerHTML = '文献搜索：'+ title;
        }

    function exit_details(){}
    reload_details()
}
