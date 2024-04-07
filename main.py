from random import *
from tem_data import *
from kivymd.app import MDApp
from kivymd.toast import toast

from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDIconButton

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.imagelist.imagelist import MDSmartTile

from kivymd.uix.list import IRightBodyTouch, TwoLineAvatarIconListItem, TwoLineListItem
from kivy_garden.qrcode.qrcode_widget import QRCodeWidget
from kivymd.uix.selectioncontrol import MDCheckbox

from kivymd.uix.screen import MDScreen
from kivy.lang.builder import Builder




from kivy.core.window import Window
# -- importing essenstial packages --


productDetail = productDetails()
OTPh = OTPHandler()
USp = signup()
# -- creating onbject for classes on tem_data --

logined_User = str()
storeDB = str()
# -- assign the name of user/store and Store Database --


Window.size = (480,750)
# --setting window size according to a mobile phone --

class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    pass
    # -- class used for assist the select screen of store --


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass
    # -- class used for assist the select screen of store --


class Login(MDScreen):
    def validate(self):
        # -- button submit press and check the below conditions --

        global logined_User, storeDB
        # -- global assignment of User and DB
        UserName = self.ids.Uname.text
        pswd = self.ids.Pass.text

        validation_result = LoginValid(UserName, pswd)
        # -- check the given username and password belongs to whom --

        if validation_result[0] == 'clint':
            logined_User = validation_result[1]
            storeDB = Market_list[logined_User][7]
            # --if there return value is clint assign values and shift to Store Screen --

            self.manager.transition.direction = 'left'
            self.manager.current = 'CHomePage'

            self.ids.Uname.text = ''
            self.ids.Pass.text = ''
            # -- clear text input after transition for further use --

        elif validation_result[0] == 'User':
            logined_User = validation_result[1]
            # -- if return value is user assign and schange screen to userscreen --

            self.manager.transition.direction = 'left'
            self.manager.current = 'CTMHome'

            self.ids.Uname.text = ''
            self.ids.Pass.text = ''

        else:
            self.LoginFail = MDDialog(
                title="Invalid Login !",
                text="Incorrect username or password. Please try again.",
                buttons=[
                    MDRaisedButton(
                        text = "OK", 
                        on_release = self.dialog_callback,
                    ),
                ],
            )
            self.LoginFail.open()
            # -- if the value is none of in the list or password was missmatch open a pop-up window --

            self.ids.Uname.text = ''
            self.ids.Pass.text = ''

    def dialog_callback(self, *args):
        self.LoginFail.dismiss()
        # -- close pop-up window --


class Basics(MDScreen):
    def on_enter(self, *args):
        self.otpbox = MDDialog(
            title = '',
            text = '',
            type = 'alert',
                buttons=[
                    MDRaisedButton(
                        text = "OK",
                        on_release = self.OTPClose,
                    ),
                ],
            )
        # -- create a pop-up for fast assignment and easy calling --
        
    def SignOTP(self):

        global PHno
        PHno = self.ids.PHno.text

        if len(PHno) == 10:
            self.ids.PHno.readonly = True
            genSOTP = OTPh.GenOTP(PHno)
            # -- verify length of phone number is 10  and generating OTP --

            if len(str(genSOTP)) == 4:

                self.otpbox.title = 'New OTP'
                self.otpbox.text = f'Your New OTP is  {str(genSOTP)} '  
                self.otpbox.open()
                # -- 4 digit for sign-up OTP --

            elif len(str(genSOTP)) == 5:
                self.otpbox.title = 'Dupicate Number'
                self.otpbox.text = 'This Number already exist, Verify the number again'
                self.otpbox.open()
                # -- if number already exist 5 digit OTP return so calling false --
                # -- Opening pop-up --

                self.ids.PHno.text = ''

        else:
            self.ids.PHno.readonly = False

    def OTPClose(self, *args):
        self.otpbox.dismiss()
        # -- dissmisal of pop-up
        
    def ValidOTP(self):
        otp = self.ids.SOTP.text

        if len(otp) == 4:
            vrfy = OTPh.VerifyNum(otp)
            # -- check wether entered OTP is same --

            if not vrfy:
                self.otpbox.title = 'Mismatch OTP'
                self.otpbox.text = "The enter OTP can't match"
                self.otpbox.open()

                self.ids.SOTP.text = ''
                self.ids.PHno.text = ''
                # -- if not verified clear input and open pop-up --

            else:
                toast("OTP verifed")

    def Details(self):
        global fname, Email

        fname = self.ids.Fname.text
        Email = self.ids.Email.text
        SOTP = self.ids.SOTP.text
        PHno = self.ids.PHno.text
        # -- assign to local variable to easy access -- 

        if fname and PHno and Email:
            NU = USp.New_User(fname, PHno, Email)
            # -- appending to database --

            if NU:
                self.manager.transition.direction = "left"
                self.manager.current = "Addr"

            else:
                toast("Length of phone number Must be 10 !")
                # -- if it return False it was an issue of Phone number --

                self.ids.PHno.text = ''
                self.ids.PHno.focus = True

        else:
            if fname == '':
                self.ids.Fname.focus = True

            elif PHno == '':
                self.ids.PHno.focus = True

            elif Email == '':
                self.ids.Email.focus = True
            # -- Set focus to the empty field --


class Addr(MDScreen):
    def Details(self):
        global state, distt, cty, st

        state = self.ids.State.text
        distt = self.ids.distict.text
        cty = self.ids.city.text
        st = self.ids.St.text
        # -- local variable for eassy access --

        if state and distt and cty and st:
            adr = USp.address(state, distt, cty, st)
            # -- append to database --

            if (adr):
            # -- Proceed to the next screen --
                self.manager.current = "Final"
                self.manager.transition.direction = "left"

        else:
            # -- Set focus to the empty field --
            if state == '':
                self.ids.State.focus = True

            elif distt == '':
                self.ids.distict.focus = True

            elif cty == '':
                self.ids.city.focus = True

            elif st == '':
                self.ids.St.focus = True


