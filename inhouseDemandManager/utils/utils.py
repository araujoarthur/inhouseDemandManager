# LEGACY CODE. NOT IN USE ANYMORE
from itertools import chain

characters = list(chain.from_iterable((chr(num),chr(num).upper()) for num in range(97,122)))
print(characters)

def validateEmail(mail:str):
    if type(mail) != str:
        raise TypeError("Argument 'mail' must be a string")
    try:
        firstStep = mail.split('@')
        
        if not(len(firstStep) == 2):
            return False
        else:
            secondStep = firstStep[1].split('.')
            print(secondStep)
            if len(secondStep) > 3:
                return False

            if len(secondStep) >= 2:
                if len(secondStep[1]) > 3:
                    return False
                elif len(secondStep[1]) == 0:
                    return False

            if len(secondStep) == 3:
                if len(secondStep[2]) > 2:
                    return False
                elif len(secondStep[2]) == 0:
                    return False
                
            for elem in secondStep:
                check = [char in characters for char in elem]
                if False in check:
                    return False
            else:
                return True
    except:
        return False
            
            
    print(secondStep)

print(validateEmail('arthur@gmail.com'))