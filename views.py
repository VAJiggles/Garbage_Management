from django.views.generic import TemplateView
from django.shortcuts import *
from app1.models import *
import re
import json
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import status
from app1.serializers import *
from django.conf import settings
from django.conf.urls.static import static
import base64
import os
from PIL import Image
import string
import random
import shutil
from fontawesome.fields import IconField
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User

icon = IconField()

def home(request):
	diction={}
	diction['value']=0
	return render_to_response("home.html",{'diction':diction})

def signup_user(request):
	diction={}
	diction['value']=0
	return render_to_response("signup_user.html", {'diction':diction})

def login_user(request):
	diction={}
	diction['value']=0
	return render_to_response("login_user.html", {'diction':diction})

def signup_driver(request):
	diction={}
	diction['value']=0
	return render_to_response("signup_driver.html", {'diction':diction})

def login_admin(request):
	diction={}
	diction['value']=0
	return render_to_response("login_admin.html", {'diction':diction})

def adminPage(request):
	return render_to_response("adminPage.html")

def validate_user(request):			
	diction = {}
	diction['value']=1
	diction['result'] = ""

	name=request.POST['name']
	address=request.POST['address']
	day=request.POST['dayDob']
	month=request.POST['monthDob']
	year=request.POST['yearDob']
	phno=request.POST['phno']
	email=request.POST['email']
	username=request.POST['username']
	pwrd=request.POST['pwrd']
	pwrd2=request.POST['pwrd2']
	pic = request.FILES['profileimage']

	flagdob=0
	flagpwrd=0

	day = int (day)
	month = int (month)
	year = int (year)

	if(year<=1899 and year>=2007):
		flagdob=1
	elif(month>0 and month<13):
		if(month==2):
			if(year%4==0 or year%100==0 or year%400==0):
				if(day>0 and day<30):
					flagdob=1
			else:
				if(day>0 and day<29):
					flagdob=1
		elif(month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
			if(day>0 and day<32):
				flagdob=1
		
		elif(month==4 or month==6 or month==9 or month==11):
			if(day>0 and day<31):
				flagdob=1

	flagemail=re.findall(r'^[a-z]([a-z]|[._]|[0-9])+@(gmail|yahoo|live).(com|in)$',email)
	flagphno=re.search(r'^[789]\d{9}$',phno)

	if(pwrd==pwrd2):
		checkpwrd=re.findall(r'(?=\A\w[^\s]{8,})(?=\S*)(?=.*[a-z]{1,}.*)(.*[A-Z]{1,}.*)(?=.*[0-9]{1,}.*)',pwrd)
		if checkpwrd:
			flagpwrd=1
	else:
		flagpwrd=2

	flagemailCount=0
	a = user_details.objects.all().values()
	l=len(a)
	i=0
	while i<l:
		if(a[i]['userEmail']==email):
			flagemailCount=1
			break
		i+=1

	flagphnoCount=0
	i=0
	phno=int(phno)
	while i<l:
		if(int(a[i]['userPhno'])==phno):
			flagphnoCount=1
			break
		i+=1

	flagusernameCount=0
	i=0
	phno=int(phno)
	while i<l:
		if(a[i]['userUname']==username):
			flagusernameCount=1
			break
		i+=1

	if not flagdob:
		diction['result'] = "Please enter valid DOB"

	elif not flagphno:
		diction['result'] = "Please enter valid phone number"

	elif not flagemail:
		diction['result'] = "Please enter valid email"

	elif flagpwrd==2:
		diction['result'] = "Please check both passwords"

	elif flagpwrd==0:
		diction['result'] = "Password doesnt match requirements"

	elif flagemailCount==1:
		diction['result'] = "Email already in use."

	elif flagphnoCount==1:
		diction['result'] = "Phone Number already in use."

	elif flagusernameCount==1:
		diction['result'] = "Username already in use."

	else:
		t=user_details()

		t.userName=name
		t.userAddress=address
		t.userPhno=phno
		t.userEmail=email
		t.userUname=username
		t.userPwrd=pwrd
		t.userProfilePicture=request.FILES['profileimage']
		t.userDay=day
		t.userMonth=month
		t.userYear=year
		t.userType=1
		t.isLoggedIn= False
		t.save()

		diction['pagevalue'] = 0
		diction['result'] = "Signup Successful"

	return render_to_response("signup_user.html", {'diction':diction})

def validate_driver(request):			
	diction = {}
	diction['value'] = 1
	diction['result'] = ""

	name=request.POST['name']
	address=request.POST['address']
	dayDob=request.POST['dayDob']
	monthDob=request.POST['monthDob']
	yearDob=request.POST['yearDob']
	phno=request.POST['phno']
	email=request.POST['email']
	username=request.POST['username']
	pwrd=request.POST['pwrd']
	pwrd2=request.POST['pwrd2']
	dayLic=request.POST['dayLic']
	monthLic=request.POST['monthLic']
	yearLic=request.POST['yearLic']
	licno=request.POST['licno']
	vehno=request.POST['vehno']	

	flagdob=0
	flagpwrd=0
	flaglicd=0
	flaglicn=0

	dayDob = int (dayDob)
	monthDob = int (monthDob)
	yearDob = int (yearDob)

	if(yearDob<=1899 and yearDob>=2007):
		flagdob=1
	elif(monthDob>0 and monthDob<13):
		if(monthDob==2):
			if(yearDob%4==0 or yearDob%100==0 or yearDob%400==0):
				if(dayDob>0 and dayDob<30):
					flagdob=1
			else:
				if(dayDob>0 and dayDob<29):
					flagdob=1
		elif(monthDob==1 or monthDob==3 or monthDob==5 or monthDob==7 or monthDob==8 or monthDob==10 or monthDob==12):
			if(dayDob>0 and dayDob<32):
				flagdob=1
		
		elif(monthDob==4 or monthDob==6 or monthDob==9 or monthDob==11):
			if(dayDob>0 and dayDob<31):
				flagdob=1

	flagemail=re.findall(r'^[a-z]([a-z]|[._]|[0-9])+@(gmail|yahoo|live).(com|in)$',email)
	flagphno=re.search(r'^[789]\d{9}$',phno)

	dayLic = int (dayLic)
	monthLic = int (monthLic)
	yearLic = int (yearLic)

	if(yearLic<=2017 and yearDob>=2037):
		flaglicd=1
	elif(monthLic>0 and monthLic<13):
		if(monthLic==2):
			if(yearLic%4==0 or yearLic%100==0 or yearLic%400==0):
				if(dayLic>0 and dayLic<30):
					flaglicd=1
			else:
				if(dayLic>0 and dayLic<29):
					flaglicd=1
		elif(monthLic==1 or monthLic==3 or monthLic==5 or monthLic==7 or monthLic==8 or monthLic==10 or monthLic==12):
			if(dayLic>0 and dayLic<32):
				flaglicd=1
		
		elif(monthLic==4 or monthLic==6 or monthLic==9 or monthLic==11):
			if(dayLic>0 and dayLic<31):
				flaglicd=1

	if(len(licno)==15):
		if (licno[:2].isalpha()):
			flaglicn=1
	
	if(pwrd==pwrd2):
		checkpwrd=re.findall(r'(?=\A\w[^\s]{8,})(?=\S*)(?=.*[a-z]{1,}.*)(.*[A-Z]{1,}.*)(?=.*[0-9]{1,}.*)',pwrd)
		if checkpwrd:
			flagpwrd=1
	else:
		flagpwrd=2

	flagemailCount=0
	a = user_details.objects.all().values()
	b = driver_info.objects.all().values()
	l=len(a)
	i=0
	while i<l:
		if(a[i]['userEmail'] == email):
			flagemailCount=1
			break
		i+=1

	flagphnoCount=0
	i=0
	phno=int(phno)
	while i<l:
		if(int(a[i]['userPhno'])== phno):
			flagphnoCount=1
			break
		i+=1

	flagusernameCount=0
	i=0
	while i<l:
		if(a[i]['userUname']== username):
			flagusernameCount=1
			break
		i+=1

	flaglinoCount=0
	i=0
	l=len(b)
	while i<l:
		if(b[i]['driverLino']== licno):
			flaglinoCount=1
			break
		i+=1

	if not flagdob:
		diction['result'] = "Please enter valid DOB"		

	elif not flagphno:
		diction['result'] = "Please enter valid phone number"		

	elif not flagemail:
		diction['result'] = "Please enter valid email"		

	elif not flaglicd:
		diction['result'] = "The License is not Valid"	

	elif flaglicn != 1:
		diction['result'] = "Please Enter a valid License Number."
		
	elif flagpwrd==2:
		diction['result'] = "Please check both passwords"		

	elif flagpwrd==0:
		diction['result'] = "Password doesnt match requirements"

	elif flagemailCount==1:
		diction['result'] = "Email already in use."

	elif flagphnoCount==1:
		diction['result'] = "Phone Number already in use."

	elif flagusernameCount==1:
		diction['result'] = "Username already in use."

	elif flaglinoCount==1:
		diction['result'] = "License Number already in use."

	else:
		s=driver_info()
		t=user_details()

		t.userName=name
		t.userAddress=address
		t.userPhno=phno
		t.userEmail=email
		t.userUname=username
		t.userPwrd=pwrd
		t.userProfilePicture=request.FILES['profileimage']
		t.userDay=dayDob
		t.userMonth=monthDob
		t.userYear=yearDob
		t.userType=2
		t.isLoggedIn = False
		t.notifications = 0
		t.save()

		s.driver_id_id = user_details.objects.get(userUname=username).id
		s.driverDayLIC=dayLic
		s.driverMonthLIC=monthLic
		s.driverYearLIC=yearLic
		s.driverLino=licno
		s.driverVeno=vehno
		s.driverLicPicture=request.FILES['licenseimage']
		s.approved= None
		s.driverArea = "Null"
		s.save()
		diction['result'] = "Signup Successful"		
		diction['pagevalue'] = 1
		
	return render_to_response("signup_driver.html",{'diction':diction})

def adminLogin(request):
	uName = request.POST['uname']
	pwrd = request.POST['pwrd']
	diction={}
	if (uName == "admin" and pwrd == "password"):
		diction['value']= 0
		diction['sidenav']= 0
		diction['result']= "true"
		request.session['id']= 0
		return render_to_response("adminPage.html", {'diction':diction})
	else:
		diction['value']=1
		diction['result']= "Invalid Email or Password"
		return render_to_response("login_admin.html",{'diction':diction})

def adLogout(request):
	del request.session['id']
	diction={}
	diction['value']=1
	diction['result']="You have been Logged out."
	return render_to_response("home.html",{'diction':diction})

def see_all_users(request):
	return render_to_response("see_all_users.html",)

def sidenav(request):
	return render_to_response("sidenav.html")

def view_all_users_right_side(request):
	diction={}
	a=user_details.objects.all().filter(userType=1)
	diction['result']="true"
	diction['pagevalue'] = 0
	diction['users']=a
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def view_all_drivers_right_side(request):
	a= driver_info.objects.all()
	i=0
	diction={}
	diction['user']=a
	diction['result']="true"
	diction['pagevalue']=1
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def search_users_right_side(request):
	diction={}
	diction['result']="search"
	return render_to_response("search_Users_right_side.html", {'diction':diction})

def search_drivers_right_side(request):
	diction={}
	diction['result']="search"
	return render_to_response("search_Drivers_right_side.html", {'diction':diction})

def find_user(request):
	uname=request.POST['find']	
	a = user_details.objects.all().values()
	i=0
	flag=-1
	diction={}
	if a:
		while i<len(a):
			if uname==a[i]['userUname'] and a[i]['userType']==1 :
				diction[0] = a[i]
				flag=1
				break
			i+=1
		if flag==1:
			diction['result'] = "true"
		else:
			diction['result'] = "false"
	else:
		diction['result'] = "false"
	return render_to_response("search_Users_right_side.html",{'diction':diction})

def find_driver(request):
	uname=request.POST['find']	
	a=user_details.objects.all().values()
	i=0
	flag=-1
	diction={}
	if a:
		while i<len(a):
			if uname==a[i]['userUname'] and a[i]['userType']==2 :
				diction[0] = a[i]
				flag=1
				break
			i+=1
		if flag==1:
			diction['result'] = "true"
		else:
			diction['result'] = "false"
	else:
		diction['result'] = "false"
	return render_to_response("search_Users_right_side.html",{'diction':diction})

def user_Login(request):
	return render_to_response("user_Login.html")

def user_login_Check(request):
	uname=request.POST['uname']
	pwrd=request.POST['pwrd']
	a=user_details.objects.all().values()
	i=0
	flag=-1
	diction={}
	if a:
		while( i<len(a) ):
			if (uname==a[i]['userUname'] and pwrd==a[i]['userPwrd']):
				diction[0]=a[i]
				request.session['user_Id']=1
				request.session['id']=a[i]['id'] 
				flag=1
				break
			i+=1
		if flag==1:
			diction['result']="true"
			diction['sidenav']=1
			return render_to_response("logged_In_user.html",{'diction':diction})
		else:
			diction['result']="Invalid Email or Password Please Try Again."
			diction['value']= 1
			return render_to_response("login_user.html",{'diction':diction})

def user_sidenav(request):
	return render_to_response("user_sidenav.html")

def logged_In_user(request):
	user_login()

def logged_out_user(request):
	del request.session['id']
	diction={}
	diction['value']=1
	diction['result']="You have been Logged out."
	return render_to_response("home.html",{'diction':diction})

def see_user_details(request):
	userid=request.session.get('id')
	a=user_details.objects.values()
	diction={}
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction=a[i]
	return render_to_response("see_user_details.html",{'diction':diction})

def update_details(request):
	userid=request.session.get('id')
	a=user_details.objects.values()
	diction={}
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction=a[i]
	print("hi")
	return render_to_response("update_details.html",{'diction':diction})

def func_update_details(request):
	userid=request.session.get('id')
	a=user_details.objects.values()
	diction={}
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction=a[i]
	name=request.POST['name']
	address=request.POST['address']
	phno=request.POST['phno']
	email=request.POST['email']
	uname=request.POST['uname']
	
	a=user_details.objects.all().values()
	i=0
	flagemail=0
	flagphno=0
	flaguname=0
	flagaddress=0
	flagname=0
	len1=len(a)
	while (i<len1):
		if (diction['userEmail']== email):
			flagemail=1
			break
		if (diction['userPhno']== phno):
			flagphno=1
			break
		if (diction['userUname']== uname):
			flaguname=1
			break
		if (diction['userAddress']== address):
			flagaddress=1
			break
		if (diction['userName']== name):
			flagname=1
			break

		if (a[i]['userEmail']== email):
			flagemail=-1
			break
		if (a[i]['userPhno']== phno):
			flagphno=-1
			break
		if (a[i]['userUname']== uname):
			flaguname=-1
			break
		if (a[i]['userAddress']== address):
			flagaddress=-1
			break
		if (a[i]['userName']== name):
			flagname=-1
			break
		i+=1

	x=re.search(r'^[789]\d{9}$',phno)
	if x:
		flagphno=1		
	else:
		flagphno=2

	x=re.findall(r'^[a-z]([a-z]|[._]|[0-9])+@(gmail|yahoo|live).(com|in)$',email)
	if x:
		flagemail=1
	else:
		flagemail=2

	if flagemail== -1:
		diction['result']="Email has already been used"
	elif flagemail== 2:
		diction['result']="Invalid Email ID"
	elif flagphno== -1:
		diction['result']="Phone Number has already been used"
	elif flagphno== 2:
		diction['result']="Invalid contact number"
	elif flagaddress== -1:
		diction['result']="Address has already been used"
	elif flaguname== -1:
		diction['result']="Username has already been used"
	else:
		t=user_details.objects.get(id=userid)
		t.userName=name
		t.userAddress=address
		t.userPhno=phno
		t.userEmail=email
		t.userUname=uname
		t.save()
		diction['userPhno']= phno
		diction['userEmail']= email
		diction['userAddress']= address
		diction['userUname']= uname
		diction['userName']= name
		diction['result']="Update Sucessfull"
		diction['value']=0

	return render_to_response("update_details.html",{'diction':diction})

def forgotpassword(request):
	diction= {}
	diction['pagevalue']= 0
	diction['value'] = 0
	return render_to_response("forgotpassword.html",{'diction':diction})

def forgot_password_check(request):
	diction = {}
	email = request.POST['email']
	digits =  request.POST['digits']

	flagemail=re.findall(r'^[a-z]([a-z]|[._]|[0-9])+@(gmail|yahoo|live).(com|in)$',email)
	if not flagemail:
		diction['result'] = "Invalid Email ID."
		diction['value'] = 1
		diction['pagevalue']= 0
		return render_to_response("forgotpassword.html",{'diction':diction})

	flagemailCount = 0
	a = user_details.objects.all().values()
	l = len(a)
	i = 0
	phno = 0
	while i<l:
		if(a[i]['userEmail']==email):
			phno = a[i]['userPhno']
			flagemailCount = 1
			break
		i+=1
	phno = phno%10000
	if( flagemailCount == 0 ):
		diction['result'] = "Invalid Email ID."
		diction['value'] = 1
		diction['pagevalue']= 0
		return render_to_response("forgotpassword.html",{'diction':diction})

	elif( len(digits) > 4 ):
		diction['result'] = "Invalid Digits entered."
		diction['value'] = 1
		diction['pagevalue']= 0
		return render_to_response("forgotpassword.html",{'diction':diction})

	else:
		if( digits == str(phno)):
			diction['value'] = 0
			diction['pagevalue'] = 2
			otp = randint(100000,999999)
			mail(email, otp)
			diction['otp'] = otp
			request.session['otp'] = otp
			request.session['user_Id'] = 1
			request.session['id'] = a[i]['id']
			return render_to_response("forgotpassword.html",{'diction':diction})

def mail(toadd, otp): 
	fromadd="varun.ajmera@science.christuniversity.in"
	toadd=toadd
	password="20199000"
	msg=MIMEMultipart()
	msg['From']=fromadd
	msg['To']=toadd
	msg['Subject']="Password Change"

	msg['Message-ID'] = make_msgid()

	body= str(otp)
	msg.attach(MIMEText(body,'plain'))

	server=smtplib.SMTP('smtp.gmail.com',25)
	server.ehlo()
	server.starttls()
	server.login(fromadd,password)
	text=msg.as_string()
	server.sendmail(fromadd,toadd,text)
	server.quit()

def otp_check(request):
	otp = request.POST['otp']

	otp1 = request.session.get('otp')
	diction = {}
	if(otp == otp1):
		diction['value'] = 0
		diction['pagevalue'] = 1
		del request.session['otp']
		return render_to_response("forgotpassword.html",{'diction':diction})
	else:
		diction['otp'] = ""
		diction['value'] = 0
		diction['result'] = "Incorrect OTP."
		diction['pagevalue'] = 1
		return render_to_response("forgotpassword.html",{'diction':diction})

def reenter_password(request):
	userid=request.session.get('id')
	a=user_details.objects.values()
	diction={}
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction = a[i]
	pwrd = request.POST['pwrd1']
	pwrd2 = request.POST['pwrd2']

	if(pwrd == pwrd2):
		checkpwrd = re.findall(r'(?=\A\w[^\s]{8,})(?=\S*)(?=.*[a-z]{1,}.*)(.*[A-Z]{1,}.*)(?=.*[0-9]{1,}.*)',pwrd)
		if checkpwrd:
			t = user_details.objects.get(id=userid)
			t.userPwrd = pwrd
			t.save()
			diction['value'] = 1
			diction['result'] = "Password has been changed."
			return render_to_response("login_user.html",{'diction':diction})
		else:
			diction['value'] = 1
			diction['result'] = "Password does not meet requirements."
			diction['pagevalue']= 1
			return render_to_response("forgotpassword.html",{'diction':diction})

	else:
		diction['value'] = 1
		diction['result'] = "Passwords dont match."
		diction['pagevalue']= 1
		return render_to_response("forgotpassword.html",{'diction':diction})

def create_schedule(request):
	userid=request.session.get('id')
	a=schedule.objects.values()
	diction={}
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['user_id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction = a[i]
			diction['result'] = "Schedule already exists. To change please Update Schedule."
			diction['value'] = 1
			diction['pagevalue'] = 0
			return render_to_response("view_schedule.html",{'diction':diction})
	t = user_details.objects.get(id=userid)
	diction['address'] = t.userAddress
	diction['value'] = 0
	diction['pagevalue'] = 0
	return render_to_response("create_schedule.html",{'diction':diction})

def check_schedule(request):
	diction = {}
	days = request.POST.getlist('days[]')
	tot = 0
	addch = request.POST.getlist('addch[]')
	community = request.POST.getlist('community[]')

	userid=request.session.get('id')
	a=user_details.objects.values()
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction = a[i]
	
	if( days != [] ):
		print(str(days))
		if( days == ['1','2','4'] ):
			tot = 7		#all three days
		elif( days == ['1','2']  ):
			tot = 3		#mon and wed
		elif( days == ['1','4']  ):
			tot = 5		#mon and fri
		elif( days == ['1']):
			tot = 1
		elif( days == ['2']):
			tot = 2
		else:
			tot = 4
	else:
		diction['value'] = 1
		diction['pagevalue']= 0
		diction['result'] = "Select Days."
		return render_to_response("create_schedule.html",{'diction':diction})

	if( community != [] ):
		diction['value'] = 0
		diction['pagevalue']= 2
		t = schedule()
		t.days = tot
		t.user_id = userid
		t.address = diction['userAddress']
		t.specialInst = request.POST['specialinst']
		t.community = True
		t.noofHouses = 0
		t.save()
		return render_to_response("create_schedule.html",{'diction':diction})

	elif( addch != [] ):
		diction['value'] = 0
		diction['pagevalue']= 1
		t = schedule()
		t.days = tot
		t.user_id = userid
		t.address = diction['userAddress']
		t.specialInst = request.POST['specialinst']
		t.community = False
		t.noofHouses = 0
		t.save()
		return render_to_response("create_schedule.html",{'diction':diction})

	else:
		diction = {}
		t = schedule()
		t.days = tot
		t.user_id = userid
		t.address = diction['userAddress']
		t.specialInst = request.POST['specialinst']
		t.community = False
		t.noofHouses = 0
		t.save()
		diction['address'] = t.address
		diction['community'] = t.community
		diction['noOfHouses'] = t.noOfHouses
		diction['days'] = t.days
		diction['specialInst'] = t.specialInst
		return render_to_response("view_schedule.html",{'diction':diction})
		
def address_change(request):
	diction = {}
	address = request.POST['address']
	userid=request.session.get('id')
	a=user_details.objects.values()
	diction={}
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction = a[i]

	t = schedule.objects.get(user_id=userid)
	t.address = address
	t.save()
	diction['address'] = t.address
	diction['community'] = t.community
	diction['noOfHouses'] = t.noOfHouses
	diction['days'] = t.days
	diction['specialInst'] = t.specialInst
	return render_to_response("view_schedule.html",{'diction':diction})

def comm_houses(request):
	diction = {}
	address = request.POST['address']
	house = request.POST['house']
	userid=request.session.get('id')
	a=user_details.objects.values()
	i=0
	flag=0
	if a:
		while( i<len(a) ):
			if (userid==a[i]['id']):
				flag=1
				break
			i+=1
		if(flag==1):
			diction = a[i]
	t = schedule.objects.get(user_id=userid)
	t.address = address
	t.community = True
	t.noOfHouses = int(house)
	t.driver_completion = 0
	t.user_approval = 0
	t.save()
	diction['address'] = t.address
	diction['community'] = t.community
	diction['noOfHouses'] = t.noOfHouses
	diction['days'] = t.days
	diction['specialInst'] = t.specialInst
	return render_to_response("view_schedule.html",{'diction':diction})

def update_schedule(request):
	userid=request.session.get('id')
	a = schedule.objects.values()
	diction = {}
	i = 0
	flag = 0
	if a:
		while( i<len(a) ):
			if ( userid == a[i]['user_id'] ):
				flag = 1
				break
			i+=1
		if(flag == 1):
			diction = a[i]
			diction['value'] = 0
			diction['pagevalue'] = 0
			return render_to_response("update_schedule.html",{'diction':diction})
	
	diction['value'] = 1
	diction['pagevalue'] = 0
	diction['result'] = "Please Schedule a pick-up first."
	t = user_details.objects.get(id=userid)
	diction['address'] = t.userAddress
	return render_to_response("create_schedule.html",{'diction':diction})

def change_schedule(request):
	days = request.POST.getlist('days[]')
	noh = request.POST['noh']
	address = request.POST['address']
	specialinst = request.POST['specialinst']
	diction = {}
	if( days != [] ):
		if( days == ['1','2','4'] ):
			tot = 7		#all three days
		elif( days == ['1','2'] ):
			tot = 3		#mon and wed
		elif( days == ['1','4']  ):
			tot = 5		#mon and fri
		elif( days == ['2','4']  ):
			tot = 6		#wed and fri
		elif( days == ['1']):
			tot = 1
		elif( days == ['2']):
			tot = 2
		else:
			tot = 4
	else:
		t = schedule.objects.get(user_id=userid)
		diction = t.get.values()
		diction['value'] = 1
		diction['pagevalue']= 0
		diction['result'] = "Select Days."
		return render_to_response("update_schedule.html",{'diction':diction})

	userid = request.session.get('id')
	t = schedule.objects.get(user_id=userid)
	t.days = tot
	t.user_id = userid
	if( address != "" ):
		t.address = address
	t.specialInst = specialinst
	if( noh == 0  ):
		t.community = False
	else:
		t.community = True
	t.noOfHouses = noh
	diction = t.get.values()
	diction['value'] = 1
	diction['result'] = "Schedule has been updated"
	t.driver_completion = 0
	t.user_approval = 0
	t.save()
	return render_to_response("view_schedule",{'diction':diction})

def view_schedule(request):
	userid=request.session.get('id')
	a = schedule.objects.values()
	diction = {}
	i = 0
	flag = 0
	if a:
		while( i<len(a) ):
			if ( userid == a[i]['user_id'] ):
				flag = 1
				break
			i+=1
		if(flag == 1):
			diction = a[i]
			diction['value'] = 0
			diction['pagevalue'] = 0
			return render_to_response("view_schedule.html",{'diction':diction})
	
	t = user_details.objects.get(id=userid)
	diction['value'] = 1
	diction['pagevalue'] = 0
	diction['result'] = "Please Schedule a pick-up first."
	diction['address'] = t.userAddress
	return render_to_response("create_schedule.html",{'diction':diction})

def approved_driver(request):
	driver = request.GET.get('id')
	print(str(driver))
	t = driver_info.objects.get(driver_id_id = driver)
	t.approved = True
	t.save()
	a = driver_info.objects.all()
	i=0
	diction={}
	diction['user']=a
	diction['result']="true"
	diction['pagevalue']=1
	diction['value'] = 1
	diction['done'] = "The Driver Has been approved."
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def disapproved_driver(request):
	diction= {}
	driver = request.GET.get('id')
	t = driver_info.objects.get(driver_id_id = driver)
	s = schedule.objects.all().values()
	i = 0
	while i<len(s):
		if( s[i]['driver_id'] == driver):
			s[i]['driver_id'] = None 
			s[i]['driver_completion'] = 0
			s[i]['user_approval'] = 0
			s.save()
		i+=1
	t.approved = False
	t.save()
	a = driver_info.objects.all()
	i=0
	diction={}
	diction['user']=a
	diction['result']="true"
	diction['pagevalue']=1
	diction['value'] = 1
	diction['done'] = "The Driver Has been Disapproved."
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def see_schedules(request):
	diction = {}
	a = schedule.objects.all().values()
	i = 0
	while i<len(a):
		if(a[i]['days'] != 0):
			diction[i] = a[i]
			diction['result'] = "true"
			diction['value'] = 0
		i+=1
	return render_to_response("see_schedules.html", {'diction':diction})

def assign_area(request):
	diction= {}
	driver = request.GET.get('id')
	t = driver_info.objects.get(driver_id_id = driver)
	diction['driverLino'] = t.driverLino
	diction['driverVeno'] = t.driverVeno
	diction['driverDayLIC'] = t.driverDayLIC
	diction['driverMonthLIC'] = t.driverMonthLIC
	diction['driverYearLIC'] = t.driverYearLIC
	diction['driver_id_id'] = driver
	diction['pagevalue'] = 2
	diction['value'] = 1
	diction['done'] = "Assign an Area to the Driver"
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def area_assigned(request):
	driver = request.GET.get('id')
	t = driver_info.objects.get(driver_id_id = driver)
	areas = request.POST['areas']
	t.driverArea = areas
	t.save()
	a= driver_info.objects.all()
	i=0
	diction={}
	diction['user']=a
	diction['result']="true"
	diction['pagevalue']=1
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def assign_driver(request):
	user_id = request.GET.get('id')
	a=user_details.objects.all().values()
	i=0
	diction={}
	while i<len(a):
		if(a[i]['userType']==2):
			diction[i]=a[i]
			diction['user_id'] = user_id
			diction['result']="true"
			diction['pagevalue'] = 3
			s = driver_info.objects.get(driver_id_id = a[i]['id'])
			diction[i]['approved'] = s.approved
			diction[i]['driverLino'] = s.driverLino
			diction[i]['driverVeno'] = s.driverVeno
			diction[i]['driverDayLIC'] = s.driverDayLIC
			diction[i]['driverMonthLIC'] = s.driverMonthLIC
			diction[i]['driverYearLIC'] = s.driverYearLIC
			diction[i]['driverArea'] = s.driverArea
		i+=1	
	diction['user_id'] = user_id
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def driver_assigned(request):
	user_id = request.GET.get('id')
	driverid = request.GET.get('driverid')
	t = schedule.objects.get(user_id = user_id)
	t.driver_id = driverid
	t.save()
	diction = {}
	a = schedule.objects.all().values()
	i = 0
	while i<len(a):
		if(a[i]['days'] != 0):
			diction[i] = a[i]
			diction['result'] = "true"
			diction['value'] = 1
			diction['done'] = "Driver Has been assigned the Schedule."
			s = user_details.objects.get(id = a[i]['user_id'])
			if s.device_id != None:
				device = FCMDevice.objects.get(device_id = s.device_id)
				device.send_message(title="Alert!", body="Driver has been assigned. Please visit the View schedules tab.", data={"test":"test"})
			else:
				s.notifications = 1
				s.save()
			s = user_details.objects.get(id = driverid)

			if s.device_id != None:
				device = FCMDevice.objects.get(device_id = s.device_id)
				device.send_message(title="Alert!", body="You have been assigned a schedule. Please visit the View schedules tab.", data={"test":"test"})
			else:
				if int(s.notifications) == 2 or int(s.notifications) == 6:
					s.notifications = 6
				elif int(s.notifications) == 0 or int(s.notifications) == 2:
					s.notifications = 2
				s.save()
		i+=1
	return render_to_response("see_schedules.html", {'diction':diction})

def adminHome(request):
	a = user_details.objects.all().values()
	usercount = 0
	drivercount = 0
	schedulecount = 0
	i = 0
	while i< len(a):
		if (a[i]['userType'] == 1):
			usercount += 1
		if(a[i]['userType'] == 2):
			drivercount += 1
		i+=1
	a = schedule.objects.all().values()
	i = 0
	while i< len(a):
		if (a[i]['driver_id'] != None):
			schedulecount += 1
		i+=1
	diction = {}
	diction['usercount'] = usercount
	diction['drivercount'] = drivercount
	diction['schedulecount'] = schedulecount

	return render_to_response("adminHome.html",{'diction':diction})





#################################################################################

class userLoginData(APIView):

	def get(self, request, format=None):
		print("hi")
		userUname = request.GET.get('userUname')
		userPwrd = request.GET.get('userPwrd')
		deviceId = request.GET.get('deviceId')
		userType = request.GET.get('userType')
		userInfo = user_details.objects.get(userUname=userUname)
		a = user_details.objects.values().filter(userUname=userUname)
		#print(a)
		diction = {}
		diction = a
		type1 = int(userType)
		type2 = diction[0]['userType']
		print("TYPE:",type1)
		if userPwrd == diction[0]['userPwrd']:
			if type1 == 2 and type2 == 2:
				b = driver_info.objects.values().filter(driver_id_id=diction[0]['id'])
				if b:
					diction = {}
					diction = b
					if diction[0]['approved'] == None:
						return HttpResponse("LOLZ2", status=status.HTTP_404_NOT_FOUND)
					elif diction[0]['approved'] == False:
						id1 = int(diction[0]['driver_id_id'])
						j = driver_info.objects.filter(driver_id_id=diction[0]['id'])
						j.delete()
						j = user_details.objects.filter(userUname=userUname)
						j.delete()
						s = schedule.objects.values().filter(driver_id=id1)
						if s:
							diction = {}
							diction = s
							i = 0
							b = []
							while i < len(diction):
								b.append(int(diction[i]['id']))
								i+=1
							print(b)
							i = 0
							while i < len(diction):
								k = schedule.objects.get(id=int(b[i]))
								k.driver_id = None
								k.driver_completion = 0
								k.user_approval = 0
								k.save()
								i+=1
						s = garbageDetails.objects.values().filter(driver_id=id1)
						if s:
							diction = {}
							diction = s
							i = 0
							b = []
							while i < len(diction):
								b.append(int(diction[i]['id']))
								i+=1
							print(b)
							i = 0
							while i < len(diction):
								k = garbageDetails.objects.get(id=int(b[i]))
								k.driver_id = None
								k.save()
								i+=1
						return HttpResponse("LOLZ2", status=status.HTTP_501_NOT_IMPLEMENTED)
					else:
						s = user_details.objects.get(userUname=userUname)
						s.isLoggedIn = True
						s.device_id = deviceId
						s.save()
						userInfo = user_details.objects.get(userUname=userUname)
						serializer = user_infoSerializer(userInfo, many=False)
						return Response(serializer.data)
				else:
					return HttpResponse("LOLZ3", status=status.HTTP_409_CONFLICT)
			else:
				if type1 == 1 and type2 == 1:
					s = user_details.objects.get(userUname=userUname)
					s.isLoggedIn = True
					s.device_id = deviceId
					s.save()
					userInfo = user_details.objects.get(userUname=userUname)
					serializer = user_infoSerializer(userInfo, many=False)
					return Response(serializer.data)
				else:
					return HttpResponse("LOLZ3", status=status.HTTP_409_CONFLICT)
		else:
			return HttpResponse("LOLZ3", status=status.HTTP_409_CONFLICT)
		pass		

	def post(self):
		pass

def storeUserData(request):
	if request.method == "POST":
		data=request.read()
		values=json.loads(data.decode("utf-8"))
		if data:
			if values['userProfilePicture'] != None:
				image = base64.b64decode(values['userProfilePicture'])
				with open("imageToSave.jpg", "wb") as fh:
					fh.write(image)
				filename = id_generator()
				filename = filename+".jpg"
				newpath = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename
				shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
				os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath)

			s = user_details()
			s.userType = 1
			s.userName = values['userName']
			s.userAddress = values['userAddress']
			s.userDay = values['userDay']
			s.userMonth = values['userMonth']
			s.userYear = values['userYear']
			s.userPhno = int (values['userPhno'])
			s.userEmail = values['userEmail']
			s.userUname = values['userUname']
			s.userPwrd = values['userPwrd']
			s.isLoggedIn = False
			s.device_id = None
			s.notifications = 0
			if values['userProfilePicture'] != None:
				s.userProfilePicture = filename
			else:
				s.userProfilePicture = None
			s.save()
			return HttpResponse("OK!")
		else:
			return HttpResponse("ERROR!")

def uploadImage(request):
	if request.method == "POST":
		data = request.read()
		values = json.loads(data.decode("utf-8"))
		print(values)
		image = base64.b64decode(values['Image'])
		#image = base64.b64decode(values['Image'] + '=' * (-len(values['Image']) % 4))
		with open("imageToSave.jpg", "wb") as fh:
			fh.write(image)
		filename = id_generator()
		filename = filename+".jpg"
		newpath = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename
		shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
		os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath)
		s = garbageDetails()
		s.garbagePicture = filename
		s.latitude = float (values['latitude'])
		s.longitude = float (values['longitude'])
		s.date = values['date']
		s.time = values['time']
		if values['user_id'] == None:
			s.user_id = 0
		else:
			s.user_id = values['user_id']
		s.garbagePictureVerification = None
		s.geotag = values['geotag']
		s.save()
		return HttpResponse("OK")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def checkDuplicateData(request):
	if request.method == "POST":
		data=request.read()
		values=json.loads(data)
		if data:
			a = user_details.objects.all().values()
			i=0
			len1 = len(a)
			while i<len1:
				print("hi")
				if values['LoginStatus'] == "true" and values['id'] == a[i]['id']:
					i+=1
					continue
				if a[i]['userEmail'] == values['userEmail']:
					return HttpResponse("LOLZ2", status=status.HTTP_404_NOT_FOUND)
				if int(a[i]['userPhno']) == int(values['userPhno']):
					return HttpResponse("LOLZ", status=status.HTTP_400_BAD_REQUEST)
				if a[i]['userUname'] == values['userUname']:
					return HttpResponse("LOLZ3", status=status.HTTP_409_CONFLICT)
				i+=1
			print("hi")
			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

