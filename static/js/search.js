// Javascript for search functionality

// Constants
const searchButton = document.getElementById('search_button');
const searchInput = document.getElementById('search');
const display = document.getElementById('display');

// Html tags for each search result.
const searchResultHtml = (item) => {
    return `
        <li class="text-lg text-text cursor-pointer hover:bg-primary dark:hover:bg-accent p-2 rounded-lg">
            <a href="/item/${item[3]}" class="flex justify-between items-center">
                <div class="flex items-center">
                    <img src="data:image/jpg;base64,${item[4]}" class="w-16 h-16 rounded-lg" alt="${item[0]}">
                    <div class="ml-2">
                        <p class="font-bold">${item[0]}</p>
                        <p class="text-sm">${item[1]}</p>
                    </div>
                </div>
                <p class="text-primary dark:text-primary-dark">${item[6]}</p>
            </a>
        </li>
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
        // Create a list of items to display
        // The list will be an unordered list of items that users can click on to view the item details
        // Each item will be a list item with appropriate styling with tailwindcss
        const list = document.createElement('ul', {id: 'item_list', class: 'rounded-md bg-background p-4 ring-1 ring-accent ring-opacity-20 shadow-lg w-full'});
        // Add each item to the list
        items.forEach(item => {
            const listItem = document.createElement('li', {class: 'text-lg text-text cursor-pointer hover:bg-primary dark:hover:bg-primary-dark p-2 rounded-lg'});
            listItem.innerHTML = searchResultHtml(item);
            list.appendChild(listItem);
        });
        // Add the list to the display
        display.appendChild(list);
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

