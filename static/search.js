
function search() {
    var searchInput = document.getElementById('search-input').value;
    console.log(searchInput)
    console.log(encodeURIComponent(searchInput))
    window.location.href = '/search?search_key=' + encodeURIComponent(searchInput);
}
