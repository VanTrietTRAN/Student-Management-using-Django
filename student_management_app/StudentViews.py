import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Students, Courses, Subjects, CustomUser, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent, NotificationStudent, StudentResult, OnlineClassRoom, SessionYearModel, \
    StudentEnrollment, Schedule


def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    
    # Lấy các môn đã đăng ký
    enrolled_subjects = StudentEnrollment.objects.filter(
        student_id=student_obj, 
        is_active=True
    ).select_related('subject_id')
    
    # Lấy lịch học của các môn đã đăng ký
    subject_ids = [enrollment.subject_id for enrollment in enrolled_subjects]
    schedule = Schedule.objects.filter(
        subject__in=subject_ids,
        is_active=True
    ).select_related('subject', 'started_by').order_by('day_of_week', 'start_time')
    
    # Lấy notifications
    notifications = NotificationStudent.objects.filter(
        student_id=student_obj
    ).order_by('-created_at')[:10]
    
    # Attendance statistics
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    
    # Subjects count
    enrolled_count = enrolled_subjects.count()
    
    # Online classroom
    session_obj=SessionYearModel.object.get(id=student_obj.session_year_id.id)
    class_room=OnlineClassRoom.objects.filter(
        subject__in=subject_ids,
        is_active=True,
        session_years=session_obj
    )

    # Chart data for attendance
    subject_name=[]
    data_present=[]
    data_absent=[]
    for enrollment in enrolled_subjects:
        subject = enrollment.subject_id
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceReport.objects.filter(
            attendance_id__in=attendance,
            status=True,
            student_id=student_obj.id
        ).count()
        attendance_absent_count=AttendanceReport.objects.filter(
            attendance_id__in=attendance,
            status=False,
            student_id=student_obj.id
        ).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home_template.html",{
        "total_attendance":attendance_total,
        "attendance_absent":attendance_absent,
        "attendance_present":attendance_present,
        "subjects":enrolled_count,
        "data_name":subject_name,
        "data1":data_present,
        "data2":data_absent,
        "class_room":class_room,
        "schedule":schedule,
        "notifications":notifications,
        "enrolled_subjects":enrolled_subjects
    })

