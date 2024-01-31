fetch('get_header')
    .then(response => response.text())
    .then(data => {
        const headerElement = document.querySelector('header');
        headerElement.innerHTML = data;
    });

function search() {
    const searchInput = document.getElementById('search-input').value;
    window.location.href = '/index?search_key=' + encodeURIComponent(searchInput);
}