class Final(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.User_id.text = PHno
        # -- Assign username as phone number --
        # -- set phone number as primary key --
        return super().on_pre_enter(*args)
    
    def compareText(self):
        npwd = self.ids.Npswd.text
        cpwd = self.ids.Cpswd

        if not npwd == cpwd.text:
            cpwd.error = True
            # -- if both password are not match then error show --

        else:
            cpwd.error = False

    def Details(self):
        global npwd, ref

        npwd = self.ids.Npswd.text
        cpwd = self.ids.Cpswd.text
        ref = self.ids.Reference.text

        if npwd and cpwd :
            managePwd = USp.New_pass(npwd, cpwd, ref)
            # -- append to database -- 

            if managePwd:

                self.manager.transition.direction = "left"
                self.manager.current = "TandC"
                # -- if added then send to next screen --

            else:
                self.MissMatch = MDDialog(
                    title="Password Mismatch",
                    text="New password and confirm password do not match. Please try again.",
                    type = 'alert',
                    buttons=[
                        MDRaisedButton(
                            text = "OK",
                            on_release = self.dialog_callback,
                        )
                    ],
                )
                self.MissMatch.open()
                # -- the error possibly wrong password --

                self.ids.Npswd.text = ''
                self.ids.Npswd.focus = True
                self.ids.Cpswd.text = ''

        else:
            if npwd == '':
                self.ids.Npswd.focus = True

            elif cpwd == '':
                self.ids.Cpswd.focus = True

    def dialog_callback(self, *args):
        self.MissMatch.dismiss()


class T_and_C(MDScreen):
    def Add_data(self):
        if self.ids.Agree.active:
            # -- if the check box is active to continue next operation --
            Done = USp.Add_details()
            # -- confirm adding the details to final database --

            if Done:
                self.MissMatch = MDDialog(
                    title="Details are added!",
                    text = "To continue use the app Please Login",
                    type = 'confirmation',
                    buttons=[
                        MDRaisedButton(
                            text = "OK",
                            on_release = self.dialog_callback,
                        )
                    ],
                )
                self.MissMatch.open()
                # -- After added then transfer to main screen and request to login --
                self.manager.transition.direction = "right"
                self.manager.current = "Login"

        else:
            snkbr = Snackbar(
                text = '  Agree with Terms and condition to continue',
                spacing = 10,
                snackbar_x= 10,
                snackbar_y= 10,
            )

            snkbr.size_hint_x = (
                Window.width - (snkbr.snackbar_x * 2)
            ) / Window.width
            snkbr.open()
            # -- else open snack bar to agree the terms and condition --

            self.ids.Agree.focus = True

    def dialog_callback(self, *args):
        self.MissMatch.dismiss()


class ForgetPassword(MDScreen):
    def on_enter(self, *args):
        self.MissMatch = MDDialog(
            title="",
            text="",
            type = 'alert',
            buttons=[
                MDRaisedButton(
                    text = "OK",
                    on_release = self.dialog_callback,
                )
            ],
        )
        # -- pre assigning the pop-up window --

    def VerifyItsME(self):
        OTPPHNO = self.ids.NewPWdPh.text
        self.NOTP = OTPh.GenOTP(OTPPHNO)
        # -- verifying phone number with OTP --

        if not self.NOTP:
            self.snkbr = Snackbar(
                text = '  Check the Number',
                spacing = 20,
                snackbar_x= 10,
                snackbar_y= 10,
            )

            self.snkbr.size_hint_x = (
                Window.width - (self.snkbr.snackbar_x * 2)
            ) / Window.width
            # -- if not OTP generated then the number must be wrong --
            self.snkbr.open()

        elif len(str(self.NOTP)) == 5:
            self.MissMatch.title = 'New OTP'
            self.MissMatch.text = f'Your New OTP is {str(self.NOTP)}'
            self.MissMatch.open()
            # -- pop-uping OTP --

        else:
            self.snkbr.text = '  Check the Number'
            self.snkbr.open()
            # -- ask the number was right --

    def VerifyOTP(self, instance):
        if instance is not None and len(instance) == 5:
            # -- checking the basics properties of OTP --
            vrfy = OTPh.VerifyNum(instance)
            if vrfy:
                toast("OTP Verified")
                # -- if verified a toast message visible --

            else:
                self.MissMatch.title = 'OTP mis-match'
                self.MissMatch.text = "The entered OTP didn't match with entered One"
                self.MissMatch.open()
                # -- else pop-up open --

    def compareText(self):
        npwd = self.ids.CNPWD.text
        cpwd = self.ids.CCPWD

        if not npwd == cpwd.text:
            cpwd.error = True
            # -- if new and confirm password missmatch shown an error --

        else:
            cpwd.error = False

    def ChangeOTPPWd(self):

        OTPPHNO = self.ids.NewPWdPh.text
        EOTP = self.ids.OTP.text
        CNewPswd = self.ids.CNPWD.text
        CCPswd = self.ids.CCPWD.text

        if OTPPHNO and EOTP and CNewPswd and CNewPswd :

            if (CNewPswd == CCPswd):
                cngedPWD = OTPh.ForGetPWD(OTPPHNO,CNewPswd, EOTP)

                if (cngedPWD):
                    self.MissMatch.title="Password Changed"
                    self.MissMatch.text = "To continue use the app Please Login"

                    self.MissMatch.open()
                    # -- if password confirmed show login screen and request login --

                    self.manager.transition.direction = "right"
                    self.manager.current = "Login"

                else:
                    self.MissMatch.title="OTP MISS-MATCH"
                    self.MissMatch.text = "Generated OTP and entered OTP was different"
                    # -- else the error by mismatch OTP --
                    self.MissMatch.open()

            else:
                self.MissMatch.title="Password Mis-match"
                self.MissMatch.text="New password and confirm password do not match. Please try again."
                # -- password was missmatch --
                self.MissMatch.open()
                
    def dialog_callback(self, *args):
        self.MissMatch.dismiss()


class STRHome(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.StrB.text = 'Balance : ' + Market_list[logined_User][8] + ' ₹'
        self.ids.StoreName.text = logined_User

        self.ids.storeID.text = 'Store ID : ' + Market_list[logined_User][1]
        self.ids.storeEmail.text = 'Store e-mail : ' + Market_list[logined_User][2]
        self.ids.storeAddr.text = 'Address : ' + str(Market_list[logined_User][3])
        self.ids.storeNo.text = 'Store No : ' + Market_list[logined_User][4]
        self.ids.storeBlnc.text = 'Balance : ' + Market_list[logined_User][8] + ' ₹'

        # -- assigning variable for label --

    def on_enter(self, *args):
        falseItem = []
        for Itm in storeDB.keys():
            if len(storeDB[Itm][1]) == 0:
                falseItem.append(Itm)

        if falseItem:
            for Itm in falseItem:
                toast(f"Item '{Itm}' removed due to empty Items")
                storeDB.pop(Itm)

            falseItem = []
            # -- if any empyt items on cart remove while entering --

    def show_online_order_dialog(self):
        self.online_order_dialog = MDDialog(
            title='Redirect alert',
            text="On press 'OK' it will redirect to an external website",
            buttons=[
                MDFlatButton(
                    text='CANCEL',
                    on_release=self.close_online_order_dialog,
                ),
                MDRaisedButton(
                    text='OK',
                    on_release=self.close_online_order_dialog,
                )
            ]
        )
        self.online_order_dialog.open()
        # -- redirect to external website --

    def close_online_order_dialog(self, *args):
        # -- Dismiss the MDDialog --
        self.online_order_dialog.dismiss()

    def confirmLogout(self):
        self.logout = MDDialog(
            title = 'Confirm Log-Out',
            buttons = [
                MDFlatButton(
                    text = 'Cancel',
                    on_press = self.logoutCancel,
                ),
                MDRaisedButton(
                    text = "OK",
                    on_press = self.logoutOK
                ),
            ],
        )
        self.logout.open()
        # -- logout button --

    def logoutCancel(self, *args):
        self.logout.dismiss()

    def logoutOK(self, *args):
        self.logout.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'Login' 
        # -- confirm log-out --


class AddItemCart(MDScreen):
    Nmrepeat = 0
    def VerifyStoreItem(self, instance):
        ItemName = self.ids.ItemName.text
        duplicate = Snackbar(
            text = f'{ItemName} not match with {instance}. Try change the location ',
            spacing = 20,
            snackbar_x= 10,
            snackbar_y= 10,
        )
        duplicate.size_hint_x = (
            Window.width - (duplicate.snackbar_x * 2)
        ) / Window.width

        if len(instance) == 3:
            for items in storeDB.keys():
                if ItemName == items:
                    # -- check if input name and cart list is repeating --
                    if not storeDB[ItemName][4] == instance:
                        # -- check the list location not equal to input loct --
                        # -- clear input --
                        self.ids.location.text = ''
                        self.ids.ItemName.text = ''
                        # open MDSnackbar if false
                        duplicate.open()

                elif storeDB[items][4] == instance:
                    # -- check location was dupicate or not --
                    self.ids.location.text = ''
                    self.ids.ItemName.text = ''
                    # -- change MDSnackbar check --
                    duplicate.text = f'{instance} already occupied'
                    duplicate.open()

    def Verify_no_item(self, instance):
        if instance.text:
            if int(instance.text) > 100:
                instance.text = '100'
                # -- maximum number of item in a carst must be 100 --
                toast('Maximum 100)')
        
    def ItemSumbit(self):
        # -- assign to a local variable for eassy access --
        self.NoItem = self.ids.NumberOfItem.text
        self.itmPrice = self.ids.ItemPrice
        self.itmloct = self.ids.location
        self.itmEXP = self.ids.DateTField.text
        self.ItemName = self.ids.ItemName.text
        self.BTHno = self.ids.batchNumber

        # -- confirmation dialog box --
        if self.ItemName and self.BTHno and self.NoItem and self.itmEXP and self.itmPrice and self.itmloct:
            self.ConfirmAddItem = MDDialog(
                title = 'confirm Item',
                text = f'item Name : {self.ItemName}\nBatch Number : {self.BTHno.text}\
                    \nNumber of Item : {self.NoItem}\nEXP Date : {self.itmEXP}\
                    \nItem Price : {self.itmPrice.text}\nItem location : {self.itmloct.text}',
                buttons = [
                    MDRaisedButton(
                        text = 'OK',
                        on_press= self.confirm,
                    ),
                ],
            )
    
        if self.NoItem and self.itmPrice and self.itmloct\
              and self.itmEXP and self.ItemName and self.BTHno:
            
            if len(self.itmPrice.text) == 2:
                # -- add '0' if price length = 2 --
                self.itmPrice.text = '0' + self.itmPrice.text

            elif len(self.itmPrice.text) == 1:
                # -- add '00' if price length = 1 --
                self.itmPrice.text = '00' + self.itmPrice.text

            
            if len(self.BTHno.text) == 3:
                # -- check the length of batch number --
                if len(self.itmloct.text) == 3:

                    # -- check the length of loct --
                    for Itname in storeDB.keys():
                        if Itname == self.ItemName:
                            if storeDB[self.ItemName][4] == self.itmloct.text:
                                if storeDB[self.ItemName][3] == self.itmPrice.text:
                                    self.ConfirmAddItem.text = f'item Name : {self.ItemName}\nBatch Number : {self.BTHno.text}\
                                                        \nNumber of Item : {self.NoItem}\nEXP Date : {self.itmEXP}\
                                                        \nWill add to the existing item!'
                                    self.Nmrepeat = 1
                                    
                                    self.ConfirmAddItem.open()

                                else:
                                    self.itmPrice.text = ''
                                    self.itmloct.text = ''
                                    toast('Item Price not match or location occupied!')

                            else:
                                self.itmPrice.text = ''
                                self.itmloct.text = ''
                                toast('Item Price not match or location occupied!')

                    else:
                        self.ConfirmAddItem.open()
                    

                else:
                    # -- else condition for length is not 3 --
                    self.itmloct.focus = True
                    self.itmloct.text = ''
                    self.itmloct.hint_text = 'Must have 3 letter location'

            else: 
                # -- else condition for length is not 3 --
                self.BTHno.focus = True
                self.BTHno.text = ''
                self.BTHno.hint_text = 'Must have 3 letter BatchNumber'

    def confirm(self, *args):
        # -- confirm added MDSnackbar --
        is_add = productDetail.AddProduct(storeDB, self.ItemName, self.BTHno.text, self.NoItem, self.itmEXP, self.itmPrice.text, self.itmloct.text, self.Nmrepeat)
        if is_add:
            self.ConfirmAddItem.dismiss()

            toast(f'{self.ItemName} added sucessfully')

            self.manager.transition.direction = 'up'
            self.manager.current = 'CHomePage'
            # --shift screen back  --
            # -- after added clear the input --

            self.ids.NumberOfItem.text = ''
            self.ids.ItemPrice.text = ''
            self.ids.location.text = ''
            self.ids.DateTField.text = ''
            self.ids.ItemName.text = ''
            self.ids.batchNumber.text = ''

        else:
            self.ConfirmAddItem.dismiss()

            self.ids.NumberOfItem.text = ''
            self.ids.ItemPrice.text = ''
            self.ids.location.text = ''
            self.ids.DateTField.text = ''
            self.ids.ItemName.text = ''
            self.ids.batchNumber.text = ''

            self.manager.transition.direction = 'up'
            self.manager.current = 'CHomePage'

            MDDialog(
                title = 'An unexpected error occur',
                text = 'Try to delete the RACK and add again',
            ).open()

    def Confirm_leave(self):
        self.leaveScreen = MDDialog(
            title = 'confirm leave',
            auto_dismiss = False,
            text = "The following filled data will be erase\n Are you sure want to confirm",
            buttons = [
                MDFlatButton(
                    text = 'CANCEL',
                    on_press=self.closeDialog
                ),
                MDRaisedButton(
                    text = 'OK',
                    on_press=self.ConfirmLeave
                ),
            ],
        )

        self.leaveScreen.open()
        # -- wline leave without adding item -- 

    def closeDialog(self, *args):
        self.leaveScreen.dismiss()

    def ConfirmLeave(self, *args):
        self.ids.NumberOfItem.text = ''
        self.ids.ItemPrice.text = ''
        self.ids.location.text = ''
        self.ids.DateTField.text = ''
        self.ids.ItemName.text = ''
        self.ids.batchNumber.text = ''

        self.leaveScreen.dismiss()
        self.manager.transition.direction = 'up'
        self.manager.current = 'CHomePage'

    def selectDate(self):
        self.date_dialog = MDDatePicker(
            min_year=2024,
            max_year = 2027,
            title_input="EXP DATE",
            mode= 'picker',
        )
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        self.date_dialog.open()
        # -- opening a date picker for experiy date selection --

    def on_save(self, instance, value, date_range):
        self.ids.DateTField.text = str(value)
        # -- saving the value --

    def on_cancel(self, instance, value):
        self.date_dialog.dismiss()


class CreateQR(MDScreen):
    def on_pre_enter(self, *args):
        for items in storeDB.keys():
            self.ids.ListViewItem.add_widget(
                TwoLineListItem(
                    text = f'{items}',
                    secondary_text = f'Location: {storeDB[items][4]}',
                    on_press= self.CreateQR
                ),
            )
            # -- showing every item on the list --

    def CreateQR(self, instance):
        value = instance.text
        # -- The selected item passes from the next screen and create QRcode --
        CreateQROut.ObjectItem = value
        self.manager.transition.direction = 'left'
        self.manager.current = 'CreateQROut'

    def on_leave(self, *args):
        self.ids.ListViewItem.clear_widgets()
        # -- after leaving clear the created QRcode --


class CreateQROut(MDScreen):
    ObjectItem = str()

    def on_enter(self, *args):
        values = generate_QR_Data(storeDB, CreateQROut.ObjectItem)
        # -- creating QRode accordinf to the cart item --
        ht = (0.25*len(values)/2)
        # -- assigning the hight of object according to image --
        self.ids.ImageView.size_hint = [1, ht]

        for itm in values:
            image = QRCodeWidget(
                data = itm,
                pos_hint = {'top': 1},
                show_border = False,
            )
            self.ids.ImageView.add_widget(image)
            # -- creating image and add to the layout --

    def saveImage(self):
        self.notify = MDDialog(
            title = 'Confirm Save',
            text = 'The following image will save as one image file',
            buttons = [
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.DismissDialog
                )
            ]
        )
        self.notify.open()
        # -- when the button save pressed the pop-up open to confirm save --

    def DismissDialog(self, *args):
        self.notify.dismiss()
        self.ids.ImageView.export_to_png("{0}-{1}.png".format(CreateQROut.ObjectItem, storeDB[CreateQROut.ObjectItem][4]))
        #-- saving image as object name and id --
        confirmationMsg = Snackbar(
            text = f"Image '{CreateQROut.ObjectItem}-{storeDB[CreateQROut.ObjectItem][4]}.png' where saved on root folder",
            spacing = 10
        )
        confirmationMsg.size_hint_x = (
            Window.width - (confirmationMsg.snackbar_x * 2)
        ) / Window.width
        confirmationMsg.open()

    def on_leave(self, *args):
        self.ids.ImageView.clear_widgets()


class DeleteFromCart(MDScreen):
    def on_pre_enter(self, *args):
        for items in storeDB.keys():
            self.ids.ListViewItem.add_widget(
                TwoLineListItem(
                    text = f'{items}',
                    secondary_text = f'Item(s): ({len(storeDB[items][1])})',
                    on_press= self.deleteItem,
                ),
            )
            # -- listing all item in the cart --

    def on_leave(self, *args):
        self.ids.ListViewItem.clear_widgets()
        # -- clear screen after leave --
        return super().on_leave(*args)
        
    def deleteItem(self, instance):
        value = instance.text
        # -- assign value for the next screen --
        DeleteCartItems.ObjectItem = value
        self.manager.transition.direction = 'left'
        self.manager.current = 'DeleteCartItems'


class DeleteCartItems(MDScreen):
    ObjectItem = str()
    PItID = []

    def on_pre_enter(self, *args):
        for sNo in storeDB[DeleteCartItems.ObjectItem][1]:
            self.ids.ListViewItem.add_widget(
                ListItemWithCheckbox(
                    text = f'product ID : {sNo}',
                    secondary_text = f'{DeleteCartItems.ObjectItem}',
                ),
            )
            # -- creating items with checkbox --
            self.ids.SelectButton.text = 'Select All'
            # -- setting label as sellect all before enter the screen --

    def CheckBoxStatus(self, Status):
        if Status:
            self.ids.SelectButton.text = 'Deselect All'
        else:
            self.ids.SelectButton.text = 'Select All'

        for Set in self.ids.ListViewItem.children:
            Set.ids.cb.active = Status
            # -- dynamic button for select and deselect all --

    def DeleteList(self):
        self.PItID = []
        for Set in self.ids.ListViewItem.children:
            if Set.ids.cb.active == True:
                self.PItID.append(Set.text[13:])
                self.pItNm = Set.secondary_text

        if self.PItID and self.pItNm:

            self.confirmation = MDDialog(
                title = 'Confirm delete',
                text = 'The selected Item Must me delete from cart \n\
                    Are you Sure want to continue ?',
                buttons = [
                    MDFlatButton(
                        text = 'Cancel',
                        on_press= self.CloseDialog
                    ),
                    MDRaisedButton(
                        text = 'OK',
                        on_press= self.deleteConfirmed
                    ),
                ],
            )
            self.confirmation.open()
            # -- confirmation for delete --

    def deleteConfirmed(self, *args):
        self.confirmation.dismiss()
        DoneMsg = Snackbar(
            text = f"{len(self.PItID)} items delete from {DeleteCartItems.ObjectItem}",
            spacing = 10,
            duration = 2,
        )
        DoneMsg.size_hint_x = (
            Window.width - (DoneMsg.snackbar_x * 2)
        ) / Window.width

        DoneMsg.open()
        
        for i in self.PItID:
            for j in storeDB[self.pItNm][1]:
                if i == j:
                    storeDB[self.pItNm][1].remove(i)
                    # -- deleting selected item --
        
        self.manager.transition.direction = 'right'
        self.manager.current = 'removeFromCart'

    def CloseDialog(self, *args):
        self.confirmation.dismiss()

    def on_leave(self, *args):
        self.ids.ListViewItem.clear_widgets()
        # -- clear screen when exits --
        return super().on_leave(*args)
    

class Offers(MDScreen):
    def on_enter(self, *args):
        self.PopUp = MDDialog(
            title = 'Alert',
            type = 'alert',
            text = "If name was ' * ' then the code apply for entire store offer",
            buttons = [
                MDRaisedButton(
                    text = 'OK',
                    on_press= self.dismissPopUp
                )
            ]
        )
        self.PopUp.open()
        # -- pop-up for guidence --

    def dismissPopUp(self, *args):
        self.PopUp.dismiss()

    def Button_confirm_press(self):
        self.MDSnackbar = Snackbar(
            text = ' ',
            spacing = 20,
            snackbar_x= 10,
            snackbar_y= 10,
            )
        
        self.MDSnackbar.size_hint_x = (
            Window.width - (self.MDSnackbar.snackbar_x * 2)
        ) / Window.width

        self.OfferName = self.ids.OfferItemName
        self.Offerdesc = self.ids.OfferDescri.text
        self.OfferPrice = self.ids.NewPrice
        self.OfferCode = self.ids.OfferCode
        
        if self.OfferPrice.text:

            if self.OfferCode.text: 

                if self.OfferName.text == '*':
                    Market_list[logined_User][6] = (self.OfferCode.text, self.OfferPrice.text)
                    # -- adding offer code to the whole store --

                    self.MDSnackbar.text = f" The Offer Code '{self.OfferCode.text}' Added to Store DB"
                    self.MDSnackbar.open()

                    self.OfferName.text = ''
                    self.OfferPrice.text = ''
                    self.OfferCode.text = ''

                    if self.Offerdesc.text:
                        self.Offerdesc.text = ''

                    self.manager.transition.direction = 'down'
                    self.manager.current = 'CHomePage'

                elif self.OfferName.text != '*':
                    # -- adding offer to indivigual item --
                    for Items in storeDB:
                        if self.OfferName.text == Items:
                            NewPrice = float(storeDB[Items][3]) - (int(self.OfferPrice.text) / 100 * float(storeDB[Items][3]))
                            # -- deduct with the percentage of offer --
                            storeDB[Items][3] = str(NewPrice)

                            self.manager.transition.direction = 'down'
                            self.manager.current = 'CHomePage'
            
                            self.MDSnackbar.text = f"Price of '{Items} dropped to {NewPrice}"
                            self.MDSnackbar.open()

                            self.OfferName.text = ''
                            self.OfferPrice.text = ''
                            self.OfferCode.text = ''

                            #if self.Offerdesc.text:
                            #    self.Offerdesc.text = ''

                            break

                    else:
                        self.OfferName.text = ''
                        self.OfferName.focus = True
                        toast('Item Not Found!')

            else:
                self.OfferCode.focus = True

        else:
            self.OfferPrice.focus = True


class ViewStock(MDScreen):
    def on_pre_enter(self, *args):
        for items in storeDB.keys():
            self.ids.ListViewItem.add_widget(
                TwoLineListItem(
                    id = items,
                    text = f'{items}',
                    secondary_text = f'Item(s): ({len(storeDB[items][1])})',
                    on_press = self.ItemOnstock
                ),
            )
            # -- adding item to the screen --

    def on_leave(self, *args):
        self.ids.ListViewItem.clear_widgets()

    def ItemOnstock(self, instance):
        self.dettOfItem = MDDialog(
            title = f'{instance.text}',
            type = 'simple',     
            text = f"Price : {storeDB[instance.text][3]}\
                \nLocation : {storeDB[instance.text][4]}\
                \nBatch No. : {storeDB[instance.text][0]}\
                \nNo. of Items : {len(storeDB[instance.text][1])}",
            buttons = [
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.closeDialog
                ),
            ],
        )
        self.dettOfItem .open()
        # --opens when touch the item --

    def closeDialog(self, *args):
        self.dettOfItem.dismiss()

