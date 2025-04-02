from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .yazee import dice

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title	

class Roll(models.Model):
 	roll = models.CharField(max_length=100)
#	side = models.CharField(max_length=100)
# 	content = models.TextField()
# 	author = models.ForeignKey(User, on_delete=models.CASCADE)

 	def __str__(self):
 		return self.roll