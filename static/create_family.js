document.addEventListener('DOMContentLoaded', function(){
    
    function showTooltip(tp, popp) {
        tp.setAttribute('data-show', '');
        popp.update();
    }

    function hideTooltip(tp) {
        tp.removeAttribute('data-show');
    }

    let loginButton = document.querySelector("#login-button");
    let nameInput = document.querySelector("input[name='family_name']");
    let secretInput = document.querySelector("input[name='family_secret']");
    let confirmationInput = document.querySelector("input[name='confirmation'");
    let nameTooltip = document.querySelector("#tooltipfn");
    let secretTooltip = document.querySelector("#tooltipfsc");
    let confirmationTooltip = document.querySelector("#tooltipconf");
    

    const popperName = Popper.createPopper(nameInput, nameTooltip,{
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

    const popperSecret = Popper.createPopper(secretInput, secretTooltip,{
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

    function checkName() {
        if (nameInput.value == '') {
            showTooltip(nameTooltip, popperName);
            return true;
        }
        else {
            hideTooltip(nameTooltip);
            return false;
        }
    }

    function checkSecret() {
        if (secretInput.value == '') {
            showTooltip(secretTooltip, popperSecret);
            return true;
        }
        else {
            hideTooltip(secretTooltip);
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

        if (checkName())
        {
            invalidField = true;
        }

        if  (checkSecret())
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

    secretInput.addEventListener('input', function(){
        checkSecret()
    });
    
    nameInput.addEventListener('input', function(){
        checkName()
    });

    confirmationInput.addEventListener('input', function(){
        checkConfirmation()
    });

})