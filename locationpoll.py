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

    def change_state(self, centre: tuple[float, float], radius: float):
        if self.coordinates.check_if_in_geofence(centre, radius):
            self.state = True
            print("State True: inside geofence")
        else: 
            self.state = False

    def trigger(self):
        if self.pstate != self.state:
            print("notify")
            self.pstate = self.state
        else:
            pass
        
def main():    
    client = Client()
    while True:        
        client.change_state(client.coordinates.coordinates, 139)
        client.trigger()
        time.sleep(10)

if __name__ == "__main__":
    main()

    
    
    