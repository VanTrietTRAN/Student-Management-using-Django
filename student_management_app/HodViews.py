import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management_app.forms import AddStudentForm, EditStudentForm
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel, \
    FeedBackStudent, FeedBackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport, \
    NotificationStudent, NotificationStaffs, Schedule, StudentEnrollment


def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    staffs=Staffs.objects.all()
    attendance_present_list_staff=[]
    attendance_absent_list_staff=[]
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)


    return render(request,"hod_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except Exception as e:
            print(e)
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                session_year=SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id=session_year
                user.students.gender=sex
                user.students.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
        credit_hours=request.POST.get("credit_hours", 3)  # Mặc định 3 tín chỉ
        fee_per_credit=request.POST.get("fee_per_credit", 0)  # Mặc định 0

        try:
            subject=Subjects(
                subject_name=subject_name,
                course_id=course,
                staff_id=staff,
                credit_hours=credit_hours,
                fee_per_credit=fee_per_credit
            )
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id=form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                session_year = SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id = session_year
                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        course_id=request.POST.get("course")
        credit_hours=request.POST.get("credit_hours", 3)
        fee_per_credit=request.POST.get("fee_per_credit", 0)

        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            course=Courses.objects.get(id=course_id)
            subject.course_id=course
            subject.credit_hours=credit_hours
            subject.fee_per_credit=fee_per_credit
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_course(request,course_id):
    course=Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")

        try:
            course=Courses.objects.get(id=course_id)
            print(Courses.course_name)
            course.course_name=course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course",kwargs={"course_id":course_id}))


def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

def student_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    subjects=Subjects.objects.all()
    session_year_id=SessionYearModel.objects.all()
    return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def admin_send_notification_student(request):
    students=Students.objects.all()
    return render(request,"hod_template/student_notification.html",{"students":students})

def admin_send_notification_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/staff_notification.html",{"staffs":staffs})

@csrf_exempt
def send_student_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    student=Students.objects.get(admin=id)
    token=student.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStudent(student_id=student,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

@csrf_exempt
def send_staff_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    staff=Staffs.objects.get(admin=id)
    token=staff.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action":"https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStaffs(staff_id=staff,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


# ============= SCHEDULE MANAGEMENT =============
def manage_schedule(request):
    """Quản lý thời khóa biểu - Hiển thị danh sách lịch học"""
    schedules = Schedule.objects.all().order_by('weekday', 'start_time')
    session_years = SessionYearModel.objects.all()
    return render(request, "hod_template/manage_schedule_template.html", {
        "schedules": schedules,
        "session_years": session_years
    })


def add_schedule(request):
    """Thêm lịch học mới"""
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    return render(request, "hod_template/add_schedule_template.html", {
        "subjects": subjects,
        "session_years": session_years
    })


def add_schedule_save(request):
    """Lưu lịch học mới"""
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject")
        session_year_id = request.POST.get("session_year")
        weekday = request.POST.get("weekday")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        room = request.POST.get("room", "")

        try:
            subject = Subjects.objects.get(id=subject_id)
            session_year = SessionYearModel.objects.get(id=session_year_id)
            
            schedule = Schedule(
                subject_id=subject,
                session_year_id=session_year,
                weekday=weekday,
                start_time=start_time,
                end_time=end_time,
                room=room
            )
            schedule.save()
            messages.success(request, "Successfully Added Schedule")
            return HttpResponseRedirect(reverse("add_schedule"))
        except:
            messages.error(request, "Failed to Add Schedule")
            return HttpResponseRedirect(reverse("add_schedule"))


def edit_schedule(request, schedule_id):
    """Chỉnh sửa lịch học"""
    schedule = Schedule.objects.get(id=schedule_id)
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    return render(request, "hod_template/edit_schedule_template.html", {
        "schedule": schedule,
        "subjects": subjects,
        "session_years": session_years,
        "id": schedule_id
    })


def edit_schedule_save(request):
    """Lưu chỉnh sửa lịch học"""
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        schedule_id = request.POST.get("schedule_id")
        subject_id = request.POST.get("subject")
        session_year_id = request.POST.get("session_year")
        weekday = request.POST.get("weekday")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        room = request.POST.get("room", "")

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            schedule.subject_id = Subjects.objects.get(id=subject_id)
            schedule.session_year_id = SessionYearModel.objects.get(id=session_year_id)
            schedule.weekday = weekday
            schedule.start_time = start_time
            schedule.end_time = end_time
            schedule.room = room
            schedule.save()
            
            messages.success(request, "Successfully Edited Schedule")
            return HttpResponseRedirect(reverse("edit_schedule", kwargs={"schedule_id": schedule_id}))
        except:
            messages.error(request, "Failed to Edit Schedule")
            return HttpResponseRedirect(reverse("edit_schedule", kwargs={"schedule_id": schedule_id}))


def delete_schedule(request, schedule_id):
    """Xóa lịch học"""
    try:
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.delete()
        messages.success(request, "Successfully Deleted Schedule")
    except:
        messages.error(request, "Failed to Delete Schedule")
    return HttpResponseRedirect(reverse("manage_schedule"))


# ========================================================================
# ADMIN GRADE MANAGEMENT - Admin có thể nhập điểm cho tất cả môn học
# ========================================================================

def admin_grade_subjects(request):
    """
    Hiển thị danh sách TẤT CẢ môn học để admin chọn môn nhập điểm
    """
    from student_management_app.models import StudentResult
    
    subjects = Subjects.objects.all().select_related('staff_id', 'course_id')
    
    # Tính toán số lượng sinh viên cho mỗi môn
    subjects_data = []
    for subject in subjects:
        enrolled_count = StudentEnrollment.objects.filter(subject_id=subject).count()
        graded_count = StudentResult.objects.filter(
            subject_id=subject
        ).exclude(
            subject_assignment_marks=0, 
            subject_exam_marks=0
        ).count()
        
        subjects_data.append({
            'subject': subject,
            'enrolled_count': enrolled_count,
            'graded_count': graded_count,
            'pending_count': enrolled_count - graded_count
        })
    
    return render(request, "hod_template/admin_grade_subjects.html", {
        "subjects_data": subjects_data
    })


def admin_enter_grades(request, subject_id):
    """
    Trang nhập điểm cho môn học (giống staff_enter_grades nhưng admin có thể vào tất cả môn)
    """
    from student_management_app.models import StudentResult
    
    try:
        subject = Subjects.objects.get(id=subject_id)
    except:
        messages.error(request, "Môn học không tồn tại!")
        return HttpResponseRedirect(reverse("admin_grade_subjects"))
    
    # Lấy danh sách sinh viên đã đăng ký môn này
    enrollments = StudentEnrollment.objects.filter(
        subject_id=subject
    ).select_related('student_id', 'student_id__admin')
    
    students_data = []
    for enrollment in enrollments:
        student = enrollment.student_id
        
        # Lấy kết quả điểm (nếu có)
        try:
            result = StudentResult.objects.get(
                student_id=student,
                subject_id=subject
            )
            # Chuyển điểm đã lưu (đã nhân hệ số) về dạng 0-100 để hiển thị
            assignment_raw = round(result.subject_assignment_marks / 0.4) if result.subject_assignment_marks > 0 else 0
            exam_raw = round(result.subject_exam_marks / 0.6) if result.subject_exam_marks > 0 else 0
        except StudentResult.DoesNotExist:
            assignment_raw = 0
            exam_raw = 0
        
        students_data.append({
            'student': student,
            'enrollment': enrollment,
            'assignment_marks': assignment_raw,
            'exam_marks': exam_raw
        })
    
    return render(request, "hod_template/admin_enter_grades.html", {
        "subject": subject,
        "students_data": students_data
    })


@csrf_exempt
def admin_save_grades(request):
    """
    Lưu điểm do admin nhập (giống staff_save_grades)
    """
    from student_management_app.models import StudentResult
    
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method"})
    
    try:
        # Parse JSON data
        data = json.loads(request.body)
        subject_id = data.get('subject_id')
        grades_data = data.get('grades', [])
        
        if not subject_id or not grades_data:
            return JsonResponse({"status": "error", "message": "Thiếu dữ liệu"})
        
        subject = Subjects.objects.get(id=subject_id)
        
        success_count = 0
        error_count = 0
        
        for grade in grades_data:
            try:
                student_id = grade['student_id']
                assignment_marks = float(grade['assignment_marks'])  # 0-100
                exam_marks = float(grade['exam_marks'])  # 0-100
                
                # Validate
                if not (0 <= assignment_marks <= 100 and 0 <= exam_marks <= 100):
                    error_count += 1
                    continue
                
                student = Students.objects.get(id=student_id)
                
                # Nhân hệ số trước khi lưu
                weighted_assignment = assignment_marks * 0.4
                weighted_exam = exam_marks * 0.6
                
                # Update hoặc create
                result, created = StudentResult.objects.get_or_create(
                    student_id=student,
                    subject_id=subject
                )
                
                result.subject_assignment_marks = weighted_assignment
                result.subject_exam_marks = weighted_exam
                result.save()
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                print(f"Error saving grade: {e}")
        
        return JsonResponse({
            "status": "success",
            "message": f"Đã lưu {success_count} điểm. Lỗi: {error_count}",
            "success_count": success_count,
            "error_count": error_count
        })
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def admin_export_subject_grades(request, subject_id):
    """
    Export điểm của môn học ra CSV (giống staff export)
    """
    import csv
    from django.http import HttpResponse
    from student_management_app.models import StudentResult
    
    try:
        subject = Subjects.objects.get(id=subject_id)
    except:
        messages.error(request, "Môn học không tồn tại!")
        return HttpResponseRedirect(reverse("admin_grade_subjects"))
    
    # Tạo response CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="diem_{subject.subject_code or subject.id}.csv"'
    
    # Write BOM for Excel UTF-8
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Header
    writer.writerow([
        'STT', 
        'Mã sinh viên', 
        'Họ và tên', 
        'Email',
        'Điểm BT (0-100)', 
        'Điểm thi (0-100)', 
        'BT×40%', 
        'Thi×60%', 
        'Tổng điểm',
        'Điểm chữ'
    ])
    
    # Data
    enrollments = StudentEnrollment.objects.filter(
        subject_id=subject
    ).select_related('student_id', 'student_id__admin')
    
    for idx, enrollment in enumerate(enrollments, 1):
        student = enrollment.student_id
        
        try:
            result = StudentResult.objects.get(
                student_id=student,
                subject_id=subject
            )
            
            # Chuyển về 0-100
            assignment_raw = round(result.subject_assignment_marks / 0.4) if result.subject_assignment_marks > 0 else 0
            exam_raw = round(result.subject_exam_marks / 0.6) if result.subject_exam_marks > 0 else 0
            
            weighted_assignment = result.subject_assignment_marks
            weighted_exam = result.subject_exam_marks
            total = weighted_assignment + weighted_exam
            
            # Điểm chữ
            if total >= 85:
                letter_grade = 'A'
            elif total >= 80:
                letter_grade = 'B+'
            elif total >= 70:
                letter_grade = 'B'
            elif total >= 65:
                letter_grade = 'C+'
            elif total >= 50:
                letter_grade = 'C'
            elif total >= 45:
                letter_grade = 'D+'
            elif total >= 40:
                letter_grade = 'D'
            else:
                letter_grade = 'F'
                
        except StudentResult.DoesNotExist:
            assignment_raw = 0
            exam_raw = 0
            weighted_assignment = 0
            weighted_exam = 0
            total = 0
            letter_grade = 'N/A'
        
        writer.writerow([
            idx,
            student.admin.username,
            f"{student.admin.first_name} {student.admin.last_name}",
            student.admin.email,
            assignment_raw,
            exam_raw,
            f"{weighted_assignment:.1f}",
            f"{weighted_exam:.1f}",
            f"{total:.1f}",
            letter_grade
        ])
    
    return response


# ========================================================================
# ADMIN REPORTS - Export báo cáo sinh viên và điểm
# ========================================================================

def admin_reports(request):
    """
    Trang quản lý báo cáo - có thể export danh sách SV và điểm
    """
    courses = Courses.objects.all()
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    
    # Thống kê
    students_count = Students.objects.all().count()
    staffs_count = Staffs.objects.all().count()
    
    return render(request, "hod_template/admin_reports.html", {
        "courses": courses,
        "subjects": subjects,
        "session_years": session_years,
        "students_count": students_count,
        "staffs_count": staffs_count
    })


def admin_export_students(request):
    """
    Export danh sách sinh viên ra CSV/Excel
    """
    import csv
    from django.http import HttpResponse
    
    course_id = request.GET.get('course_id', None)
    session_id = request.GET.get('session_id', None)
    
    # Filter students
    students = Students.objects.all().select_related('admin', 'course_id', 'session_year_id')
    
    if course_id:
        students = students.filter(course_id=course_id)
    if session_id:
        students = students.filter(session_year_id=session_id)
    
    # Create CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="danh_sach_sinh_vien.csv"'
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Header
    writer.writerow([
        'STT',
        'Mã sinh viên',
        'Họ và tên',
        'Email',
        'Địa chỉ',
        'Khóa học',
        'Năm học',
        'Ngày tham gia'
    ])
    
    # Data
    for idx, student in enumerate(students, 1):
        writer.writerow([
            idx,
            student.admin.username,
            f"{student.admin.first_name} {student.admin.last_name}",
            student.admin.email,
            student.address,
            student.course_id.course_name,
            f"{student.session_year_id.session_start_year} - {student.session_year_id.session_end_year}",
            student.admin.date_joined.strftime('%Y-%m-%d')
        ])
    
    return response


def admin_export_grades(request):
    """
    Export điểm của tất cả sinh viên trong một môn ra CSV
    """
    import csv
    from django.http import HttpResponse
    from student_management_app.models import StudentResult
    
    subject_id = request.GET.get('subject_id', None)
    
    if not subject_id:
        messages.error(request, "Vui lòng chọn môn học!")
        return HttpResponseRedirect(reverse("admin_reports"))
    
    try:
        subject = Subjects.objects.get(id=subject_id)
    except:
        messages.error(request, "Môn học không tồn tại!")
        return HttpResponseRedirect(reverse("admin_reports"))
    
    # Create CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="diem_{subject.subject_code or subject.id}.csv"'
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Header
    writer.writerow([
        'STT',
        'Mã SV',
        'Họ tên',
        'Email',
        'Môn học',
        'Giảng viên',
        'Điểm BT',
        'Điểm thi',
        'Tổng',
        'Điểm chữ'
    ])
    
    # Get all results for this subject
    results = StudentResult.objects.filter(subject_id=subject).select_related(
        'student_id', 'student_id__admin'
    )
    
    for idx, result in enumerate(results, 1):
        student = result.student_id
        total = result.subject_assignment_marks + result.subject_exam_marks
        
        if total >= 85:
            letter = 'A'
        elif total >= 70:
            letter = 'B'
        elif total >= 50:
            letter = 'C'
        elif total >= 40:
            letter = 'D'
        else:
            letter = 'F'
        
        writer.writerow([
            idx,
            student.admin.username,
            f"{student.admin.first_name} {student.admin.last_name}",
            student.admin.email,
            subject.subject_name,
            f"{subject.staff_id.first_name} {subject.staff_id.last_name}",
            f"{result.subject_assignment_marks:.1f}",
            f"{result.subject_exam_marks:.1f}",
            f"{total:.1f}",
            letter
        ])
    
    return response


# ========================================================================
# USER MANAGEMENT - Activate/Deactivate, Reset Password
# ========================================================================

@csrf_exempt
def toggle_user_status(request, user_id):
    """
    Bật/tắt trạng thái active của user
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"})
    
    try:
        user = CustomUser.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        status_text = "kích hoạt" if user.is_active else "vô hiệu hóa"
        
        return JsonResponse({
            "status": "success",
            "message": f"Đã {status_text} tài khoản {user.email}",
            "is_active": user.is_active
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User không tồn tại"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt  
def reset_user_password(request, user_id):
    """
    Reset password của user về 'admin'
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"})
    
    try:
        user = CustomUser.objects.get(id=user_id)
        user.set_password('admin')
        user.save()
        
        return JsonResponse({
            "status": "success",
            "message": f"Đã reset password của {user.email} về 'admin'"
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({"status": "error", "message": "User không tồn tại"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


# ============================================================================
# NOTIFICATION MANAGEMENT (Quản lý Thông báo)
# ============================================================================

def admin_view_notifications(request):
    """
    Admin xem lịch sử tất cả thông báo đã gửi cho staff và student
    """
    staff_notifications = NotificationStaffs.objects.all().order_by('-created_at')
    student_notifications = NotificationStudent.objects.all().order_by('-created_at')
    
    context = {
        'staff_notifications': staff_notifications,
        'student_notifications': student_notifications,
        'staff_count': staff_notifications.count(),
        'student_count': student_notifications.count(),
    }
    return render(request, "hod_template/admin_view_notifications.html", context)


def admin_delete_notification(request, notification_id, notification_type):
    """
    Admin xóa thông báo (staff hoặc student)
    notification_type: 'staff' hoặc 'student'
    """
    try:
        if notification_type == 'staff':
            notification = NotificationStaffs.objects.get(id=notification_id)
        else:
            notification = NotificationStudent.objects.get(id=notification_id)
        
        notification.delete()
        messages.success(request, "Đã xóa thông báo thành công!")
    except Exception as e:
        messages.error(request, f"Lỗi khi xóa thông báo: {str(e)}")
    
    return redirect('admin_view_notifications')



