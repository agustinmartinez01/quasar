from django.db import models
from django.contrib.postgres.fields import JSONField
from django_extensions.db.fields import SlugField
# Create your models here.
class Satelite(models.Model):
    """
    Model entitie Satelite
    """
    slug = SlugField(
        db_index=True,
        unique=True,
        blank=True
        )
    name = models.CharField(
        null=False, 
        max_length=100,
        default=''
        )
    _distance = models.FloatField(null=False, default=0.0)
    _latitude =  models.FloatField(null=True)
    _longitude =   models.FloatField(null=True)
    _message = JSONField(default=list, blank=True, null=True)


    def set_message(self, message_input):
        self.message = message_input

    
    def set_point(self, latitude, _longitude):
        self._latitude = latitude
        self._longitude = _longitude

    def set_name(self, name_input):
        self.name = name_input

    def set_distance(self, distance):
        self._distance = distance

    def get_distance(self):
        return self._distance

    def get_location(self):
        if self._latitude!=0.0 and self._longitude!=0.0:
            return {'x':self._longitude, 'y': self._latitude}
        return None
        
    def get_message(self):
        return self._message