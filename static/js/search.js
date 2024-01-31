
function search() {
    const searchInput = document.getElementById('search-input').value;
    window.location.href = '/index?search_key=' + encodeURIComponent(searchInput);
}
