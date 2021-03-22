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
        :return: Float, Float
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
        """

        :return: Bool
        """
        return self._satelite1.get_location() is not None and self._satelite2.get_location() is not None and self._satelite3.get_location() is not None

    def get_all_distance(self):
        return self._satelite1.get_distance() is not None and self._satelite2.get_distance() is not None and self._satelite3.get_distance() is not None

    def get_all_message(self):
        return self._satelite1.get_message() is not None and self._satelite2.get_message() is not None and self._satelite3.get_message() is not None

    def get_location(self):
        """
            :param parser: Self instance
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
            
        return None, None


    def get_phrase(self, array1, array2, array3, index):
        """
            :param parser: Three Arrays and one positions index result
            :return: resulting message partial

        """
        try:
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
        except Exception:
            return None



    def get_message(self):
        """
            :param parser: Self instance
            :return: message resultant complete
        """
        message = ''
        data_message = None
        if self.get_all_message():

            size_min_message = min(min(len(self._satelite1.get_message()), len(self._satelite2.get_message())), len(self._satelite3.get_message()))
            size_max_message = max(max(len(self._satelite1.get_message()), len(self._satelite2.get_message())),
                                   len(self._satelite3.get_message()))
            if len(self._satelite1.get_message()) == size_max_message and self._satelite1.get_message()[0]=='':
                message_satelite = self._satelite1.get_message()
                self._satelite1.set_message(message_satelite[1:])
            if len(self._satelite2.get_message()) == size_max_message and self._satelite2.get_message()[0]=='':
                message_satelite = self._satelite2.get_message()
                self._satelite2.set_message(message_satelite[1:])
            if len(self._satelite3.get_message()) == size_max_message and self._satelite3.get_message()[0] == '':
                message_satelite = self._satelite3.get_message()
                self._satelite3.set_message(message_satelite[1:])
            for index in list(range(size_min_message)):
                data_message = self.get_phrase(self._satelite1.get_message(), self._satelite2.get_message(), self._satelite3.get_message(), index)
                if data_message is not None:
                    message = message+" " + data_message
                else:
                    break

        return message[1:] if message != '' else None
            

    def trilateracion(self, point_a, dist_a, point_b, dist_b, point_c, dist_c):
        """
            :param parser: Point_a Point_b Point_c Distance_a Distance_b Distance_c
            :return: Float, Float Longitude and Latitude
        """

        """se localiza el dispositivo por medio de las
           fuerzas de las senales captadas y de la ubicacion de
           las antenas
           Documentacion http://cecilia-urbina.blogspot.com/2013/05/geolocalizacion-por-trilateracion.html
            """
        x =None
        y = None
        d = 3
        i = 2.5
        j = -4
        # se definen las coordenadas de la Antena A
        ax = point_a['x']
        ay = point_a['y']
        # se define la cobertura Antena A
        ar = dist_a
        # se definen las coordenadas de la Antena B
        bx = point_b['x']
        by = point_b['y']
        # se define la cobertura Antena B
        br = dist_b
        # se definen las coordenadas de la Antena C
        cx = point_c['x']
        cy = point_c['y']
        # se define la cobertura de la Antena c
        cr = dist_c
        # se localiza la ubicacion del receptor
        try:
            x = (ar ** 2 - br ** 2 + d ** 2) / float((2 * d))
            y = ((ar ** 2 - br ** 2 + i ** 2 + j ** 2) / (2 * j)) - ((float(i / j)) * x)
        except Exception:
            print(traceback.format_exc())
        return x, y
