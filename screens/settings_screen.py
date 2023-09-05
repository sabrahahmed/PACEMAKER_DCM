import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
from time import sleep


class SettingsScreen:
    def __init__(self):
        self.window_size = (1280, 720)
        self.current_user = ""
        self.current_pass = ""

    def create_layout(self):
        top_left = [
            [sg.Image(key='IMAGE', enable_events=True)]
        ]

        buttons = [
            [sg.Button("Sign Out", key="SIGN-OUT")],
            [sg.Button("Delete Account", button_color="Black", key="DELETE")],
            [sg.InputText(password_char="*", key="PASS", size=(30, 40), do_not_clear=False)],
            [sg.Text("Reenter password to delete account", font=('Courier New', 10, 'bold'))],
        ]

        utility = [
            [sg.Text("Application Version: 2.70", font=('Courier New', 10, 'normal'))],
            [sg.Text("Pacemaker Serial Number: H00140", font=('Courier New', 10, 'normal'))],
            [sg.Text("Institution: McMaster University", font=('Courier New', 10, 'normal'))]
        ]

        layout = [
            [sg.Column(top_left, element_justification="left", expand_x=True)],
            [sg.VPush()],
            [sg.Column(buttons, element_justification="center", expand_x=True, expand_y=True)],
            [sg.VPush()],
            [sg.Column(utility, element_justification="center", expand_x=True, expand_y=True)],
        ]

        return layout

    def run(self):
        # IMAGE SETTINGS
        filename = "images/back_button.png"
        size = (30, 30)
        img = Image.open(filename)
        img = img.resize(size, resample=Image.BICUBIC)

        sg.theme('Reddit')

        layout = self.create_layout()

        window = sg.Window('Pacemaker DCM User Settings', layout, margins=(0, 0), finalize=True, resizable=False,
                           size=self.window_size)

        # Convert im to ImageTk.PhotoImage after window finalized
        image = ImageTk.PhotoImage(image=img)

        # update image in sg.Image
        window['IMAGE'].update(data=image)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                window.close()
                return "EXIT"

            if event == "SIGN-OUT":
                window.close()
                return "WELCOME"

            if event == "DELETE":
                if values['PASS'] == self.current_pass:
                    try:
                        conn = sqlite3.connect('user_credentials.db')
                        cursor = conn.cursor()

                        cursor.execute("DELETE FROM users WHERE username=?", (self.current_user,))
                        conn.commit()
                        event = sg.WIN_CLOSED
                        conn = sqlite3.connect('pacemaker_settings.db')
                        cursor = conn.cursor()

                        cursor.execute("DELETE FROM AAI WHERE username=?", (self.current_user,))
                        cursor.execute("DELETE FROM AOO WHERE username=?", (self.current_user,))
                        cursor.execute("DELETE FROM VOO WHERE username=?", (self.current_user,))
                        cursor.execute("DELETE FROM VVI WHERE username=?", (self.current_user,))

                        conn.commit()
                        conn.close()
                        sg.popup_quick_message("Account deleted", text_color="Red")
                        sleep(2)
                        window.close()
                        return "WELCOME"

                    except Exception as e:
                        sg.popup_quick_message("Error: " + str(e), text_color="Red")

                else:
                    sg.popup_quick_message("Incorrect Password", text_color="Red")
            if event == "IMAGE":
                window.close()
                return "MAIN"


