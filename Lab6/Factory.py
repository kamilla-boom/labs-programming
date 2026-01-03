from Circle import Circle
from Square import Square
from Triangle import Triangle
from Group import Group

class Factory:

    def create_shape(self, type_shape):

        if type_shape == "Circle":
            return Circle()
        elif type_shape == "Square":
            return Square()
        elif type_shape == "Triangle":
            return Triangle()
        elif type_shape == "Group":
            return Group()
        else:
            raise ValueError("Invalid shape")
