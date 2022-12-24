document.addEventListener('DOMContentLoaded', function(){
    // Nav JS

    let divNewDemand = document.querySelector('#newDemandDropdown');
    let divGroups = document.querySelector('#groupsDropdown');
    let divProfile = document.querySelector('#profileDropdown');

    function showCustomMenu(men) {
        men.setAttribute('showMenu','');
        return;
    }

    function hideCustomMenu(men) {
        men.removeAttribute('showMenu');
        return;
    }

    for (let divd of [divNewDemand, divGroups, divProfile]){
        
        let dropdownButton = divd.querySelector('.cst-dropdown'); // Button
        let dropMenu = divd.querySelector(".dropdownMenu");

        dropdownButton.addEventListener('mouseover', function(){
            dropdownButton.classList.remove('cst-dropdown-out');
            dropdownButton.classList.add('cst-dropdown-over');
            dropMenu.setAttribute('showMenu','');
        });
        dropdownButton.addEventListener('mouseout', function(){
            dropdownButton.classList.add('cst-dropdown-out');
            dropdownButton.classList.remove('cst-dropdown-over');
        });
        divd.addEventListener('mouseout', function(){
            // Temporary Fix.
            setTimeout(() => {  
                if ((divd.querySelector(".cst-dropdown:hover") == null) && (divd.querySelector(".dropdownMenu:hover") == null)) {
                    hideCustomMenu(dropMenu)
                } 
            }, 100);
        });
    }
    
    // End Nav JS

});