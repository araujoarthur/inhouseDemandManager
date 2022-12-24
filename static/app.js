document.addEventListener('DOMContentLoaded', function(){
    let dropdownProfileButton = document.querySelector('#profileButton');
    let dropdownGroupsButton = document.querySelector('#groupsButton');
    let dropdownNewDemandButton = document.querySelector('#newDemandButton');

    let divNewDemand = document.querySelector('#newDemandDropdown');
    let divGroups = document.querySelector('#groupsDropdown');
    let divProfile = document.querySelector('#profileDropdown');

    for (let divd of [divNewDemand, divGroups, divProfile]){
        
        let dropdown = divd.querySelector('.cst-dropdown')

        dropdown.addEventListener('mouseover', function(){
            dropdown.classList.remove('cst-dropdown-out');
            dropdown.classList.add('cst-dropdown-over');
            dropMenu = divd.querySelector(".dropdownMenu");
            dropMenu.style.display = 'block';
        });
        dropdown.addEventListener('mouseout', function(){
            dropdown.classList.add('cst-dropdown-out');
            dropdown.classList.remove('cst-dropdown-over');
        });
        divd.addEventListener('mouseout', function(){
            divd.querySelector('.dropdownMenu').style.display = '';  
        });
    }


});