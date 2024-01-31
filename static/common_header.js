fetch('get_header')
    .then(response => response.text())
    .then(data => {
        const headerElement = document.querySelector('header');
        headerElement.innerHTML = data;

    console.log(data)
    });
