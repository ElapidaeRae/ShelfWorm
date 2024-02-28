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

