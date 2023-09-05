import PySimpleGUI as sg
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
from modules.modes_tabs import Mode
from modules.electrogram import graph
from connection.pacemaker_connection import *
from utilities.user import user


def get_current_time():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%H:%M:%S")
    return timestampStr


class MainScreen:
    def __init__(self):
        self.window_size = (1280, 720)
        self.current_user = user.get_username()
        self.current_pass = user.get_password()
        self.window = None

    def create_layout(self):
        # FOOTER
        welcome = [
            [sg.Text("Welcome, " + self.current_user + "!", background_color="Black", text_color="White")]
        ]

        top_right = [
            [sg.Image(key='SETTINGS', enable_events=True)],
        ]

        footer = [
            [sg.Column(welcome, background_color="Black"),
             sg.Push(background_color="Black"),
             sg.Column(top_right, background_color="Black")],
        ]

        # E-GRAM
        a_graph = [[sg.Canvas(size=(900, 300), key='CANVAS1')]]
        v_graph = [[sg.Canvas(size=(900, 300), key='CANVAS2')]]

        electrogram = [
            [sg.TabGroup(
                [[
                    sg.Tab("Atrial", a_graph, expand_x=True, element_justification="center"),
                    sg.Tab("Ventricular", v_graph, expand_x=True, element_justification="center"),
                ],
                ],
                tab_location="topleft",
                title_color="White",
                tab_background_color='Black',
                selected_title_color="White",
                selected_background_color='#007ad2',
                tab_border_width=1,
                border_width=0,
                size=(900, 300)
            )
            ]]

        e_buttons = [
            [sg.VPush()],
            [sg.Image(key='START', enable_events=True, pad=(0, 5), tooltip="Start electrogram")],
            [sg.Image(key='STOP', enable_events=True, pad=(0, 5), tooltip="Stop electrogram")],
            [sg.Image(key='IMPORT', enable_events=True, pad=(0, 5), tooltip="Import current pacemaker parameters")],
            [sg.VPush()],
        ]

        electrogram_buttons = [
            [sg.TabGroup(
                [[sg.Tab("", e_buttons),
                  ],
                 ],
                tab_location="top",
                title_color="White",
                tab_background_color='White',
                selected_title_color="White",
                selected_background_color='White',
                tab_border_width=0,
                border_width=0,
                size=(150, 300),
            )
            ]]

        # PACING MODES
        pacing_mode = Mode()

        modes = [
            [sg.TabGroup(
                [[
                    sg.Tab("AOO", pacing_mode.AOO(), expand_x=True, element_justification="Center", key="AOO"),
                    sg.Tab("AAI", pacing_mode.AAI(), expand_x=True, element_justification="Center", key="AAI"),
                    sg.Tab("VOO", pacing_mode.VOO(), expand_x=True, element_justification="Center", key="VOO"),
                    sg.Tab("VVI", pacing_mode.VVI(), expand_x=True, element_justification="Center", key="VVI"),
                ],
                ],
                key="MODES",
                tab_location="topleft",
                title_color="White",
                tab_background_color='Black',
                selected_title_color="White",
                selected_background_color='#007ad2',
                tab_border_width=0,
                border_width=1,
                size=(1050, 300),
                focus_color="#007ad2"
            )
            ]]

        # DEVICE + CONSOLE LEFT TAB
        tab = [
            [sg.TabGroup(
                [[
                    sg.Tab("", self.left_tab(), expand_x=True, element_justification="left", background_color='white'),
                ],
                ],
                tab_location="bottom",
                title_color="White",
                tab_background_color='White',
                selected_title_color="White",
                selected_background_color='White',
                tab_border_width=0,
                border_width=0,
                size=(265, 1000),
            )
            ]]

        left = [
            [sg.Column(tab, expand_x=True, element_justification="left")],
        ]

        right = [
            [sg.Column(electrogram),
             sg.Column(electrogram_buttons)],
            [sg.Column(modes, expand_x=True, element_justification="right")],
        ]

        layout = [
            [sg.Column(footer, expand_x=True, element_justification="center", background_color="Black")],
            [sg.Column(left, background_color="White", expand_x=True, element_justification="left"),
             sg.VerticalSeparator(pad=(0, 10)),
             sg.Column(right, background_color="White")]
        ]

        return layout

    def connect_popup(self, previous):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H:%M:%S")

        sg.theme('Reddit')

        device_name = 'PACEMAKER123'
        buttons = [
            [sg.Text(device_name + " detected.", font=('Courier New', 10, 'bold')), ],
            [sg.Text("Would you like to connect?", font=('Courier New', 10, 'normal'))],
            [sg.Button("YES", key="YES"), sg.Button("NO", key="NO")],
        ]

        layout = [
            [sg.VPush()],
            [sg.Column(buttons, element_justification="center", expand_x=True, expand_y=True)],
            [sg.VPush()],
        ]

        window = sg.Window('Connection', layout, margins=(0, 0), finalize=True, resizable=False)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                previous.enable()
                return "EXIT"

            if event == "YES":
                previous.enable()
                previous.Element('device_name').update("PACEMAKER123")
                previous.Element('STATUS').update("Connected")
                # previous.Element("CONNECT").update("DISCONNECT")
                console.append(" Connected: " + timestampStr)
                previous.Element("CONSOLE").update(console)
                window.close()

            if event == "NO":
                previous.enable()
                window.close()

    # DISCONNECT FROM PACEMAKER PROMPT
    def disconnect_popup(self, previous):
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H:%M:%S")

        sg.theme('Reddit')

        device_name = 'PACEMAKER123'
        buttons = [
            [sg.Text(device_name + " connected.", font=('Courier New', 10, 'bold')), ],
            [sg.Text("Would you like to disconnect?", font=('Courier New', 10, 'normal'))],
            [sg.Button("YES", key="YES"), sg.Button("NO", key="NO")],
        ]

        layout = [
            [sg.VPush()],
            [sg.Column(buttons, element_justification="center", expand_x=True, expand_y=True)],
            [sg.VPush()],
        ]

        window = sg.Window('Connection', layout, margins=(0, 0), finalize=True, resizable=False)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                window.close()
                previous.enable()
                return "EXIT"

            if event == "YES":
                previous.enable()
                previous.Element('device_name').update("No Device Connected")
                previous.Element('STATUS').update("Disconnected")
                previous.Element("CONNECT").update("CONNECT")
                console.append(" Disconnected: " + timestampStr)
                previous.Element("CONSOLE").update(console)
                window.close()

            if event == "NO":
                previous.enable()
                window.close()

    # LEFT TAB ON MAIN SCREEN WITH DEVICE INFORMATION + CONSOLE
    def left_tab(self):
        # ports = ["COM6", "COM7"]
        device = [
            [sg.Text("DEVICE", font=('Courier New', 15, 'bold'))],
            [sg.InputText(key="PORT", size=(10, 40), do_not_clear=False, tooltip="Port Number (e.g. COM6)"),
             sg.Button("Connect", button_color="#007ad2", font=10, visible=True, key="CONNECT")],
            [sg.Text("NO DEVICE CONNECTED", font=('Courier New', 10, 'bold'), key="device_name")],
            [sg.Text("Disconnected", text_color="Grey", font=('Courier New', 10, 'italic'), key='STATUS'),
             ],
        ]
        # sg.Combo(ports, readonly=True, tooltip="Port", key="PORT") pad=(10, 10)
        global console
        console = [" Login: " + get_current_time()]

        list = [
            [sg.Listbox(console, size=(350, 350), background_color="White", no_scrollbar=False, key='CONSOLE',
                        text_color="Black", font=('Courier New', 10, 'italic'))]]

        console_list = [
            [sg.Text("CONSOLE", font=('Courier New', 15, 'bold'))],
            [sg.Column(list)],
        ]

        layout = [
            [sg.Column(device)],
            [sg.Column(console_list)],

        ]

        return layout

    def load_and_resize_image(self, filename, size=(30, 30)):
        img = Image.open(filename)
        img = img.resize(size, resample=Image.BICUBIC)
        return ImageTk.PhotoImage(image=img)

    def setup_window(self):
        sg.theme('Reddit')
        layout = self.create_layout()
        window = sg.Window('Pacemaker DCM', layout, margins=(0, 0), finalize=True, resizable=False,
                           size=self.window_size)
        return window

    def update_images(self, window):
        image1 = self.load_and_resize_image("images/user_icon.jpg")
        image2 = self.load_and_resize_image("images/load_image.jpg")
        image3 = self.load_and_resize_image("images/send_button.jpg")
        image4 = self.load_and_resize_image("images/start_button.png")
        image5 = self.load_and_resize_image("images/stop_button.png")
        image6 = self.load_and_resize_image("images/import_button.png")

        window['SETTINGS'].update(data=image1)
        window['START'].update(data=image4)
        window['STOP'].update(data=image5)
        window['IMPORT'].update(data=image6)

        # Update other elements with appropriate images
        for mode_key in ["AOO", "AAI", "VOO", "VVI"]:
            window[f'{mode_key}_LOAD'].update(data=image2)
            window[f'{mode_key}_SEND'].update(data=image3)

    def aoo_send(self, values, coms, conn):
        if values["AOO_LRL"] and values["AOO_URL"] and values["AOO_AA"] and values["AOO_APW"]:
            if values["AOO_LRL"] < values["AOO_URL"]:
                AOO_values = (
                    values["AOO_LRL"],
                    values["AOO_URL"],
                    values["AOO_APW"],
                    values["AOO_AA"],
                    self.current_user,
                )
                # Update the existing row in the "AOO" table for the current user
                cursor = conn.cursor()
                cursor.execute("UPDATE AOO SET LRL = ?, URL = ?, APW = ?, AA = ? WHERE username = ?",
                               (*AOO_values, self.current_user))
                conn.commit()

                if coms.send_para(2, self.current_user):
                    sg.popup_quick_message("AOO inputs sent to pacemaker", text_color="Green")
                    console.append(" Sent AOO: " + get_current_time())
                    self.window.Element('CONSOLE').update(console)
                    self.window.refresh()
                else:
                    sg.popup_quick_message("AOO inputs failed to send to pacemaker", text_color="Red")
            else:
                sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
                                       text_color="Red")
        else:
            sg.popup_quick_message("Missing parameters", text_color="Red")

    def aoo_load(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT LRL, URL, AA, APW FROM AOO WHERE username = ?", (self.current_user,))
        row = cursor.fetchone()

        if row is not None:
            lrl, url, aa, apw = row

            self.window.Element('AOO_LRL').update(lrl)
            self.window.Element('AOO_URL').update(url)
            self.window.Element('AOO_AA').update(aa)
            self.window.Element('AOO_APW').update(apw)

            console.append(" Loaded AOO: " + get_current_time())
            self.window.Element('CONSOLE').update(console)
            self.window.refresh()
        else:
            sg.popup_quick_message("No previous parameters found for the current user", text_color="Red")

    def aai_send(self, values, coms, conn):
        if values["AAI_LRL"] and values["AAI_URL"] and values["AAI_ARP"] and values["AAI_H"] \
                and values["AAI_AA"] and values["AAI_APW"] and values["AAI_AS"] and values["AAI_RS"]:
            if values["AAI_LRL"] < values["AAI_URL"]:
                AAI_values = (
                    values["AAI_LRL"],
                    values["AAI_URL"],
                    values["AAI_ARP"],
                    values["AAI_H"],
                    values["AAI_AA"],
                    values["AAI_APW"],
                    values["AAI_AS"],
                    values["AAI_RS"],
                    self.current_user,
                )
                # Update the existing row in the "AOO" table for the current user
                cursor = conn.cursor()
                cursor.execute('''UPDATE AAI SET 
                                    LRL = ?, 
                                    URL = ?, 
                                    ARP = ?, 
                                    PVARP = ?, 
                                    H = ?, 
                                    AA = ?,
                                    APW = ?,
                                    "AS" = ?,
                                    "RS" = ?,                                                                        
                                    WHERE username = ?
                                ''',
                               AAI_values, self.current_user)
                conn.commit()

                if coms.send_para(4, self.current_user):
                    sg.popup_quick_message("AAI inputs sent to pacemaker", text_color="Green")
                    console.append(" Sent AAI: " + get_current_time())
                    self.window.Element('CONSOLE').update(console)
                    self.window.refresh()
                else:
                    sg.popup_quick_message("AAI inputs failed to send to pacemaker", text_color="Red")
            else:
                sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
                                       text_color="Red")
        else:
            sg.popup_quick_message("Missing parameters", text_color="Red")

    def aai_load(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT LRL, URL, ARP, PVARP, H, AA, APW, AS, RS FROM AAI WHERE username = ?",
                       (self.current_user,))
        row = cursor.fetchone()

        if row is not None:
            lrl, url, arp, pvarp, h, aa, apw, as_val, rs = row

            self.window.Element('AAI_LRL').update(lrl)
            self.window.Element('AAI_URL').update(url)
            self.window.Element('AAI_ARP').update(arp)
            self.window.Element('AAI_PVARP').update(pvarp)
            self.window.Element('AAI_H').update(h)
            self.window.Element('AAI_AA').update(aa)
            self.window.Element('AAI_APW').update(apw)
            self.window.Element('AAI_AS').update(as_val)
            self.window.Element('AAI_RS').update(rs)

            console.append(" Loaded AAI: " + get_current_time())
            self.window.Element('CONSOLE').update(console)
            self.window.refresh()
        else:
            sg.popup_quick_message("No previous AAI parameters found for the current user", text_color="Red")

    def voo_send(self, values, coms, conn):
        f = open("data/data.json", "r+")
        data = json.load(f)

        if values["VOO_LRL"] and values["VOO_URL"] and values["VOO_VA"] and values["VOO_VPW"]:
            if values["VOO_LRL"] < values["VOO_URL"]:
                VOO_values = (
                    values["VOO_LRL"],
                    values["VOO_URL"],
                    values["VOO_VA"],
                    values["VOO_VPW"],
                    self.current_user,
                )
                # Update the existing row in the "AOO" table for the current user
                cursor = conn.cursor()
                cursor.execute('''UPDATE VOO SET 
                                    LRL = ?, 
                                    URL = ?, 
                                    VA = ?, 
                                    VPW = ?, 
                                                ''',
                               VOO_values, self.current_user)
                conn.commit()

                data[self.current_user]["VOO"] = {

                }
                open("data/data.json", "w").write(json.dumps(data, indent=4, separators=(',', ': ')))
                if coms.send_para(1, self.current_user):
                    sg.popup_quick_message("VOO inputs sent to pacemaker", text_color="Green")
                    console.append(" Sent VOO: " + get_current_time())
                    self.window.Element('CONSOLE').update(console)
                    self.window.refresh()
                else:
                    sg.popup_quick_message("VOO inputs failed to send to pacemaker", text_color="Red")
            else:
                sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
                                       text_color="Red")
        else:
            sg.popup_quick_message("Missing parameters", text_color="Red")

    def voo_load(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT LRL, URL, VA, VPW FROM VOO WHERE username = ?", (self.current_user,))
        row = cursor.fetchone()

        if row is not None:
            lrl, url, va, vpw = row

            self.window.Element('VOO_LRL').update(lrl)
            self.window.Element('VOO_URL').update(url)
            self.window.Element('VOO_VA').update(va)
            self.window.Element('VOO_VPW').update(vpw)

            console.append(" Loaded VOO: " + get_current_time())
            self.window.Element('CONSOLE').update(console)
            self.window.refresh()
        else:
            sg.popup_quick_message("No previous VOO parameters found for the current user", text_color="Red")

    def vvi_send(self, values, coms, conn):
        if values["VVI_LRL"] and values["VVI_URL"] and values["VVI_VRP"] and values["VVI_H"] \
                and values["VVI_VA"] and values["VVI_VPW"] and values["VVI_VS"] and values["VVI_RS"]:
            if values["VVI_LRL"] < values["VVI_URL"]:
                VVI_values = (
                    values["VVI_LRL"],
                    values["VVI_URL"],
                    values["VVI_VRP"],
                    values["VVI_H"],
                    values["VVI_VA"],
                    values["VVI_VPW"],
                    values["VVI_VS"],
                    values["VVI_RS"],
                    self.current_user,
                )
                # Update the existing row in the "AOO" table for the current user
                cursor = conn.cursor()
                cursor.execute('''UPDATE VVI SET 
                                    LRL = ?, 
                                    URL = ?, 
                                    VRP = ?, 
                                    H = ?, 
                                    VA = ?,
                                    VPW = ?,
                                    "VS" = ?,
                                    "RS" = ?,                                                                        
                                    WHERE username = ?
                                ''',
                               VVI_values, self.current_user)
                conn.commit()

                if coms.send_para(3, self.current_user):
                    sg.popup_quick_message("VVI inputs sent to pacemaker", text_color="Green")
                    console.append(" Sent VVI: " + get_current_time())
                    self.window.Element('CONSOLE').update(console)
                    self.window.refresh()
                else:
                    sg.popup_quick_message("VVI inputs failed to send to pacemaker", text_color="Red")
            else:
                sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
                                       text_color="Red")
        else:
            sg.popup_quick_message("Missing parameters", text_color="Red")

    def vvi_load(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT LRL, URL, VRP, H, VA, VPW, VS, RS FROM VVI WHERE username = ?", (self.current_user,))
        row = cursor.fetchone()

        if row is not None:
            lrl, url, vrp, h, va, vpw, vs, rs = row

            # Update the GUI elements with the retrieved values
            self.window.Element('VVI_LRL').update(lrl)
            self.window.Element('VVI_URL').update(url)
            self.window.Element('VVI_VRP').update(vrp)
            self.window.Element('VVI_H').update(h)
            self.window.Element('VVI_VA').update(va)
            self.window.Element('VVI_VPW').update(vpw)
            self.window.Element('VVI_VS').update(vs)
            self.window.Element('VVI_RS').update(rs)

            console.append(" Loaded VVI: " + get_current_time())
            self.window.Element('CONSOLE').update(console)
            self.window.refresh()
        else:
            sg.popup_quick_message("No previous VVI parameters found for the current user", text_color="Red")

    def import_data(self, coms, conn):
        mode = coms.rqst_para(self.current_user)
        cursor = conn.cursor()

        if mode == 1:
            cursor.execute("SELECT LRL, URL, VA, VPW FROM VOO WHERE username = ?", (self.current_user,))
            row = cursor.fetchone()
            if row is not None:
                self.window['MODES'].Widget.select(2)
                lrl, url, va, vpw = row
                self.window['VOO_LRL'].update(lrl)
                self.window['VOO_URL'].update(url)
                self.window['VOO_VA'].update(va)
                self.window['VOO_VPW'].update(vpw)
                self.window.refresh()

        if mode == 2:
            cursor.execute("SELECT LRL, URL, AA, APW FROM AOO WHERE username = ?", (self.current_user,))
            row = cursor.fetchone()
            if row is not None:
                self.window['MODES'].Widget.select(0)
                lrl, url, aa, apw = row
                self.window['AOO_LRL'].update(lrl)
                self.window['AOO_URL'].update(url)
                self.window['AOO_AA'].update(aa)
                self.window['AOO_APW'].update(apw)
                self.window.refresh()

        if mode == 3:
            cursor.execute("SELECT LRL, URL, VRP, H, VA, VPW, VS, RS FROM VVI WHERE username = ?", (self.current_user,))
            row = cursor.fetchone()
            if row is not None:
                self.window['MODES'].Widget.select(3)
                lrl, url, vrp, h, va, vpw, vs, rs = row
                self.window['VVI_LRL'].update(lrl)
                self.window['VVI_URL'].update(url)
                self.window['VVI_VRP'].update(vrp)
                self.window['VVI_H'].update(h)
                self.window['VVI_VA'].update(va)
                self.window['VVI_VPW'].update(vpw)
                self.window['VVI_VS'].update(vs)
                self.window['VVI_RS'].update(rs)
                self.window.refresh()

        if mode == 4:
            cursor.execute("SELECT LRL, URL, ARP, H, AA, APW, AS, RS FROM AAI WHERE username = ?", (self.current_user,))
            row = cursor.fetchone()
            if row is not None:
                self.window['MODES'].Widget.select(1)
                lrl, url, arp, h, aa, apw, as_, rs = row
                self.window['AAI_LRL'].update(lrl)
                self.window['AAI_URL'].update(url)
                self.window['AAI_ARP'].update(arp)
                self.window['AAI_H'].update(h)
                self.window['AAI_AA'].update(aa)
                self.window['AAI_APW'].update(apw)
                self.window['AAI_AS'].update(as_)
                self.window['AAI_RS'].update(rs)
                self.window.refresh()

        sg.popup_quick_message("Current pacemaker parameters")

    def run(self):
        self.window = self.setup_window()
        self.update_images(self.window)

        # flag variable for disk
        connect = False

        # varible to hold port identifier set by user
        port = ""

        while True:
            self.window.refresh()
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                self.window.close()
                return "EXIT"

            if event == "DISCONNECT":
                self.window.disable()
                self.connect_popup(self.window)

            if event == "SETTINGS":
                self.window.close()
                return "SETTINGS"

            if event == "CONNECT":
                if not connect:
                    port = values["PORT"]
                    coms = Connect(port)
                    try:
                        try_port = coms.is_connected()
                    except:
                        try_port = False
                    del (coms)
                    if try_port:
                        connect = True
                        self.window.disable()
                        self.connect_popup(self.window)
            coms = Connect(port)

            # # create object coms to send data to pacemaker through serial

            try:
                try_port = coms.is_connected()
            except:
                try_port = False
            if not try_port:
                if connect:
                    connect = False
                    # update the console and page showing not connected
                    dateTimeObj = datetime.now()
                    timestampStr = dateTimeObj.strftime("%H:%M:%S")
                    self.window.Element('device_name').update("No Device Connected")
                    self.window.Element('STATUS').update("Disconnected")
                    console.append(" Disconnected: " + timestampStr)
                    self.window.Element("CONSOLE").update(console)
                    sg.popup_quick_message("Device Disconnected", text_color="Red")

            if connect:
                # create object coms to send data to pacemaker through serial
                # coms = Connect(port)
                # try:
                #     try_port = coms.is_connected()
                # except:
                #     try_port = False
                # if not try_port:
                #     connect = False
                #     # update the console and page showing not connected
                #     dateTimeObj = datetime.now()
                #     timestampStr = dateTimeObj.strftime("%H:%M:%S")
                #     window.Element('device_name').update("No Device Connected")
                #     window.Element('STATUS').update("Disconnected")
                #     console.append(" Disconnected: " + timestampStr)
                #     window.Element("CONSOLE").update(console)
                #     sg.popup_quick_message("Device Disconnected", text_color="Red")

                conn = sqlite3.connect('pacemaker_settings.db')

                if event == "AOO_SEND": self.aoo_send(values, coms, conn)

                if event == "AOO_LOAD": self.aoo_load(conn)

                if event == "AAI_SEND": self.aai_send(values, coms, conn)

                if event == "AAI_LOAD": self.aai_load(conn)

                if event == "VOO_SEND": self.voo_send(values, coms, conn)

                if event == "VOO_LOAD": self.voo_load(conn)

                if event == "VVI_SEND": self.vvi_send(values, coms, conn)

                if event == "VVI_LOAD": self.vvi_load(conn)

                if event == "IMPORT": self.import_data(coms, conn)

                if event == "START": graph(self.window)

            if not connect:
                sg.popup_quick_message("No Device Connected", text_color="Red")


