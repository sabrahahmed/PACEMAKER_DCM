import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
import bcrypt
from utilities.user import user


class LoginScreen:
    def __init__(self):
        self.window_size = (1280, 720)
        self.current_user = ""
        self.current_pass = ""

    def create_layout(self):
        left_side = [
            [sg.Image(key='LOGIN_IMAGE', background_color="Black")]
        ]

        login_button = [
            [sg.Button("Login", size=(25, 1), pad=(5, 5), button_color='Black', bind_return_key=True, border_width=3)]
        ]

        register_button = [
            [sg.Text("Back", enable_events=True, key="BACK", text_color='#007ad2')],
        ]

        right_side = [
            [sg.Text("Username:")],
            [sg.InputText(key="USER", size=(30, 40), do_not_clear=False, pad=(10, 10))],
            [sg.Text("Password:")],
            [sg.InputText(key="PASS", password_char="*", size=(30, 40), do_not_clear=False, pad=(10, 10))],
            [sg.Column(login_button, element_justification='center', expand_x=True)],
            [sg.Column(register_button, element_justification='center', expand_x=True)],
        ]

        column2 = [
            [sg.Column(right_side)]
        ]

        main = [
            [sg.Column(column2, expand_x=True, element_justification="center")]
        ]

        layout = [
            [sg.Column(left_side),
             sg.Column(main, pad=(20, 20), expand_x=True, element_justification="center"),
             ]
        ]

        return layout

    def run(self):
        # LOGIN SCREEN IMAGE
        filename = "images/login_image.jpg"
        size = (640, 720)
        img = Image.open(filename)
        img = img.resize(size, resample=Image.BICUBIC)

        sg.theme('DefaultNoMoreNagging')

        layout = self.create_layout()
        window = sg.Window('Pacemaker DCM Login', layout, margins=(0, 0), finalize=True, resizable=False,
                           size=self.window_size)

        # Convert im to ImageTk.PhotoImage after window finalized
        image = ImageTk.PhotoImage(image=img)
        window['LOGIN_IMAGE'].update(data=image)

        # Create an event loop
        while True:
            event, values = window.read()

            if event == "Login":
                # Check if inputs are empty
                if values['USER'] and values['PASS']:
                    # Check login data in SQLite database
                    self.current_user = values['USER']
                    self.current_pass = values['PASS']

                    try:
                        conn = sqlite3.connect('user_credentials.db')
                        cursor = conn.cursor()

                        # Retrieve hashed password from database for given username
                        cursor.execute("SELECT password FROM users WHERE username=?", (self.current_user,))
                        hashed_password = cursor.fetchone()

                        if hashed_password:
                            # Verify password against hashed password
                            if bcrypt.checkpw(self.current_pass.encode('utf-8'), hashed_password[0]):
                                conn.close()
                                window.close()
                                user.set_credentials(self.current_user, self.current_pass)
                                return "MAIN"

                            else:
                                sg.popup_quick_message("Incorrect Password", text_color="Red")
                        else:
                            sg.popup_quick_message("Not an active user", text_color="Red")

                    except Exception as e:
                        sg.popup_quick_message("Error: " + str(e), text_color="Red")

            if event == sg.WIN_CLOSED:
                window.close()
                return "EXIT"

            if event == "BACK":
                window.close()
                return "WELCOME"


