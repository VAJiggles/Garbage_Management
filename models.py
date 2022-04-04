from django.db import models


class user_details(models.Model):
	userProfilePicture = models.ImageField(upload_to = 'C://Users/varun/Desktop/Project/garbagemanagement/UserImages', default = 'C://Users/varun/Desktop/Images/defaultpicture.png')
	userName= models.CharField(max_length=25)
	userDay= models.IntegerField()
	userMonth= models.IntegerField()
	userYear= models.IntegerField()
	userAddress= models.TextField()
	userEmail=models.CharField(max_length=50)
	userPhno=models.BigIntegerField()
	userUname=models.CharField(max_length=25)
	userPwrd=models.CharField(max_length=25)
	userType = models.IntegerField()
	isLoggedIn = models.BooleanField()
	device_id = models.CharField(max_length = 50, blank = True, null = True)
	notifications =  models.IntegerField()

	def __str__(self):
		return self.userName

	class Meta:
		verbose_name_plural = "User Info"

class driver_info(models.Model):
	driver_id = models.ForeignKey('user_details', on_delete=models.CASCADE)
	driverLicPicture = models.ImageField(upload_to = 'C://Users/varun/Desktop/Project/garbagemanagement/UserImages', default = 'C://Users/varun/Desktop/Images/defaultpicture.png')
	driverDayLIC=models.IntegerField()
	driverMonthLIC=models.IntegerField()
	driverYearLIC=models.IntegerField()
	driverLino=models.CharField(max_length=15)
	driverVeno=models.CharField(max_length=10)
	approved=models.NullBooleanField(blank= True, null=True)
	driverArea=models.CharField(max_length=20, blank= True, null=True)

class garbageDetails(models.Model):
	garbagePicture = models.ImageField(upload_to = 'C://Users/varun/Desktop/Project/garbagemanagement/UserImages', default = 'C:/Users/Deeraj Ramchandani/Desktop/Images/defaultpicture.png')
	#garbagePicture = models.TextField()
	#garbagePictureVerification = models.TextField(blank=True, null=True)
	garbagePictureVerification = models.ImageField(upload_to = 'C://Users/varun/Desktop/Project/garbagemanagement/UserImages', default = 'C:/Users/Deeraj Ramchandani/Desktop/Images/defaultpicture.png', blank=True, null=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	geotag = models.TextField()
	user_id = models.IntegerField()
	time = models.CharField(max_length=25)
	driver_id = models.IntegerField(blank=True, null=True)
	date = models.CharField(max_length=25)

	class Meta:
		verbose_name_plural = "Garbage Details"

class schedule(models.Model):
	user_id = models.IntegerField()
	address = models.TextField(blank=True, null=True)
	days = models.IntegerField()
	community = models.BooleanField()
	noOfHouses = models.IntegerField(blank=True, null=True)
	specialInst = models.TextField(blank=True, null=True)
	driver_id = models.IntegerField(blank=True, null=True)
	landmark = models.CharField(max_length=30, blank=True, null=True)
	driver_completion = models.IntegerField(blank=True, null=True)
	user_approval = models.IntegerField(blank=True, null=True)

	class Meta:
		verbose_name_plural = "Schedule"