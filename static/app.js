document.addEventListener('DOMContentLoaded', function(){
    dropdownProfile = document.querySelector('#profileButton');
    dropdownGroups = document.querySelector('#groupsButton');
    dropdownNewDemand = document.querySelector('#newDemandButton');

    for (let dropdown of [dropdownProfile, dropdownGroups, dropdownNewDemand]){
        dropdown.addEventListener('mouseover', function(){

            dropdown.classList.remove('cst-dropdown-out');
            dropdown.classList.add('cst-dropdown-over');
            
        });
        dropdown.addEventListener('mouseout', function(){

            dropdown.classList.add('cst-dropdown-out');
            dropdown.classList.remove('cst-dropdown-over');
        });
    }
});