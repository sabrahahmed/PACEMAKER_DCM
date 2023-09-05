import PySimpleGUI as sg
from PIL import Image, ImageTk


class WelcomeScreen:
    def __init__(self):
        self.window_size = (1280, 720)

    def create_layout(self):
        top = [
            [sg.Image(key='LAUNCH_IMAGE')]
        ]

        bottom = [
            [sg.Button("Login", size=(15, 1), pad=(25, 0), button_color='Black on White', bind_return_key=True,
                       key="LOGIN"),
             sg.Button("Register", size=(15, 1), pad=(25, 0), button_color='Black on White', bind_return_key=True,
                       key="REGISTER")]
        ]

        layout = [
            [sg.Column(top, background_color="Black")],
            [sg.Column(bottom, background_color="Black", expand_x=True, element_justification="center")]
        ]

        return layout

    def run(self):
        # LAUNCH SCREEN IMAGE
        filename = "images/launch_image.jpg"
        size = (1280, 630)
        img = Image.open(filename)
        img = img.resize(size, resample=Image.BICUBIC)

        sg.theme('DefaultNoMoreNagging')

        layout = self.create_layout()

        window = sg.Window('Pacemaker DCM Login', layout, margins=(0, 0), finalize=True, resizable=False,
                           size=self.window_size, background_color="Black")

        # Convert im to ImageTk.PhotoImage after window finalized and update image in sg.Image
        image = ImageTk.PhotoImage(image=img)
        window['LAUNCH_IMAGE'].update(data=image)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                return "EXIT"

            if event == "LOGIN":
                window.close()
                return "LOGIN"

            if event == "REGISTER":
                window.close()
                return "REGISTER"


