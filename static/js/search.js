// Javascript for search functionality

// Constants
const searchButton = document.getElementById('search_button');
const searchInput = document.getElementById('search');
const display = document.getElementById('display');

// Html tags for each search result.
const searchResultHtml = (item) => {
    return `
    <tr class="table-row hover:bg-primary p-2 rounded-lg text-text dark:text-text-dark" onclick="window.location.href='/book/${item[4]}'">
        <td class="table-cell"><a href="/book/${item[4]}">${item[0]}</a></td>
        <td class="table-cell"><a href="/book/${item[4]}">${item[1]}</a></td>
        <td class="table-cell"><a href="/book/${item[4]}">${item[2]}</a></td>
        <td class="table-cell"><a href="/book/${item[4]}">${item[3]}</a></td>
        <td class="table-cell"><a href="/book/${item[4]}">${item[7]}</a></td>
    </tr>
    `;
}


// Function to search for a specific item
function search() {
    // Get the input value
    let input = document.getElementById('search').value;
    // Get the list of items to search through from the book database by making a request to the server
    const requestOptions = {
        method: 'POST',
        body: JSON.stringify({input: input}),
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow'
    };
    console.log('requestOptions: ', requestOptions);
    // Make the request to the api endpoint to search for the ite
    fetch('/api/search', requestOptions)
    // Convert the response to json
    .then(response => response.json())
    // Display the items
    .then(result => displayItems(result))
    // Log any errors
    .catch(error => console.log('error', error));
    console.log('searching for: ' + input);
}

// Function to display the items
function displayItems(result) {
    // Get the list of items
    const items = result;
    console.log('items: ' + items);
    // Clear the previous items
    display.innerHTML = '';
    // If there are no items, display a message
    if (items.length === 0) {
        display.innerHTML = 'No items found...';
    }
    // Otherwise, display the items
    else {
        // For each item, display it in the display div
        items.forEach(item => {
            display.innerHTML += searchResultHtml(item);
        });
    }
}



window.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    searchInput.addEventListener('input', function() {
        if (searchInput.value.length > 2) {
            search();
        }
    });
});