class WithdrawAmount(MDScreen):
    def ConfirmLeave(self):
        self.DialogLeave = MDDialog(
            title = 'Confirm Leave!',
            text = 'The following transation will close',
            buttons = [
                MDFlatButton(
                    text = 'Cancel',
                    on_press = self.CloseDialog
                ),
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.ConfirmQuit
                )
            ]
        )
        self.DialogLeave.open()

    def CloseDialog(self, *args):
        self.DialogLeave.dismiss()

    def ConfirmQuit(self, *args):
        self.DialogLeave.dismiss()
        self.manager.transition.direction = 'down'
        self.manager.current = 'CHomePage'

        self.ids.STHUPI.text = ''
        self.ids.STHAmount.text = ''
        self.ids.STPPass.text = ''

    def CheckBalance(self, instance):
        if not instance <= Market_list[logined_User][8]:
            self.ids.STHAmount.text = Market_list[logined_User][8]
            toast('Exceed the amount')

    def ConfirmWithdraw(self):
        UPId = self.ids.STHUPI
        self.STHAmount = self.ids.STHAmount
        STPPass = self.ids.STPPass

        if UPId.text:
            if self.STHAmount.text:
                if STPPass.text:
                    if STPPass.text == Market_list[logined_User][5]:
                        if self.STHAmount.text <= Market_list[logined_User][8]:
                            # -- checking the given amount is less ot equal to wallet amt --
                            self.ConfirmWD = MDDialog(
                                title = 'Confirm withdraw',
                                text = f"The amount {self.STHAmount.text} with draw from account {Market_list[logined_User][0]}\n\
                                Are you sure want to continue ?",
                                buttons = [
                                    MDFlatButton(
                                        text = 'Cancel',
                                        on_press = self.WDCancel
                                    ),
                                    MDRaisedButton(
                                        text = 'OK',
                                        on_press = self.WDOk
                                    )
                                ]
                            )
                            self.ConfirmWD.open()

                        else:
                            self.STHAmount.text = ''
                            self.STHAmount.focus = True
                            toast("Exceed the total balance")

                    else:
                        STPPass.text = ''
                        STPPass.focus = True
                        toast("Password Mismatch")

                else:
                    STPPass.focus = True

            else:
                self.STHAmount.focus = True

        else:
            UPId.focus = True

    def WDOk(self, *args):
        self.ConfirmWD.dismiss()
        Market_list[logined_User][8] = str(float(Market_list[logined_User][8]) - int(self.STHAmount.text))
        # -- reduce amount from the wallet --
        self.manager.transition.direction = 'down'
        self.manager.current = 'CHomePage'

        self.ids.STHUPI.text = ''
        self.ids.STHAmount.text = ''
        self.ids.STPPass.text = ''

    def WDCancel(self, *args):
        self.ConfirmWD.dismiss()


