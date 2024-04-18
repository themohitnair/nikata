from geopy import distance, point
from coordinates import Coordinates


# college_centre = 13.031009729710282, 77.56534607566735 
# college_edge = 13.030204226341525, 77.5643711284555 
# geofence_radius = 139

# print(check_ifingeofence((13.029882955480707, 77.5643615701495)))
# print(check_ifingeofence((13.030264755587472, 77.56458141118748)))



class Client:
    def __init__(self):
        self.pstate = False
        self.state: bool = None
        self.coordinates = Coordinates(Coordinates.get_coordinates())

    def change_state(self):
        if self.coordinates.check_if_in_geofence():
            self.state = True
        else: 
            self.state = False

    def trigger(self):
        if self.pstate != self.state:
            # notify action
            self.pstate = self.state
        else:
            pass
        

    
    
    