def updateUserData(request):
	if request.method == "POST":
		data=request.read()
		print("whats up")
		values=json.loads(data)
		if data:
			if values['userProfilePicture'] != None:
				image = base64.b64decode(values['userProfilePicture'])
				with open("imageToSave.jpg", "wb") as fh:
					fh.write(image)
				filename = id_generator()
				filename = filename+".jpg"
				newpath = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename
				shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
				os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath)
			s = user_details.objects.get(id=values['id'])
			s.userName = values['userName']
			s.userAddress = values['userAddress']
			s.userDay = values['userDay']
			s.userMonth = values['userMonth']
			s.userYear = values['userYear']
			s.userPhno = int (values['userPhno'])
			s.userEmail = values['userEmail']
			s.userUname = values['userUname']
			s.userPwrd = values['userPwrd']
			if values['userProfilePicture'] != None:
				s.userProfilePicture = filename
			else:
				s.userProfilePicture = None
			s.save()
			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

def storeSchedule(request):
	print("hi")
	if request.method == "POST":
		data=request.read()
		values=json.loads(data)
		print(values)
		if data:
			s = schedule()
			if values['address'] != None:
				s.address = values['address']
			else:
				s.address = None
			s.days = int(values['days'])
			if values['community'] == False:
				s.community = False
				s.noOfHouses = None
			else:
				s.community = True
				s.noOfHouses = int(values['noOfHouses'])
			s.specialInst = values['specialInst']
			s.driver_id = None
			s.user_id = int(values['user_id'])
			s.landmark = values['landmark']
			s.driver_completion = 0
			s.user_approval = 0
			s.save()
			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