class CTMHome(MDScreen):
    def on_pre_enter(self, *args):
        self.ids.btmNav.current = 'screen 1'
        
        self.ids.HomeSBln.text = 'Balance: ' + User_list[logined_User][5] + '  ₹'
        self.ids.CTWBaln.text = 'Balance: ' + User_list[logined_User][5] + '  ₹'
        self.ids.CTBaln.text = 'Balance: ' + User_list[logined_User][5] + '  ₹'
        # --balance screen of different places --
        
        self.ids.CTWUname.text = 'Hi, ' + User_list[logined_User][0]
        self.ids.CTUname.text = 'Hi, ' + User_list[logined_User][0]
        self.ids.USerPhoneNumberWT.text = '(+91) ' + logined_User
        # -- Username and phone number --

        self.ids.PrfNo.text = 'Ph Number : ' + logined_User
        self.ids.PrfUname.text = 'Name : ' + User_list[logined_User][0]
        self.ids.Uaddr.text = 'Address : ' + str(User_list[logined_User][2])
        self.ids.Email.text = 'Email : ' + User_list[logined_User][1]
        # -- User Details --

        # -- customer home screen variables --

    def on_enter(self, *args):
        already = User_list[logined_User][6]
        if already:
            for ady in already:
                for store in Market_list:
                    if ady == Market_list[store][6][0]:
                        CDView = MDCard(
                            spacing = 10,
                            padding = 10,
                            size_hint = [1, 0.5]
                        )
                        # -- creating a card look for show offer text --

                        CDView.add_widget(
                            MDLabel(
                                text = f'{store} : {ady[0]}'
                            )
                        )
                        # -- lable the offer inside the card --

                        CDView.add_widget(
                            MDLabel(
                                text = 'pending',
                                pos_hint = {'right': 1}
                            )
                        )
                        self.ids.OfferList.add_widget(CDView)


        count = 1        
        ptoims = ['BINGO', 'KNIFE', 'LED 9W', 'PEN (BLACK)', 'PEN (BLUE)', 'WALLET', 'MILKMAID', 'RICE 1KG', 'SUGAR 500G']
        while (count <= 6):
            ptm = choice(ptoims)
            
            PtoCard = MDSmartTile(
                lines = 2,
                radius = 24,
                box_radius =  [0, 0, 24, 24],
                box_color = [0.2, 0.2, 0.2, 0.7],
                source = f'IMG/{ptm}.jpg',
            )

            PtoCard.add_widget(
                MDLabel(
                    text = f'{ptm}'
                )
            )

            PtoCard.add_widget(
                MDIconButton(
                    icon = 'heart-outline',
                    theme_icon_color = "Custom",
                    on_press = lambda *args: self.RrcImSearch(ptm)
                )
            )
            
            self.ids.RemdItm.add_widget(PtoCard)
            ptoims.remove(ptm)
            count += 1

    def on_kv_post(self, base_widget):
        for stores in Market_list.keys():
            code = Market_list[stores][6]

            notiView = MDCard(
                spacing = 10,
                padding = 10,
                elevation = 2,
                orientation = 'vertical',
            )
            
            notiView.add_widget(
                MDLabel(
                    text = f'{stores}',
                    font_size = 30,
                    bold = True,
                )
            )
            notiView.add_widget(
                MDLabel(
                    text = f'Store {stores} added an offer of {code[0][1]} %\n.Go and grab it!',
                    font_size = 25,
                )
            )
            self.ids.Notify.add_widget(notiView)

        '''else:
            self.ids.Notify.size_hint = (1,1)
            self.ids.Notify.add_widget(
                MDLabel(
                    text = 'No new notification!',
                    bold = True,
                    halign = 'center'
                )
            )'''

    def ClearNoti(self):
        self.ids.Notify.clear_widgets()

    def RrcImSearch(self, ItemName):
        flag = 0
        for stName in Market_list.keys():
            StrDb = Market_list[stName][7]
            for itms in StrDb.keys():
                if itms == ItemName:
                    MDDialog(
                        title = 'GRAB YOUR ITEM!',
                        text = f'{ItemName} found on {stName} bought before stock out!'
                    ).open()
                    flag = 1
                    break

        if flag == 0:
            MDDialog(
                title = 'OUT OF ORDER!',
                text = f'{ItemName} Not found near by store'
            ).open()
            
    def OnlineOrder(self):
        self.OnlineDialog = MDDialog(
            title = 'Redirection alert',
            text = "On press 'OK' it will redirect to an external website",
            buttons = [
                MDFlatButton(
                    text = 'Cancel',
                    on_press = self.OrderDialogClose
                ),
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.OrderDialogClose
                )
            ]
        )
        self.OnlineDialog.open()
        # --redirect to external website after clicking the button --

    def CheckOCode(self):
        # --adding offer code for the store --
        UserCode = self.ids.IPCode.text
        for store in Market_list:
            code = Market_list[store][6][0]
            print(code)
                # -- checking the code form the store side if exist or not --
            if code[0] == UserCode:
                already = User_list[logined_User][6]
                # -- verifying the code is not repeating on the user side --
                if already:
                    for ady in already:
                        if code[0] == ady:
                            toast("The entered code is already exist!")
                            self.ids.IPCode.text = ''
                            # --if already exist show alert --
                            break
                    else:
                        CDView = MDCard(
                            spacing = 10,
                            padding = 10,
                            size_hint = [1, 0.5]
                        )
                        # -- creating a card look for show offer text --

                        CDView.add_widget(
                            MDLabel(
                                text = f'{store} : {code[0]}'
                            )
                        )
                        # -- lable the offer inside the card --

                        CDView.add_widget(
                            MDLabel(
                                text = 'pending',
                                pos_hint = {'right': 1}
                            )
                        )
                        self.ids.OfferList.add_widget(CDView)
                        # --adding to the screen -- 
                        self.ids.IPCode.text = ''

                        User_list[logined_User][6].append(code)
                        # -- adding offercode to the user database --
                        break
                    
        else:
            self.ids.IPCode.text = ''
            toast("Invalid Code!")
            # -- showing invalid code --

    def logoutValidate(self):
        self.CLogout = MDDialog(
            title = 'Confirm log-out ?',
            buttons = [
                MDFlatButton(
                    text = 'Cancel',
                    on_press = self.closeDg,
                ),
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.LogOK 
                )
            ]
        )
        self.CLogout.open()

    def CustomerCare_support(self):
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Whatsapp": "whatsapp",
            "Phone": "phone",
            "E-Mail": "gmail"
        }
        # -- oppen a new screen for contact customer care --

        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
            bottom_sheet_menu.open()

    def OrderDialogClose(self, *args):
        self.OnlineDialog.dismiss()

    def closeDg(self, *args):
        self.CLogout.dismiss()

    def LogOK(self, *args):
        self.CLogout.dismiss()

        self.manager.transition.direction = 'right'
        self.manager.current = 'Login'

    def on_leave(self, *args):
        self.ids.OfferList.clear_widgets()
        self.ids.RemdItm.clear_widgets()


