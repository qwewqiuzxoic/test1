from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print('Kiwoom')
        self.login_event_loop = None

        self.account_num = None

        self.get_ocx_instance()
        self.event_sloats()
        self.signal_login_commConnect()
        self.get_account_info()
        self.ditail_account_info()
    def get_ocx_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def event_sloats(self):
        self.OnEventConnect.connect(self.login_slot)
        self.OnReceiveTrData.connect(self.trdata_slot)

    def login_slot(self,errCode):
        print(errors(errCode))
        self.login_event_loop.exit()
        print(self.login_event_loop)

    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(String)", "ACCNO")
        self.account_num = account_list.split(';')[0]
        print(self.account_num, "111")

    def signal_login_commConnect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()
        print(self.login_event_loop)


    def ditail_account_info(self):
        print('예수금')
        self.dynamicCall("SetInputValue(String,String)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(String,String)","비밀번호","rlaehd95")
        self.dynamicCall("SetInputValue(String,String)","비밃전호입력매체구분","00")
        self.dynamicCall("SetInputValue(String,String)","조회구분","2")
        self.dynamicCall("CommRqData(String,String,int,String)","예수금상세요청","opw00001","0","2000")

    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        if sRQName == "예수금상세요청":
            deposit = self.dynamicCall("GetCommData(String,String,int,String)",sTrCode,sRQName,0,"예수금")
            print(int(deposit))
            ok_deposit = self.dynamicCall("GetCommData(String,String,int,String)",sTrCode,sRQName,0,"출금가능금액")
            print("출금 가능 금액", ok_deposit)