def checkSchedule(request):
	ida = request.GET.get('id')
	print(ida)
	a = schedule.objects.values().filter(user_id=ida)
	print(a)
	if len(a) == 1:
		return HttpResponse("ok", status=status.HTTP_200_OK)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

class downloadSchedule(APIView):

	def get(self, request, format=None):
		ida = request.GET.get('id')
		scheduleObj = schedule.objects.get(user_id=ida)
		serializer = scheduleSerializer(scheduleObj, many=False)
		return Response(serializer.data)
		pass		
		
	def post(self):
		pass

class driverSchedule(APIView):

	def get(self, request, format=None):
		ida = request.GET.get('id')
		scheduleObj = user_details.objects.get(id=ida)
		serializer = driverScheduleSerializer(scheduleObj, many=False)
		return Response(serializer.data)
		pass		
		
	def post(self):
		pass

class licenseInfo(APIView):

	def get(self, request, format=None):
		ida = request.GET.get('id')
		scheduleObj = driver_info.objects.get(driver_id=ida)
		print(scheduleObj)
		serializer = licenseInfoSerializer(scheduleObj, many=False)
		return Response(serializer.data)
		pass		
		
	def post(self):
		pass

def updateSchedule(request):
	print("hi")
	if request.method == "POST":
		data=request.read()
		values=json.loads(data)
		print(values)
		if data:
			s = schedule.objects.get(user_id=values['user_id'])
			if values['address'] != None:
				s.address = values['address']
			else:
				s.address = None
			s.days = int(values['days'])
			if values['community'] == False:
				s.community = False
				s.noOfHouses = None
			else:
				s.community = True
				s.noOfHouses = int(values['noOfHouses'])
			s.specialInst = values['specialInst']
			s.driver_id = None
			s.user_id = int(values['user_id'])
			s.landmark = values['landmark']
			s.driver_completion = 0
			s.user_approval = 0
			s.save()
			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

