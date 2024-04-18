from geopy import distance, point

class Coordinates:
    def __init__(self):
        self.coordinates = None

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value: tuple[float, float]):
        latitude, longitude = value
        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
            self._coordinates = (latitude, longitude)
        else:
            raise ValueError("Latitude or longitude is out of valid range")

    def check_if_in_geofence(self, other_coordinates: tuple[float, float], radius: float) -> bool:
        return distance.distance(point.Point(self.coordinates), point.Point(other_coordinates)).meters <= radius
    
    @staticmethod
    def get_coordinates():
        ...
        return (13.032, 77.567)