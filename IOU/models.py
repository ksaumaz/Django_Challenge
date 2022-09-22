from django.db import models
from django.forms import ValidationError
from django.core.validators import RegexValidator

class User(models.Model):
	name = models.CharField(max_length=50, primary_key=True, validators=[RegexValidator(r'^[a-zA-Z ]*$', 'Only characters are allowed.')])

	def __str__(self):
		return self.name
		
	def save(self, *args, **kwargs):
		self.full_clean()
		super(User, self).save(*args, **kwargs)
	
	def clean(self):
		self.name = self.name.title()
		if User.objects.filter(name__iexact=self.name).exists():
			raise ValidationError('User already exists')

def validate_iou_amount(value):
	if value > 0:
		return value
	else:
		raise ValidationError("Amount must be greater than 0")

class IOU(models.Model):
	lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lender')
	borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrower')
	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[validate_iou_amount])

	def __str__(self):
		return '{} owes {} {}'.format(self.borrower, self.lender, self.amount)

	def clean(self):
		if self.lender == self.borrower:
			raise ValidationError("Lender and borrower cannot be the same")

	def save(self, *args, **kwargs):
		self.full_clean()
		return super(IOU, self).save(*args, **kwargs)