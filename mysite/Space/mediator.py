import math
import numpy
from abc import ABC
import traceback

class Mediator(ABC):
    """
    The Mediator interface declares a method used by components to getLocation the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """

    def get_ocation(self, distances):
        """
        :param parser: Float
        :return: {x:Float, y:Float} 
        """
        pass

    def get_message(self, message):
        """
        :param parser: [strings]
        :return: message
        """
        pass

class ConcreteMediator(Mediator):


    def __init__(self, satelite1, satelite2, satelite3):
        self._satelite1 = satelite1
        self._satelite1.mediator = self
        self._satelite2 = satelite2
        self._satelite2.mediator = self
        self._satelite3 = satelite3
        self._satelite3.mediator = self
        self.message = ''


    def get_all_location(self):
        return self._satelite1.get_location() is not None and self._satelite2.get_location() is not None and self._satelite3.get_location() is not None

    def get_all_distance(self):
        return self._satelite1.get_distance() is not None and self._satelite2.get_distance() is not None and self._satelite3.get_distance() is not None

    def get_all_message(self):
        return self._satelite1.get_message() is not None and self._satelite2.get_message() is not None and self._satelite3.get_message() is not None

    def get_location(self):
        """
            :param parser: TSelf instance
            :return: resulting point

        """
        if self.get_all_location() and self.get_all_distance():
            return self.trilateracion(
                self._satelite1.get_location(),
                self._satelite1.get_distance(),
                self._satelite2.get_location(),
                self._satelite2.get_distance(),
                self._satelite3.get_location(),
                self._satelite3.get_distance(),
            )
            
        return {'x':None, 'y':None}


    def get_phrase(self, array1, array2, array3, index):
        """
            :param parser: Three Arrays and one positions index result
            :return: resulting message

        """
        if array1[index] != '':
            return array1[index]
        elif array2[index] != '':
            return array2[index]
        elif array3[index] != '':
            return array3[index]
        else:
            array1.pop(index)
            array2.pop(index)
            array3.pop(index)
            return self.get_phrase(array1, array2, array3, index)



    def get_message(self):
        """
            :param parser: Self instance
            :return: message resultant
        """
        message = ''
        if self.get_all_message():
            size_min_message = min(min(len(self._satelite1.get_message()), len(self._satelite2.get_message())), len(self._satelite3.get_message()))
            for index in list(range(size_min_message-1)):
                message = message+" " + self.get_phrase(self._satelite1.get_message(), self._satelite2.get_message(), self._satelite3.get_message(), index)

        return message
            

    def trilateracion(self, point_a, dist_a, point_b, dist_b, point_c, dist_c):
        """
            :param parser: Point_a Point_b Point_c Distance_a Distance_b Distance_c
            :return: {x:Float, y:Float} Longitude and Latitude
        """
        earthR = 6371
        lat = None
        lon = None
        try:
            xA = earthR *(math.cos(math.radians(point_a['y'])) * math.cos(math.radians(point_a['x'])))
            yA = earthR *(math.cos(math.radians(point_a['y'])) * math.sin(math.radians(point_a['x'])))
            zA = earthR *(math.sin(math.radians(point_a['y'])))

            xB = earthR *(math.cos(math.radians(point_b['y'])) * math.cos(math.radians(point_b['x'])))
            yB = earthR *(math.cos(math.radians(point_b['y'])) * math.sin(math.radians(point_b['x'])))
            zB = earthR *(math.sin(math.radians(point_b['y'])))

            xC = earthR *(math.cos(math.radians(point_c['y'])) * math.cos(math.radians(point_c['x'])))
            yC = earthR *(math.cos(math.radians(point_c['y'])) * math.sin(math.radians(point_c['x'])))
            zC = earthR *(math.sin(math.radians(point_c['y'])))

            P1 = numpy.array([xA, yA, zA])
            P2 = numpy.array([xB, yB, zB])
            P3 = numpy.array([xC, yC, zC])

            #from wikipedia
            #transform to get circle 1 at origin
            #transform to get circle 2 on x axis
            ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
            i = numpy.dot(ex, P3 - P1)
            ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
            ez = numpy.cross(ex,ey)
            d = numpy.linalg.norm(P2 - P1)
            j = numpy.dot(ey, P3 - P1)

            #from wikipedia
            #plug and chug using above values
            x = (pow(dist_a,2) - pow(dist_b,2) + pow(d,2))/(2*d)
            y = ((pow(dist_a,2) - pow(dist_c,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

            # only one case shown here
            z = numpy.sqrt(abs(pow(dist_a,2) - pow(x,2) - pow(y,2)))

            #triPt is an array with ECEF x,y,z of trilateration point
            triPt = P1 + x*ex + y*ey + z*ez

            #convert back to lat/long from ECEF
            #convert to degrees
            lat = math.degrees(math.asin(int(abs(triPt[2]) / earthR)))
            lon = math.degrees(math.atan2(triPt[1],triPt[0]))
        except Exception:
            print(traceback.format_exc())

        return lat, lon