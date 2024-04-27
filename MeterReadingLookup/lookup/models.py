
from django.db import models


class ParsedData(models.Model):
    file_name = models.CharField()
    MPAN_Core = models.CharField(max_length=13)
    validation_status = models.CharField(max_length=1)
    serial_number = models.CharField(max_length=10)
    reading_status = models.CharField(max_length=1)
    meter_id = models.CharField(max_length=2)
    reading_date_time = models.DateTimeField()
    register_reading = models.DecimalField(max_digits=9, decimal_places=1)
    reading_method = models.CharField(max_length=1)
    reading_flag = models.CharField(max_length=1)


