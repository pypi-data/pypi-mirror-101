

def truthy_question(message: str) -> bool:
    while True:
        res = input("{} (y/n)".format(message))
        if(res.lower() in "yes"):
            return True
        elif(res.lower() in "no"):
            return False
        else:
            print("{} is not understood.".format(res))