class ShoppingList(MDScreen):
    def on_enter(self, *args):
        loct = User_list[logined_User][2]
        self.state = loct[0]
        self.dict = loct[1]
        self.city = loct[2]
        self.area = loct[3]

        for STName in Market_list.keys():
            SDB = Market_list[STName][7]
            addr = Market_list[STName][3]

            for PDName in SDB.keys():
                if addr[0] == self.state:
                    if addr[1] == self.dict:
                        if addr[2] == self.city:
                            self.ids.ListViewItem.add_widget(
                                ListItemWithCheckbox(
                                    text = f'{PDName}',
                                    secondary_text = f'{STName} ({self.city})'
                                )
                            )
                        else:
                            self.ids.ListViewItem.add_widget(
                                ListItemWithCheckbox(
                                    text = f'{PDName}',
                                    secondary_text = f'{STName} ({self.dict})'
                                )
                            )
                    else:
                        self.ids.ListViewItem.add_widget(
                                ListItemWithCheckbox(
                                    text = f'{PDName}',
                                    secondary_text = f'{STName} ({self.state})'
                                )
                            )
                        
    def on_leave(self, *args):
        self.ids.ListViewItem.clear_widgets()


class Addcash(MDScreen):
    def VerifyNumber(self, instance):
        if len(instance.text) == 10:
            if logined_User == instance.text:
                OTPpy = OTPh.GenOTP(instance.text)
                # -- verifying number and generating OTP

                self.OTPShow = MDDialog(
                    title = 'OTP',
                    text = f'Your New OTP is {str(OTPpy)}',
                    buttons = [
                        MDRaisedButton(
                            text = 'OK',
                            on_press = self.OTPDClose
                        )
                    ]
                )
                self.OTPShow.open()
            
            else:
                instance.text = ''
                instance.focus = True
                toast('Number not found!')
            
    def OTPVrify(self, instance):
        if len(instance.text) == 5:
            if(OTPh.VerifyNum(instance.text)):
                toast("OTP Verified!")
                instance.readonly = True
                # -- verifying OTP --

            else:
                instance.text = ''
                self.OTPShow.title = 'OTP Mis-Match'
                self.OTPShow.text = 'The Entered OTP is not match with given one!'
                self.OTPShow.open()
                # -- if not verified then show a pop-up --

    def Verify_Pay(self):
        UserPwd = self.ids.UserPassword
        amount = self.ids.PayAmd
        UsrPhno = self.ids.UPIPhno
        otp = self.ids.OTPpay

        if UsrPhno.text and otp.text:
            if UserPwd.text:
                if amount.text:
                    if UserPwd.text == User_list[logined_User][3]:
                        User_list[logined_User][5] = str(float(User_list[logined_User][5]) + int(amount.text))
                        # --confirming and add money to the wallet --

                        self.manager.transition.direction = 'down'
                        self.manager.current = 'CTMHome'

                        UserPwd.text = ''
                        amount.text = ''
                        UsrPhno.text = ''
                        otp.text = ''

                    else:
                        UserPwd.text = ''
                        UserPwd.focus = True
                        toast("Password Mis-match")
                
                else:
                    amount.focus = True
                    toast("Enter anmount")

            else:
                UserPwd.focus = True
                toast('Enter Password')

        else:
            UsrPhno.focus = True
            toast("Verify OTP first!")

    def PayLeave(self):
        self.leave = MDDialog(
            title = 'Confirm Leave',
            text = 'While press OK the Entered Data will clear and leave the screen\
                Are you sure Want to continue?',
            buttons = [
                MDFlatButton(
                    text = 'Cancel',
                    on_press = self.ClosePL
                ),
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.LeaveScreen
                )
            ]
        )
        self.leave.open()
        # -- leave without payment --

    def LeaveScreen(self, *args):
        self.leave.dismiss()
        self.ids.UserPassword.text = ''
        self.ids.PayAmd.text = ''
        self.ids.UPIPhno.text = ''
        self.ids.OTPpay.text = ''

        self.manager.transition.direction = 'down'
        self.manager.current = 'CTMHome'
                
    def OTPDClose(self, *args):
        self.OTPShow.dismiss()
    
    def ClosePL(self, *args):
        self.leave.dismiss()


