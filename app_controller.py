from screens.welcome_screen import WelcomeScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.main_screen import MainScreen
from screens.settings_screen import SettingsScreen


# AppController class
class AppController:
    def __init__(self):
        self.current_screen = None

    def run(self):
        # Initialize with the WelcomeScreen
        self.current_screen = WelcomeScreen()

        while True:
            next_screen = self.current_screen.run()

            if next_screen == "LOGIN":
                self.current_screen = LoginScreen()
            elif next_screen == "REGISTER":
                self.current_screen = RegisterScreen()
            elif next_screen == "MAIN":
                self.current_screen = MainScreen()
            elif next_screen == "SETTINGS":
                self.current_screen = SettingsScreen()
            elif next_screen == "WELCOME":
                self.current_screen = WelcomeScreen()
            elif next_screen == "EXIT":
                break  # Exit the application