def join_class_room(request,subject_id,session_year_id):
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    subjects=Subjects.objects.filter(id=subject_id)
    if subjects.exists():
        session=SessionYearModel.object.filter(id=session_year_obj.id)
        if session.exists():
            subject_obj=Subjects.objects.get(id=subject_id)
            course=Courses.objects.get(id=subject_obj.course_id.id)
            check_course=Students.objects.filter(admin=request.user.id,course_id=course.id)
            if check_course.exists():
                session_check=Students.objects.filter(admin=request.user.id,session_year_id=session_year_obj.id)
                if session_check.exists():
                    onlineclass=OnlineClassRoom.objects.get(session_years=session_year_id,subject=subject_id)
                    return render(request,"student_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

                else:
                    return HttpResponse("This Online Session is Not For You")
            else:
                return HttpResponse("This Subject is Not For You")
        else:
            return HttpResponse("Session Year Not Found")
    else:
        return HttpResponse("Subject Not Found")


def student_view_attendance(request):
    student=Students.objects.get(admin=request.user.id)
    course=student.course_id
    subjects=Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendance.html",{"subjects":subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request,"student_template/student_apply_leave.html",{"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    staff_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request,"student_template/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))

def student_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        address=request.POST.get("address")
        gender=request.POST.get("gender")
        
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            student=Students.objects.get(admin=customuser)
            student.address=address
            if gender:
                student.gender=gender
            
            # Xử lý upload ảnh đại diện
            if request.FILES.get('profile_pic'):
                student.profile_pic=request.FILES['profile_pic']
            
            student.save()
            messages.success(request, "Cập nhật thông tin thành công")
            return HttpResponseRedirect(reverse("student_profile"))
        except Exception as e:
            messages.error(request, f"Cập nhật thất bại: {str(e)}")
            return HttpResponseRedirect(reverse("student_profile"))

@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=Students.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def student_all_notification(request):
    student=Students.objects.get(admin=request.user.id)
    notifications=NotificationStudent.objects.filter(student_id=student.id)
    return render(request,"student_template/all_notification.html",{"notifications":notifications})

def student_view_result(request):
    try:
        student=Students.objects.get(admin=request.user.id)
        studentresult=StudentResult.objects.filter(student_id=student.id)
        return render(request,"student_template/student_result.html",{"studentresult":studentresult})
    except Exception as e:
        messages.error(request, f"Chưa có bảng điểm. Vui lòng liên hệ giảng viên hoặc admin.")
        return HttpResponseRedirect(reverse("student_home"))


# ============= COURSE ENROLLMENT =============
def student_view_subjects(request):
    """Xem danh sách môn học có thể đăng ký"""
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    session_year = student.session_year_id
    
    # Lấy tất cả môn học của khóa
    all_subjects = Subjects.objects.filter(course_id=course)
    
    # Lấy các môn đã đăng ký
    enrolled_subjects = StudentEnrollment.objects.filter(
        student_id=student,
        session_year_id=session_year,
        is_active=True
    ).values_list('subject_id', flat=True)
    
    return render(request, "student_template/view_subjects.html", {
        "subjects": all_subjects,
        "enrolled_subjects": enrolled_subjects,
        "student": student
    })


def student_enroll_subject(request, subject_id):
    """Đăng ký môn học"""
    try:
        student = Students.objects.get(admin=request.user.id)
        subject = Subjects.objects.get(id=subject_id)
        session_year = student.session_year_id
        
        # Kiểm tra số môn đã đăng ký (giới hạn 8 môn)
        enrolled_count = StudentEnrollment.objects.filter(
            student_id=student, 
            is_active=True
        ).count()
        
        if enrolled_count >= 8:
            messages.error(request, "Bạn đã đăng ký tối đa 8 môn học. Vui lòng hủy đăng ký môn khác trước khi đăng ký môn mới.")
            return HttpResponseRedirect(reverse("student_view_subjects"))
        
        # Kiểm tra đã đăng ký môn này chưa
        if StudentEnrollment.objects.filter(student_id=student, subject_id=subject, is_active=True).exists():
            messages.warning(request, "Bạn đã đăng ký môn học này rồi")
        else:
            enrollment = StudentEnrollment(
                student_id=student,
                subject_id=subject,
                session_year_id=session_year,
                is_active=True
            )
            enrollment.save()
            messages.success(request, f"Đăng ký thành công môn {subject.subject_name}")
    except Exception as e:
        messages.error(request, f"Đăng ký thất bại: {str(e)}")
    
    return HttpResponseRedirect(reverse("student_view_subjects"))


def student_drop_subject(request, subject_id):
    """Hủy đăng ký môn học"""
    try:
        student = Students.objects.get(admin=request.user.id)
        subject = Subjects.objects.get(id=subject_id)
        session_year = student.session_year_id
        
        enrollment = StudentEnrollment.objects.get(
            student_id=student,
            subject_id=subject,
            session_year_id=session_year
        )
        enrollment.is_active = False
        enrollment.save()
        
        messages.success(request, f"Đã hủy đăng ký môn {subject.subject_name}")
    except:
        messages.error(request, "Hủy đăng ký thất bại")
    
    return HttpResponseRedirect(reverse("student_view_subjects"))


def student_view_fees(request):
    """Xem học phí của các môn đã đăng ký"""
    student = Students.objects.get(admin=request.user.id)
    session_year = student.session_year_id
    
    # Lấy các môn đã đăng ký
    enrollments = StudentEnrollment.objects.filter(
        student_id=student,
        session_year_id=session_year,
        is_active=True
    ).select_related('subject_id')
    
    # Tính tổng học phí
    total_credits = 0
    total_fee = 0
    fee_details = []
    
    for enrollment in enrollments:
        subject = enrollment.subject_id
        subject_fee = subject.get_total_fee()
        total_credits += subject.credit_hours
        total_fee += subject_fee
        
        fee_details.append({
            'subject': subject,
            'credit_hours': subject.credit_hours,
            'fee_per_credit': subject.fee_per_credit,
            'total_fee': subject_fee
        })
    
    return render(request, "student_template/view_fees.html", {
        "fee_details": fee_details,
        "total_credits": total_credits,
        "total_fee": total_fee,
        "student": student
    })


def student_view_schedule(request):
    """Xem thời khóa biểu"""
    student = Students.objects.get(admin=request.user.id)
    session_year = student.session_year_id
    
    # Lấy các môn đã đăng ký
    enrolled_subjects = StudentEnrollment.objects.filter(
        student_id=student,
        session_year_id=session_year,
        is_active=True
    ).values_list('subject_id', flat=True)
    
    # Lấy lịch học của các môn đã đăng ký
    schedules = Schedule.objects.filter(
        subject_id__in=enrolled_subjects,
        session_year_id=session_year
    ).order_by('weekday', 'start_time')
    
    # Sắp xếp theo thứ trong tuần
    schedule_by_day = {}
    for schedule in schedules:
        day = schedule.get_weekday_display()
        if day not in schedule_by_day:
            schedule_by_day[day] = []
        schedule_by_day[day].append(schedule)
    
    return render(request, "student_template/view_schedule.html", {
        "schedule_by_day": schedule_by_day,
        "student": student
    })


def student_view_subject_description(request, subject_id):
    """Xem/Download file mô tả môn học"""
    try:
        subject = Subjects.objects.get(id=subject_id)
        
        if subject.subject_description_file:
            return render(request, "student_template/view_subject_description.html", {
                "subject": subject
            })
        else:
            messages.warning(request, "No description file available for this subject")
            return HttpResponseRedirect(reverse("student_view_subjects"))
    except:
        messages.error(request, "Subject not found")
        return HttpResponseRedirect(reverse("student_view_subjects"))
