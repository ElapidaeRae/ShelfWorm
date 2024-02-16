// Javascript for search functionality

// Constants
const searchButton = document.getElementById('search_button');
const searchInput = document.getElementById('search');
const display = document.getElementById('display');

// Html tags for each search result.
const searchResultHtml = (item) => {
    return `
        <li class="text-lg text-text cursor-pointer hover:bg-primary dark:hover:bg-primary-dark p-2 rounded-lg">
            <a href="/item/${item.isbn}" class="flex justify-between items-center">
                <div class="flex items-center">
                    <img src="${item.image}" class="w-16 h-16 rounded-lg" alt="${item.title}">
                    <div class="ml-2">
                        <p class="font-bold">${item.title}</p>
                        <p class="text-sm">${item.author}</p>
                    </div>
                </div>
                <p class="text-primary dark:text-primary-dark">${item.price}</p>
            </a>
        </li>
    `;
}


// Function to search for a specific item
function search() {
    // Get the input value
    let input = document.getElementById('search').value;
    input = input.toLowerCase();
    // Get the list of items to search through from the book database by making a request to the server
    const requestOptions = {
        method: 'POST',
        body: JSON.stringify({input: input}),
        redirect: 'follow'
    };
    // Make the request to the api endpoint to search for the ite
    fetch('/api/search', requestOptions)
        // Convert the response to json
    .then(response => response.json())
        // Display the items that match the search query
        .then(result => displayItems(result))
        // Catch any errors and log them to the console
        .catch(error => console.log('error', error));
}

// Function to display the items
function displayItems(result) {
    // Get the list of items
    const items = result;
    // Get the div where the items will be displayed
    // Clear the previous items
    display.innerHTML = '';
    // If there are no items, display a message
    if (items.length === 0) {
        display.innerHTML = 'No items found';
    }
    // Otherwise, display the items
    else {
        // Create a list of items to display
        // The list will be an unordered list of items that users can click on to view the item details
        // Each item will be a list item with appropriate styling with tailwindcss
        const list = document.createElement('ul', {id: 'item_list', class: 'w-full bg-background dark:bg-background-dark p-4 rounded-lg shadow-lg mt-4'});
        // Add each item to the list
        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.innerHTML = searchResultHtml(item);
            list.appendChild(listItem);
        });
        // Add the list to the display
        display.appendChild(list);
    }
}

// Event listener for the search bar to call the search function when the user types more than 2 characters
document.getElementById('search').addEventListener('input', function() {
    if (document.getElementById('search').value.length > 2) {
        search();
    }
});

