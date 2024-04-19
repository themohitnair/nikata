from geopy import distance, point

class Coordinates:
    def __init__(self, latitude: float, longitude: float):
        self.coordinates = (latitude, longitude)

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

    def check_if_in_geofence(self, centre_coordinates: tuple[float, float], radius: float) -> bool:
        return distance.distance(point.Point(self.coordinates), point.Point(centre_coordinates)).meters <= radius
    
    @classmethod
    def get_current_coordinates(cls):
        return cls(13.032, 77.567)