import sys
import requests

from PyQt5.QtWidgets import QApplication,  QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel('Enter city name:',self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.weather_label = QLabel('', self)
        self.description = QLabel('', self)
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle('Weather App')
        self.setGeometry(100, 100, 400, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.weather_label)
        layout.addWidget(self.description)

       
        self.setLayout(layout)
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        
        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.weather_label.setObjectName('weather_label')
        self.description.setObjectName('description')

        self.setStyleSheet("""
            Qlabel,QPushButton {
                font-family: Arial, sans-serif;
                font-size: 20px;
                color: #333;
            }
            QLabel#city_label {
                font-weight: bold;
                font-size: 24px;
            }
            QLineEdit#city_input {
                font-size: 16px;
                padding: 5px;
            }
            QPushButton#get_weather_button {
                background-color: #4CAF50;
                font-weight: bold;
            }
            QLabel#weather_label{
                font-size: 45px;
            }
            QLabel#description {
                font-size: 20px;
            }
                           """)
        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        api_key = "c967ded808f51a850f0e4574d3aaa556"
        city = self.city_input.text()
        url= f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            data =  response.json()
        
            if data['cod'] == 200:
                 self.display_weather(data)

        except requests.exceptions.HTTPError :
            match response.status_code:
                case 400:
                    self.display_error("Bad Request: Please check the city name.")
                case 401:
                    self.display_error("Unauthorized: Invalid API key.")
                case 403:
                    self.display_error("Forbidden: Access denied.")
                case 404:
                    self.display_error("City not found. Please check the name.")
                case 500:
                    self.display_error("Internal Server Error. Please try again later.")
                case 502:
                    self.display_error("Bad Gateway. Please try again later.")
                case 503:
                    self.display_error("Service Unavailable. Please try again later.")
                case 504:
                    self.display_error("Gateway Timeout. Please try again later.")
                case _:
                    self.display_error("An unexpected error occurred.")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error: Please check your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out. Please try again later.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects. Please check the URL.")
        except requests.exceptions.RequestException as e:
            self.display_error(str(e))
        
    

    def display_error(self, message):
        self.weather_label.setStyleSheet("color: red; font-size: 24px;")
        self.weather_label.setText("Error")
        self.description.setText(message)
    
    def display_weather(self,data):
        
        self.weather_label.setText(f"{round(data['main']['temp'] - 273.15)} C")
        if data['main']['temp'] < 298.15:
            self.weather_label.setStyleSheet("color: blue; font-size:60px;")
        else:
            self.weather_label.setStyleSheet("color: orange; font-size: 60px;")
        self.description.setStyleSheet("color: black; font-size: 45px;")
        self.description.setText(data['weather'][0]['description'].capitalize())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
