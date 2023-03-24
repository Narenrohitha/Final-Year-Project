from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Department(models.Model):
	dept_name=models.CharField(max_length=20,null=False)
	def __str__(self):
		return self.dept_name
class Employee(models.Model):
	user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	phone=models.PositiveIntegerField(null=False)
	qualification=models.CharField(max_length=20)
	address=models.TextField(max_length=100)
	role=models.CharField(max_length=25)
	dept=models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
	leader=models.CharField(max_length=25)
	profile=models.ImageField(upload_to ='profile/')
	doj=models.DateField()
	salary=models.PositiveIntegerField()
	status=models.PositiveIntegerField(default=0)
	def __str__(self):
		return self.user.username
class Shift(models.Model):
	shiftname=models.CharField(max_length=20,null=True)
	starttime=models.TimeField()
	endtime=models.TimeField()
	def __str__(self):
		return self.shiftname
class Rewards(models.Model):
	rewardname=models.CharField(max_length=20,null=False)
	rewardtype=models.CharField(max_length=20,null=False)
	rewardbenifit=models.CharField(max_length=20,null=False)
	point=models.PositiveIntegerField(default=0)
	valid_to=models.DateField(auto_now_add=True)
	def __str__(self):
		return self.rewardname
class Attendance(models.Model):
	employee=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	shift=models.ForeignKey(Shift, null=True, on_delete=models.CASCADE)
	intime=models.TimeField(auto_now_add=True)
	outtime=models.TimeField(default=0)
	status=models.PositiveIntegerField()
	show=models.PositiveIntegerField(default=0)
	def __str__(self):
		return self.employee.username
class Emprewards(models.Model):
	employee=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	reason=models.CharField(max_length=200,null=False)
	description=models.TextField(max_length=150)
	proff=models.FileField(upload_to='proofs/')
	status=models.PositiveIntegerField(default=0)
	createdate=models.DateField(auto_now_add=True)
	def __str__(self):
		return self.employee.username
class Challenges(models.Model):
	creator=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	employee=models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
	job=models.CharField(max_length=200,null=False)
	startdate=models.DateField(auto_now_add=True)
	enddate=models.DateField()
	status=models.PositiveIntegerField(default=0)
	def __str__(self):
		return self.creator
class Points(models.Model):
	employee=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
	points=models.PositiveIntegerField()
	def __str__(self):
		return self.employee.username
class makeawards(models.Model):
	awards=models.ForeignKey(Rewards, null=True,on_delete=models.CASCADE)
	employee=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
	def __self__(self):
		return self.User.username
class Createshift(models.Model):
	employee=models.ForeignKey(Employee,null=True,on_delete=models.CASCADE)
	shift=models.ForeignKey(Shift,null=True,on_delete=models.CASCADE)
	def __self__(self):
		return self.employee.User.username
