from geopy.point import Point
from geopy.distance import distance


college_centre = 13.031009729710282, 77.56534607566735 
# college_edge = 13.030204226341525, 77.5643711284555 
geofence_radius = 139

state = False

def check_ifingeofence(coordinates: tuple[float, float]):
    if distance(Point(coordinates), Point(college_centre)).meters <= 139:
        return True
    else: 
        return False
    
def change_state_and_notify
    
# print(check_ifingeofence((13.029882955480707, 77.5643615701495)))
# print(check_ifingeofence((13.030264755587472, 77.56458141118748)))