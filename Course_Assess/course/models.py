from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone
# Create your models here.
class Course(models.Model):
    dept = models.CharField(max_length=100)
    name = models.CharField(max_length=1000)
    syllabus = models.CharField(max_length=500)
    prof = models.CharField(max_length=100)
    credit = models.IntegerField()
    stars = models.FloatField(null=True)
    year = models.IntegerField(null=True)
    count = models.IntegerField(null=True)

    class Meta:
        unique_together =  ('name', 'prof')

    def __str__(self):
        temp = '{0} - {1}'
        return temp.format(self.name, self.prof)

class Assessment(models.Model):
    course = models.OneToOneField(Course, related_name='course_comments',on_delete=models.CASCADE)
    post = models.ForeignKey(User, related_name='user_comments', on_delete = models.CASCADE)
    star = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    contents = models.TextField(blank=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.star)



