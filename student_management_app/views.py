import datetime
import json
import os

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd
from student_management_app.models import CustomUser, Courses, SessionYearModel
from student_management_system import settings


def showDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("Ok")

def signup_admin(request):
    return render(request,"signup_admin_page.html")

def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.objects.all()
    return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})

def signup_staff(request):
    return render(request,"signup_staff_page.html")

def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

def do_signup_student(request):
    if request.method != "POST":
        messages.error(request, "Invalid Request Method")
        return HttpResponseRedirect(reverse("signup_student"))
    
    # Get form data
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    # Validate required fields
    if not all([first_name, last_name, username, email, password, address, session_year_id, course_id, sex]):
        messages.error(request, "All fields are required")
        return HttpResponseRedirect(reverse("signup_student"))

    try:
        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return HttpResponseRedirect(reverse("signup_student"))
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return HttpResponseRedirect(reverse("signup_student"))

        # Handle profile picture upload
        profile_pic_url = ""
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        # Create user
        user = CustomUser.objects.create_user(
            username=username, 
            password=password, 
            email=email, 
            last_name=last_name,
            first_name=first_name, 
            user_type=3
        )
        
        # Get course and session year objects
        course_obj = Courses.objects.get(id=course_id)
        session_year = SessionYearModel.objects.get(id=session_year_id)
        
        # Create student profile
        from student_management_app.models import Students
        student = Students(
            admin=user,
            address=address,
            course_id=course_obj,
            session_year_id=session_year,
            gender=sex,
            profile_pic=profile_pic_url
        )
        student.save()
        
        messages.success(request, "Successfully Registered! You can now login with your credentials.")
        return HttpResponseRedirect(reverse("show_login"))
        
    except Courses.DoesNotExist:
        messages.error(request, "Selected course does not exist")
        return HttpResponseRedirect(reverse("signup_student"))
    except SessionYearModel.DoesNotExist:
        messages.error(request, "Selected session year does not exist")
        return HttpResponseRedirect(reverse("signup_student"))
    except Exception as e:
        messages.error(request, f"Failed to Register Student: {str(e)}")
        return HttpResponseRedirect(reverse("signup_student"))
