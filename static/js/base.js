// Magnetic button for the index page using gsap

// Find the button with the id of 'magButton'
const magButton = document.getElementById('magButton');
let bounds = magButton.getBoundingClientRect();

window.addEventListener('resize', () => {
    bounds = magButton.getBoundingClientRect();
});

// Add an event listener to the button that listens for a mousemove event
magButton.addEventListener('mousemove', (e) => {
    const mouseX = e.pageX - bounds.left;
    const mouseY = e.pageY - bounds.top;

    gsap.to(magButton, {
        x: (mouseX - bounds.width / 2) * 0.9,
        y: (mouseY - bounds.height / 2) * 0.9,
        duration: 0.7,
        ease: 'power3.out'
    });
    }
);

// Add an event listener to the button that listens for a mouseleave event
magButton.addEventListener('mouseleave', () => {
    gsap.to(magButton, {
        x: 0,
        y: 0,
        duration: 0.7,
        ease: 'elastic.out(1, 0.3)'
    });
});

// Add an event listener to the button that listens for a click event
magButton.addEventListener('click', () => {
    gsap.to(magButton, {
        scale: 0.9,
        duration: 0.1,
        ease: 'power3.out',
        onComplete: () => {
            gsap.to(magButton, {
                scale: 1,
                duration: 0.1,
                ease: 'power3.out'
            });
        }
    });
});

// Add an event listener to the button that listens for a mouseenter event
magButton.addEventListener('mouseenter', () => {
    gsap.to(magButton, {
        scale: 1.1,
        duration: 0.3,
        ease: 'power3.out'
    });
});

// Add an event listener to the button that listens for a mouseleave event
magButton.addEventListener('mouseleave', () => {
    gsap.to(magButton, {
        scale: 1,
        duration: 0.3,
        ease: 'power3.out'
    });
});

// End of magnetic button functionality


// Implementing the dropdown menu functionality

// There are currently two dropdowns in the header, one for the user and one for the cart. Both are implemented in the same way.
// The dropdown is hidden by default and is shown when the user clicks on the dropdown button.
// The dropdown is hidden when the user clicks outside of the dropdown.
// Dropdown buttons have the ids of 'ProfileDropdownButton' and 'CartDropdownButton' respectively.
// The content of the dropdowns is in the last child of the dropdown buttons with the class of 'dropdown-content'.

// Find the dropdown buttons
const profileDropdownButton = document.getElementById('ProfileDropdownButton');
const cartDropdownButton = document.getElementById('CartDropdownButton');

// Find the dropdown content
const profileDropdownContent = profileDropdownButton.lastElementChild;
const cartDropdownContent = cartDropdownButton.lastElementChild;

// Add an event listener to the document that listens for a click event
document.addEventListener('click', (e) => {
    // If the user clicks outside of the profile dropdown, hide the dropdown
    if (!profileDropdownButton.contains(e.target)) {
        profileDropdownContent.style.display = 'none';
    }
    // If the user clicks outside of the cart dropdown, hide the dropdown
    if (!cartDropdownButton.contains(e.target)) {
        cartDropdownContent.style.display = 'none';
    }
});

// Add an event listener to the profile dropdown button that listens for a click event
profileDropdownButton.addEventListener('click', () => {
    // If the dropdown is hidden, show the dropdown
    if (profileDropdownContent.style.display === 'none') {
        profileDropdownContent.style.display = 'block';
    }
    // If the dropdown is shown, hide the dropdown
    else {
        profileDropdownContent.style.display = 'none';
    }
});

// Add an event listener to the cart dropdown button that listens for a click event
cartDropdownButton.addEventListener('click', () => {
    // If the dropdown is hidden, show the dropdown
    if (cartDropdownContent.style.display === 'none') {
        cartDropdownContent.style.display = 'block';
    }
    // If the dropdown is shown, hide the dropdown
    else {
        cartDropdownContent.style.display = 'none';
    }
});

// End of dropdown menu functionality

