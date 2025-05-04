import timeit
class Coordinate:
    def __init__(self, lat: float, long: float) -> None:
        self._latitude = self._longitude = None
        self.latitude = lat
        self.longitude = long

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, lat_value: float) -> None:
        if lat_value not in range(-90, 90 + 1):
            raise ValueError(f"{lat_value} is an invalid value for latitude")
        self._latitude = lat_value

    @property 
    def longitude(self) -> float: 
        return self._longitude

    @longitude.setter
    def longitude(self, long_value: float) -> None:
        if long_value not in range(-180, 180 + 1):
            raise ValueError(f"{long_value} is an invalid value for longitude")
        self._longitude = long_value

class BareCoordinates:
    def __init__(self, lat: float, long: float) -> None:
        self._latitude = self._longitude = None
        self.latitude = lat
        self.longitude = long

def create_coord_1():
    x = BareCoordinates(82, 10)
    return x
def create_coord_2():
    y = Coordinate(50, 10)
    return y
if __name__ == "__main__":
    code_without_prop = timeit.timeit(create_coord_1, number=1000)
    print(f"Code without properties: {code_without_prop:.6f} seconds")
    code_with_prop = timeit.timeit(create_coord_2, number=1000)
    print(f"Code with properties: {code_with_prop:.6f} seconds")
    print(f"Properties impact on performance: {(code_with_prop/code_without_prop):.02f} slower",)
