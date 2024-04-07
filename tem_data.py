from random import *

STORE_DB = {}

# store database also add and mention in the store details

ATUStore = {
    'LED 9W': ['A24', ['000', '001', '002', '003'], '2103024', '155', 'A01'],
    'PEN (BLACK)': ['A24', ['000', '001', '002', '003'], '2103024', '10', 'A02'],
    'PEN (BLUE)': ['A24', ['000', '001', '002', '003'], '2103024', '10', 'A03'],
    'DEODORANT' : ['B24', ['001','002','003','004','010'],'2003024', '99', 'A04'],
    'RICE 1KG': ['B24', ['020','021','022'], '200324', '60', 'A05'],
}

# name: [BatchNo, [ItemID], expDate, price, location]

store1234 = {
    'NAME_OF_PRODUCT': ['A05', ['000', '020', '041'], '1212023', '100', '03F'],
    'BINGO': ['B01', ['000', '002', '003'], '9876543', '100', '02F'],
    'KNIFE': ['A15',['000', '997', '998', '999'], '1234567', '999', '01F'],
    'WALLET': ['B22', [], '8765432', '150', '123'],
    'SUGAR': ['B25', ['023', '024', '025'], '1203024', '030', '04F'],
}

# Phone Number: [name, email, (address), password, reference, balance, [avOffer], [reward]]

User_list = {
    'ph' : ['fname', 'Email', "addrs", "pwd", "Ref", '1000', ['OFFerCode'], []],
    '9876543210': ['AKG','AKG@gmail.com', ('KERALA','CALICUT','PUTHIYARA','PUTHIYARA'),'123456','','10000', [''], [10]],
    '1234567890': ['ABC','ABC@gmail.com', ('1','2','3','4'), '543210', '', '1000', [''], ['']],
    '9400642545': ['ANANTHU', 'ananthus1687@gmail.com', ('KERALA','CALICUT','KETTANGAL','NIT'), 'Ananthu@28','REFID','100000', [('SPECIAL10',10)], [100]],
}

# UniqueSID: [storename, storeID, email, address, contact, password, offercode, storeDB, Income]
# store must be added manually

Market_list = {
    'storename': ['storeName', 'storeid', 'email', ['STATE', 'DICT', 'CITY'], 'contact', 'password', [('OFFERCODE', 100)], STORE_DB, 'Income'],
    'AbcStores': ['abc Stores', '1234', 'abcstore@gmail.com', ['KERALA', 'CALICUT', 'MUKKAM'], '1234567890', '543210', [('SPECIAL10',10)], store1234, '100000'],
    'ATU-S': ['ATU Market', '9999', 'atumart@gmail.com', ['KERALA', 'CALICUT', 'KETTANGAL'], '9400642545', '1234567890', [('FLAT020', 20)], ATUStore, '100000']
}

# ItemName: [batch, (ItemID), expdate, price, location]
#1234002B01987654310002F
#1234999A15123456799901F


def LoginValid(Uname : str, Password : str):
    for User in User_list.keys():
        if User == Uname and User_list[User][3] == Password:
            return ('User', User)

    else:
        for clint in Market_list.keys():
            if clint == Uname or Market_list[clint][1] and Market_list[clint][5] == Password:
                return ('clint', clint)
            
    return 'False'


class OTPHandler:
    def GenOTP(self, Number : str):
        global NewOtp
        a = len(Number)

        if a == 10:
            for Users in User_list.keys():

                if(Number == Users):
                    num = randint(10000,99999)
                    NewOtp = num
                    return NewOtp

            else: 
                num = randint(1000,9999)
                NewOtp = num
                return NewOtp
            
        return False

    def ForGetPWD(self, Phone : str ,Npwd : str, OTPCheck : str):
        if(OTPCheck == str(NewOtp)):
            print( OTPCheck, NewOtp)
            User_list[Phone][3] = Npwd
            return True
        
        return False

    def VerifyNum(self, OTPCheck : str):
        if(OTPCheck == str(NewOtp)):
            return True
        
        return False

local_list = []


class signup:
    def New_User(self, Fname : str, Phno : str, Email : str):
        global name, email, Phone
        a = len(Phno)

        if a ==10 :
            Phone = Phno

        else: 
            return False
        
        exten = Email

        if exten[-10:] != '@gmail.com':
            Email = Email + '@gmail.com'

        email = Email
        name = Fname

        local_list.append(name)
        local_list.append(email)

        return True
        
    def address(self, state : str, Distr : str, city : str, st_name : str):
        global addr 

        addr = st_name,city,Distr,st_name,st_name,state
        local_list.append(addr)
        return True
        
    def New_pass(self, fPassword : str, CPassword : str, refrence : str | None = ''):
        global Final_Password, ref
        if refrence :
            print('have a reference')
            ref = refrence
            
        else:
            print("ref = None")
            ref = ''

        if fPassword == CPassword:
            Final_Password = fPassword
            local_list.append(Final_Password)
            local_list.append(ref)
            local_list.append('0')
            local_list.append([''])
            local_list.append([])
            return True
        
        else:
            return False
        
    def Add_details(self):
        User_list[Phone] = local_list
        print(User_list)
        return True


class productDetails:
    def AddProduct(self, storeDB : str, nameOfProduct : str, BatchNo : str, ItemID : str, expdate : str, Price : str, loct : str, status : int):
        listItem = []

        if status:
            lastOne = int(storeDB[nameOfProduct][1][-1])
            if lastOne == 999:
                return False
            
            else:
                lastOne = lastOne + 1

                for item in range(lastOne, (lastOne + int(ItemID))):
                    print(item)
                    item = str(item)

                    if len(item) == 2:
                        item = '0' + item
                        storeDB[nameOfProduct][1].append(item)

                    elif len(item) == 1:
                        item = '00' + item
                        storeDB[nameOfProduct][1].append(item)

                expdate = expdate[8:10] + expdate[5:7] + expdate[1:4]
                storeDB[nameOfProduct][2] = expdate 

                return True

        else:

            for item in range(0, int(ItemID)):
                
                item = str(item)
                if len(item) == 2:
                    item = '0' + item
                    listItem.append(item)

                elif len(item) == 1:
                    item = '00' + item
                    listItem.append(item)

            expdate = expdate[8:10] + expdate[5:7] + expdate[1:4]

            product_detail_list = [BatchNo, listItem, expdate, Price, loct]
            storeDB[nameOfProduct] = product_detail_list

            return True


def generate_QR_Data(storeDB : str, ItemName : str): 
    returnlist = []
    item = storeDB[ItemName]
    # -- data = | storeID | itemID | batchID | EXPDATE | Price | loct | --
    for sname in Market_list.keys():
        if Market_list[sname][7] == storeDB:
            SID = Market_list[sname][1]
            break

    for IID in item[1]:
        data = SID + IID + item[0] + item[2] + item[3] + item[4]
        if len(data) == 23:
            returnlist.append(data)
        
    return returnlist
