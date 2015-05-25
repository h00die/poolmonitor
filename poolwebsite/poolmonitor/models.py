from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

class Sensor(models.Model):
    """
        Each sensor, since we can have multiple (pool, hot tub, fridge etc)
    """
    readingChoices = (
        ('Temp', 'Temperature'),
        ('pH', 'Acidity')
    )
    readingUnits = (
        ('F', 'Fahrenheit'),
        ('C', 'Celsius')
    )

    description_text     = models.CharField('Sensor Description', max_length=255)
    file_system_location = models.CharField('File System location of Sensor in /sys/bus/w1/devices/', max_length=50, default='28-nnnnn',
                                            help_text="To determine your device run 'ls /sys/bus/w1/devices' and look for items with 28- in their name",
                                            primary_key=True)
    polling_interval     = models.IntegerField('Frequency to check temperature in minutes', default=15)
    location_image       = models.ImageField('Optional image of location (possible future implementation)', blank=True)
    reading_type         = models.CharField('Reading Type', choices=readingChoices, max_length=4)
    reading_units        = models.CharField('Reading Measurement Units', choices=readingUnits, max_length=2)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'sensor_file_system_location': self.file_system_location})

    def __str__(self):
        return "%s (%s)" %(self.description_text, self.file_system_location)
    
class Reading(models.Model):
    """
        A reading from the sensor (ie temperature)
    """

    reading      = models.IntegerField('Reading Value')
    reading_date = models.DateTimeField('Reading Date', default=timezone.now)
    sensor       = models.ForeignKey(Sensor)
    
    def __str__(self):
        return str(self.reading)

    class Meta:
        get_latest_by = "reading_date"