"""
file that contain the implementation of the validation function for the input forms 
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
"""
import re

def check_mail(email):
    mail_regEx = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if(re.search(mail_regEx,email)):
        return True, "Valid Email"
    else:
        return False, "Not a Valid Email"

def check_psw(psw):
    password = psw
    flag = 0
    if (len(password)<8): 
        flag = -1
        outcome = "Not a Valid Password: at least 8 characters required"
    elif not re.search("[a-z]", password): 
        flag = -1
        outcome = "Not a Valid Password: at least 1 lowercase character required"
    elif not re.search("[A-Z]", password): 
        flag = -1
        outcome = "Not a Valid Password: at least 1 uppercase character required"
    elif not re.search("[0-9]", password): 
        flag = -1
        outcome = "Not a Valid Password: at least 1 digit required"
    elif re.search("\s", password): 
        flag = -1
        outcome = "Not a Valid Password: it must not contain spaces"
    else: 
        return True, "Valid Password"
    if flag ==-1:
        return False, outcome

def check_name(name):
    if re.search("^[A-Z]'?[- a-zA-Z]+$",name):
        return True, "Valid Name"
    else:
        return False, "Invalid Name"

def check_surname(surname):
    if re.search("^[A-Z]'?[- a-zA-Z]+$",surname):
        return True, "Valid Surname"
    else:
        return False, "Invalid Surname"

def check_balance(balance):
    if re.search("^[+-]?[0-9]+\.?[0-9]*$",balance):
        return True, "Valid balance"
    else:
        return False, "Invalid balance"

def check_odd(odd):
    if re.search("^[0-9]+\.?[0-9]+$",odd):
        return True, "Valid odd"
    else:
        return False, "Invalid odd"

def check_eventName(event_name):
    if re.search("^[A-Z]?[ a-zA-Z]+-{1}[A-Z]? *[ a-zA-Z]+$",event_name):
        return True, "Valid Event Name"
    else:
        return False, "Invalid Event Name"
    

