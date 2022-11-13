def seda_prime(number):
    if number == 1:
        return False
    elif number == 2 :
        return True
    else:
       for num in range(2, number + 1):
        if number % num == 0 :
            return False
        else : 
            return True

def orkun_prime(number):
    if number == 1: return False
    return len([num for num in range(2, number // 2 + 1) if number % num == 0]) == 0

def irem_prime(num):
    if(num>1):
        a = list(range(3,num//2 + 1))
        for i in a:
           if num%i == 0:
                return False
        else:
            return True
    else:
        return False