class TransferAmd(MDScreen):
    def Verify_usr_No(self, instance):
        if len(instance.text) == 10:
            if not instance.text == logined_User:
                instance.focus = True
                instance.text = ''
                # -- check the number was same --

                toast("Check Your Number!")

    def Verify_rsf_No(self, instance):
        if len(instance.text) == 10:
            for RNo in User_list.keys():
                if instance.text == RNo:
                    break
                # -- checking the other user to transfer --

            else:
                toast("Reciver Number is not found!")

    def AmountCheck(self, instance):
        if not instance.text <= User_list[logined_User][5]:
            instance.text = ''
            instance.focus = True
            toast("Insufficient balance!")
            # -- check the account have suffisent balance --

    def GOBack(self):
        self.leave = MDDialog(
            title = 'Confirm Leave',
            text = 'While press OK the Entered Data will clear and leave the screen\
                Are you sure Want to continue?',
            buttons = [
                MDFlatButton(
                    text = 'Cancel',
                    on_press = self.CloseTS
                ),
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.LeaveScreen
                )
            ]
        )
        self.leave.open()

    def LeaveScreen(self, *args):
        self.leave.dismiss()
        self.ids.SendPhno.text = ''
        self.ids.reciverPh.text = ''
        self.ids.TfrAmt.text = ''
        self.ids.UserPassword.text = ''

        self.manager.transition.direction = 'down'
        self.manager.current = 'CTMHome'

    def CloseTS(self, *args):
        self.leave.dismiss()

    def transferConfirm(self):
        Sno = self.ids.SendPhno
        Tno = self.ids.reciverPh
        Tpy = self.ids.TfrAmt
        UPWd = self.ids.UserPassword

        if Sno.text:
            if Tno.text:
                if Tpy.text:
                    if UPWd.text:
                        if UPWd.text == User_list[logined_User][3]:
                            self.Confirmation = MDDialog(
                                title = 'Transfer confirmation',
                                text = f"The {Tpy.text} Transfer to {Tno.text} ₹ ('{User_list[Tno.text][0]}').\
                                    Are you sure want to continue ?",
                                buttons = [
                                    MDFlatButton(
                                        text = 'Cancel',
                                        on_press = self.CnfClose
                                    ),
                                    MDRaisedButton(
                                        text = 'OK',
                                        on_press = self.DialogCnf
                                    )
                                ]
                            )
                            self.Confirmation.open()
                            # --show name and number to confirm the other user --

                        else:
                            UPWd.focus = True
                            UPWd.text = ''
                            toast('Password Mis-match!')

                    else:
                        UPWd.focus = True
                        toast('Password is required!')

                else:
                    Tpy.focus = True
                    toast('Amount required!')

            else:
                Tno.focus = True
                toast('Reciver Number required!')

        else:
            Sno.focus = True
            toast('User Number Required')

    def CnfClose(self, *args):
        self.Confirmation.dismiss()

    def DialogCnf(self, *args):
        self.Confirmation.dismiss()
        Tno = self.ids.reciverPh.text
        Tpy = self.ids.TfrAmt.text

        User_list[logined_User][5] = str(float(User_list[logined_User][5]) - int(Tpy))
        # -- deducting amount from the sending user --
        User_list[Tno][5] = str(float(User_list[Tno][5]) + int(Tpy))
        # -- crediting amount to other user --

        self.ids.SendPhno.text = ''
        self.ids.reciverPh.text = ''
        self.ids.TfrAmt.text = ''
        self.ids.UserPassword.text = ''
        
        self.manager.transition.direction = 'down'
        self.manager.current = 'CTMHome'


