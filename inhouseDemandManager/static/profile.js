document.addEventListener('DOMContentLoaded', () => {
    function parseArgs(argp){
        let argp_s = argp.slice(1, argp.length).split('=');
        let retObj = {}

        for(let i = 0; i <= argp_s.length; i++)
        {
            retObj[argp_s[i]] = argp_s[i + 1];
        }
        
        return retObj;
    }

    // Add a event listener to the button in cases where it exists. 
    args = window.location.search
    
    if (args.length > 0)
    {
        args_dict = parseArgs(args);
        if (!args_dict.hasOwnProperty('create')){
            document.querySelector('.createProfile').addEventListener('click', () => {
                window.location.href = "/profile?create=True";
            });
        }
    }
    else
    {
        document.querySelector('.createProfile').addEventListener('click', () => {
            window.location.href = "/profile?create=True";
        });
    }
});