def storePhoneData(request):
	if request.method == "POST":
		data=request.read()
		values=json.loads(data)
		print(values)
		if data:
			device = FCMDevice()
			device.device_id = values['deviceId']
			device.registration_id = values['token']
			device.type = "Android"
			device.name = "Device"
			device.user = User.objects.all().first()
			device.save()
			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

def logoutUser(request):
	ida = request.GET.get('id')
	s = user_details.objects.get(id=ida)
	s.isLoggedIn = False
	s.device_id = None
	s.notifications = 0
	s.save()
	return HttpResponse("ok", status=status.HTTP_200_OK)

def storeDriverData(request):
	if request.method == "POST":
		data=request.read()
		values=json.loads(data.decode("utf-8"))
		if data:
			if values['userProfilePicture'] != None:
				image = base64.b64decode(values['userProfilePicture'])
				with open("imageToSave.jpg", "wb") as fh:
					fh.write(image)
				filename = id_generator()
				filename = filename+".jpg"
				newpath = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename
				shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
				os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath)

			if values['driverLicPicture'] != None:
				image = base64.b64decode(values['driverLicPicture'])
				with open("imageToSave.jpg", "wb") as fh:
					fh.write(image)
				filename1 = id_generator()
				filename1 = filename1+".jpg"
				newpath1 = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename1
				shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
				os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath1)

			s = user_details()
			s.userType = 2
			s.userName = values['userName']
			s.userAddress = values['userAddress']
			s.userDay = values['userDay']
			s.userMonth = values['userMonth']
			s.userYear = values['userYear']
			s.userPhno = int (values['userPhno'])
			s.userEmail = values['userEmail']
			s.userUname = values['userUname']
			s.userPwrd = values['userPwrd']
			s.isLoggedIn = False
			s.device_id = None
			s.notifications = 0
			s.userProfilePicture = filename
			s.save()

			d = driver_info()

			d.driver_id_id = user_details.objects.get(userUname=values['userUname']).id
			d.driverLicPicture = filename1
			d.driverDayLIC = values['driverDayLIC']
			d.driverMonthLIC = values['driverMonthLIC']
			d.driverYearLIC = values['driverYearLIC']
			d.driverLino = values['driverLino']
			d.driverVeno = values['driverVeno']
			d.approved = None
			d.driverArea = None

			d.save()
			return HttpResponse("OK!")
		else:
			return HttpResponse("ERROR!")
	else:
		return HttpResponse("ERROR!")

