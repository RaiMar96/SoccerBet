"""
Main file that contain the implementation of REST call for the interaction with the SoccerBet Stats Server
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
"""
import json
import requests

stats_server_url = "http://127.0.0.1:9090"

# Rest Calls for the users stats 
def registerUserStats(user_id):
    data = {
        "user_id": user_id,
        "paid_money" : 0.00,
        "betted_money":0.00,
        "won_money":0.00,
        "num_wbet":0,
        "num_fbet":0
    }
    data_json = json.dumps(data)
    res = requests.post(stats_server_url + "/userstats" , data= data_json)
    return res

def updateBettedAmountUserStats(user_id,betted_money):
    data = {
        "betted_money" : betted_money
    }
    data_json = json.dumps(data)
    res = requests.put(stats_server_url + f"/userstats/{user_id}/bet"  , data= data_json)
    return res

def deletUserStats(user_id):
    res = requests.delete(stats_server_url + f"/userstats/{user_id}")
    return res

def getUserBarGraph(user_id):
    res = requests.get(stats_server_url + f"/userstats/{user_id}/bargraph")
    return res

def getUserPieGraph(user_id):
    res = requests.get(stats_server_url + f"/userstats/{user_id}/piegraph")
    return res
    
def getUserStats(user_id):
    res = requests.get(stats_server_url + f"/userstats/{user_id}")
    return res

def updateUserPaidStats(user_id,paid_money):
    data = {
        "paid_money" : paid_money
    }
    data_json = json.dumps(data)
    res = requests.put(stats_server_url + f"/userstats/{user_id}/paid"  , data= data_json)
    return res

def updateUserWonStats(user_id,won_money):
    data = {
        "won_money" : won_money
    }
    data_json = json.dumps(data)
    res = requests.put(stats_server_url + f"/userstats/{user_id}/won"  , data= data_json)
    return res

def updateUserLoseStats(user_id):
    res = requests.put(stats_server_url + f"/userstats/{user_id}/lose")
    return res

# Rest Calls for the sistem stats 
def updateUserCountReg():
    res = requests.put(stats_server_url + "/sistemstats/user/register")
    return res

def updateUserCountDel():
    res = requests.put(stats_server_url + "/sistemstats/user/delete")
    return res

def updateBetSistemStats(money_gained):
    data = {
        "money_gained" : money_gained
    }
    data_json = json.dumps(data)
    res = requests.put(stats_server_url + "/sistemstats/bet"  , data= data_json)
    return res

def updateWbetSistemStats(money_paid):
    data = {
        "money_paid" : money_paid
    }
    data_json = json.dumps(data)
    res = requests.put(stats_server_url + "/sistemstats/wbet"  , data= data_json)
    return res

def updateFbetSistemStats():
    res = requests.put(stats_server_url + "/sistemstats/fbet")
    return res

def getSistemStats():
    res = requests.get(stats_server_url + "/sistemstats")
    return res

def getSistemPieGraph():
    res = requests.get(stats_server_url + "/sistemstats/piegraph")
    return res

def getSistemBarGraph():
    res = requests.get(stats_server_url + "/sistemstats/bargraph")
    return res

def deleteSistemStats():
    res = requests.delete(stats_server_url + "/sistemstats")
    return res

def createSistemStats():
    data = {
        "registered_users": 0,
        "bet_count" : 0,
        "wbet_count": 0,
        "fbet_count":0,
        "money_gained": 0.00,
        "money_paid": 0.00
    }
    data_json = json.dumps(data)
    res = requests.post(stats_server_url + "/sistemstats"  , data= data_json)
    return res

