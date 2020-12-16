"""
Main file that contain the implementation of REST call for the interaction with the SoccerBet Server
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
"""
import json
import requests

# Classe di Auth Custom creata per usare il beare token come auth metod
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

server_url = "http://127.0.0.1:8080"
def pingServer():
    res = requests.get(server_url + "/ping")
    return res

#User REST calls
def login(email,password):
    data = {
        "email" : email,
        "password" : password
    }
    data_json = json.dumps(data)
    res = requests.post(server_url + "/login" , data= data_json)
    return res


def register(name,surname,email,password,admin_flag):
    data = {
        "name" : name,
        "surname" : surname,
        "email" : email,
        "password" : password,
        "admin": admin_flag 
    }
    data_json = json.dumps(data)
    res = requests.post(server_url + "/register" , data= data_json)
    return res

def getUsers(token):
    res = requests.get(server_url + "/user", auth = BearerAuth(token))
    return res

def getUser(token,user_id):
    res = requests.get(server_url + f"/user/{user_id}", auth = BearerAuth(token))
    return res

def updateUser(token, user_id, name, surname, email, password,balance,admin):
    data = {
        "name" : name,
        "surname" : surname,
        "email" : email,
        "password" : password,
        "balance" : balance,
        "admin" : admin
    }
    data_json = json.dumps(data)
    res = requests.put(server_url + f"/user/{user_id}",data= data_json , auth = BearerAuth(token))
    return res

def deleteUser(token,user_id):
    res = requests.delete(server_url + f"/user/{user_id}", auth = BearerAuth(token))
    return res

def modifyUserBalance(token,user_id, update_quantity):
    data = {
        "update_quantity" : update_quantity
    }
    data_json = json.dumps(data)
    res = requests.put(server_url + f"/user/balance/{user_id}", data= data_json, auth = BearerAuth(token))
    return res

#Event REST calls
def getEvents(token):
    res = requests.get(server_url + "/event", auth = BearerAuth(token))
    return res

def getEvent(token,event_id):
    res = requests.get(server_url + f"/event/{event_id}",auth = BearerAuth(token))
    return res

def insertEvent(token,name, start_d, start_m, start_y, start_h, start_mm, end_d, end_m, end_y, end_h, end_mm, home, X, away, GG, NG, Over2, Under2):
    data = {
        "name" : name,
        "start_date":{
            "d" : start_d,
            "m" : start_m,
            "y" : start_y,
            "h" : start_h,
            "mm" : start_mm
        },
        "end_date":{
            "d" : end_d,
            "m" : end_m,
            "y" : end_y,
            "h" : end_h,
            "mm" : end_mm
        },       
        "odds":{
            "1" : home,
            "X" : X,
            "2" : away,
            "GG" : GG,
            "NG" : NG,
            "Over_2,5" : Over2,
            "Under_2,5" : Under2
        }      
    }
    data_json = json.dumps(data)
    res = requests.post(server_url + "/event" , data= data_json, auth = BearerAuth(token))
    return res


def  updateEvent(token,event_id, name, start_d, start_m, start_y, start_h, start_mm, end_d, end_m, end_y, end_h, end_mm, home, X, away, GG, NG, Over2, Under2):
    data = {
        "name" : name,
        "start_date":{
            "d" : start_d,
            "m" : start_m,
            "y" : start_y,
            "h" : start_h,
            "mm" : start_mm
        },
        "end_date":{
            "d" : end_d,
            "m" : end_m,
            "y" : end_y,
            "h" : end_h,
            "mm" : end_mm
        },       
        "odds":{
            "1" : home,
            "X" : X,
            "2" : away,
            "GG" : GG,
            "NG" : NG,
            "Over_2,5" : Over2,
            "Under_2,5" : Under2
        }      
    }
    data_json = json.dumps(data)
    res = requests.put(server_url + f"/event/{event_id}" , data= data_json, auth = BearerAuth(token))
    return res

def deleteEvent(token,event_id):
    res = requests.delete(server_url + f"/event/{event_id}", auth = BearerAuth(token))
    return res

#Bet REST calls
def getBets(token):
    res = requests.get(server_url + "/bet", auth = BearerAuth(token))
    return res

def getBet(token,bet_id):
    res = requests.get(server_url + f"/bet/{bet_id}", auth = BearerAuth(token))
    return res

def getBetPerUser(token,user_id):
    res = requests.get(server_url + f"/bet/user/{user_id}", auth = BearerAuth(token))
    return res

def insertBet(token,bet):
    data_json = json.dumps(bet)
    res = requests.post(server_url + "/bet" , data= data_json, auth = BearerAuth(token))
    return res

def deleteBet(token,bet_id):
    res = requests.delete(server_url + f"/bet/{bet_id}", auth = BearerAuth(token))
    return res

#Ended Bet REST calls
def getWonBets(token):
    res = requests.get(server_url + "/endedbet/won", auth = BearerAuth(token))
    return res

def getLostBets(token):
    res = requests.get(server_url + "/endedbet/lost",auth = BearerAuth(token))
    return res

def getEndedBet(token,end_bet_id):
    res = requests.get(server_url + f"/endedbet/{end_bet_id}",auth = BearerAuth(token))
    return res

def getWonBetsPerUser(token,user_id):
    res = requests.get(server_url + f"/endedbet/won/user/{user_id}",auth = BearerAuth(token))
    return res

def getLostBetsPerUser(token,user_id):
    res = requests.get(server_url + f"/endedbet/lost/user/{user_id}",auth = BearerAuth(token))
    return res

def insertEndedBet(token,bet_id,won_flag):
    data = {
        "bet_id" : bet_id,
        "won" : won_flag
    }
    data_json = json.dumps(data)
    res = requests.post(server_url + "/endedbet" , data= data_json,auth = BearerAuth(token))
    return res

def deleteEndedBet(token,end_bet_id):
    res = requests.delete(server_url + f"/endedbet/{end_bet_id}",auth = BearerAuth(token))
    return res