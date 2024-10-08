from datetime import timezone

from django.db import models


class ParsedData(models.Model):
    file_name = models.CharField()
    MPAN_Core = models.CharField(max_length=13)
    validation_status = models.CharField(max_length=1)
    serial_number = models.CharField(max_length=10)
    reading_type = models.CharField(max_length=1)


class RegisterReadings(models.Model):
    meter_id = models.CharField(max_length=2)
    reading_date_time = models.DateTimeField()
    register_reading = models.DecimalField(max_digits=9, decimal_places=1)
    reading_method = models.CharField(max_length=1)
    reading_flag = models.CharField(max_length=1)
    reading_reason_code = models.CharField(max_length=2)
    reading_status = models.CharField(max_length=2)
    site_visit_check_code = models.CharField(max_length=2)
    # One MPAN and serial number can have multiple meter ids and  registries
    mpan = models.ForeignKey(ParsedData, on_delete=models.CASCADE)