def checkDriverDuplicateData(request):
	if request.method == "POST":
		data=request.read()
		values=json.loads(data)
		if data:
			a = user_details.objects.all().values()
			b = driver_info.objects.all().values()
			i=0
			len1 = len(a)
			while i<len1:
				print("hi")
				if values['LoginStatus'] == "true" and values['id'] == a[i]['id']:
					i+=1
					continue
				if a[i]['userEmail'] == values['userEmail']:
					return HttpResponse("LOLZ2", status=status.HTTP_404_NOT_FOUND)
				if int(a[i]['userPhno']) == int(values['userPhno']):
					return HttpResponse("LOLZ", status=status.HTTP_400_BAD_REQUEST)
				if a[i]['userUname'] == values['userUname']:
					return HttpResponse("LOLZ3", status=status.HTTP_409_CONFLICT)
				i+=1
			i=0;
			len2 = len(b)
			while i < len2:
				if values['LoginStatus'] == "true" and values['id'] == b[i]['driver_id_id']:
					i+=1
					continue
				if b[i]['driverLino'] == values['driverLino']:
					return HttpResponse("LOLZ2", status=status.HTTP_501_NOT_IMPLEMENTED)
				if b[i]['driverVeno'] == values['driverVeno']:
					return HttpResponse("LOLZ", status=status.HTTP_503_SERVICE_UNAVAILABLE)
				i+=1
			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

