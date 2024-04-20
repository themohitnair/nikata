from geopy import distance, point
from coordinates import Coordinates
import time


# college_centre = 13.031009729710282, 77.56534607566735 
# college_edge = 13.030204226341525, 77.5643711284555 
# geofence_radius = 139

# print(check_ifingeofence((13.029882955480707, 77.5643615701495)))
# print(check_ifingeofence((13.030264755587472, 77.56458141118748)))



class Client:
    def __init__(self):
        self.pstate = False
        self.state: bool = None
        self.coordinates = Coordinates.get_current_coordinates()
        self.radius = Client.get_radius()
        self.unames = Client.get_unames()

    @property 
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radius):
        if radius <= 1500000:
            self._radius = radius
        else:
            raise ValueError("radius is out of valid range (1.5 million meters)") #1.5 million meters is an approximation of the half of the East-West extent of the Republic of India lol
    # Note to server-side coder: This validation of radius is not a good practice because it is being done in the server side and I will be removing this validation and transferring it to the client-side JS functions.

    @classmethod
    def get_radius():
        radius = 139 
        # insert radius extraction logic from json payload sent by app
        return radius

    def change_state(self, centre: tuple[float, float], radius: float):
        if self.coordinates.check_if_in_geofence(centre, radius):
            self.state = True
            print("State True: inside geofence") 
        else: 
            self.state = False

    def trigger(self):
        if self.pstate != self.state:
            print("notify") # notification function (telegram part)
            self.pstate = self.state
        else:
            pass
    
    @classmethod
    def get_unames():
        unames = []
        # insert username extraction logic from json payload sent by app
        return unames
    # have not made unames a property because I will not validate it in server-side code. The usernames will be validated by JS in the client-side
        

def main():    
    client = Client()
    while True:        
        client.change_state(client.coordinates.coordinates, client.radius)
        client.trigger()
        time.sleep(20)

if __name__ == "__main__":
    main()

    
    
    