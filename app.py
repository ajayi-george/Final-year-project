from kivymd.app import MDApp
import threading
from kivymd.uix.button import  MDFillRoundFlatButton
from kivy.uix.screenmanager import ScreenManager, CardTransition
from kivy.utils import platform, QueryDict, rgba
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ListProperty
import pyttsx3
import smtplib
from kivymd.uix.dialog import MDDialog
import os
from kivymd.toast import toast
from google.cloud import bigquery
from email.message import EmailMessage
import pandas as pd
import re
import imaplib
import email
from email.header import Header, decode_header, make_header
import azurestuff as az
import email_check as ec
import mysql.connector

# TODO: You may know an easier way to get the size of a computer display.


class WindowManager(ScreenManager):
    pass


class AutoSender(MDApp):
    # stored all my screens here to reduce loading time. If it's not clear.let me know so i can explain
    screens_store = JsonStore(f"screens.json")
    # screens_store = JsonStore(f"{path}/screens.json")
    screen_history = ListProperty()
    colors = QueryDict()
    colors.primary = rgba("#143EBE")
    colors.bg = rgba("#1f1f1f")
    colors.secondary = rgba("#492b7c")
    colors.warning = rgba("#c83416")
    colors.danger = rgba("#b90000")
    colors.success = rgba("#0F7A60")
    colors.white = rgba("#FFFFFF")
    colors.yellow = rgba("#f6d912")
    colors.orange = rgba("#ed8a0a")
    colors.black = rgba("#333333")
    colors.grey = rgba("#f1f1f1")

    fonts = QueryDict()
    fonts.heading = 'yourfont'
    fonts.subheading = 'yourfont'
    fonts.body = 'yourfont'

    fonts.size = QueryDict()
    fonts.size.heading = "30sp"
    fonts.size.icon = "30sp"
    fonts.size.h1 = "24sp"
    fonts.size.h2 = "22sp"
    fonts.size.h3 = "18sp"
    fonts.size.h4 = "16sp"
    fonts.size.h5 = "14sp"
    fonts.size.h6 = "12sp"
    fonts.size.h7 = "5sp"
    fonts.size.bar = "3sp"

    # listener = sr.Recognizer()

    # engine for converting speech to text (object)
    engine = pyttsx3.init()

    desktop = os.path.expanduser("~/Desktop/").replace("\\", "/")
    documents = os.path.expanduser("~/Documents/").replace("\\", "/")
    downloads = os.path.expanduser("~/Downloads/").replace("\\", "/")
    path_list = [downloads, desktop, documents]
    email_pattern = "['a-zA-Z0-9']+@[a-zA-Z]+\.[com|edu|ng|org]"
    emails = {'george': 'george.ajayi@stu.cu.edu.ng', 'aj': 'olanrewajuajayi2003@gmail.com',
              'christopher': 'christopher.akpoguma@stu.cu.edu.ng'}
    # openai.api_key = "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"

    # engine for converting speech to text function

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.wm = WindowManager(transition=CardTransition())

    # self.change_screen("home")
    # def build(self):

    def build(self):

        # Create a list of all screen, loop through it and add it to the screenmanager
        # and return the screenmanager.
        self.theme_cls.primary_hue = "A100"
        self.theme_cls.material_style = "M3"
        # self.theme_cls.theme_style = "Dark"
        self.wm = WindowManager()
        self.change_screen("splash")

        return self.wm

    def on_start(self):

        Clock.schedule_once(lambda ev: self.post_build_init(ev), 1)
        Clock.schedule_once(self.after_splash, 4)
        # Clock.schedule_once(self.start_func, 2)

    def post_build_init(self, ev):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:  # if the esc key is pressed for desktop, it takes you to the previous screen. Thesame for the backbutton for android
            self.goback()
            return True

    def after_splash(self, *args):
        self.change_screen("login")

    def dialogs(self):
        yes_button = MDFillRoundFlatButton(text="Yes", on_press=self.start)
        no_button = MDFillRoundFlatButton(text="No", on_press=self.close_dialog)
        self.logout_dialog = MDDialog(title="Permissions", text="Allow system to access files and folders on your computer", buttons=[yes_button, no_button])
        self.logout_dialog.open()

    def close_dialog(self,obj):
        self.logout_dialog.dismiss()

    def login(self, *args):
        # try:
        email = self.wm.get_screen('login').ids["email"].text
        password = self.wm.get_screen('login').ids["password"].text

        if email == "":
            toast("enter email")
        elif password == '':
            toast('enter password')
        else:
            # Set the environment variable
            conn = mysql.connector.connect(host='localhost', user='root', password='jesus', database='emaildb')
            cursor = conn.cursor()

            sql = f"SELECT * from details WHERE `email` = '{email}' AND `password` = '{password}'"

            cursor.execute(sql)

            result = cursor.fetchall()
            print(result)
            if result:
                firstname = result[0][3]
                lastname = result[0][4]
                self.change_screen("home")
                self.wm.get_screen('home').ids["username"].text= f"Hey {firstname} {lastname}"

                toast('Logged in successfully!')
            else:
                toast('Invalid email or password')
        # except Exception as e:
        #     print(str(e))

    #     self.change_screen("home")





    def start(self,*args):
        self.logout_dialog.dismiss()
        thread = threading.Thread(target=self.func)
        thread.setDaemon(True)
        thread.start()

    def talk(self, text):
        self.engine.say(text)
        self.wm.get_screen("home").ids['instruction'].text = text
        self.engine.setProperty('rate', 150)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.runAndWait()

    def func(self):
        self.talk('')
        self.talk("Hello I am mail bot, your  email assistant")
        self.get_user_details()

    def read_unseen_messages(self):
        host = "imap.gmail.com"
        username = "georgeajakadrex@gmail.com"
        pwd = "forwimzzgddvgigc"
        mail = imaplib.IMAP4_SSL(host)
        mail.login(username, pwd)
        mail.select("inbox")
        _, search_data = mail.search(None, "UNSEEN")
        for num in search_data[0].split()[-2:]:
            _, data = mail.fetch(num, '(RFC822)')
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['from', 'subject'.split("<")[0], 'date']:
                print("{}:{}".format(header, str(make_header(
                    decode_header(email_message[header])))))
                self.talk("{}:{}".format(header, str(make_header(
                    decode_header(email_message[header])))))
            # download email attachment
            for part in email_message.walk():
                if part.get_content_disposition() == 'attachment':
                    # Get the filename and save the attachment to disk
                    filename = part.get_filename()
                    open(os.path.join(self.desktop, filename), 'wb').write(
                        part.get_payload(decode=True))

    def get_user_details(self):
        try:
            SENDER_EMAIL = self.wm.get_screen('login').ids["email"].text
            password = self.wm.get_screen('login').ids["password"].text

            self.talk(
                "Please ensure the recipients emails are stored in a Microsoft Excel worksheet")

            self.talk(
                'if you already have this, please respond with proceed')


            while True:
                res = self.get_info()
                if 'proceed' in res.lower():

                    break
                else:
                    self.talk('please respond audibly with proceed')
                    continue



            while True:
                self.talk('What is the name of the file?')
                file = self.get_info()

                self.talk(
                    f'You said {file.lower()} is this correct?,respond with a yes or no')
                response=self.get_info()
                if 'yes' in response.lower():
                    break
                else:
                    continue



            confirm = []
            for path in self.path_list:
                directory = path
                file_path = f"{directory}{file.lower()}.xlsx"
                if os.path.isfile(file_path) is True:
                    data_frame = pd.read_excel(file_path)
                    self.talk("Okay , this file exists, do you want to send an attachment with this mail, please respond with\
                                                    yes or nevermind")
                    answer1 = self.get_info()
                    if 'yes' in f"{answer1.lower()}":
                        self.send_email_with_attachment(
                            password, data_frame, SENDER_EMAIL)
                    else:
                        self.send_email_without_attachment(
                            password, SENDER_EMAIL)
                else:
                    confirm.append('false')
            if len(confirm) > 2:
                self.talk(
                    'Sorry, It seems the file you mentioned does not exist on your system')
                self.talk(
                    'ensure the file is either in your downloads,documents or desktop directory')
                exception = pd.read_excel('~/Documents/1234')


        except Exception as e:

            print(str(e))
    def send_email_without_attachment(self, app_password, SENDER_EMAIL):
        try:
            response2 = 'no'
            self.talk('who do you want to send an email to?')
            recipient = self.get_info()
            self.wm.get_screen(
                "home").ids['instruction'].text = f'You: {recipient}' + '\n\n'
            while response2 == 'no':
                self.talk('what is the subject of your email')
                subject = self.get_info()
                self.talk(f'you said {subject}')
                self.wm.get_screen(
                    "home").ids['instruction'].text = f'You: you said {subject},respond with yes or no?' + '\n\n'
                self.talk('is this right?,please respond with yes or no')
                response2 = self.get_info()
            response = "no"
            while response == 'no':
                self.talk('what should I send?')
                body = self.get_info()
                self.talk(f'you said {body}')
                self.wm.get_screen(
                    "home").ids['instruction'].text = f'You: you said {body}' + '\n\n'
                self.talk('is this right?,please respond with yes or no')
                response = self.get_info()

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = self.emails[recipient]
            content = body
            msg.set_content(content)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(SENDER_EMAIL, app_password)
                smtp.send_message(msg)
            self.talk('do you want to send another email?')
            start = self.get_info()
            if 'yes' in start:
                self.send_email_without_attachment(app_password, SENDER_EMAIL)
        except:
            print('error')


    def get_info(self):
        while True:
            # Perform speech recognition
            result = az.recognize_from_microphone()

            # Check if the result is None
            if result is None:
                self.talk("No speech detected. Please repeat yourself.")
                continue  # Continue to the next iteration of the loop

            # Process the recognized speech
            return result
            break




    def send_email_with_attachment(self, app_password, data, SENDER_EMAIL):
        checklist = []
        dataframe = data
        self.talk(
            f'please ensure the attachment/attachments you want to send to each recipient are stored in a folder.')
        self.talk('if you have already done this, respond with proceed')
        # res=self.get_info()
        while True:
            res = self.get_info()
            if 'proceed' in res.lower():
                break
            else:
                self.talk('please respond with proceed')
                continue







        extension = {'option 1': '.pdf', 'option 2': '.xlsx', 'option 3': '.docx', 'pdf': '.pdf', 'word': '.docx', 'excel':
                     '.xlsx', 'microsoft word': 'docx', 'microsoft excel': '.xlsx', "option one": '.pdf', "option two": '.xlsx',
                     "option three": '.docx'}
        self.talk('What is the format of this attachments')
        while True:
            self.talk('select one of the options')
            self.talk(
                'option 1 is pdf, option 2 is Microsoft Excel, and Option 3 is Microsoft word')
            choice = self.get_info().lower().strip('.')


            self.talk(f'you selected {choice}, yes or no')
            res=self.get_info()
            if 'yes' in res.lower().strip('.'):
                break
            else:
                continue


        # ans = 'no'
        # ans = self.get_info()
        while True:
            self.talk('what is the name of the folder')
            folder = self.get_info()
            # textarea.insert(END, f'You: {folder}' + '\n\n')
            self.wm.get_screen(
                "home").ids['instruction'].text = f'You: {folder}' + '\n\n'
            self.talk(
                f"You said {folder.lower().strip('.')} is this correct, respond with a yes or no")
            ans = self.get_info()
            if 'yes' in ans.lower():
                break
            else:
                continue

        # checks each directory if the folder exists
        for path in self.path_list:
            directory = path+folder.lower().strip('.')
            if os.path.exists(directory) is True:
                users = directory
                self.talk('the folder exists')
            else:
                value = 'false'
                checklist.append(value)
        # if the folder does not exist in any of the specified directories
        if len(checklist) > 2:
            self.talk('this folder does not exist')
            self.talk(
                'please ensure the folder is in either your downloads,documents or desktop directory')
            exception = pd.read_excel('~/Documents/1234')

        else:

            while True:
                self.talk('what is the subject of your email')
                subject = self.get_info()
                self.talk(f'you said "{subject}"')

                self.wm.get_screen(
                    "home").ids['instruction'].text = f'You: {subject}' + '\n\n'
                self.talk('is this right?,please respond with yes or no')
                response2 = self.get_info()
                if 'yes' in response2.lower():
                    break
                # textarea.insert(END, f'You: {response2}' + '\n\n')
                #     self.wm.get_screen(
                #         "home").ids['instruction'].text = f'You: {response2}' + '\n\n'
                else:
                    continue



            while True:
                self.talk('what should I send?')
                body = self.get_info()
                self.talk(f'you said {body}')

                self.wm.get_screen(
                    "home").ids['instruction'].text = f'You: {body}' + '\n\n'
                self.talk('Is this correct?, respond with a yes or no')
                response3 = self.get_info()
                if 'yes' in response3.lower():
                    break
                    self.wm.get_screen(
                        "home").ids['instruction'].text = f'You: {response3}' + '\n\n'
                else:
                    continue


            self.wm.get_screen(
                "home").ids['instruction'].text = 'Sending...' + '\n\n'
            # sends the attachment to each recipient
            failed_emails=[]
            wrong_files=[]
            for index, row in dataframe.iterrows():
                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = SENDER_EMAIL
                msg['To'] = row['email']
                is_valid=ec.validate(row['email'])
                if is_valid =='Invalid':
                    failed_emails.append(row['email'])
                    continue
                msg.set_content(f"{body}")
                attach = users+'/'+f"{row['attachment']}"
                file_path = attach+f"{extension[choice]}"
                failed_emails = []
                if os.path.exists(file_path) is True:
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    msg.add_attachment(file_data, maintype="application",
                                       subtype=f"{extension[choice]}", filename=os.path.basename(file_path))

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(SENDER_EMAIL, app_password)
                        smtp.send_message(msg)
                else:
                    wrong_files.append(row['email'])
                    continue


            sent_emails=dataframe.shape[0]-len(failed_emails)
        if sent_emails == 0:
            self.talk('unable to send any e-mail')

        else:
            self.talk(
                f'your mail was succesfully sent to {sent_emails} recipients with the attachments as you requested')

    def change_screen(self, screen_name, __from_goback=False):
        # self.wm.current = screen_name
        # checks if the screen already exists in the screen manager
        # if the screen is not yet in the screen manager,
        if not self.wm.has_screen(screen_name):
            # gets the key screen name from the screens.json file
            getter = self.screens_store.get(screen_name)
            # executes the value of the import key in the screens.json file
            exec(getter['import'])
            print(getter['object'])
            print(getter['import'])
            # calls the screen class to get the instance of it
            screen_object = eval(getter["object"])
            # automatically sets the screen name using the arg that passed in set_current
            screen_object.name = screen_name
            # Builder.load_file(getter['kv'])
            # finnaly adds the screen to the screen-manager
            self.wm.add_widget(screen_object)
            # changes the screen to the specified screen
            # self.wm.current = screen_name
            # Builder.load_file(getter['kv'])

        # if the screens is already in the screen manager,
        # changes the screen to the specified screen
        self.wm.current = screen_name

        # if not __from_goback:
        if screen_name != "splash":
            self.screen_history.append({"name": screen_name, })

    def goback(self):
        if len(self.screen_history) > 1:
            self.screen_history.pop()
            prev_screen = self.screen_history[-1]
            print(self.screen_history)
            print(prev_screen)

            self.change_screen(prev_screen["name"])

    def logout(self):
        self.change_screen("login")