class driverLoginData(APIView):

	def get(self, request, format=None):
		ida = request.GET.get('id')
		driverInfo = driver_info.objects.get(driver_id_id=ida)
		serializer = driver_infoSerializer(driverInfo, many=False)
		return Response(serializer.data)
		pass		
		
	def post(self):
		pass

def updateDriverData(request):
	if request.method == "POST":
		data=request.read()
		values=json.loads(data)
		if data:
			if values['userProfilePicture'] != None:
				image = base64.b64decode(values['userProfilePicture'])
				with open("imageToSave.jpg", "wb") as fh:
					fh.write(image)
				filename = id_generator()
				filename = filename+".jpg"
				newpath = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename
				shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
				os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath)

			if values['driverLicPicture'] != None:
				image = base64.b64decode(values['driverLicPicture'])
				with open("imageToSave.jpg", "wb") as fh:
					fh.write(image)
				filename1 = id_generator()
				filename1 = filename1+".jpg"
				newpath1 = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename1
				shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
				os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath1)

			s = user_details.objects.get(id=values['id'])
			s.userName = values['userName']
			s.userAddress = values['userAddress']
			s.userDay = values['userDay']
			s.userMonth = values['userMonth']
			s.userYear = values['userYear']
			s.userPhno = int (values['userPhno'])
			s.userEmail = values['userEmail']
			s.userUname = values['userUname']
			s.userPwrd = values['userPwrd']
			if values['userProfilePicture'] != None:
				s.userProfilePicture = filename
			else:
				s.userProfilePicture = None
			s.save()

			d = driver_info.objects.get(driver_id_id=values['id'])

			d.driver_id_id = user_details.objects.get(userUname=values['userUname']).id
			d.driverLicPicture = filename1
			d.driverDayLIC = values['driverDayLIC']
			d.driverMonthLIC = values['driverMonthLIC']
			d.driverYearLIC = values['driverYearLIC']
			d.driverLino = values['driverLino']
			d.driverVeno = values['driverVeno']
			if values['isActive'] == "false":
				print("MAA KII")
				d.approved = None
				d.driverArea = None
				id1 = int(values['id'])
				s = schedule.objects.values().filter(driver_id=id1)
				if s:
					diction = {}
					diction = s
					i = 0
					b = []
					while i < len(diction):
						b.append(int(diction[i]['id']))
						i+=1
					print(b)
					i = 0
					while i < len(diction):
						k = schedule.objects.get(id=int(b[i]))
						k.driver_id = None
						k.driver_completion = 0
						k.user_approval = 0
						k.save()
						i+=1
				s = garbageDetails.objects.values().filter(driver_id=id1)
				if s:
					diction = {}
					diction = s
					i = 0
					b = []
					while i < len(diction):
						b.append(int(diction[i]['id']))
						i+=1
					print(b)
					i = 0
					while i < len(diction):
						k = garbageDetails.objects.get(id=int(b[i]))
						k.driver_id = None
						k.save()
						i+=1
			d.save()

			return HttpResponse("ok", status=status.HTTP_200_OK)
		else:
			return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)
	else:
		return HttpResponse("fail", status=status.HTTP_504_GATEWAY_TIMEOUT)

