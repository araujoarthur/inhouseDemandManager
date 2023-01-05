document.addEventListener('DOMContentLoaded', function(){
    
    function showTooltip(tp, popp) {
        tp.setAttribute('data-show', '');
        popp.update();
    }

    function hideTooltip(tp) {
        tp.removeAttribute('data-show');
    }

    let joinButton = document.querySelector("#join-button");
    let codeInput = document.querySelector("input[name='familycode']");
    let secretInput = document.querySelector("input[name='familysecret']");
    let codeTooltip = document.querySelector("#tooltipcode");
    let secretTooltip = document.querySelector("#tooltipsecret");

    const popperCode = Popper.createPopper(codeInput, codeTooltip,{
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

    function checkCode() {
        if (codeInput.value == '') {
            showTooltip(codeTooltip, popperCode);
            return true;
        }
        else {
            hideTooltip(codeTooltip);
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


    joinButton.addEventListener('click', function(e){
   
        let invalidField = false

        if (checkCode())
        {
            invalidField = true;
        }

        if  (checkSecret())
        {
            invalidField = true;
        }

        if (invalidField == true)
        {
            e.preventDefault()  ;
        }
        
    })

    codeInput.addEventListener('input', function(){
        checkCode()
    });
    secretInput.addEventListener('input', function(){
        checkSecret()
    });

})