from geopy import distance, point
import time


# college_centre = 13.031009729710282, 77.56534607566735 
# college_edge = 13.030204226341525, 77.5643711284555 
# geofence_radius = 139

# print(check_ifingeofence((13.029882955480707, 77.5643615701495)))
# print(check_ifingeofence((13.030264755587472, 77.56458141118748)))



class Client:
    def __init__(self):
        self.pstate: bool = False
        self.state: bool = None
        self.centre: tuple[float, float] = Client.get_centre()
        self.coordinates: tuple[float, float] = Client.get_current_coordinates()
        self.radius: int = Client.get_radius()
        self.unames: list[str] = Client.get_unames()
        self.geoname: str = Client.get_geoname()

    @property 
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, radius):
        self._radius = radius

    @staticmethod
    def get_radius():
        radius = 139 # placeholder
        # insert radius extraction logic from json payload sent by app
        return radius

    def change_state(self):
        if self.check_if_in_geofence():
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

    @staticmethod
    def get_geoname() -> str:
        #insert geofence name extraction logic from json payload sent by app
        geoname = "Ramaiah Institute of Technology" #placeholder value
        return geoname

    @staticmethod
    def get_centre() -> tuple[float, float]:
        latitude = 13.031009729710282 # placeholder values
        longitude = 77.56534607566735 # placeholder values
        # insert centre extraction logic from json payload sent by app
        return (latitude, longitude)
    
    @staticmethod
    def get_unames() -> list[str]:
        unames = []
        # insert username extraction logic from json payload sent by app
        return unames
    # have not made unames a property because I will not validate it in server-side code. The usernames will be validated by JS in the client-side

    @staticmethod
    def get_current_coordinates() -> tuple[float, float]:
        # insert extraction logic from app payload to the server
        latitude = 13.030510693670998 # placeholder value for latitude: within the geofence so the location polling changes state
        longitude = 77.5653442911208 # placeholder value for longitude: within the geofence so the location polling changes state
        return (latitude, longitude) # returns a coordinates object, used by the client class; a coordinates object is created every 20 seconds by the loop by get_current_coordinates()
    
    def check_if_in_geofence(self) -> bool:
        return distance.distance(point.Point(self.coordinates), point.Point(self.centre)).meters <= self.radius
        

def main():    
    client = Client()
    while True:        
        client.change_state()
        client.trigger()
        time.sleep(20)

if __name__ == "__main__":
    main()

    
    
    