class MoreRecomd(MDScreen):
    def on_enter(self, *args):
        count = 1
        ptoims = ['BINGO', 'KNIFE', 'LED 9W', 'PEN (BLACK)', 'PEN (BLUE)', 'WALLET', 'MILKMAID', 'RICE 1KG', 'SUGAR 500G']
        while (count <= 9):
            ptm = choice(ptoims)
            
            PtoCard = MDSmartTile(
                lines = 2,
                radius = 24,
                box_radius =  [0, 0, 24, 24],
                box_color = [0.2, 0.2, 0.2, 0.7],
                size_hint = (None, None),
                source = f'IMG/{ptm}.jpg',
            )

            PtoCard.add_widget(
                MDLabel(
                    text = f'{ptm}'
                )
            )

            
            self.ids.MoreRmd.add_widget(PtoCard)
            ptoims.remove(ptm)
            count += 1
    
class Offline(MDScreen):
    data_table = None
    QRcam = None
    VariableSid = None
    slno = 0
    finalPrice = float()
    cartItemList = []

    def on_pre_enter(self, *args):
        if not self.data_table:
            self.data_table = MDDataTable(
                size_hint = (1, 1),
                use_pagination = True,
                pagination_menu_pos = 'auto',
                background_color_cell="#451938",
                background_color_header = "#65275d",
                pos_hint = {'center_x': 0.5},

                column_data=[
                    ("SLNo", 10),
                    ("Product",40),
                    ("ID", 20),
                    ("Batch No.", 20),
                    ("Price", 15),
                ],

                row_data = self.cartItemList,
            )
            self.ids.DataTable.add_widget(self.data_table)
            # -- creating a table to show purchased items --
            # -- row data update when QRcode Scaned --
            
    
        self.confirmPay = MDDialog(
            title = 'Confirm payment',
            auto_dismiss = False,
            text = f"Amount of {str(self.finalPrice)} ₹ Press 'PAY' to confirm payment",
            type = 'confirmation',
            buttons = [
                MDFlatButton(
                    text = 'CANCEL',
                    on_press=self.Paycallback,
                ),
                MDRaisedButton(
                    text = 'PAY',
                    on_press = self.payAmounts,
                )
            ],
        )

    def QRreaded_data(self, value):
        global storeDB
        # -- slicing and filter input -- 
        self.ItemError = MDDialog(
            title = 'Item Error',
            text = "Item didn't exist\ncontact Manager for further information",
            type = 'alert',
            buttons = [
                MDRaisedButton(
                    text = 'OK',
                    on_press = self.ItemErrorclr,
                ),
            ]
        )
        

        value = value[2:-1]
        if len(value) == 23:
            for STName in Market_list:
                if value[:4] == Market_list[STName][1]:
                    self.ids.QRCam.stop()
                    self.storeName = STName
                    storeDB = Market_list[STName][7] # -- Store Name --
                    self.StoreID = value[:4] # -- fetching store ID --
                    # -- verifying the items is from same store --
                    if not self.VariableSid or self.VariableSid == self.StoreID:
                        # -- slicing the balance part of QR -- 
                        self.ItemID = value[4:7] # -- Item ID --
                        self.Batch = value[7:10] # -- Batch Number --
                        # -- expire date fexhing and processing --
                        self.EXP = value[10:12] + '/' + value[12:14] + '/' + value[14:17]
                        self.Price = value[17:20] # -- slicing Price --
                        self.LOCT = value[20:] # -- slice location --

                        for product in self.cartItemList:
                            if product[2] == self.ItemID and product[3] == self.Batch:
                                # -- if exist then show error -- 
                                exist = Snackbar(
                                    # -- Repeation Error --
                                    text = '  The Item already exist on the cart list!',
                                    spacing = 20,
                                    snackbar_x= 10,
                                    snackbar_y= 10,
                                )
                                # -- setting the snakbar to same size of window --
                                exist.size_hint_x = (
                                    Window.width - (exist.snackbar_x * 2)
                                ) / Window.width
                                exist.open()
                                self.ids.QRCam.start()
                                break

                        else:
                            for IName in storeDB.keys():
                                if storeDB[IName][4] == self.LOCT:
                                    for ItmID in storeDB[IName][1]:
                                        if ItmID ==self.ItemID:
                                            self.PDName = IName
                                            self.ids.QRCam.stop()
                                            self.ConfirmItem = MDDialog(
                                                # -- auto dismiss dismiss alertbox when click somewere --
                                                auto_dismiss = False,
                                                # -- Title of dialog --
                                                title = "Confirm Item",
                                                # -- product details after fetching the details --
                                                text = f'Item name : {self.PDName} ,\
                                                \nItemID :{self.ItemID},\nBatch : {self.Batch},\
                                                \nExp Date : {self.EXP},\nPrice : {self.Price} ₹,\
                                                \nLocation : {self.LOCT}',
                                                type = 'confirmation',
                                                buttons = [
                                                    MDFlatButton(
                                                        text = 'CANCEL',
                                                        on_press=self.callback,
                                                    ),
                                                    MDRaisedButton(
                                                        text = "ADD TO CART",
                                                        on_press=self.AddItem,
                                                    ),
                                                ],
                                            )
                                            self.ConfirmItem.open()
                                            break

                                    else:
                                        self.ItemError.open()

                                    break
                        
                            else:
                                self.ItemError.open()

                            break

                
                    else:
                        self.ItemError.title = "Store ID mismatch"
                        self.ItemError.text = 'The scanned product is not belong to this store \
                                    \ncontact manager to further information'

                        self.ItemError.open()
                
    def ItemErrorclr(self, *args):
        self.ItemError.dismiss()
        self.ids.QRCam.start()

    def callback(self, *args):
        self.ConfirmItem.dismiss()
        self.ids.QRCam.start()


    def AddItem(self, *args):
        # --check the user still have enough balance --
        if (float(self.finalPrice) + int(self.Price)) <= float(User_list[logined_User][5]):
            # -- if product was confimed add to the datatable --
            self.slno = self.slno + 1
            # -- updating final price for the payment button --
            self.finalPrice = self.finalPrice + int(self.Price)
            # -- add to the list for updating the table --
            self.cartItemList.append((self.slno, self.PDName, self.ItemID, self.Batch, self.Price))
            # -- updating Data Table --
            self.data_table.row_data = self.cartItemList
            # -- incrementing the value of payent button --
            self.ids.PayBtn.text = 'Pay '+ str(self.finalPrice) +' ₹'
            # -- remove item from the database --
            storeDB[self.PDName][1].remove(self.ItemID)
            # -- restart QR scanner --
            self.ids.QRCam.start()
            # -- close the alert box --
            self.ConfirmItem.dismiss()
            # -- setting storeID for manage DB --
            self.VariableSid = self.StoreID

        else:
            self.ConfirmItem.dismiss()
            self.lowBlnc = MDDialog(
                title = 'Check Balance!',
                text = 'The balance in wallet is not enough to bought this item.',
                type = 'alert',
                auto_dismiss = False,
                buttons = [
                    MDRaisedButton(
                        text = 'OK',
                        md_bg_color = [1, 0, 0, 1],
                        on_press = self.NoBln
                    )
                ]
            )
            self.lowBlnc.open()

    def NoBln(self, *args):
        self.lowBlnc.dismiss()
        self.ids.QRCam.start()

    def BackBtn(self):
        self.BackAlert = MDDialog(
            auto_dismiss = False,
            title = 'Confirm Back',
            text='On press ok the data will lose\nAre you want to continue',
            type= 'alert',
            buttons = [
                MDFlatButton(
                    text = 'CANCEL',
                    on_press=self.BackbtnCallback,
                ),
                MDRaisedButton(
                    text = "CONFIRM",
                    on_press=self.Back,
                ),
            ],
        )
        self.BackAlert.open()

    def Back(self, *args):
        # -- close backBTN alert --
        self.BackAlert.dismiss()
        # -- clear the cart List from the data table
        self.cartItemList = []
        if self.data_table:
            self.data_table.row_data = []

        self.finalPrice = 0
        self.ids.PayBtn.text = 'Pay '+ str(self.finalPrice) +' ₹'
        self.manager.transition.direction = 'down'
        self.manager.current = 'CTMHome'

    def PayAmount(self):
        # -- payment confirm Alert Box --
        if not self.ids.PayBtn.text == 'Pay 0 ₹' :
            if not User_list[logined_User][6] == '':
                for usrofr in User_list[logined_User][6]:
                    for oftstr in Market_list.keys():
                        
                        strOfrcode = Market_list[oftstr][6][0]
                        print(strOfrcode[0])
                        print(usrofr)
                        if strOfrcode[0] == usrofr[0] and self.StoreID == Market_list[oftstr][1]:
                            if self.finalPrice >= 150:
                                self.UserOdder = MDDialog(
                                    title = 'An Offer code found!',
                                    text = f'An offer of {usrofr[1]}% found. Would you like to use it ?',
                                    buttons = [
                                        MDFlatButton(
                                            text = 'NO',
                                            on_press = self.Continue_Payment,
                                        ),
                                        MDRaisedButton(
                                            text = 'YES',
                                            on_press = lambda *args: self.UseOffer(usrofr)
                                        )
                                    ]
                                )
                                self.UserOdder.open()
                                break
                        
                    else:
                        self.confirmPay.text = f"Amount of {str(self.finalPrice)} ₹ Press 'PAY' to confirm payment"
                        self.confirmPay.open()
                    break
                
                else:
                    self.confirmPay.text = f"Amount of {str(self.finalPrice)} ₹ Press 'PAY' to confirm payment"
                    self.confirmPay.open()

            else:
                self.confirmPay.text = f"Amount of {str(self.finalPrice)} ₹ Press 'PAY' to confirm payment"
                self.confirmPay.open()

        else:
            self.manager.transition.direction = 'right'
            self.manager.current = 'CTMHome'


    def Continue_Payment(self, *args):
        if self.UserOdder:
            self.UserOdder.dismiss()
        self.confirmPay.text = f"Amount of {str(self.finalPrice)} ₹ Press 'PAY' to confirm payment"
        self.confirmPay.open()

    def UseOffer(self, percent):
        self.UserOdder.dismiss()
        User_list[logined_User][6].remove(percent)
        self.finalPrice = self.finalPrice - (percent[1] /100 *self.finalPrice)
        self.ids.PayBtn.text = 'Pay '+ str(self.finalPrice) +' ₹'

        #self.confirmPay.text = f"Amount of {str(self.finalPrice)} ₹ Press 'PAY' to confirm payment"
        #self.confirmPay.open()

        
    def payAmounts(self, *args):
        reward = float()
        self.confirmPay.dismiss()
        self.cartItemList = []
        self.data_table.row_data = []

        if float(User_list[logined_User][5]) >= float(self.finalPrice):
            User_list[logined_User][5] = str(float(User_list[logined_User][5]) - float(self.finalPrice))
            Market_list[self.storeName][8] = str(float(Market_list[self.storeName][8]) + float(self.finalPrice))

            if self.finalPrice > 499:
                reward = (self.finalPrice / 25)

            self.finalPrice = 0
            self.ids.PayBtn.text = 'Pay '+ str(self.finalPrice) +' ₹'

            self.cartItemList = []
            self.data_table.row_data = []

            self.manager.transition.direction = 'right'
            self.manager.current = 'CTMHome'

        if not reward == 0:
            User_list[logined_User][7].append(reward)

            MDDialog(
                title = 'REWARD!',
                text = f'A reward of {str(reward)} ₹ pending'
            ).open()


    def Paycallback(self, *args):
        self.confirmPay.dismiss()

    def BackbtnCallback(self, *args):
        self.BackAlert.dismiss()
    

    def on_leave(self, *args):
        self.ids.DataTable.clear_widgets()
        self.data_table = None


