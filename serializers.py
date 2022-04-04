from rest_framework import serializers
from app1.models import *

class user_infoSerializer(serializers.ModelSerializer):

	class Meta:
		model = user_details
		fields = '__all__'

class duplicateUserInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = user_details
		fields = ('userEmail', 'userPhno', 'userUname')

class scheduleSerializer(serializers.ModelSerializer):

	class Meta:
		model = schedule
		fields = '__all__'

class driverScheduleSerializer(serializers.ModelSerializer):

	class Meta:
		model = user_details
		fields = ('userPhno', 'userName')

class licenseInfoSerializer(serializers.ModelSerializer):

	class Meta:
		model = driver_info
		fields = '__all__'

class driver_infoSerializer(serializers.ModelSerializer):

	class Meta:
		model = driver_info
		fields = '__all__'

class userInfoSchedule(serializers.ModelSerializer):

	class Meta:
		model = user_details
		fields = ('id', 'userPhno', 'userName', 'userAddress')

class garbageInfoSchedule1(serializers.ModelSerializer):

	class Meta:
		model = garbageDetails
		fields = ('id', 'geotag')

class garbageInfoSchedule(serializers.ModelSerializer):

	class Meta:
		model = garbageDetails
		fields = '__all__'