class pickups(APIView):

	def get(self, request, format=None):
		print("hi")
		ida = request.GET.get('id')
		scheduleObj = schedule.objects.filter(driver_id=ida)
		if scheduleObj:
			serializer = scheduleSerializer(scheduleObj, many=True)
			return Response(serializer.data)
		else:
			return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)
		pass		
		
	def post(self):
		pass

class detailsUserSchedule(APIView):

	def get(self, request, format=None):
		print("hi")
		ida = request.GET.get('id')
		scheduleObj = user_details.objects.get(id=ida)
		serializer = userInfoSchedule(scheduleObj, many=False)
		return Response(serializer.data)
		pass		
		
	def post(self):
		pass

def updateCompletion(request):
	ida = request.GET.get('id')
	day = request.GET.get('day')
	a = schedule.objects.values().filter(id=ida)
	diction = {}
	diction = a
	print(diction)
	s = schedule.objects.get(id=ida)
	s.driver_completion = int(diction[0]['driver_completion']) + int(day)
	s.save()
	return HttpResponse()

def uPickups(request):
	ida = request.GET.get('id')
	day = request.GET.get('day')
	a = schedule.objects.values().filter(id=ida)
	diction = {}
	diction = a
	print(diction)
	s = schedule.objects.get(id=ida)
	s.user_approval = int(diction[0]['user_approval']) + int(day)
	s.save()
	return HttpResponse()

