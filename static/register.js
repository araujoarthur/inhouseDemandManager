document.addEventListener('DOMContentLoaded', function(){
    
    function showTooltip(tp, popp) {
        tp.setAttribute('data-show', '');
        popp.update();
    }

    function hideTooltip(tp) {
        tp.removeAttribute('data-show');
    }

    let loginButton = document.querySelector("#login-button");
    let usernameInput = document.querySelector("input[name='username']");
    let passwordInput = document.querySelector("input[name='password']");
    let confirmationInput = document.querySelector("input[name='confirmation'");
    let usernameTooltip = document.querySelector("#tooltipuser");
    let passwordTooltip = document.querySelector("#tooltippass");
    let confirmationTooltip = document.querySelector("#tooltipconf");
    

    const popperUsername = Popper.createPopper(usernameInput, usernameTooltip,{
        placement:'right',
        modifiers:[
            {
                name: 'offset',
                options: {
                    offset:[0, 8]
                }
            }
        ]
    });

    const popperPassword = Popper.createPopper(passwordInput, passwordTooltip,{
        placement:'right',
        modifiers:[
            {
                name: 'offset',
                options: {
                    offset:[0, 8]
                }
            }
        ]
    });

    const popperConfirmation = Popper.createPopper(confirmationInput, confirmationTooltip,{
        placement:'right',
        modifiers:[
            {
                name: 'offset',
                options: {
                    offset:[0, 8]
                }
            }
        ]
    });

    function checkUsername() {
        if (usernameInput.value == '') {
            showTooltip(usernameTooltip, popperUsername);
            return true;
        }
        else {
            hideTooltip(usernameTooltip);
            return false;
        }
    }

    function checkPassword() {
        if (passwordInput.value == '') {
            showTooltip(passwordTooltip, popperPassword);
            return true;
        }
        else {
            hideTooltip(passwordTooltip);
            return false;
        }  
    }

    function checkConfirmation() {
        if (confirmationInput.value == '') {
            showTooltip(confirmationTooltip, popperConfirmation);
            return true;
        }
        else {
            hideTooltip(confirmationTooltip);
            return false;
        }
    }

    loginButton.addEventListener('click', function(e){
   
        let invalidField = false

        if (checkUsername())
        {
            invalidField = true;
        }

        if  (checkPassword())
        {
            invalidField = true;
        }

        if (checkConfirmation())
        {
            invalidField = true;
        }

        if (invalidField == true)
        {
            e.preventDefault()  ;
        }
        
    })

    passwordInput.addEventListener('input', function(){
        checkPassword()
    });
    usernameInput.addEventListener('input', function(){
        checkUsername()
    });
    confirmationInput.addEventListener('input', function(){
        checkUsername()
    });

})