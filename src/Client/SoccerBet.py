"""
Main file that contain the implementation of the Soccer Bet GUI Client
Created by:
Raiti Mario O55000434
Nardo Gabriele Salvatore O55000430
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime
from Ui_SoccerBet import Ui_MainWindow
import Rest_Requests as req
import Stats_Rest_Requests as sts_req
import FormValidator as valid
import GuiTools
import requests
from collections import OrderedDict


class SoccerBetUiController():
    def __init__(self):
        self.my_wnd = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.my_wnd)
        self.ui.stackedWidget.setCurrentWidget(self.ui.Login)
        self.connectSignals()
        self.initVariables()

    def initVariables(self):
        self.bet_dict = {
            "user_id" : "",
            "betted_amount" : "",
            "betted_amount" : "",
            "event_outcomes" : "",
        }
        self.logged_user_info = {
            "logged_user_id": "",
            "token" : "",
            "adminFlag" : False
        }


        self.ui.AdminHome_eventStartDate_line.setDateTime(QDateTime.currentDateTime())
        self.ui.AdminHome_eventEndDate_line.setDateTime(QDateTime.currentDateTime())


    def connectSignals(self):
        self.ui.Login_btn.clicked.connect(self.onLoginBtn)
        self.ui.Register_btn.released.connect(self.showRegistrationPage)
        
        self.ui.reg_registration_btn.clicked.connect(self.onRegisterBtn)
        self.ui.back_to_login_btn.released.connect(self.showLoginPage)

        self.ui.AdminHome_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.AdminHome_to_Users_page_btn.clicked.connect(self.showAdminUsers)
        self.ui.AdminHome_to_Event_page_btn.clicked.connect(self.showAdminHome)
        self.ui.AdminHome_to_Bets_page_btn.clicked.connect(self.showAdminBets)
        self.ui.AdminHome_NewEvent_btn.clicked.connect(self.onNewEventBtn)
        self.ui.AdminHome_to_Stats_page_btn.clicked.connect(self.showAdminStats)
        self.ui.AdminHome_to_Profile_page_btn.clicked.connect(self.showAdminProfile)
        
        self.ui.AdminUsers_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.AdminUsers_to_Users_page_btn.clicked.connect(self.showAdminUsers)
        self.ui.AdminUsers_to_Event_page_btn.clicked.connect(self.showAdminHome)
        self.ui.AdminUsers_to_Bets_page_btn.clicked.connect(self.showAdminBets)
        self.ui.AdminUsers_to_Stats_page_btn.clicked.connect(self.showAdminStats)
        self.ui.AdminUsers_to_Profile_page_btn.clicked.connect(self.showAdminProfile)

        self.ui.AdminProfile_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.AdminProfile_to_Users_page_btn.clicked.connect(self.showAdminUsers)
        self.ui.AdminProfile_to_Event_page_btn.clicked.connect(self.showAdminHome)
        self.ui.AdminProfile_to_Bets_page_btn.clicked.connect(self.showAdminBets)
        self.ui.AdminProfile_to_Stats_page_btn.clicked.connect(self.showAdminStats)
        self.ui.AdminProfile_DeleteProfile_btn.clicked.connect(self.onDeleteUserBtn)
        self.ui.AdminProfile_UpdateUserInfo_btn.clicked.connect(self.onUpdateAdminInfoBtn)

        self.ui.AdminBets_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.AdminBets_to_Users_page_btn.clicked.connect(self.showAdminUsers)
        self.ui.AdminBets_to_Event_page_btn.clicked.connect(self.showAdminHome)
        self.ui.AdminBets_to_Bets_page_btn.clicked.connect(self.showAdminBets)
        self.ui.AdminBets_to_Stats_page_btn.clicked.connect(self.showAdminStats)
        self.ui.AdminBets_to_profile_page_btn.clicked.connect(self.showAdminProfile)

        self.ui.AdminStats_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.AdminStats_to_Users_page_btn.clicked.connect(self.showAdminUsers)
        self.ui.AdminStats_to_Event_page_btn.clicked.connect(self.showAdminHome)
        self.ui.AdminStats_to_Bets_page_btn.clicked.connect(self.showAdminBets)
        self.ui.AdminStats_to_Stats_page_btn.clicked.connect(self.showAdminStats)
        self.ui.AdminStats_to_Profile_page_btn.clicked.connect(self.showAdminProfile)

        self.ui.UserHome_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.UserHome_to_Profile_page_btn.clicked.connect(self.showUserProfile)
        self.ui.UserHome_to_bet_page_btn.clicked.connect(self.showUserBets)
        self.ui.UserHome_Event_page_btn.clicked.connect(self.showUserHome)
        self.ui.UserHome_to_stats_page_btn.clicked.connect(self.showUserStats)
        self.ui.UserHome_InsertBet_btn.clicked.connect(self.onInsertBetbtn)
        self.ui.UserHome_BettedAmount_spin.valueChanged.connect(self.setPotentialWin) 

        self.ui.UserBets_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.UserBets_to_Event_page_btn.clicked.connect(self.showUserHome)
        self.ui.UserBets_to_Bets_page_btn.clicked.connect(self.showUserBets)
        self.ui.UsersBets_to_Profile_page_btn.clicked.connect(self.showUserProfile)
        self.ui.UserBets_to_Stats_page_btn.clicked.connect(self.showUserStats)
        
        self.ui.UserProfile_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.UserProfile_to_Event_page_btn.clicked.connect(self.showUserHome)
        self.ui.UserProfile_to_bet_page_btn.clicked.connect(self.showUserBets)
        self.ui.UserProfile_UpdateUserInfo_btn.clicked.connect(self.onUpdateUserInfoBtn)
        self.ui.UserProfile_UpdateBalance_btn.clicked.connect(self.onUpdateUserBalanceBtn)
        self.ui.UserProfile_DeleteProfile_btn.clicked.connect(self.onDeleteUserBtn)
        self.ui.UserProfile_to_stats_page_btn.clicked.connect(self.showUserStats)
        
        self.ui.UserStats_LogOut_btn.clicked.connect(self.onLogoutBtn)
        self.ui.UserStats_to_Stats_page_btn.clicked.connect(self.showUserStats)
        self.ui.UsersStats_to_Profile_page_btn.clicked.connect(self.showUserProfile)
        self.ui.UserStats_to_Bets_page_btn.clicked.connect(self.showUserBets)
        self.ui.UserStast_to_Event_page_btn.clicked.connect(self.showUserHome)

        self.ui.AdminUsers_UserInfos_tbl.cellDoubleClicked.connect(self.onViewUsersGraph)
        self.ui.AdminBets_Bets_tbl.cellDoubleClicked.connect(self.onViewBetInfo)
        self.ui.UserBets_Bets_tbl.cellDoubleClicked.connect(self.onViewBetInfo)

    # Function to interact with the server
    def onLoginBtn(self):
        self.email = self.ui.login_mail_line.text()
        self.password = self.ui.login_psw_line.text()
        is_valid_email, res_mail = valid.check_mail(self.email)
        is_valid_psw, res_psw = valid.check_psw(self.password)
        if(is_valid_email and is_valid_psw):
            res = req.login(self.email,self.password)
            # cleaning the input line before changing page
            self.ui.login_psw_line.clear()
            self.ui.login_mail_line.clear()
            if(res.status_code == 404):
                msg = GuiTools.MessageBox("Bad credentials", "Login failed, user not found" ,self.my_wnd.geometry().center())
                msg.showMessageError()
            else:
                response_data = res.json()
                self.logged_user_info["logged_user_id"] = response_data['id']
                self.logged_user_info["token"] = response_data['token']
                if(response_data['admin'] == False):
                    self.quota_totale = 1.00
                    self.potential_win = 1.00
                    self.ui.UserHome_quotaTotale.setText(str(self.quota_totale))
                    self.setPotentialWin()
                    self.ev_list = []
                    self.selected_event_ids = []
                    self.ui.UserHome_Bet_tbl.setRowCount(0)
                    self.showUserHome()
                if(response_data['admin'] == True):
                    self.logged_user_info["adminFlag"] = True
                    self.showAdminHome()
        else:
            msg = GuiTools.MessageBox("Bad credentials", "Invalid Mail or Password, Please insert the correct ones" ,self.my_wnd.geometry().center())
            msg.showMessageError()


    def onRegisterBtn(self):
        self.name = self.ui.reg_name_line.text()
        self.surname = self.ui.reg_surname_line.text()
        self.email = self.ui.reg_mail_line.text()
        self.password = self.ui.reg_psw_line.text()
        self.admin_flag = self.ui.isAdmin_checkBox.isChecked() 
        is_valid_email, res_mail = valid.check_mail(self.email)
        is_valid_psw, res_psw = valid.check_psw(self.password)
        is_valid_name, res_name = valid.check_name(self.name)
        is_valid_surname, res_surname = valid.check_surname(self.surname)
        if(is_valid_email and is_valid_psw and is_valid_name and is_valid_surname):
            res = req.register(self.name,self.surname,self.email,self.password,self.admin_flag)  
            # cleaning the input line before changing page
            self.ui.reg_psw_line.clear()
            self.ui.reg_mail_line.clear()
            self.ui.reg_surname_line.clear()
            self.ui.reg_name_line.clear()

            if(res.status_code == 201):
                res_sts = sts_req.updateUserCountReg()
                if(res_sts.status_code == 200):
                    res_log = req.login(self.email,self.password)
                    response_data = res_log.json()
                    res_upd_sts = sts_req.registerUserStats(response_data['id'])
                    if(res_upd_sts.status_code != 201):
                        msg = GuiTools.MessageBox("Error", "Error during stats update" ,self.my_wnd.geometry().center())
                        msg.showMessageError()

                    msg = GuiTools.MessageBox("Success", "Registration Correctly Completed, Please Login" , self.my_wnd.geometry().center())
                    msg.showMessageInfo()
                    self.showLoginPage()
                else:
                    msg = GuiTools.MessageBox("Error", "Error during stats update ( user count )" ,self.my_wnd.geometry().center())
                    msg.showMessageError()
            else:
                msg = GuiTools.MessageBox("Error", "Registration Failed" ,self.my_wnd.geometry().center())
                msg.showMessageError()
        else:
            msg = GuiTools.MessageBox("Bad credentials", "Name:" + res_name +"\n" + "Surname:" + res_surname + "\n" + "Email:" + res_mail +"\n" + "Password:" + res_psw , self.my_wnd.geometry().center())
            msg.showMessageError()


    def onLogoutBtn(self):
        if(self.logged_user_info["logged_user_id"] != ""): 
            self.logged_user_info["logged_user_id"] == ""
            self.logged_user_info["token"] == ""
            self.logged_user_info["adminFlag"] = False
            self.ui.stackedWidget.setCurrentWidget(self.ui.Login)

    def onUpdateUserInfoBtn(self):
        self.new_name = self.ui.UserProfile_name_line.text()
        self.new_surname = self.ui.UserProfile_surname_line.text()
        self.new_mail = self.ui.UserProfile_mail_line.text()
        self.new_psw = self.ui.UserProfile_pass_line.text()
        self.new_balance =  self.ui.UserProfile_show_balance_line.text()
        is_valid_email, res_mail = valid.check_mail(self.new_mail)
        is_valid_psw, res_psw = valid.check_psw(self.new_psw)
        is_valid_name, res_name = valid.check_name(self.new_name)
        is_valid_surname, res_surname = valid.check_surname(self.new_surname)
        if(is_valid_email and is_valid_psw and is_valid_name and is_valid_surname):
            res = req.updateUser(self.logged_user_info["token"],self.logged_user_info["logged_user_id"],self.new_name,self.new_surname,self.new_mail,self.new_psw,float(self.new_balance.replace('€ ','')),False)
            if(res.status_code == 200):
                msg = GuiTools.MessageBox("Success", "Profile Updated Correctly" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
            elif(res.status_code == 401):
                msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                self.onLogoutBtn()
            else:
                msg = GuiTools.MessageBox("Error", "Update Failed" ,self.my_wnd.geometry().center())
                msg.showMessageError()
        else:
            msg = GuiTools.MessageBox("Bad credentials", "Name:" + res_name +"\n" + "Surname:" + res_surname + "\n" + "Email:" + res_mail +"\n" + "Password:" + res_psw , self.my_wnd.geometry().center())
            msg.showMessageError()
    
    def onUpdateAdminInfoBtn(self):
        self.new_name = self.ui.AdminProfile_name_line.text()
        self.new_surname = self.ui.AdminProfile_surname_line.text()
        self.new_mail = self.ui.AdminProfile_mail_line.text()
        self.new_psw = self.ui.AdminProfile_pass_line.text()
        is_valid_email, res_mail = valid.check_mail(self.new_mail)
        is_valid_psw, res_psw = valid.check_psw(self.new_psw)
        is_valid_name, res_name = valid.check_name(self.new_name)
        is_valid_surname, res_surname = valid.check_surname(self.new_surname)
        if(is_valid_email and is_valid_psw and is_valid_name and is_valid_surname):
            res = req.updateUser(self.logged_user_info["token"],self.logged_user_info["logged_user_id"],self.new_name,self.new_surname,self.new_mail,self.new_psw,0.0,True)
            if(res.status_code == 200):
                msg = GuiTools.MessageBox("Success", "Profile Updated Correctly" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
            elif(res.status_code == 401):
                msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                self.onLogoutBtn()
            else:
                msg = GuiTools.MessageBox("Error", "Update Failed" ,self.my_wnd.geometry().center())
                msg.showMessageError()
        else:
            msg = GuiTools.MessageBox("Bad credentials", "Name:" + res_name +"\n" + "Surname:" + res_surname + "\n" + "Email:" + res_mail +"\n" + "Password:" + res_psw , self.my_wnd.geometry().center())
            msg.showMessageError()

    def onUpdateUserBalanceBtn(self):
        self.new_balance = self.ui.UserProfile_balance_line.text()
        is_valid_balance, res_balance = valid.check_balance(self.new_balance)
        if(is_valid_balance):
            res = req.modifyUserBalance(self.logged_user_info["token"],self.logged_user_info["logged_user_id"],float(self.new_balance))
            if(res.status_code == 200):
                if(self.new_balance.find("-") == -1):
                    res_sts = sts_req.updateUserPaidStats(self.logged_user_info["logged_user_id"],float(self.new_balance))
                    if(res_sts.status_code != 200):
                        msg = GuiTools.MessageBox("Error", "Errore durante aggiornamento statistiche utente" ,self.my_wnd.geometry().center())
                        msg.showMessageError()

                self.ui.UserProfile_balance_line.clear()
                self.onProfile()
                msg = GuiTools.MessageBox("Success", "Balance Updated Correctly" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
            elif(res.status_code == 401):
                msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                self.onLogoutBtn()
            else:
                msg = GuiTools.MessageBox("Error", "Update Failed" ,self.my_wnd.geometry().center())
                msg.showMessageError()
        else:
            msg = GuiTools.MessageBox("Bad credentials", res_balance , self.my_wnd.geometry().center())
            msg.showMessageError()

    def onUpdateEventBtn(self,ev_id):
        self.dlg = GuiTools.EditEventDialog(self.my_wnd.geometry().center())
        res = req.getEvent(self.logged_user_info["token"],ev_id)
        if(res.status_code == 200):
            self.event_infos = res.json()
            self.dlg.Mdl_Name_lineEdit.setText(self.event_infos["name"])
            self.dlg.Mdl_Quota_1_LineEdit.setText(str(round(self.event_infos["odds"]["1"],2)))
            self.dlg.Mdl_Quota_X_LineEdit.setText(str(round(self.event_infos["odds"]["X"],2)))
            self.dlg.Mdl_Quota_2_LineEdit.setText(str(round(self.event_infos["odds"]["2"],2)))
            self.dlg.Mdl_Quota_GG_LineEdit.setText(str(round(self.event_infos["odds"]["GG"],2)))
            self.dlg.Mdl_Quota_NG_LineEdit.setText(str(round(self.event_infos["odds"]["NG"],2)))
            self.dlg.Mdl_Quota_Ovr_LineEdit.setText(str(round(self.event_infos["odds"]["OVER_2,5"],2)))
            self.dlg.Mdl_Quota_Undr_LineEdit.setText(str(round(self.event_infos["odds"]["UNDER_2,5"],2)))
            self.dlg.Mdl_StartDate_lineEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(self.event_infos["start_date"]["year"], self.event_infos["start_date"]["month"], self.event_infos["start_date"]["day"]), QtCore.QTime(self.event_infos["start_date"]["hour"], self.event_infos["start_date"]["minute"], 0)))
            self.dlg.Mdl_EndDate_lineEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(self.event_infos["end_date"]["year"], self.event_infos["end_date"]["month"], self.event_infos["end_date"]["day"]), QtCore.QTime(self.event_infos["end_date"]["hour"], self.event_infos["end_date"]["minute"], 0)))
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "Event not found" ,self.my_wnd.geometry().center())
            msg.showMessageError()
        self.dlg.Mdl_EditEvent_btn.clicked.connect(lambda : self.updateEvent(ev_id,self.dlg))  
        self.dlg.exec_()

    def onDeleteUserBtn(self):
        self.dlg = GuiTools.CustomDialog("Attenzione","Sicuro di voler eliminare il tuo profilo ??",self.my_wnd.geometry().center())
        self.dlg.buttonBox.accepted.connect(self.deleteProfile)
        self.dlg.exec_()
    
    def onDeleteEventBtn(self,ev_id):
        self.dlg = GuiTools.CustomDialog("Attenzione","Sicuro di voler eliminare l'evento",self.my_wnd.geometry().center())
        self.dlg.buttonBox.accepted.connect(lambda : self.deleteEvent(ev_id))
        self.dlg.exec_()
    
    def onDeleteBetBtn(self,bet_id):
        self.dlg = GuiTools.CustomDialog("Attenzione","Sicuro di voler annullare la scommessa??",self.my_wnd.geometry().center())
        self.dlg.buttonBox.accepted.connect(lambda : self.deleteBet(bet_id))
        self.dlg.exec_()
    
    def onDeleteEndBetBtn(self,ebet_id):
        self.dlg = GuiTools.CustomDialog("Attenzione","Sicuro di voler eliminare la scommessa conclusa??",self.my_wnd.geometry().center())
        self.dlg.buttonBox.accepted.connect(lambda : self.deleteEbet(ebet_id))
        self.dlg.exec_()
    
    def onCheckBetBtn(self,bet_id,won_flag,*args, **kwargs):
        money_paid = kwargs.get('c', None)
        user_id = kwargs.get('d', None)
        if(won_flag == True):
            self.dlg = GuiTools.CustomDialog("Attenzione","Sicuro di voler rendere vincente la scommessa??",self.my_wnd.geometry().center())
            self.dlg.buttonBox.accepted.connect(lambda : self.CheckBet(bet_id,won_flag,c=money_paid,d=user_id))
        else:
            self.dlg = GuiTools.CustomDialog("Attenzione","Sicuro di rendere perdente la scommessa??",self.my_wnd.geometry().center())
            self.dlg.buttonBox.accepted.connect(lambda : self.CheckBet(bet_id,won_flag,d=user_id))
        self.dlg.exec_()

    def onNewEventBtn(self):
        # Obtain Event name 
        self.event_name = self.ui.AdminHome_eventName_line.text()
        # Partitioning start date
        self.startDate_day = self.ui.AdminHome_eventStartDate_line.sectionText(self.ui.AdminHome_eventStartDate_line.sectionAt(0))
        self.startDate_month = self.ui.AdminHome_eventStartDate_line.sectionText(self.ui.AdminHome_eventStartDate_line.sectionAt(1))
        self.startDate_year = self.ui.AdminHome_eventStartDate_line.sectionText(self.ui.AdminHome_eventStartDate_line.sectionAt(2))
        self.startDate_hour = self.ui.AdminHome_eventStartDate_line.sectionText(self.ui.AdminHome_eventStartDate_line.sectionAt(3))
        self.startDate_minute = self.ui.AdminHome_eventStartDate_line.sectionText(self.ui.AdminHome_eventStartDate_line.sectionAt(4))
        #Partitioning end date
        self.endDate_day = self.ui.AdminHome_eventEndDate_line.sectionText(self.ui.AdminHome_eventEndDate_line.sectionAt(0))
        self.endDate_month = self.ui.AdminHome_eventEndDate_line.sectionText(self.ui.AdminHome_eventEndDate_line.sectionAt(1))
        self.endDate_year = self.ui.AdminHome_eventEndDate_line.sectionText(self.ui.AdminHome_eventEndDate_line.sectionAt(2))
        self.endDate_hour = self.ui.AdminHome_eventEndDate_line.sectionText(self.ui.AdminHome_eventEndDate_line.sectionAt(3))
        self.endDate_minute = self.ui.AdminHome_eventEndDate_line.sectionText(self.ui.AdminHome_eventEndDate_line.sectionAt(4))
        # Obtain the odss
        self.odd_1 = self.ui.AdminHome_Odd_1_line.text()
        self.odd_2 = self.ui.AdminHome_Odd_2_line.text()
        self.odd_X = self.ui.AdminHome_Odd_X_line.text()
        self.odd_GG = self.ui.AdminHome_Odd_GG_line.text()
        self.odd_NG = self.ui.AdminHome_Odd_NG_line.text()
        self.odd_Ovr = self.ui.AdminHome_Odd_Ovr_line.text()
        self.odd_Undr = self.ui.AdminHome_Odd_Undr_line.text()
        # Validation
        is_valid_odd_1, res_odd_1 = valid.check_odd(self.odd_1)
        is_valid_odd_2, res_odd_2 = valid.check_odd(self.odd_2)
        is_valid_odd_X, res_odd_X = valid.check_odd(self.odd_X)
        is_valid_odd_GG, res_odd_GG = valid.check_odd(self.odd_GG)
        is_valid_odd_NG, res_odd_NG = valid.check_odd(self.odd_NG)
        is_valid_odd_Ovr, res_odd_Ovr = valid.check_odd(self.odd_Ovr)
        is_valid_odd_Undr, res_odd_Undr = valid.check_odd(self.odd_Undr)
        is_valid_ev_name , res_ev_name = valid.check_eventName(self.event_name)

        if(self.ui.AdminHome_eventStartDate_line.dateTime() >= QDateTime.currentDateTime()):
            is_valid_startDate = True
            res_startDate = "valid Start Date"
        else:
            is_valid_startDate = False
            res_startDate = "Invalid Start Date"

        if(self.ui.AdminHome_eventEndDate_line.dateTime() > self.ui.AdminHome_eventStartDate_line.dateTime()):
            is_valid_endDate = True
            res_endDate = "valid end Date"
        else:
            is_valid_endDate = False
            res_endDate = "Invalid end Date"

        # Post Request
        if(is_valid_startDate and is_valid_endDate and is_valid_odd_1 and is_valid_odd_2 and is_valid_odd_X and is_valid_odd_GG and is_valid_odd_NG and is_valid_odd_Ovr and is_valid_odd_Undr and is_valid_ev_name):
            res = req.insertEvent(self.logged_user_info["token"],self.event_name,int(self.startDate_day),int(self.startDate_month),int(self.startDate_year),int(self.startDate_hour),int(self.startDate_minute),int(self.endDate_day),int(self.endDate_month),int(self.endDate_year),int(self.endDate_hour),int(self.endDate_minute),float(self.odd_1),float(self.odd_X),float(self.odd_2),float(self.odd_GG),float(self.odd_NG),float(self.odd_Ovr),float(self.odd_Undr))
            # cleaning the input line before changing page
            self.ui.AdminHome_eventName_line.clear()
            self.ui.AdminHome_eventStartDate_line.clear()
            self.ui.AdminHome_eventEndDate_line.clear()
            self.ui.AdminHome_Odd_1_line.clear()
            self.ui.AdminHome_Odd_X_line.clear()
            self.ui.AdminHome_Odd_2_line.clear()
            self.ui.AdminHome_Odd_GG_line.clear()
            self.ui.AdminHome_Odd_NG_line.clear()
            self.ui.AdminHome_Odd_Ovr_line.clear()
            self.ui.AdminHome_Odd_Undr_line.clear()

            if(res.status_code == 201):
                msg = GuiTools.MessageBox("Success", "Event Correctly Inserted" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                self.showAdminHome()
            elif(res.status_code == 401):
                msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                self.onLogoutBtn()
            else:
                msg = GuiTools.MessageBox("Error", "Event not inserted " ,self.my_wnd.geometry().center())
                msg.showMessageError()
        else:
            msg = GuiTools.MessageBox("Bad Values", "Event Name:" + res_ev_name +"\n" + "Start date:" + res_startDate +"\n" + "End date:" + res_endDate +"\n" + "Odd 1:" + res_odd_1 + "\n" + "Odd 2:" + res_odd_2 +"\n" + "Odd X:" + res_odd_X +"\n" + "Odd GG:" + res_odd_GG +"\n" + "Odd NG:" + res_odd_NG +"\n" + "Odd Over 2,5:" + res_odd_Ovr +"\n" + "Odd Under 2,5:" + res_odd_Undr , self.my_wnd.geometry().center())
            msg.showMessageError()

    def delRow(self,evento):
        self.ui.UserHome_Bet_tbl.removeRow(self.ui.UserHome_Bet_tbl.currentIndex().row())
        self.selected_event_ids.remove(evento["event_id"])
        self.ev_list.remove(evento)
        self.potential_win = self.potential_win/evento["odd"]
        self.ui.UserHome_PotentialWin_lbl.setText(str(round(self.potential_win,2)))
        self.quota_totale = self.quota_totale/evento["odd"]
        self.ui.UserHome_quotaTotale.setText(str(round(self.quota_totale,2)))

        self.ui.delView_btn.remove(self.ui.delView_btn[self.ui.UserHome_Bet_tbl.currentIndex().row()])
    
    def onInsertBetbtn(self):
        self.betted_amount = self.ui.UserHome_BettedAmount_spin.value()
        self.bet_dict["user_id"] = self.logged_user_info["logged_user_id"]
        self.bet_dict["betted_amount"] = round(float(self.betted_amount),2)
        self.bet_dict["potential_win"] = round(float(self.potential_win),2)
        self.bet_dict["event_outcomes"] = self.ev_list

        res_user = req.getUser(self.logged_user_info["token"],self.logged_user_info["logged_user_id"])
        if(res_user.status_code == 200):
            self.user_infos = res_user.json()
            if(self.user_infos["balance"] < self.bet_dict["betted_amount"]):
                msg = GuiTools.MessageBox("Error", "Saldo insufficiente" , self.my_wnd.geometry().center())
                msg.showMessageError()
            else:
                if(self.ui.UserHome_Bet_tbl.rowCount() > 0):
                    res = req.insertBet(self.logged_user_info["token"],self.bet_dict)
                    if(res.status_code == 201):
                        res_sts = sts_req.updateBetSistemStats(self.bet_dict["betted_amount"])
                        res_sts_user = sts_req.updateBettedAmountUserStats(self.logged_user_info["logged_user_id"],self.bet_dict["betted_amount"])
                        if(res_sts.status_code != 200 and res_sts_user.status_code != 200):
                            msg = GuiTools.MessageBox("Error", "Errore durante aggioranemnto stats sistema ( bet count / update money_gained )" ,self.my_wnd.geometry().center())
                            msg.showMessageError()

                        msg = GuiTools.MessageBox("Success", "Scommessa  inviata correttamente" ,self.my_wnd.geometry().center())
                        msg.showMessageInfo()
                    elif(res.status_code == 401):
                        msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
                        msg.showMessageInfo()
                        self.onLogoutBtn()
                    else:
                        msg = GuiTools.MessageBox("Error", "Impossibile prenotare la scomessa" ,self.my_wnd.geometry().center())
                        msg.showMessageError()
                else:
                    msg = GuiTools.MessageBox("Error", "Inserire almeno un evento!" ,self.my_wnd.geometry().center())
                    msg.showMessageError()


        elif(res_user.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "User not found" ,self.my_wnd.geometry().center())
            msg.showMessageError()
        


    def setPotentialWin(self):
        self.potential_win = round(self.quota_totale * self.ui.UserHome_BettedAmount_spin.value(),2)
        self.ui.UserHome_PotentialWin_lbl.setText(str(round(self.potential_win,2)))
    
    def onProfile(self):
        res = req.getUser(self.logged_user_info["token"],self.logged_user_info["logged_user_id"])
        if(res.status_code == 200):
            self.user_infos = res.json()
            self.ui.UserProfile_name_line.setText(self.user_infos['name'])
            self.ui.UserProfile_surname_line.setText(self.user_infos['surname'])
            self.ui.UserProfile_mail_line.setText(self.user_infos['email'])
            self.ui.UserProfile_pass_line.setText(self.user_infos['password'])
            self.ui.UserProfile_show_balance_line.setText("€ " + str(round(self.user_infos['balance'],2)))
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "User not found" ,self.my_wnd.geometry().center())
            msg.showMessageError()
    
    def onProfileAdmin(self):
        res = req.getUser(self.logged_user_info["token"],self.logged_user_info["logged_user_id"])
        if(res.status_code == 200):
            self.user_infos = res.json()
            self.ui.AdminProfile_name_line.setText(self.user_infos['name'])
            self.ui.AdminProfile_surname_line.setText(self.user_infos['surname'])
            self.ui.AdminProfile_mail_line.setText(self.user_infos['email'])
            self.ui.AdminProfile_pass_line.setText(self.user_infos['password'])
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "User not found" ,self.my_wnd.geometry().center())
            msg.showMessageError()
    
    def CheckBet(self,bet_id,won_flag,*args, **kwargs):
        money_paid = kwargs.get('c', None)
        user_id = kwargs.get('d', None)
        res = req.insertEndedBet(self.logged_user_info["token"],bet_id,won_flag)
        if(res.status_code == 201):
            if(won_flag == True):
                res_sts = sts_req.updateWbetSistemStats(money_paid)
                res_sts_usr = sts_req.updateUserWonStats(user_id,money_paid)
            else:
                res_sts = sts_req.updateFbetSistemStats()
                res_sts_usr = sts_req.updateUserLoseStats(user_id)

            if(res_sts.status_code != 200 and res_sts_usr.status_code != 200):
                msg = GuiTools.MessageBox("Error", "Errore durante aggiornamento delle end bet" ,self.my_wnd.geometry().center())
                msg.showMessageError()

            self.dlg.accept()
            msg = GuiTools.MessageBox("Success", "Bet Validated" ,self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.showAdminBets()

        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "Bet not Validated" ,self.my_wnd.geometry().center())
            msg.showMessageError()
    
    def deleteProfile(self):
        res = req.deleteUser(self.logged_user_info["token"],self.logged_user_info["logged_user_id"])
        if(res.status_code == 200):
            res_sts = sts_req.updateUserCountDel()
            res_sts_usr = sts_req.deletUserStats(self.logged_user_info["logged_user_id"])
            if(res_sts.status_code != 200 and res_sts_usr.status_code != 200):
                msg = GuiTools.MessageBox("Error", "Errore durante aggiornamento stats di sistema" ,self.my_wnd.geometry().center())
                msg.showMessageError()

            self.dlg.accept()
            msg = GuiTools.MessageBox("Success", "Profile deleted successfully" ,self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.showLoginPage()
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "Error During the profile Elimination" ,self.my_wnd.geometry().center())
            msg.showMessageError()
    
    def deleteEvent(self,ev_id):
        res = req.deleteEvent(self.logged_user_info["token"],ev_id)
        if(res.status_code == 200):
            self.dlg.accept()
            msg = GuiTools.MessageBox("Success", "Event deleted successfully" ,self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.showAdminHome()
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "Error During the event Elimination" ,self.my_wnd.geometry().center())
            msg.showMessageError()

    def deleteBet(self,bet_id):
        res = req.deleteBet(self.logged_user_info["token"],bet_id)
        if(res.status_code == 200):
            self.dlg.accept()
            msg = GuiTools.MessageBox("Success", "Bet deleted successfully" ,self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.showAdminBets()
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "Error During the bet Elimination" ,self.my_wnd.geometry().center())
            msg.showMessageError()

    def deleteEbet(self,ebet_id):
        res = req.deleteEndedBet(self.logged_user_info["token"],ebet_id)
        if(res.status_code == 200):
            self.dlg.accept()
            msg = GuiTools.MessageBox("Success", "Bet deleted successfully" ,self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.showAdminBets()
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            msg = GuiTools.MessageBox("Error", "Error During the bet Elimination" ,self.my_wnd.geometry().center())
            msg.showMessageError()
    
    def getEvents(self):
        res = req.getEvents(self.logged_user_info["token"])
        if(res.status_code == 200):
            self.events_infos = res.json()
            return self.events_infos
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.events_infos = None
            return self.events_infos

    def getUsers(self):
        res = req.getUsers(self.logged_user_info["token"])
        if(res.status_code == 200):
            self.users_infos = res.json()
            return self.users_infos
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.user_infos = None
            return self.user_infos

    def getBets(self):
        res = req.getBets(self.logged_user_info["token"])
        if(res.status_code == 200):
            self.bets_infos = res.json()
            return self.bets_infos
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.bets_infos = None
            return self.bets_infos

    def getBetsPerUser(self,user_id):
        res = req.getBetPerUser(self.logged_user_info["token"],user_id)
        if(res.status_code == 200):
            self.bets_infos = res.json()
            return self.bets_infos
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.bets_infos = None
            return self.bets_infos

    def getBet(self,bet_id):
        res = req.getBet(self.logged_user_info["token"],bet_id)
        if(res.status_code == 200):
            self.bets_infos = res.json()
            return self.bets_infos
        elif(res.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.bets_infos = None
            return self.bets_infos

    def getEndbets(self):
        res_w = req.getWonBets(self.logged_user_info["token"])
        res_f = req.getLostBets(self.logged_user_info["token"])
        if(res_w.status_code == 200 and res_w.status_code == 200):
            self.wbets_infos = res_w.json()
            self.fbets_infos = res_f.json()
            return self.wbets_infos,self.fbets_infos
        elif(res_w.status_code == 401 or res_f.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.wbets_infos = None
            self.fbets_infos = None
            return self.wbets_infos,self.fbets_infos

    def getEndbetsPerUser(self,user_id):
        res_w = req.getWonBetsPerUser(self.logged_user_info["token"],user_id)
        res_f = req.getLostBetsPerUser(self.logged_user_info["token"],user_id)
        if(res_w.status_code == 200 and res_w.status_code == 200):
            self.wbets_infos = res_w.json()
            self.fbets_infos = res_f.json()
            return self.wbets_infos,self.fbets_infos
        elif(res_w.status_code == 401 or res_f.status_code == 401):
            msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
            msg.showMessageInfo()
            self.onLogoutBtn()
        else:
            self.wbets_infos = None
            self.fbets_infos = None
            return self.wbets_infos,self.fbets_infos

    def getUserStats(self,user_id):
        res_stats = sts_req.getUserStats(user_id)
        if(res_stats.status_code == 200):
            self.user_stats = res_stats.json()
            return self.user_stats
        else:
            self.user_stats = None
            return self.user_stats
    
    def getSistemStats(self):
        res_stats = sts_req.getSistemStats()
        if(res_stats.status_code == 200):
            self.sis_stats = res_stats.json()
            return self.sis_stats
        else:
            self.sis_stats = None
            return self.sis_stats

    def getUserBGraph(self,user_id):
        res_graph = sts_req.getUserBarGraph(user_id)
        if(res_graph.status_code == 200):
            file = open(f"./media/UserGraph/{user_id}_bar.png", "wb")
            file.write(res_graph.content)
            file.close()

    def getUserPGraph(self,user_id):
        res_graph = sts_req.getUserPieGraph(user_id)
        if(res_graph.status_code == 200):
            file = open(f"./media/UserGraph/{user_id}_pie.png", "wb")
            file.write(res_graph.content)
            file.close()

    def getAdminBGraph(self):
        res_graph = sts_req.getSistemBarGraph()
        if(res_graph.status_code == 200):
            file = open(f"./media/SistemGraph/bar.png", "wb")
            file.write(res_graph.content)
            file.close()

    def getAdminPGraph(self):
        res_graph = sts_req.getSistemPieGraph()
        if(res_graph.status_code == 200):
            file = open(f"./media/SistemGraph/pie.png", "wb")
            file.write(res_graph.content)
            file.close()
        
    def updateEvent(self,ev_id,dlg):
        # Obtain Event name 
        self.event_name = self.dlg.Mdl_Name_lineEdit.text()
        # Partitioning start date
        self.startDate_day = dlg.Mdl_StartDate_lineEdit.sectionText(dlg.Mdl_StartDate_lineEdit.sectionAt(0))
        self.startDate_month = dlg.Mdl_StartDate_lineEdit.sectionText(dlg.Mdl_StartDate_lineEdit.sectionAt(1))
        self.startDate_year = dlg.Mdl_StartDate_lineEdit.sectionText(dlg.Mdl_StartDate_lineEdit.sectionAt(2))
        self.startDate_hour = dlg.Mdl_StartDate_lineEdit.sectionText(dlg.Mdl_StartDate_lineEdit.sectionAt(3))
        self.startDate_minute = dlg.Mdl_StartDate_lineEdit.sectionText(dlg.Mdl_StartDate_lineEdit.sectionAt(4))
        #Partitioning end date
        self.endDate_day = dlg.Mdl_EndDate_lineEdit.sectionText(dlg.Mdl_EndDate_lineEdit.sectionAt(0))
        self.endDate_month = dlg.Mdl_EndDate_lineEdit.sectionText(dlg.Mdl_EndDate_lineEdit.sectionAt(1))
        self.endDate_year = dlg.Mdl_EndDate_lineEdit.sectionText(dlg.Mdl_EndDate_lineEdit.sectionAt(2))
        self.endDate_hour = dlg.Mdl_EndDate_lineEdit.sectionText(dlg.Mdl_EndDate_lineEdit.sectionAt(3))
        self.endDate_minute = dlg.Mdl_EndDate_lineEdit.sectionText(dlg.Mdl_EndDate_lineEdit.sectionAt(4))
        # Obtain the odss
        self.odd_1 = dlg.Mdl_Quota_1_LineEdit.text()
        self.odd_2 = dlg.Mdl_Quota_2_LineEdit.text()
        self.odd_X = dlg.Mdl_Quota_X_LineEdit.text()
        self.odd_GG = dlg.Mdl_Quota_GG_LineEdit.text()
        self.odd_NG = dlg.Mdl_Quota_NG_LineEdit.text()
        self.odd_Ovr = dlg.Mdl_Quota_Ovr_LineEdit.text()
        self.odd_Undr = dlg.Mdl_Quota_Undr_LineEdit.text()
        # Validation
        is_valid_odd_1, res_odd_1 = valid.check_odd(self.odd_1)
        is_valid_odd_2, res_odd_2 = valid.check_odd(self.odd_2)
        is_valid_odd_X, res_odd_X = valid.check_odd(self.odd_X)
        is_valid_odd_GG, res_odd_GG = valid.check_odd(self.odd_GG)
        is_valid_odd_NG, res_odd_NG = valid.check_odd(self.odd_NG)
        is_valid_odd_Ovr, res_odd_Ovr = valid.check_odd(self.odd_Ovr)
        is_valid_odd_Undr, res_odd_Undr = valid.check_odd(self.odd_Undr)
        is_valid_ev_name , res_ev_name = valid.check_eventName(self.event_name)

        if(dlg.Mdl_StartDate_lineEdit.dateTime() >= QDateTime.currentDateTime()):
            is_valid_startDate = True
            res_startDate = "valid Start Date"
        else:
            is_valid_startDate = False
            res_startDate = "Invalid Start Date"

        if(dlg.Mdl_EndDate_lineEdit.dateTime() > dlg.Mdl_StartDate_lineEdit.dateTime()):
            is_valid_endDate = True
            res_endDate = "valid end Date"
        else:
            is_valid_endDate = False
            res_endDate = "Invalid end Date"
        
        # Put Request
        if(is_valid_startDate and is_valid_endDate and is_valid_odd_1 and is_valid_odd_2 and is_valid_odd_X and is_valid_odd_GG and is_valid_odd_NG and is_valid_odd_Ovr and is_valid_odd_Undr and is_valid_ev_name):
            res = req.updateEvent(self.logged_user_info["token"],ev_id,self.event_name,int(self.startDate_day),int(self.startDate_month),int(self.startDate_year),int(self.startDate_hour),int(self.startDate_minute),int(self.endDate_day),int(self.endDate_month),int(self.endDate_year),int(self.endDate_hour),int(self.endDate_minute),float(self.odd_1),float(self.odd_X),float(self.odd_2),float(self.odd_GG),float(self.odd_NG),float(self.odd_Ovr),float(self.odd_Undr))
            if(res.status_code == 200):
                msg = GuiTools.MessageBox("Success", "Event Correctly Inserted" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                dlg.accept()
                self.showAdminHome()
            elif(res.status_code == 401):
                msg = GuiTools.MessageBox("Error", "Sessione Scaduta" , self.my_wnd.geometry().center())
                msg.showMessageInfo()
                self.onLogoutBtn()
            else:
                msg = GuiTools.MessageBox("Error", "Event not inserted " ,self.my_wnd.geometry().center())
                msg.showMessageError()
        else:
            msg = GuiTools.MessageBox("Bad Values", "Event Name:" + res_ev_name +"\n" + "Start date:" + res_startDate +"\n" + "End date:" + res_endDate +"\n" + "Odd 1:" + res_odd_1 + "\n" + "Odd 2:" + res_odd_2 +"\n" + "Odd X:" + res_odd_X +"\n" + "Odd GG:" + res_odd_GG +"\n" + "Odd NG:" + res_odd_NG +"\n" + "Odd Over 2,5:" + res_odd_Ovr +"\n" + "Odd Under 2,5:" + res_odd_Undr , self.my_wnd.geometry().center())
            msg.showMessageError()

    #Functions to set data into the tables in the GUI pages
    def setTableAdmin_getUsers(self,data):
        if(data != None): 
            self.user_ids = []
            self.horHeaders = ["Id Utente","Nome", "Cognome", "Email", "Saldo"]
            self.keys = ["_id","name", "surname", "email", "balance"]
            self.ui.AdminUsers_UserInfos_tbl.setRowCount(0)
            self.ui.AdminUsers_UserInfos_tbl.setColumnCount(5)
            
            for elem in data:
                if(elem["admin"] == True):
                    data.remove(elem)

            for m in range(len(data)):
                self.user_ids.append(data[m]["_id"]["$oid"])
                self.ui.AdminUsers_UserInfos_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == "_id"):
                        item = data[m][key]["$oid"]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminUsers_UserInfos_tbl.setItem(m, n, newitem)
                    elif(key == "balance"):
                        item = data[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminUsers_UserInfos_tbl.setItem(m, n, newitem)
                    else:
                        item = data[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminUsers_UserInfos_tbl.setItem(m, n, newitem)
            self.ui.AdminUsers_UserInfos_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminUsers_UserInfos_tbl.horizontalHeader().setVisible(True)
    
        else:
            self.horHeaders = ["Id Utente","Nome", "Cognome", "Email", "Saldo"]
            self.ui.AdminUsers_UserInfos_tbl.setRowCount(0)
            self.ui.AdminUsers_UserInfos_tbl.setColumnCount(5)
            self.ui.AdminUsers_UserInfos_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminUsers_UserInfos_tbl.horizontalHeader().setVisible(True)
    
    def onViewUsersGraph(self, row, column):
        user_id = self.user_ids[row]
        self.dlg = GuiTools.UserInfoDialog(self.my_wnd.geometry().center())
        self.getUserBGraph(user_id)
        self.dlg.DialogInfoUser_lbl.setPixmap(QtGui.QPixmap(f"./media/UserGraph/{user_id}_bar.png"))
        self.dlg.exec_()

    def setTableAdmin_getEvents(self, data):
        if(data != None):
            self.horHeaders = ["Nome Evento", "Inizio", "Fine", "1","X", "2", "GG", "NG", "Over_2,5", "Under_2,5","Modifica","Elimina"]
            self.keys = ["name", "start_date", "end_date", "odds","Modifica","Elimina"]
            self.ui.AdminHome_EventInfos_tbl.setRowCount(0)
            self.ui.AdminHome_EventInfos_tbl.setColumnCount(12)
            self.ui.AdminHome_EventInfos_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminHome_EventInfos_tbl.horizontalHeader().setVisible(True)
            self.event_ids = []
            self.ui.del_btn = []
            self.ui.edit_btn = []

            for m in range(len(data)):
                temp = {
                    "1" : data[m]["odds"]["1"],
                    "X" : data[m]["odds"]["X"],
                    "2" : data[m]["odds"]["2"],
                    "GG" : data[m]["odds"]["GG"],
                    "NG" : data[m]["odds"]["NG"],
                    "OVER_2,5" : data[m]["odds"]["OVER_2,5"],
                    "UNDER_2,5" : data[m]["odds"]["UNDER_2,5"]
                }
                data[m]["odds"] = OrderedDict(temp)
                self.event_ids.append(data[m]["_id"]["$oid"])
                self.ui.AdminHome_EventInfos_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == "Elimina"):
                        self.ui.del_btn.append(QtWidgets.QPushButton("Elimina"))
                        self.ui.del_btn[self.ui.AdminHome_EventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onDeleteEventBtn(self.event_ids[self.ui.AdminHome_EventInfos_tbl.currentIndex().row()]))
                        self.ui.AdminHome_EventInfos_tbl.setCellWidget(m, n + 6, self.ui.del_btn[self.ui.AdminHome_EventInfos_tbl.currentIndex().row()])
                    elif(key == "Modifica"):
                        self.ui.edit_btn.append(QtWidgets.QPushButton("Modifica"))
                        self.ui.edit_btn[self.ui.AdminHome_EventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onUpdateEventBtn(self.event_ids[self.ui.AdminHome_EventInfos_tbl.currentIndex().row()]))
                        self.ui.AdminHome_EventInfos_tbl.setCellWidget(m, n + 6, self.ui.edit_btn[self.ui.AdminHome_EventInfos_tbl.currentIndex().row()])
                    elif(key == "start_date" or key == "end_date"):
                        item = str(data[m][key]["day"]) + "/" + str(data[m][key]["month"]) + "/" + str(data[m][key]["year"]) + " , " + str(data[m][key]["hour"]) + ":" + str(data[m][key]["minute"]) 
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminHome_EventInfos_tbl.setItem(m, n, newitem)
                    elif(key == "odds"):
                        for k, elem in enumerate(data[m][key]):
                            item = data[m][key][elem]
                            item = round(item,2)
                            newitem = QtWidgets.QTableWidgetItem(str(item))
                            self.ui.AdminHome_EventInfos_tbl.setItem(m, n+k, newitem)
                    else:
                        item = data[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminHome_EventInfos_tbl.setItem(m, n, newitem)
                
        else:
            self.horHeaders = ["Nome Evento", "Inizio", "Fine", "1","X" "2", "GG", "NG", "Over_2,5", "Under_2,5","Modifica","Elimina"]
            self.ui.AdminHome_EventInfos_tbl.setRowCount(0)
            self.ui.AdminHome_EventInfos_tbl.setColumnCount(12)
            self.ui.AdminHome_EventInfos_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminHome_EventInfos_tbl.horizontalHeader().setVisible(True)

    def setTableAdmin_getBets(self, data):
        if(data != None):
            self.horHeaders = ["Id Scommessa","Id Utente","Importo Scomesso","Vincita Potenziale","Vincente","Perdente","Annulla"]
            self.keys = ["_id","user_id","betted_amount","potential_win","Vincente","Perdente","Annulla"]
            self.ui.AdminBets_Bets_tbl.setRowCount(0)
            self.ui.AdminBets_Bets_tbl.setColumnCount(7)
            self.ui.AdminBets_Bets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminBets_Bets_tbl.horizontalHeader().setVisible(True)
            self.bet_ids = []
            self.ui.Betdel_btn = []
            self.ui.Betfail_btn = []
            self.ui.Betwin_btn = []

            for m in range(len(data)):
                self.bet_ids.append(data[m]["_id"]["$oid"])
                self.ui.AdminBets_Bets_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == "_id"):
                        item = data[m][key]["$oid"]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Bets_tbl.setItem(m, n, newitem)
                    elif(key == "Perdente"):
                        self.ui.Betfail_btn.append(QtWidgets.QPushButton("Perdente"))
                        self.ui.Betfail_btn[self.ui.AdminBets_Bets_tbl.currentIndex().row()].clicked.connect(lambda : self.onCheckBetBtn(self.bet_ids[self.ui.AdminBets_Bets_tbl.currentIndex().row()],False,d=data[self.ui.AdminBets_Bets_tbl.currentIndex().row()]["user_id"]))
                        self.ui.AdminBets_Bets_tbl.setCellWidget(m, n , self.ui.Betfail_btn[self.ui.AdminBets_Bets_tbl.currentIndex().row()])
                    elif(key == "Vincente"):
                        self.ui.Betwin_btn.append(QtWidgets.QPushButton("Vincente"))
                        self.ui.Betwin_btn[self.ui.AdminBets_Bets_tbl.currentIndex().row()].clicked.connect(lambda : self.onCheckBetBtn(self.bet_ids[self.ui.AdminBets_Bets_tbl.currentIndex().row()],True,c=data[self.ui.AdminBets_Bets_tbl.currentIndex().row()]["potential_win"],d=data[self.ui.AdminBets_Bets_tbl.currentIndex().row()]["user_id"]))
                        self.ui.AdminBets_Bets_tbl.setCellWidget(m, n , self.ui.Betwin_btn[self.ui.AdminBets_Bets_tbl.currentIndex().row()])
                    elif(key == "Annulla"):
                        self.ui.Betdel_btn.append(QtWidgets.QPushButton("Annulla"))
                        self.ui.Betdel_btn[self.ui.AdminBets_Bets_tbl.currentIndex().row()].clicked.connect(lambda : self.onDeleteBetBtn(self.bet_ids[self.ui.AdminBets_Bets_tbl.currentIndex().row()]))
                        self.ui.AdminBets_Bets_tbl.setCellWidget(m, n , self.ui.Betdel_btn[self.ui.AdminBets_Bets_tbl.currentIndex().row()])
                    elif(key == "potential_win"):
                        item = data[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Bets_tbl.setItem(m, n, newitem)
                    else:
                        item = data[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Bets_tbl.setItem(m, n, newitem)

        else:
            self.horHeaders = ["Id Scommessa","Id Utente","Importo Scomesso","Vincita Potenziale","Vincente","Perdente","Annulla"]
            self.ui.AdminBets_Bets_tbl.setRowCount(0)
            self.ui.AdminBets_Bets_tbl.setColumnCount(7)
            self.ui.AdminBets_Bets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminBets_Bets_tbl.horizontalHeader().setVisible(True)

    def setTableAdmin_getEndBets(self,data_won,data_lose):   
        if(data_lose != None): 
            self.horHeaders = ["Id Utente","Id Scommessa","Vincita",""]
            self.keys = ["user_id","bet_id","won_amount",""]
            self.ui.AdminBets_Fbets_tbl.setRowCount(0)
            self.ui.AdminBets_Fbets_tbl.setColumnCount(4)
            self.ui.AdminBets_Fbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminBets_Fbets_tbl.horizontalHeader().setVisible(True)
            self.fbet_ids = []
            self.ui.Fbetdel_btn = []  
            for m in range(len(data_lose)):
                self.fbet_ids.append(data_lose[m]["_id"]["$oid"])
                self.ui.AdminBets_Fbets_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == ""):
                        self.ui.Fbetdel_btn.append(QtWidgets.QPushButton("Elimina"))
                        self.ui.Fbetdel_btn[self.ui.AdminBets_Fbets_tbl.currentIndex().row()].clicked.connect(lambda : self.onDeleteEndBetBtn(self.fbet_ids[self.ui.AdminBets_Fbets_tbl.currentIndex().row()]))
                        self.ui.AdminBets_Fbets_tbl.setCellWidget(m, n , self.ui.Fbetdel_btn[self.ui.AdminBets_Fbets_tbl.currentIndex().row()])
                    elif(key == "won_amount"):
                        item = data_lose[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Fbets_tbl.setItem(m, n, newitem)
                    else:
                        item = data_lose[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Fbets_tbl.setItem(m, n, newitem)
        else:
            self.horHeaders = ["Id Utente","Id Scommessa","Vincita"]
            self.ui.AdminBets_Fbets_tbl.setRowCount(0)
            self.ui.AdminBets_Fbets_tbl.setColumnCount(3)
            self.ui.AdminBets_Fbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminBets_Fbets_tbl.horizontalHeader().setVisible(True)

        if(data_won != None):
            self.horHeaders = ["Id Utente","Id Scommessa","Vincita",""]
            self.keys = ["user_id","bet_id","won_amount",""]
            self.ui.AdminBets_Wbets_tbl.setRowCount(0)
            self.ui.AdminBets_Wbets_tbl.setColumnCount(4)
            self.ui.AdminBets_Wbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminBets_Wbets_tbl.horizontalHeader().setVisible(True)    
            self.wbet_ids = []
            self.ui.Wbetdel_btn = []
            for m in range(len(data_won)):
                self.wbet_ids.append(data_won[m]["_id"]["$oid"])
                self.ui.AdminBets_Wbets_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == ""):
                        self.ui.Wbetdel_btn.append(QtWidgets.QPushButton("Elimina"))
                        self.ui.Wbetdel_btn[self.ui.AdminBets_Wbets_tbl.currentIndex().row()].clicked.connect(lambda : self.onDeleteEndBetBtn(self.wbet_ids[self.ui.AdminBets_Wbets_tbl.currentIndex().row()]))
                        self.ui.AdminBets_Wbets_tbl.setCellWidget(m, n , self.ui.Wbetdel_btn[self.ui.AdminBets_Wbets_tbl.currentIndex().row()])
                    elif(key == "won_amount"):
                        item = data_won[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Wbets_tbl.setItem(m, n, newitem)
                    else:
                        item = data_won[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.AdminBets_Wbets_tbl.setItem(m, n, newitem)
        else:
            self.horHeaders = ["Id Utente","Id Scommessa","Vincita"]
            self.ui.AdminBets_Wbets_tbl.setRowCount(0)
            self.ui.AdminBets_Wbets_tbl.setColumnCount(3)
            self.ui.AdminBets_Wbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.AdminBets_Wbets_tbl.horizontalHeader().setVisible(True)
    
    def setTableUser_getBets(self, data):
        if(data != None):
            self.horHeaders = ["Id Scommessa","Importo Scomesso","Vincita Potenziale"]
            self.keys = ["_id","betted_amount","potential_win"]
            self.ui.UserBets_Bets_tbl.setRowCount(0)
            self.ui.UserBets_Bets_tbl.setColumnCount(3)
            self.ui.UserBets_Bets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserBets_Bets_tbl.horizontalHeader().setVisible(True)
            self.bet_ids = []

            for m in range(len(data)):
                self.bet_ids.append(data[m]["_id"]["$oid"])
                self.ui.UserBets_Bets_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == "_id"):
                        item = data[m][key]["$oid"]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Bets_tbl.setItem(m, n, newitem)
                    elif(key == "potential_win"):
                        item = data[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Bets_tbl.setItem(m, n, newitem)
                    else:
                        item = data[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Bets_tbl.setItem(m, n, newitem)

        else:
            self.horHeaders = ["Id Scommessa","Importo Scomesso","Vincita Potenziale"]
            self.ui.UserBets_Bets_tbl.setRowCount(0)
            self.ui.UserBets_Bets_tbl.setColumnCount(3)
            self.ui.UserBets_Bets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserBets_Bets_tbl.horizontalHeader().setVisible(True)
        
    def setTableUser_getEndBets(self,data_won,data_lose):   
        if(data_lose != None): 
            self.horHeaders = ["Id Scommessa","Vincita"]
            self.keys = ["bet_id","won_amount"]
            self.ui.UserBets_Fbets_tbl.setRowCount(0)
            self.ui.UserBets_Fbets_tbl.setColumnCount(2)
            self.ui.UserBets_Fbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserBets_Fbets_tbl.horizontalHeader().setVisible(True)
            self.fbet_ids = []
            for m in range(len(data_lose)):
                self.fbet_ids.append(data_lose[m]["_id"]["$oid"])
                self.ui.UserBets_Fbets_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == "won_amount"):
                        item = data_lose[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Fbets_tbl.setItem(m, n, newitem)
                    else:
                        item = data_lose[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Fbets_tbl.setItem(m, n, newitem)
        else:
            self.horHeaders = ["Id Scommessa","Vincita"]
            self.ui.UserBets_Fbets_tbl.setRowCount(0)
            self.ui.UserBets_Fbets_tbl.setColumnCount(2)
            self.ui.UserBets_Fbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserBets_Fbets_tbl.horizontalHeader().setVisible(True)

        if(data_won != None):
            self.horHeaders = ["Id Scommessa","Vincita"]
            self.keys = ["bet_id","won_amount"]
            self.ui.UserBets_Wbets_tbl.setRowCount(0)
            self.ui.UserBets_Wbets_tbl.setColumnCount(2)
            self.ui.UserBets_Wbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserBets_Wbets_tbl.horizontalHeader().setVisible(True)
            self.wbet_ids = []    
            
            for m in range(len(data_won)):
                self.wbet_ids.append(data_won[m]["_id"]["$oid"])
                self.ui.UserBets_Wbets_tbl.insertRow(m)
                for n, key in enumerate(self.keys):
                    if(key == "won_amount"):
                        item = data_won[m][key]
                        item = round(item,2)
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Wbets_tbl.setItem(m, n, newitem)
                    else:
                        item = data_won[m][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserBets_Wbets_tbl.setItem(m, n, newitem)
        else:
            self.horHeaders = ["Id Scommessa","Vincita"]
            self.ui.UserBets_Wbets_tbl.setRowCount(0)
            self.ui.UserBets_Wbets_tbl.setColumnCount(2)
            self.ui.UserBets_Wbets_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserBets_Wbets_tbl.horizontalHeader().setVisible(True)

    def setTableUser_getEvents(self, data):
        if(data != None):
            self.horHeaders = ["Nome Evento", "Inizio", "Fine", "1","X", "2", "GG", "NG", "Over_2,5", "Under_2,5"]
            self.keys = ["name", "start_date", "end_date", "odds"]
            self.ui.UserHomeEventInfos_tbl.setRowCount(0)
            self.ui.UserHomeEventInfos_tbl.setColumnCount(10)
            self.ui.UserHomeEventInfos_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserHomeEventInfos_tbl.horizontalHeader().setVisible(True)
            self.event_ids = []
            self.ui.odd1_btn = []
            self.ui.oddX_btn = []
            self.ui.odd2_btn = []
            self.ui.oddGG_btn = []
            self.ui.oddNG_btn = []
            self.ui.oddOvr_btn = []
            self.ui.oddUndr_btn = []
        
            for m in range(len(data)):
                temp = {
                    "1" : data[m]["odds"]["1"],
                    "X" : data[m]["odds"]["X"],
                    "2" : data[m]["odds"]["2"],
                    "GG" : data[m]["odds"]["GG"],
                    "NG" : data[m]["odds"]["NG"],
                    "OVER_2,5" : data[m]["odds"]["OVER_2,5"],
                    "UNDER_2,5" : data[m]["odds"]["UNDER_2,5"]
                }
                data[m]["odds"] = OrderedDict(temp)

                self.ev_start_date = QtCore.QDateTime(QtCore.QDate(data[m]["start_date"]["year"], data[m]["start_date"]["month"], data[m]["start_date"]["day"]), QtCore.QTime(data[m]["start_date"]["hour"], data[m]["start_date"]["minute"], 0))
                if(self.ev_start_date > QDateTime.currentDateTime()):
                    self.event_ids.append(data[m]["_id"]["$oid"])
                    self.ui.UserHomeEventInfos_tbl.insertRow(m)
                    for n, key in enumerate(self.keys):
                        if(key == "start_date" or key == "end_date"):
                            item = str(data[m][key]["day"]) + "/" + str(data[m][key]["month"]) + "/" + str(data[m][key]["year"]) + " , " + str(data[m][key]["hour"]) + ":" + str(data[m][key]["minute"]) 
                            newitem = QtWidgets.QTableWidgetItem(str(item))
                            self.ui.UserHomeEventInfos_tbl.setItem(m, n, newitem)
                        elif(key == "odds"):
                            for k, elem in enumerate(data[m][key]):
                                if(elem == "1"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.odd1_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.odd1_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.odd1_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"1"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k , self.ui.odd1_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                                elif(elem == "X"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.oddX_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.oddX_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.oddX_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"X"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k , self.ui.oddX_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                                elif(elem == "2"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.odd2_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.odd2_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.odd2_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"2"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k , self.ui.odd2_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                                elif(elem == "GG"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.oddGG_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.oddGG_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.oddGG_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"GG"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k , self.ui.oddGG_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                                elif(elem == "NG"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.oddNG_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.oddNG_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.oddNG_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"NG"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k, self.ui.oddNG_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                                elif(elem == "OVER_2,5"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.oddOvr_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.oddOvr_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.oddOvr_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"OVER_2,5"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k, self.ui.oddOvr_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                                elif(elem == "UNDER_2,5"):
                                    item = data[m][key][elem]
                                    item = round(item,2)
                                    self.ui.oddUndr_btn.append(QtWidgets.QPushButton(str(item)))
                                    self.ui.oddUndr_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].setFlat(True)
                                    self.ui.oddUndr_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()].clicked.connect(lambda : self.onSelectEventForBet(data[self.ui.UserHomeEventInfos_tbl.currentIndex().row()],"UNDER_2,5"))
                                    self.ui.UserHomeEventInfos_tbl.setCellWidget(m, n + k, self.ui.oddUndr_btn[self.ui.UserHomeEventInfos_tbl.currentIndex().row()])
                        else:
                            item = data[m][key]
                            newitem = QtWidgets.QTableWidgetItem(str(item))
                            self.ui.UserHomeEventInfos_tbl.setItem(m, n, newitem)

        else:
            self.horHeaders = ["Nome Evento", "Inizio", "Fine", "1","X","2", "GG", "NG", "Over_2,5", "Under_2,5"]
            self.ui.UserHomeEventInfos_tbl.setRowCount(0)
            self.ui.UserHomeEventInfos_tbl.setColumnCount(10)
            self.ui.UserHomeEventInfos_tbl.setHorizontalHeaderLabels(self.horHeaders)
            self.ui.UserHomeEventInfos_tbl.horizontalHeader().setVisible(True)
    
    #Utility function for bets
    def onViewBetInfo(self,row, column):
        bet_id = self.bet_ids[row]
        self.dlg = GuiTools.BetInfoDialog(self.my_wnd.geometry().center())
        bet_infos = self.getBet(bet_id)
        event_id_key = "Event_id_"
        event_name_key = "Event_name_"
        outcome_name_key = "Outcome_name_"
        event_outcome_key = "Event_outcome_"

        if(bet_infos != None):
            size = (len(bet_infos["event_outcomes"]))//4
            keys = [[] for j in range(size)]
            for i in range(size):
                keys[i].append(event_id_key + str(i+1))
                keys[i].append(event_name_key + str(i+1))
                keys[i].append(event_outcome_key + str(i+1))
                keys[i].append(outcome_name_key + str(i+1))
                self.dlg.BetInfo_tbl.insertRow(i)
                for col, key in enumerate(keys[i]):
                    if(key == f"Event_outcome_{i+1}"):
                        item = bet_infos["event_outcomes"][key]
                        newitem = QtWidgets.QTableWidgetItem(str(round(item,2)))
                        self.dlg.BetInfo_tbl.setItem(i,col, newitem)
                    else:
                        item = bet_infos["event_outcomes"][key]
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.dlg.BetInfo_tbl.setItem(i,col, newitem)
        self.dlg.exec_()

    def onSelectEventForBet(self,data,elem):
        self.horHeaders = ["Evento Selezionato",""]
        self.ui.UserHome_Bet_tbl.setColumnCount(2)
        self.ui.UserHome_Bet_tbl.setHorizontalHeaderLabels(self.horHeaders)
        self.ui.UserHome_Bet_tbl.horizontalHeader().setVisible(True)

        if(data["_id"]["$oid"] in self.selected_event_ids):
            msg = GuiTools.MessageBox("Error", "Evento già presente, eliminalo se vuoi cambiare esito " ,self.my_wnd.geometry().center())
            msg.showMessageError()
        else:
            self.ui.delView_btn = []
            self.quota_totale = 1.00
            self.potential_win = 1.00
            self.ui.UserHome_Bet_tbl.setRowCount(0)     
            if(len(self.ev_list) < 20):
                self.selected_event_ids.append(data["_id"]["$oid"])
                self.ev_list.append({
                    "event_id" : data["_id"]["$oid"],
                    "event_name": data["name"],
                    "outcome_name": elem,
                    "odd" : round(data["odds"][elem],2)
                })
            for row_index in range(len(self.ev_list)):
                self.ui.UserHome_Bet_tbl.insertRow(row_index)
                for n, key in enumerate(self.horHeaders):
                    if(key == ""):
                        self.ui.delView_btn.append(QtWidgets.QPushButton("Rimuovi"))
                        self.ui.delView_btn[self.ui.UserHome_Bet_tbl.currentIndex().row()].clicked.connect(lambda : self.delRow(self.ev_list[self.ui.UserHome_Bet_tbl.currentIndex().row()]))
                        self.ui.UserHome_Bet_tbl.setCellWidget(row_index,n,self.ui.delView_btn[self.ui.UserHome_Bet_tbl.currentIndex().row()])
                    else:
                        item = self.ev_list[row_index]["event_name"] + "\n" + self.ev_list[row_index]["outcome_name"] + " : " + str(round(self.ev_list[row_index]["odd"],2))
                        newitem = QtWidgets.QTableWidgetItem(str(item))
                        self.ui.UserHome_Bet_tbl.setItem(row_index, n, newitem)

                        self.quota_totale = self.quota_totale * self.ev_list[row_index]["odd"]
                        self.ui.UserHome_quotaTotale.setText(str(round(self.quota_totale,2)))
                        self.potential_win = self.quota_totale * self.ui.UserHome_BettedAmount_spin.value()
                        self.ui.UserHome_PotentialWin_lbl.setText(str(round(self.potential_win,2)))

            if(len(self.ev_list) >= 20):
                msg = GuiTools.MessageBox("Error", "Hai raggiunto il limite massimo di eventi giocabili" ,self.my_wnd.geometry().center())
                msg.showMessageError()


    # Function to navigate into the GUI
    def show(self):
        self.my_wnd.show()

    def showRegistrationPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Registration)

    def showLoginPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Login)

    def showUserProfile(self):
        self.onProfile()
        self.ui.stackedWidget.setCurrentWidget(self.ui.UserProfile)

    def showUserHome(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.UserHome)
        self.events = self.getEvents()
        self.setTableUser_getEvents(self.events)

    def showUserBets(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.UserBets)
        self.bets = self.getBetsPerUser(self.logged_user_info["logged_user_id"])
        self.setTableUser_getBets(self.bets)
        self.wbets,self.fbets = self.getEndbetsPerUser(self.logged_user_info["logged_user_id"])
        self.setTableUser_getEndBets(self.wbets,self.fbets)

    def showUserStats(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.UserStats)
        self.stats = self.getUserStats(self.logged_user_info["logged_user_id"])
        if(self.stats != None):
            self.ui.UserStats_paid_money_lbl.setText("€ " + str(round(self.stats[0]["paid_money"],2)))
            self.ui.UserStats_won_money_lbl.setText("€ " + str(round(self.stats[0]["won_money"],2)))
            self.ui.UserStats_betted_money_lbl.setText("€ " + str(round(self.stats[0]["betted_money"],2)))
            self.ui.UserStats_num_wbet_lbl.setText(str(self.stats[0]["num_wbet"]))
            self.ui.UserStats_num_fbet_lbl.setText(str(self.stats[0]["num_fbet"]))
            self.getUserBGraph(self.logged_user_info["logged_user_id"])
            user_id = self.logged_user_info["logged_user_id"]
            self.ui.UserStats_Bar_lbl.setPixmap(QtGui.QPixmap(f"./media/UserGraph/{user_id}_bar.png"))
            if(self.stats[0]["num_wbet"] > 0 or self.stats[0]["num_fbet"] > 0):
                self.getUserPGraph(self.logged_user_info["logged_user_id"])
                self.ui.UserStats_Pie_lbl.setPixmap(QtGui.QPixmap(f"./media/UserGraph/{user_id}_pie.png"))
            else:
                self.ui.UserStats_Pie_lbl.setText("Grafico Sommesse Vinte/Perse  non disponibile")
            

    def showAdminHome(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AdminHome)
        self.ui.AdminHome_eventStartDate_line.setDateTime(QDateTime.currentDateTime())
        self.ui.AdminHome_eventEndDate_line.setDateTime(QDateTime.currentDateTime())
        self.events = self.getEvents()
        self.setTableAdmin_getEvents(self.events)

    def showAdminUsers(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AdminUsers)
        self.users = self.getUsers()
        self.setTableAdmin_getUsers(self.users)
    
    def showAdminProfile(self):
        self.onProfileAdmin()
        self.ui.stackedWidget.setCurrentWidget(self.ui.AdminProfile)

    def showAdminBets(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AdminBets)
        self.bets = self.getBets()
        self.setTableAdmin_getBets(self.bets)
        self.wbets,self.fbets = self.getEndbets()
        self.setTableAdmin_getEndBets(self.wbets,self.fbets)

    def showAdminStats(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.AdminStats)
        self.stats = self.getSistemStats()
        if(self.stats != None):
            self.ui.AdminStats_registered_users_lbl.setText(str(round(self.stats[0]["registered_users"],2)))
            self.ui.AdminStats_num_bet_lbl.setText(str(self.stats[0]["bet_count"]))
            self.ui.AdminStats_num_wbet_lbl.setText(str(self.stats[0]["wbet_count"]))
            self.ui.AdminStats_num_fbet_lbl.setText(str(self.stats[0]["fbet_count"]))
            self.ui.AdminStats_money_gained_lbl.setText("€ " + str(round(self.stats[0]["money_gained"],2)))
            self.ui.AdminStats_money_paid_lbl.setText("€ " +str(round(self.stats[0]["money_paid"],2)))
            self.getAdminBGraph()
            self.ui.AdminStats_Bar_lbl.setPixmap(QtGui.QPixmap("./media/sistemGraph/bar.png"))
            if(self.stats[0]["wbet_count"] > 0 or self.stats[0]["fbet_count"] > 0):
                self.getAdminPGraph()
                self.ui.AdminStats_Pie_lbl.setPixmap(QtGui.QPixmap("./media/SistemGraph/pie.png"))
            else:
                self.ui.UserStats_Pie_lbl.setText("Grafico Sommesse Vinte/Perse  non disponibile")

if __name__ == "__main__":
    try:
        res_alive = req.pingServer()
        res_stats = sts_req.getSistemStats()
        res_value = res_stats.json()
        if(len(res_value) == 0):
            sts_req.createSistemStats()

        app = QtWidgets.QApplication(sys.argv)
        SoccerBet_window = SoccerBetUiController()
        SoccerBet_window.show()
        sys.exit(app.exec_())

    except requests.exceptions.ConnectionError as errc:
        app = QtWidgets.QApplication(sys.argv)
        SoccerBet_window = SoccerBetUiController()
        SoccerBet_window.show()
        
        msg = GuiTools.MessageBox("Connection Error", str(errc) + "\n\n" + "Please close the application and retry later" , SoccerBet_window.my_wnd.geometry().center())
        msg.showMessageError()
        
        sys.exit(app.exec_())

        