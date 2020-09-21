from django.db import models

class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True)
	valid_from = models.DateField()
	valid_to = models.DateField()
	active = models.BooleanField()

	def __str__(self):
		return self.code
