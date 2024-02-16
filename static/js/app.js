
const dropdownButton = document.getElementById('dropdown_button')

dropdownButton.addEventListener('click', function() {
    document.getElementById('dropdown_content').classList.toggle('show')

    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
        if (!event.target.matches('.dropdown_button')) {
            const dropdowns = document.getElementsByClassName("dropdown_content");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }
})

