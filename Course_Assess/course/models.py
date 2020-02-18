from django.db import models

# Create your models here.
class Course(models.Model):
    dept = models.CharField(max_length=100)
    name = models.CharField(max_length=1000)
    syllabus = models.CharField(max_length=500)
    prof = models.CharField(max_length=100)
    credit = models.IntegerField()
    stars = models.FloatField(null=True)
    year = models.IntegerField()

    def __str__(self):
        return self.name
