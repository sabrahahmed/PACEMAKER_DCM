import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
import bcrypt
from utilities.user import user


class RegisterScreen:
    def __init__(self):
        self.window_size = (1280, 720)
        self.current_user = ""
        self.current_pass = ""

    def create_layout(self):
        left_side = [
            [sg.Image(key='REGISTER_IMAGE')]
        ]

        register_button = [
            [sg.Button("Register", size=(25, 1), pad=(5, 5), button_color='Black', bind_return_key=True,
                       border_width=3)]
        ]

        back_button = [
            [sg.Text("Back", enable_events=True, key="BACK", text_color='#007ad2')],
        ]

        right_side = [
            [sg.Text("Username:")],
            [sg.InputText(key="USER", size=(30, 40), do_not_clear=True, pad=(10, 10))],
            [sg.Text("Password:")],
            [sg.InputText(key="PASS", password_char="*", size=(30, 40), do_not_clear=False, pad=(10, 10))],
            [sg.Text("Reenter Password:")],
            [sg.InputText(key="REENTER", password_char="*", size=(30, 40), do_not_clear=False, pad=(10, 10))],
            [sg.Column(register_button, element_justification='center', expand_x=True)],
            [sg.Column(back_button, element_justification='center', expand_x=True)]
        ]

        column2 = [
            [sg.Column(right_side)]
        ]

        main = [
            [sg.Column(column2, expand_x=True, element_justification="center")]
        ]

        layout = [
            [sg.Column(left_side),
             sg.Column(main, pad=(20, 20), expand_x=True, element_justification="Center"),
             ]
        ]

        return layout

    def run(self):
        # REGISTER SCREEN IMAGE
        filename = "images/login_image.jpg"
        size = (640, 720)
        img = Image.open(filename)
        img = img.resize(size, resample=Image.BICUBIC)

        sg.theme('DefaultNoMoreNagging')

        layout = self.create_layout()

        window = sg.Window('Pacemaker DCM Registration', layout, margins=(0, 0), finalize=True,
                           resizable=False, size=self.window_size)

        # Convert im to ImageTk.PhotoImage after window finalized
        image = ImageTk.PhotoImage(image=img)
        # update image in sg.Image
        window['REGISTER_IMAGE'].update(data=image)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                return "EXIT"

            if event == "BACK":
                window.close()
                return "WELCOME"

            if event == 'Register':
                if values['USER'] and values['PASS']:
                    if values['PASS'] == values['REENTER']:
                        special_characters = """#$%&'()*!+,-."/:;<=>?@[\]^_`{|}~"""

                        if any(c in special_characters for c in values['USER']):
                            sg.popup_quick_message("Username cannot contain spaces or special characters",
                                                   text_color="Red")

                        elif len(values['PASS']) < 8:
                            sg.popup_quick_message("Password must be at least 8 characters", text_color="Red")

                        else:
                            self.current_user = values['USER']
                            self.current_pass = values['PASS']

                            try:
                                conn = sqlite3.connect('user_credentials.db')
                                cursor = conn.cursor()

                                cursor.execute("SELECT * FROM users WHERE username=?", (self.current_user,))
                                existing_user = cursor.fetchone()

                                if existing_user:
                                    sg.popup_quick_message("Already an active user. Please try a new username.",
                                                           text_color="Red")
                                else:
                                    hashed_password = bcrypt.hashpw(self.current_pass.encode('utf-8'), bcrypt.gensalt())

                                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                                   (self.current_user, hashed_password))
                                    conn.commit()

                                    conn = sqlite3.connect('pacemaker_settings.db')
                                    cursor = conn.cursor()

                                    cursor.execute("INSERT INTO AAI (username) VALUES (?)", (self.current_user,))
                                    cursor.execute("INSERT INTO AOO (username) VALUES (?)", (self.current_user,))
                                    cursor.execute("INSERT INTO VOO (username) VALUES (?)", (self.current_user,))
                                    cursor.execute("INSERT INTO VVI (username) VALUES (?)", (self.current_user,))

                                    # cursor.execute(f"INSERT INTO {self.current_user} (username) VALUES (?)",
                                    #                (self.current_user,))

                                    conn.commit()
                                    conn.close()
                                    window.close()
                                    user.set_credentials(self.current_user, self.current_pass)
                                    return "MAIN"

                            except Exception as e:
                                sg.popup_quick_message("Error: " + str(e), text_color="Red")
                    else:
                        sg.popup_quick_message("Passwords do not match.", text_color="Red")



