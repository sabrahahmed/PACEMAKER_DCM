from pathlib import Path
import PySimpleGUI as sg
from app_controller import AppController


def main():
    app = AppController()
    app.run()


# CLASS FOR ALL WINDOW SCREENS
# class Screen:
#     def __init__(self):
#         self.window_size = (1280, 720)
#         self.current_user = ""
#         self.current_pass = ""
#
#     def welcome_screen(self):
#
#         # LAUNCH SCREEN IMAGE
#         filename = "images/launch_image.jpg"
#         size = (1280, 630)
#         img = Image.open(filename)
#         img = img.resize(size, resample=Image.BICUBIC)
#
#         sg.theme('DefaultNoMoreNagging')
#
#         layout = Layout()
#         window = sg.Window('Pacemaker DCM Login', layout.welcome(), margins=(0, 0), finalize=True, resizable=False,
#                            size=self.window_size, background_color="Black")
#
#         # Convert im to ImageTk.PhotoImage after window finalized and update image in sg.Image
#         image = ImageTk.PhotoImage(image=img)
#         window['LAUNCH_IMAGE'].update(data=image)
#
#         while True:
#             event, values = window.read()
#
#             if event == sg.WIN_CLOSED:
#                 window.close()
#                 break
#
#             if event == "LOGIN":
#                 window.close()
#                 self.login_screen()
#
#             if event == "REGISTER":
#                 window.close()
#                 self.register_screen()
#
#     def login_screen(self):
#         # LOGIN SCREEN IMAGE
#         filename = "images/login_image.jpg"
#         size = (640, 720)
#         img = Image.open(filename)
#         img = img.resize(size, resample=Image.BICUBIC)
#
#         sg.theme('DefaultNoMoreNagging')
#
#         layout = Layout()
#         window = sg.Window('Pacemaker DCM Login', layout.login(), margins=(0, 0), finalize=True, resizable=False,
#                            size=self.window_size)
#
#         # Convert im to ImageTk.PhotoImage after window finalized
#         image = ImageTk.PhotoImage(image=img)
#         window['LOGIN_IMAGE'].update(data=image)
#
#         # Create an event loop
#         while True:
#             event, values = window.read()
#
#             if event == "Login":
#                 # Check if inputs are empty
#                 if values['USER'] and values['PASS']:
#                     # Check login data in SQLite database
#                     self.current_user = values['USER']
#                     self.current_pass = values['PASS']
#
#                     try:
#                         conn = sqlite3.connect('user_credentials.db')
#                         cursor = conn.cursor()
#
#                         # Retrieve hashed password from database for given username
#                         cursor.execute("SELECT password FROM users WHERE username=?", (self.current_user,))
#                         hashed_password = cursor.fetchone()
#
#                         if hashed_password:
#                             # Verify password against hashed password
#                             if bcrypt.checkpw(self.current_pass.encode('utf-8'), hashed_password[0]):
#                                 conn.close()
#                                 window.close()
#                                 self.main_screen()
#                             else:
#                                 sg.popup_quick_message("Incorrect Password", text_color="Red")
#                         else:
#                             sg.popup_quick_message("Not an active user", text_color="Red")
#
#                     except Exception as e:
#                         sg.popup_quick_message("Error: " + str(e), text_color="Red")
#
#             if event == sg.WIN_CLOSED:
#                 window.close()
#                 break
#
#             if event == "BACK":
#                 window.close()
#                 self.welcome_screen()
#
#     def register_screen(self):
#         # REGISTER SCREEN IMAGE
#         filename = "images/login_image.jpg"
#         size = (640, 720)
#         img = Image.open(filename)
#         img = img.resize(size, resample=Image.BICUBIC)
#
#         sg.theme('DefaultNoMoreNagging')
#
#         layout = Layout()
#
#         window = sg.Window('Pacemaker DCM Registration', layout.register(), margins=(0, 0), finalize=True,
#                            resizable=False, size=self.window_size)
#
#         # Convert im to ImageTk.PhotoImage after window finalized
#         image = ImageTk.PhotoImage(image=img)
#         # update image in sg.Image
#         window['REGISTER_IMAGE'].update(data=image)
#
#         while True:
#             event, values = window.read()
#
#             if event == sg.WIN_CLOSED:
#                 window.close()
#                 break
#             if event == "BACK":
#                 window.close()
#                 self.welcome_screen()
#                 # login()
#             if event == 'Register':
#                 if values['USER'] and values['PASS']:
#                     if values['PASS'] == values['REENTER']:
#                         special_characters = """#$%&'()*!+,-."/:;<=>?@[\]^_`{|}~"""
#
#                         if any(c in special_characters for c in values['USER']):
#                             sg.popup_quick_message("Username cannot contain spaces or special characters",
#                                                    text_color="Red")
#
#                         elif len(values['PASS']) < 8:
#                             sg.popup_quick_message("Password must be at least 8 characters", text_color="Red")
#
#                         else:
#                             self.current_user = values['USER']
#                             self.current_pass = values['PASS']
#
#                             try:
#                                 conn = sqlite3.connect('user_credentials.db')
#                                 cursor = conn.cursor()
#
#                                 cursor.execute("SELECT * FROM users WHERE username=?", (self.current_user,))
#                                 existing_user = cursor.fetchone()
#
#                                 if existing_user:
#                                     sg.popup_quick_message("Already an active user. Please try a new username.",
#                                                            text_color="Red")
#                                 else:
#                                     hashed_password = bcrypt.hashpw(self.current_pass.encode('utf-8'), bcrypt.gensalt())
#
#                                     cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
#                                                    (self.current_user, hashed_password))
#                                     conn.commit()
#
#                                     conn = sqlite3.connect('pacemaker_settings.db')
#                                     cursor = conn.cursor()
#
#                                     cursor.execute("INSERT INTO AAI (username) VALUES (?)", (self.current_user,))
#                                     cursor.execute("INSERT INTO AOO (username) VALUES (?)", (self.current_user,))
#                                     cursor.execute("INSERT INTO VOO (username) VALUES (?)", (self.current_user,))
#                                     cursor.execute("INSERT INTO VVI (username) VALUES (?)", (self.current_user,))
#
#                                     # cursor.execute(f"INSERT INTO {self.current_user} (username) VALUES (?)",
#                                     #                (self.current_user,))
#
#                                     conn.commit()
#                                     conn.close()
#                                     window.close()
#                                     self.main_screen()
#
#                             except Exception as e:
#                                 sg.popup_quick_message("Error: " + str(e), text_color="Red")
#                     else:
#                         sg.popup_quick_message("Passwords do not match.", text_color="Red")
#
#     def main_screen(self):
#         # IMAGE 2
#         filename2 = "images/user_icon.jpg"
#         img2 = Image.open(filename2)
#         img2 = img2.resize((30, 30), resample=Image.BICUBIC)
#
#         # IMAGE 3
#         filename3 = "images/load_image.jpg"
#         img3 = Image.open(filename3)
#         img3 = img3.resize((30, 30), resample=Image.BICUBIC)
#
#         # IMAGE 4
#         filename4 = "images/send_button.jpg"
#         img4 = Image.open(filename4)
#         img4 = img4.resize((30, 30), resample=Image.BICUBIC)
#
#         # IMAGE 5
#         filename5 = "images/start_button.png"
#         img5 = Image.open(filename5)
#         img5 = img5.resize((30, 30), resample=Image.BICUBIC)
#
#         # IMAGE 6
#         filename6 = "images/stop_button.png"
#         img6 = Image.open(filename6)
#         img6 = img6.resize((30, 30), resample=Image.BICUBIC)
#
#         # IMAGE 7
#         filename7 = "images/import_button.png"
#         img7 = Image.open(filename7)
#         img7 = img7.resize((30, 30), resample=Image.BICUBIC)
#
#         sg.theme('Reddit')
#
#         # FOOTER
#         welcome = [
#             [sg.Text("Welcome, " + self.current_user + "!", background_color="Black", text_color="White")]
#         ]
#
#         top_right = [
#             [sg.Image(key='SETTINGS', enable_events=True)],
#         ]
#
#         footer = [
#             [sg.Column(welcome, background_color="Black"),
#              sg.Push(background_color="Black"),
#              sg.Column(top_right, background_color="Black")],
#         ]
#
#         # E-GRAM
#         a_graph = [[sg.Canvas(size=(900, 300), key='CANVAS1')]]
#         v_graph = [[sg.Canvas(size=(900, 300), key='CANVAS2')]]
#
#         electrogram = [
#             [sg.TabGroup(
#                 [[
#                     sg.Tab("Atrial", a_graph, expand_x=True, element_justification="center"),
#                     sg.Tab("Ventricular", v_graph, expand_x=True, element_justification="center"),
#                 ],
#                 ],
#                 tab_location="topleft",
#                 title_color="White",
#                 tab_background_color='Black',
#                 selected_title_color="White",
#                 selected_background_color='#007ad2',
#                 tab_border_width=1,
#                 border_width=0,
#                 size=(900, 300)
#             )
#             ]]
#
#         e_buttons = [
#             [sg.VPush()],
#             [sg.Image(key='START', enable_events=True, pad=(0, 5), tooltip="Start electrogram")],
#             [sg.Image(key='STOP', enable_events=True, pad=(0, 5), tooltip="Stop electrogram")],
#             [sg.Image(key='IMPORT', enable_events=True, pad=(0, 5), tooltip="Import current pacemaker parameters")],
#             [sg.VPush()],
#         ]
#
#         electrogram_buttons = [
#             [sg.TabGroup(
#                 [[sg.Tab("", e_buttons),
#                   ],
#                  ],
#                 tab_location="top",
#                 title_color="White",
#                 tab_background_color='White',
#                 selected_title_color="White",
#                 selected_background_color='White',
#                 tab_border_width=0,
#                 border_width=0,
#                 size=(150, 300),
#             )
#             ]]
#
#         # PACING MODES
#         pacing_mode = Mode()
#
#         modes = [
#             [sg.TabGroup(
#                 [[
#                     sg.Tab("AOO", pacing_mode.AOO(), expand_x=True, element_justification="Center", key="AOO"),
#                     sg.Tab("AAI", pacing_mode.AAI(), expand_x=True, element_justification="Center", key="AAI"),
#                     sg.Tab("VOO", pacing_mode.VOO(), expand_x=True, element_justification="Center", key="VOO"),
#                     sg.Tab("VVI", pacing_mode.VVI(), expand_x=True, element_justification="Center", key="VVI"),
#                     # sg.Tab("AOOR", pacing_mode.AOOR()),
#                     # sg.Tab("AAIR", pacing_mode.AAIR()),
#                     # sg.Tab("VOOR", pacing_mode.VOOR()),
#                     # sg.Tab("VVIR", pacing_mode.VVIR())
#                 ],
#                 ],
#                 key="MODES",
#                 tab_location="topleft",
#                 title_color="White",
#                 tab_background_color='Black',
#                 selected_title_color="White",
#                 selected_background_color='#007ad2',
#                 tab_border_width=0,
#                 border_width=1,
#                 size=(1050, 300),
#                 focus_color="#007ad2"
#             )
#             ]]
#
#         # DEVICE + CONSOLE LEFT TAB
#         tab = [
#             [sg.TabGroup(
#                 [[
#                     sg.Tab("", left_tab(), expand_x=True, element_justification="left", background_color='white'),
#                 ],
#                 ],
#                 tab_location="bottom",
#                 title_color="White",
#                 tab_background_color='White',
#                 selected_title_color="White",
#                 selected_background_color='White',
#                 tab_border_width=0,
#                 border_width=0,
#                 size=(265, 1000),
#             )
#             ]]
#
#         left = [
#             [sg.Column(tab, expand_x=True, element_justification="left")],
#         ]
#
#         right = [
#             [sg.Column(electrogram),
#              sg.Column(electrogram_buttons)],
#             [sg.Column(modes, expand_x=True, element_justification="right")],
#         ]
#
#         layout = [
#             [sg.Column(footer, expand_x=True, element_justification="center", background_color="Black")],
#             [sg.Column(left, background_color="White", expand_x=True, element_justification="left"),
#              sg.VerticalSeparator(pad=(0, 10)),
#              sg.Column(right, background_color="White")]
#         ]
#
#         window = sg.Window('Pacemaker DCM', layout, margins=(0, 0), finalize=True, resizable=False,
#                            size=self.window_size)
#
#         # Convert im to ImageTk.PhotoImage after window finalized
#         image2 = ImageTk.PhotoImage(image=img2)
#         image3 = ImageTk.PhotoImage(image=img3)
#         image4 = ImageTk.PhotoImage(image=img4)
#         image5 = ImageTk.PhotoImage(image=img5)
#         image6 = ImageTk.PhotoImage(image=img6)
#         image7 = ImageTk.PhotoImage(image=img7)
#
#         # update image in sg.Image
#         window['SETTINGS'].update(data=image2)
#         window['START'].update(data=image5)
#         window['STOP'].update(data=image6)
#         window['IMPORT'].update(data=image7)
#
#         window['AOO_LOAD'].update(data=image3)
#         window['AOO_SEND'].update(data=image4)
#
#         window['AAI_LOAD'].update(data=image3)
#         window['AAI_SEND'].update(data=image4)
#
#         window['VOO_LOAD'].update(data=image3)
#         window['VOO_SEND'].update(data=image4)
#
#         window['VVI_LOAD'].update(data=image3)
#         window['VVI_SEND'].update(data=image4)
#
#         # flag variable for disk
#         connect = False
#
#         # varible to hold port identifier set by user
#         port = ""
#
#         while True:
#             window.refresh()
#             event, values = window.read()
#             if event == sg.WIN_CLOSED:
#                 window.close()
#                 break
#             if event == "DISCONNECT":
#                 window.disable()
#                 connect_popup(window)
#
#             if event == "SETTINGS":
#                 window.close()
#                 self.settings_screen()
#
#             if event == "CONNECT":
#                 if connect == False:
#                     port = values["PORT"]
#                     coms = Connect(port)
#                     try:
#                         try_port = coms.is_connected()
#                     except:
#                         try_port = False
#                     del (coms)
#                     if try_port:
#                         connect = True
#                         window.disable()
#                         connect_popup(window)
#
#             # create object coms to send data to pacemaker through serial
#             coms = Connect(port)
#             try:
#                 try_port = coms.is_connected()
#             except:
#                 try_port = False
#             if not try_port:
#                 if connect:
#                     connect = False
#                     # update the console and page showing not connected
#                     dateTimeObj = datetime.now()
#                     timestampStr = dateTimeObj.strftime("%H:%M:%S")
#                     window.Element('device_name').update("No Device Connected")
#                     window.Element('STATUS').update("Disconnected")
#                     console.append(" Disconnected: " + timestampStr)
#                     window.Element("CONSOLE").update(console)
#                     sg.popup_quick_message("Device Disconnected", text_color="Red")
#
#             if not connect:
#                 # create object coms to send data to pacemaker through serial
#                 # coms = Connect(port)
#                 # try:
#                 #     try_port = coms.is_connected()
#                 # except:
#                 #     try_port = False
#                 # if not try_port:
#                 #     connect = False
#                 #     # update the console and page showing not connected
#                 #     dateTimeObj = datetime.now()
#                 #     timestampStr = dateTimeObj.strftime("%H:%M:%S")
#                 #     window.Element('device_name').update("No Device Connected")
#                 #     window.Element('STATUS').update("Disconnected")
#                 #     console.append(" Disconnected: " + timestampStr)
#                 #     window.Element("CONSOLE").update(console)
#                 #     sg.popup_quick_message("Device Disconnected", text_color="Red")
#
#                 conn = sqlite3.connect('pacemaker_settings.db')
#                 cursor = conn.cursor()
#
#                 if event == "AOO_SEND":
#
#                     if values["AOO_LRL"] and values["AOO_URL"] and values["AOO_AA"] and values["AOO_APW"]:
#
#                         if values["AOO_LRL"] < values["AOO_URL"]:
#
#                             AOO_values = (
#                                 values["AOO_LRL"],
#                                 values["AOO_URL"],
#                                 values["AOO_APW"],
#                                 values["AOO_AA"],
#                                 self.current_user,
#                             )
#
#                             # Update the existing row in the "AOO" table for the current user
#                             cursor.execute("UPDATE AOO SET LRL = ?, URL = ?, APW = ?, AA = ? WHERE username = ?",
#                                            AOO_values)
#
#                             conn.commit()
#                             # conn.close()
#
#                             # send parameters and check if they were sent properly
#                             if coms.send_para(2, self.current_user):
#                                 sg.popup_quick_message("AOO inputs sent to pacemaker", text_color="Green")
#                                 console.append(" Sent AOO: " + currentTime())
#                                 window.Element('CONSOLE').update(console)
#                                 window.refresh()
#                             else:
#                                 sg.popup_quick_message("AOO inputs failed to send to pacemaker", text_color="Red")
#                         else:
#                             sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
#                                                    text_color="Red")
#
#                     else:
#                         sg.popup_quick_message("Missing parameters", text_color="Red")
#
#                 if event == "AOO_LOAD":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if data[self.current_user]["AOO"]["LRL"] == "":
#                         sg.popup_quick_message("No previous paramaters saved")
#                     else:
#                         window.Element('AOO_LRL').update(data[self.current_user]["AOO"]["LRL"])
#                         window.Element('AOO_URL').update(data[self.current_user]["AOO"]["URL"])
#                         window.Element('AOO_AA').update(data[self.current_user]["AOO"]["AA"])
#                         window.Element('AOO_APW').update(data[self.current_user]["AOO"]["APW"])
#                         console.append(" Loaded AOO: " + currentTime())
#                         window.Element('CONSOLE').update(console)
#                         window.refresh()
#
#                 if event == "AAI_SEND":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if values["AAI_LRL"] and values["AAI_URL"] and values["AAI_ARP"] and values["AAI_H"] \
#                             and values["AAI_AA"] and values["AAI_APW"] and values["AAI_AS"] and values["AAI_RS"]:
#                         if values["AAI_LRL"] < values["AAI_URL"]:
#
#                             data[self.current_user]["AAI"] = {
#                                 "LRL": values["AAI_LRL"],
#                                 "URL": values["AAI_URL"],
#                                 "ARP": values["AAI_ARP"],
#                                 "PVARP": values["AAI_PVARP"],
#                                 "H": values["AAI_H"],
#                                 "AA": values["AAI_AA"],
#                                 "APW": values["AAI_APW"],
#                                 "AS": values["AAI_AS"],
#                                 "RS": values["AAI_RS"]
#                             }
#
#                             open("data/data.json", "w").write(json.dumps(data, indent=4, separators=(',', ': ')))
#
#                             # send parameters and check if they were sent properly
#                             if coms.send_para(4, self.current_user):
#                                 sg.popup_quick_message("AAI inputs sent to pacemaker", text_color="Green")
#                                 console.append(" Sent AAI: " + currentTime())
#                                 window.Element('CONSOLE').update(console)
#                                 window.refresh()
#                             else:
#                                 sg.popup_quick_message("AAI inputs failed to send to pacemaker", text_color="Red")
#
#                         else:
#                             sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
#                                                    text_color="Red")
#
#                     else:
#                         sg.popup_quick_message("Missing parameters", text_color="Red")
#
#                 if event == "AAI_LOAD":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if data[self.current_user]["AAI"]["LRL"] == "":
#                         sg.popup_quick_message("No previous paramaters saved", text_color="Red")
#                     else:
#                         window.Element('AAI_LRL').update(data[self.current_user]["AAI"]["LRL"])
#                         window.Element('AAI_URL').update(data[self.current_user]["AAI"]["URL"])
#                         window.Element('AAI_ARP').update(data[self.current_user]["AAI"]["ARP"])
#                         window.Element('AAI_PVARP').update(data[self.current_user]["AAI"]["PVARP"])
#                         window.Element('AAI_H').update(data[self.current_user]["AAI"]["H"])
#                         window.Element('AAI_AA').update(data[self.current_user]["AAI"]["AA"])
#                         window.Element('AAI_APW').update(data[self.current_user]["AAI"]["APW"])
#                         window.Element('AAI_AS').update(data[self.current_user]["AAI"]["AS"])
#                         window.Element('AAI_RS').update(data[self.current_user]["AAI"]["RS"])
#                         console.append(" Loaded AAI: " + currentTime())
#                         window.Element('CONSOLE').update(console)
#                         window.refresh()
#
#                 if event == "VOO_SEND":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if values["VOO_LRL"] and values["VOO_URL"] and values["VOO_VA"] and values["VOO_VPW"]:
#                         if values["VOO_LRL"] < values["VOO_URL"]:
#
#                             data[self.current_user]["VOO"] = {
#                                 "LRL": values["VOO_LRL"],
#                                 "URL": values["VOO_URL"],
#                                 "VA": values["VOO_VA"],
#                                 "VPW": values["VOO_VPW"]
#                             }
#
#                             open("data/data.json", "w").write(json.dumps(data, indent=4, separators=(',', ': ')))
#
#                             # send parameters and check if they were sent properly
#                             if coms.send_para(1, self.current_user):
#                                 sg.popup_quick_message("VOO inputs sent to pacemaker", text_color="Green")
#                                 console.append(" Sent VOO: " + currentTime())
#                                 window.Element('CONSOLE').update(console)
#                                 window.refresh()
#                             else:
#                                 sg.popup_quick_message("VOO inputs failed to send to pacemaker", text_color="Red")
#
#                         else:
#                             sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
#                                                    text_color="Red")
#
#                     else:
#                         sg.popup_quick_message("Missing parameters", text_color="Red")
#
#                 if event == "VOO_LOAD":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if data[self.current_user]["VOO"]["LRL"] == "":
#                         sg.popup_quick_message("No previous paramaters saved", text_color="Red")
#                     else:
#                         window.Element('VOO_LRL').update(data[self.current_user]["VOO"]["LRL"])
#                         window.Element('VOO_URL').update(data[self.current_user]["VOO"]["URL"])
#                         window.Element('VOO_VA').update(data[self.current_user]["VOO"]["VA"])
#                         window.Element('VOO_VPW').update(data[self.current_user]["VOO"]["VPW"])
#                         console.append(" Loaded VOO: " + currentTime())
#                         window.Element('CONSOLE').update(console)
#                         window.refresh()
#
#                 if event == "VVI_SEND":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if values["VVI_LRL"] and values["VVI_URL"] and values["VVI_VRP"] and values["VVI_H"] \
#                             and values["VVI_VA"] and values["VVI_VPW"] and values["VVI_VS"] and values["VVI_RS"]:
#
#                         if values["VVI_LRL"] < values["VVI_URL"]:
#
#                             data[self.current_user]["VVI"] = {
#                                 "LRL": values["VVI_LRL"],
#                                 "URL": values["VVI_URL"],
#                                 "VRP": values["VVI_VRP"],
#                                 "H": values["VVI_H"],
#                                 "VA": values["VVI_VA"],
#                                 "VPW": values["VVI_VPW"],
#                                 "VS": values["VVI_VS"],
#                                 "RS": values["VVI_RS"]
#                             }
#
#                             open("data/data.json", "w").write(json.dumps(data, indent=4, separators=(',', ': ')))
#
#                             # send parameters and check if they were sent properly
#                             if coms.send_para(3, self.current_user):
#                                 sg.popup_quick_message("VVI inputs sent to pacemaker", text_color="Green")
#                                 console.append(" Sent VVI: " + currentTime())
#                                 window.Element('CONSOLE').update(console)
#                                 window.refresh()
#                             else:
#                                 sg.popup_quick_message("VVI inputs failed to send to pacemaker", text_color="Red")
#
#                         else:
#                             sg.popup_quick_message("Lower Rate Limit must be smaller than Upper Rate Limit",
#                                                    text_color="Red")
#                     else:
#                         sg.popup_quick_message("Missing parameters", text_color="Red")
#
#                 if event == "VVI_LOAD":
#
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#
#                     if data[self.current_user]["VVI"]["LRL"] == "":
#                         sg.popup_quick_message("No previous paramaters saved")
#                     else:
#                         window.Element('VVI_LRL').update(data[self.current_user]["VVI"]["LRL"])
#                         window.Element('VVI_URL').update(data[self.current_user]["VVI"]["URL"])
#                         window.Element('VVI_VRP').update(data[self.current_user]["VVI"]["VRP"])
#                         window.Element('VVI_H').update(data[self.current_user]["VVI"]["H"])
#                         window.Element('VVI_VA').update(data[self.current_user]["VVI"]["VA"])
#                         window.Element('VVI_VPW').update(data[self.current_user]["VVI"]["VPW"])
#                         window.Element('VVI_VS').update(data[self.current_user]["VVI"]["VS"])
#                         window.Element('VVI_RS').update(data[self.current_user]["VVI"]["RS"])
#                         console.append(" Loaded VVI: " + currentTime())
#                         window.Element('CONSOLE').update(console)
#                         window.refresh()
#
#                 if event == "START":
#                     graph(window)
#
#                 if event == "IMPORT":
#                     f = open("data/data.json", "r+")
#                     data = json.load(f)
#                     mode = coms.rqst_para(self.current_user)
#                     if mode == 1:
#                         window['MODES'].Widget.select(2)
#                         window['VOO_LRL'].update(data[self.current_user]["VOO"]["LRL"])
#                         window['VOO_URL'].update(data[self.current_user]["VOO"]["URL"])
#                         window['VOO_VA'].update(data[self.current_user]["VOO"]["VA"])
#                         window['VOO_VPW'].update(data[self.current_user]["VOO"]["VPW"])
#                         window.refresh()
#
#                     if mode == 2:
#                         window['MODES'].Widget.select(0)
#                         window['AOO_LRL'].update(data[self.current_user]["AOO"]["LRL"])
#                         window['AOO_URL'].update(data[self.current_user]["AOO"]["URL"])
#                         window['AOO_AA'].update(data[self.current_user]["AOO"]["AA"])
#                         window['AOO_APW'].update(data[self.current_user]["AOO"]["APW"])
#                         window.refresh()
#
#                     if mode == 3:
#                         window['MODES'].Widget.select(3)
#                         window['VVI_LRL'].update(data[self.current_user]["VVI"]["LRL"])
#                         window['VVI_URL'].update(data[self.current_user]["VVI"]["URL"])
#                         window['VVI_VRP'].update(data[self.current_user]["VVI"]["VRP"])
#                         window['VVI_H'].update(data[self.current_user]["VVI"]["H"])
#                         window['VVI_VA'].update(data[self.current_user]["VVI"]["VA"])
#                         window['VVI_VPW'].update(data[self.current_user]["VVI"]["VPW"])
#                         window['VVI_VS'].update(data[self.current_user]["VVI"]["VS"])
#                         window['VVI_RS'].update(data[self.current_user]["VVI"]["RS"])
#                         window.refresh()
#
#                     if mode == 4:
#                         window['MODES'].Widget.select(1)
#                         window['AAI_LRL'].update(data[self.current_user]["AAI"]["LRL"])
#                         window['AAI_URL'].update(data[self.current_user]["AAI"]["URL"])
#                         window['AAI_ARP'].update(data[self.current_user]["AAI"]["ARP"])
#                         window['AAI_H'].update(data[self.current_user]["AAI"]["H"])
#                         window['AAI_AA'].update(data[self.current_user]["AAI"]["AA"])
#                         window['AAI_APW'].update(data[self.current_user]["AAI"]["APW"])
#                         window['AAI_AS'].update(data[self.current_user]["AAI"]["AS"])
#                         window['AAI_RS'].update(data[self.current_user]["AAI"]["RS"])
#                         window.refresh()
#
#                     sg.popup_quick_message("Current pacemaker parameters")
#
#             if not connect:
#                 sg.popup_quick_message("No Device Connected", text_color="Red")
#
#     def settings_screen(self):
#         # IMAGE SETTINGS
#         filename = "images/back_button.png"
#         size = (30, 30)
#         img = Image.open(filename)
#         img = img.resize(size, resample=Image.BICUBIC)
#
#         sg.theme('Reddit')
#
#         top_left = [
#             [sg.Image(key='IMAGE', enable_events=True)]
#         ]
#
#         buttons = [
#             [sg.Button("Sign Out", key="SIGN-OUT")],
#             [sg.Button("Delete Account", button_color="Black", key="DELETE")],
#             [sg.InputText(password_char="*", key="PASS", size=(30, 40), do_not_clear=False)],
#             [sg.Text("Reenter password to delete account", font=('Courier New', 10, 'bold'))],
#         ]
#
#         utility = [
#             [sg.Text("Application Version: 2.70", font=('Courier New', 10, 'normal'))],
#             [sg.Text("Pacemaker Serial Number: H00140", font=('Courier New', 10, 'normal'))],
#             [sg.Text("Institution: McMaster University", font=('Courier New', 10, 'normal'))]
#         ]
#
#         layout = [
#             [sg.Column(top_left, element_justification="left", expand_x=True)],
#             [sg.VPush()],
#             [sg.Column(buttons, element_justification="center", expand_x=True, expand_y=True)],
#             [sg.VPush()],
#             [sg.Column(utility, element_justification="center", expand_x=True, expand_y=True)],
#         ]
#
#         window = sg.Window('Pacemaker DCM User Settings', layout, margins=(0, 0), finalize=True, resizable=False,
#                            size=self.window_size)
#
#         # Convert im to ImageTk.PhotoImage after window finalized
#         image = ImageTk.PhotoImage(image=img)
#
#         # update image in sg.Image
#         window['IMAGE'].update(data=image)
#
#         while True:
#             event, values = window.read()
#             if event == sg.WIN_CLOSED:
#                 window.close()
#                 break
#             if event == "SIGN-OUT":
#                 window.close()
#                 self.welcome_screen()
#
#             if event == "DELETE":
#                 if values['PASS'] == self.current_pass:
#                     try:
#                         conn = sqlite3.connect('user_credentials.db')
#                         cursor = conn.cursor()
#
#                         cursor.execute("DELETE FROM users WHERE username=?", (self.current_user,))
#                         conn.commit()
#
#                         conn = sqlite3.connect('pacemaker_settings.db')
#                         cursor = conn.cursor()
#
#                         cursor.execute("DELETE FROM AAI WHERE username=?", (self.current_user,))
#                         cursor.execute("DELETE FROM AOO WHERE username=?", (self.current_user,))
#                         cursor.execute("DELETE FROM VOO WHERE username=?", (self.current_user,))
#                         cursor.execute("DELETE FROM VVI WHERE username=?", (self.current_user,))
#
#                         conn.commit()
#                         conn.close()
#                         sg.popup_quick_message("Account deleted", text_color="Red")
#                         sleep(2)
#                         window.close()
#                         self.welcome_screen()
#
#                     except Exception as e:
#                         sg.popup_quick_message("Error: " + str(e), text_color="Red")
#
#                 else:
#                     sg.popup_quick_message("Incorrect Password", text_color="Red")
#             if event == "IMAGE":
#                 window.close()
#                 self.main_screen()


# CONNECTION TO PACEMAKER POP-UP

# RUN CODE
if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd()
    # create the settings object and use ini format
    settings = sg.UserSettings(
        path=SETTINGS_PATH, filename="config.ini", use_config_file=True, convert_bools_and_none=True
    )
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    main()
