from geopy import distance, point
import time
import telebot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
nikbot = telebot.TeleBot(TOKEN)


# college_centre = 13.031009729710282, 77.56534607566735 
# college_edge = 13.030204226341525, 77.5643711284555 
# geofence_radius = 139

# print(check_ifingeofence((13.029882955480707, 77.5643615701495)))
# print(check_ifingeofence((13.030264755587472, 77.56458141118748)))



class Client:
    def __init__(self, request_body: dict = None):
        if request_body is None:
            raise ValueError("Request body not supplied")

        self.name = request_body.get('name')
        self.pstate: bool = False
        self.state: bool | None = None
        self.centre: tuple[float, float] = request_body.get('center_coordinates')
        self.coordinates: tuple[float, float] = request_body.get('curr_coordinates')
        self.radius: int = request_body.get('radius')
        self.chat_ids: list[str] = request_body.get('chat_ids')
        self.geoname: str = request_body.get('geoname')

    def change_state(self) -> None:
        if self.check_if_in_geofence():
            self.state = True
            print("State True: inside geofence") 
        else: 
            self.state = False

    def trigger(self) -> None:
        if self.pstate != self.state:
            self.notify()
            self.pstate = self.state
        else:
            pass

    def check_if_in_geofence(self) -> bool:
        return distance.distance(point.Point(self.coordinates), point.Point(self.centre)).meters <= self.radius
    
    def notify(self) -> None:
        message = f"{self.name} has {'entered' if self.state else 'exited'} {self.geoname}"
        for chatid in self.chat_ids:
            try:                
                nikbot.send_message(chatid, message)
            except telebot.apihelper.ApiTelegramException:
                continue # might filter uninitiated chatIDs in client side later


# placeholder main: to be implemented in server
def main():    
    client = Client()
    while True:        
        client.change_state()
        client.trigger()
        time.sleep(20)


if __name__ == "__main__":
    main()