class getGarbageDetails(APIView):

	def get(self, request, format=None):
		print("hi")
		ida = request.GET.get('id')
		scheduleObj = garbageDetails.objects.filter(driver_id=ida)
		scheduleObj1 = garbageDetails.objects.values().filter(driver_id=ida, garbagePictureVerification="")
		print(scheduleObj1)
		if scheduleObj:
			serializer = garbageInfoSchedule1(scheduleObj, many=True)
			return Response(serializer.data)
		else:
			return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)
		pass		
		
	def post(self):
		pass

class fullGarbageDetails(APIView):

	def get(self, request, format=None):
		print("hi")
		ida = request.GET.get('id')
		scheduleObj = garbageDetails.objects.get(id=ida)
		if scheduleObj:
			serializer = garbageInfoSchedule(scheduleObj, many=False)
			print(serializer.data)
			return Response(serializer.data)
			#return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)
		else:
			return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)
		pass		
		
	def post(self):
		pass

def sendImage(request):
	if request.method == "POST":
		data = request.read()
		values = json.loads(data.decode("utf-8"))
		if values:

			image = base64.b64decode(values['garbagePictureValidation'])
			with open("imageToSave.jpg", "wb") as fh:
				fh.write(image)
			filename = id_generator()
			filename = filename+".jpg"
			newpath = "C://Users/varun/Desktop/Project/garbagemanagement/UserImages/"+filename
			shutil.move("imageToSave.jpg","C://Users/varun/Desktop/Project/garbagemanagement/UserImages/")
			os.rename("C://Users/varun/Desktop/Project/garbagemanagement/UserImages/imageToSave.jpg", newpath)

			s = garbageDetails.objects.get(id=int(values['id']))
			s.garbagePictureVerification = filename
			s.save()
			return HttpResponse("OK")
		else:
			return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)
	else:
		return HttpResponse("", status=status.HTTP_400_BAD_REQUEST)

def see_garbage(request):
	diction = {}
	a = garbageDetails.objects.all()
	#print(len(a))
	i = 0
	diction = {}
	if a:
		while i < len(a):
			diction[i] = a[i]
			diction['result'] = "true"
			diction['value'] = 0
			i+=1
	print(diction)
	return render_to_response("see_garbage.html", {'diction':diction})

def garbage_assign(request):
	ida = request.GET.get('id')
	a=user_details.objects.all().values()
	i=0
	diction={}
	while i<len(a):
		if(a[i]['userType']==2):
			diction[i]=a[i]
			diction['gid'] = ida
			diction['result']="true"
			diction['pagevalue'] = 4
			s = driver_info.objects.get(driver_id_id = a[i]['id'])
			diction[i]['approved'] = s.approved
			diction[i]['driverLino'] = s.driverLino
			diction[i]['driverVeno'] = s.driverVeno
			diction[i]['driverDayLIC'] = s.driverDayLIC
			diction[i]['driverMonthLIC'] = s.driverMonthLIC
			diction[i]['driverYearLIC'] = s.driverYearLIC
			diction[i]['driverArea'] = s.driverArea
		i+=1	
	diction['gid'] = ida
	return render_to_response("see_all_users_right_side.html", {'diction':diction})

def gdriverAssigned(request):
	gid = request.GET.get('gid')
	driverid = request.GET.get('driverid')
	t = garbageDetails.objects.get(id = gid)
	t.driver_id = driverid
	t.save()
	diction = {}
	a = garbageDetails.objects.all()
	c = garbageDetails.objects.all().values()
	i = 0
	while i<len(a):
		diction[i] = a[i]
		diction['result'] = "true"
		diction['value'] = 1
		diction['done'] = "Driver Has been assigned the Schedule."

		s = user_details.objects.get(id = int(driverid))
		if s.device_id != None:
			device = FCMDevice.objects.get(device_id = s.device_id)
			device.send_message(title="Alert!", body="You have been assigned a garbage. Please visit the garbage pickup tab.", data={"test":"test"})
		else:
			if int(s.notifications) == 2 or int(s.notifications) == 6:
				s.notifications = 6
			elif int(s.notifications) == 0 or int(s.notifications) == 4:
				s.notifications = 4
			s.save()
		i+=1
	return render_to_response("see_garbage.html", {'diction':diction})

def generate_report(request):
	diction = {}
	schedulecount = 0
	f = open("report.txt","w+")
	f.write("\n SAMPLE REPORT\n ------------\n")
	a = user_details.objects.filter(userType=1)
	f.write("\n\n The number of users registered: "+str(len(a)))
	a = user_details.objects.filter(userType=2)
	f.write("\n\n The number drivers registered: "+str(len(a)))
	
	a = driver_info.objects.filter(approved = True)
	f.write("\n\n The number drivers approved: "+str(len(a)))

	a = driver_info.objects.filter(approved = False)
	f.write("\n\n The number drivers disapproved: "+str(len(a)))

	a = driver_info.objects.filter(approved = None)
	f.write("\n\n The number drivers not yet approved: "+str(len(a)))
	a = schedule.objects.all().values()
	i = 0
	while(i<len(a)):
		if(a[i]['driver_id'] != ""):
			schedulecount += 1
		i+=1
	f.write("\n\n The number schedules asssigned: "+str(schedulecount))
	f.write("\n\n The number schedules not yet asssigned: "+str(len(a)-schedulecount))
	a = garbageDetails.objects.all()
	f.write("\n\n Amount of Garbage Photos uploaded to database: "+str(len(a)))
	b = garbageDetails.objects.filter(driver_id = None)
	f.write("\n\n Amount of Garbage Photos that have been assigned: "+str(len(a) - len(b)))
	b = garbageDetails.objects.filter(garbagePictureVerification = "")
	f.write("\n\n Garbage that has been picked up from picture upload: "+str(len(a) - len(b)))

	a = schedule.objects.all().values()
	i = 0
	mon = 0
	wed = 0
	fri = 0
	while(i<len(a)):
		if( a[i]['days'] != 0 ):
			if( a[i]['days'] == 7 ):
				mon+=1
				wed+=1
				fri+=1	#all three days
			elif( a[i]['days'] == 3 ):
				mon+=1
				wed+=1		#mon and wed
			elif( a[i]['days'] == 5  ):
				mon+=1
				fri+=1		#mon and fri
			elif( a[i]['days'] == 6  ):
				wed+=1
				fri+=1		#wed and fri
			elif( a[i]['days'] == 1):
				mon+=1
			elif( a[i]['days'] == 2 ):
				wed+=1
			else:
				fri+=1
		i+=1

	f.write("\n\n Monday pick-ups: "+str(mon))
	f.write("\n\n Wednesday pick-ups: "+str(wed))
	f.write("\n\n Friday pick-ups: "+str(fri))
	diction['value'] = 1
	diction['result'] = "true"
	diction['done'] = "The Report has been genereated!"
	return render_to_response("adminPage.html",{'diction':diction})