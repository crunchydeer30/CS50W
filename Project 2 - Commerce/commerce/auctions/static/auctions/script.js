<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", () => {

    let searchBar = document.querySelector('.search-bar')
    let searchInput = document.querySelector('#search-input');
    let searchResults = document.querySelector('#search-results');

    /*search.addEventListener('keyup', async function() {
        let response = await fetch('/search?q=' + search.value);
        let results = await response.text();
        if (results.length != 5) {
            console.log(results.length)
            searchResults.innerHTML = results;
            document.querySelector('.search-bar').style.borderRadius='10px 10px 0px 0px';     
        }       
        else {
            searchResults.innerHTML ='';
            document.querySelector('.search-bar').style.borderRadius='20px 20px 20px 20px';
        }
    })*/

    searchInput.addEventListener('keyup', async function() {
        fetch('/search?q=' + searchInput.value)
        .then(response => response.text())
        .then(results => {
            console.log(results)
            if (results.length != 0) {
                console.log(results)
                console.log(results.length)
                searchResults.innerHTML = results;
                searchBar.style.borderRadius = '10px 10px 0 0';   
            }       
            else {
                searchResults.innerHTML ='';
                searchBar.style.borderRadius = '20px';
            }
        })
        
    })

    searchInput.addEventListener('focus', () => {
        if (searchInput.value.length == 0 || searchResults.innerHTML == '') {
            searchBar.style.borderRadius = '20px'; 
        }
        else {
            searchBar.style.borderRadius = '10px 10px 0 0';
        }       
    })


    searchInput.addEventListener('focusout', () => {
        searchBar.style.borderRadius = '20px'; 
    })


=======
document.addEventListener("DOMContentLoaded", () => {

    let searchBar = document.querySelector('.search-bar')
    let searchInput = document.querySelector('#search-input');
    let searchResults = document.querySelector('#search-results');

    /*search.addEventListener('keyup', async function() {
        let response = await fetch('/search?q=' + search.value);
        let results = await response.text();
        if (results.length != 5) {
            console.log(results.length)
            searchResults.innerHTML = results;
            document.querySelector('.search-bar').style.borderRadius='10px 10px 0px 0px';     
        }       
        else {
            searchResults.innerHTML ='';
            document.querySelector('.search-bar').style.borderRadius='20px 20px 20px 20px';
        }
    })*/

    searchInput.addEventListener('keyup', async function() {
        fetch('/search?q=' + searchInput.value)
        .then(response => response.text())
        .then(results => {
            console.log(results)
            if (results.length != 0) {
                console.log(results)
                console.log(results.length)
                searchResults.innerHTML = results;
                searchBar.style.borderRadius = '10px 10px 0 0';   
            }       
            else {
                searchResults.innerHTML ='';
                searchBar.style.borderRadius = '20px';
            }
        })
        
    })

    searchInput.addEventListener('focus', () => {
        if (searchInput.value.length == 0 || searchResults.innerHTML == '') {
            searchBar.style.borderRadius = '20px'; 
        }
        else {
            searchBar.style.borderRadius = '10px 10px 0 0';
        }       
    })


    searchInput.addEventListener('focusout', () => {
        searchBar.style.borderRadius = '20px'; 
    })


>>>>>>> 55b03087149b060a03fb91d3d02364719933cb76
})