class RewardScreen(MDScreen):
    def on_enter(self, *args):
        if User_list[logined_User][7]:
            for amd in  User_list[logined_User][7]:
                rewardView = MDCard(
                    spacing = 10,
                    padding = 10,
                    elevation = 2,
                )
                rewardView.add_widget(
                    MDLabel(
                        text = f'Reward: {amd} ₹',
                        halign = 'center',
                    )
                )

                rewardView.add_widget(
                    MDRaisedButton(
                        text = 'claim',
                        on_press = lambda *args: self.AddRewaed(amd)
                    )
                )

                self.ids.RewardIm.add_widget(rewardView)

        else:
            self.ids.RewardIm.add_widget(
                MDLabel(
                    text = 'No active rewards',
                    halign = 'center',
                )
            )

    def on_leave(self, *args):
        self.ids.RewardIm.clear_widgets()

    def AddRewaed(self, Amount):
        User_list[logined_User][5] = str(float(User_list[logined_User][5]) + Amount)
        User_list[logined_User][7].remove(Amount)

        self.manager.transition.direction = 'down'
        self.manager.current = 'CTMHome'

        toast(f'{Amount} ₹ Added')


#--------------------------------------------------------------------------------------------------------------------------------------

class E_Kart(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = 'BlueGray'
        return Builder.load_file("Login.kv")
    # --importing the design and setting it as dark mode -- 

    def Text_Capital(self, instance):
        # -- text capitalize function --
        if instance.text:
            instance.text = instance.text.upper()

#-------------------------------------------------------------------------------------------------------------------------------------

 
if __name__ == "__main__":
    # -- Starting the app --
    E_Kart().run()
