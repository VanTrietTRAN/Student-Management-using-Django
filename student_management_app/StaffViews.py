import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from student_management_app.models import Subjects, SessionYearModel, Students, Attendance, AttendanceReport, \
    LeaveReportStaff, Staffs, FeedBackStaffs, CustomUser, Courses, NotificationStaffs, StudentResult, OnlineClassRoom, \
    SubjectDescriptionFile
from django.core.files.storage import FileSystemStorage


def staff_home(request):
    #For Fetch All Student Under Staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    #Fetch Attendance Data by Subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})

def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))

def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    subjects_count=Subjects.objects.filter(staff_id=user.id).count()
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff,"subjects_count":subjects_count})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            
            # Handle profile picture upload
            if request.FILES.get('profile_pic'):
                staff.profile_pic=request.FILES['profile_pic']
            
            staff.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return HttpResponseRedirect(reverse("staff_profile"))
        except Exception as e:
            messages.error(request, "Cập nhật thông tin thất bại!")
            return HttpResponseRedirect(reverse("staff_profile"))

def staff_my_subjects(request):
    """View để hiển thị danh sách môn học mà giảng viên đang giảng dạy"""
    from student_management_app.models import Schedule, StudentEnrollment
    
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    
    # Lấy thêm thông tin số sinh viên và lịch học cho mỗi môn
    subjects_data = []
    for subject in subjects:
        # Đếm số sinh viên đăng ký môn này
        student_count = StudentEnrollment.objects.filter(subject_id=subject.id).count()
        
        # Lấy lịch học (nếu có)
        try:
            schedule = Schedule.objects.get(subject_id=subject.id)
        except Schedule.DoesNotExist:
            schedule = None
        
        subjects_data.append({
            'id': subject.id,
            'subject_code': subject.subject_code,
            'subject_name': subject.subject_name,
            'credit_hours': subject.credit_hours,
            'student_count': student_count,
            'schedule': schedule
        })
    
    return render(request, "staff_template/staff_my_subjects.html", {"subjects": subjects_data})

def staff_view_class_students(request, subject_id):
    """View để hiển thị danh sách sinh viên đăng ký môn học"""
    from student_management_app.models import StudentEnrollment, StudentResult
    
    subject = Subjects.objects.get(id=subject_id)
    
    # Lấy danh sách sinh viên đăng ký môn này
    enrollments = StudentEnrollment.objects.filter(subject_id=subject_id)
    
    students_data = []
    for enrollment in enrollments:
        student = enrollment.student_id
        
        # Lấy điểm của sinh viên (nếu có)
        try:
            result = StudentResult.objects.get(student_id=student.id, subject_id=subject_id)
            assignment_marks = result.subject_assignment_marks
            exam_marks = result.subject_exam_marks
            total_marks = assignment_marks + exam_marks if assignment_marks and exam_marks else None
        except StudentResult.DoesNotExist:
            assignment_marks = None
            exam_marks = None
            total_marks = None
        
        students_data.append({
            'id': student.id,
            'admin': student.admin,
            'gender': student.gender,
            'assignment_marks': assignment_marks,
            'exam_marks': exam_marks,
            'total_marks': total_marks
        })
    
    return render(request, "staff_template/staff_view_class_students.html", {
        "subject": subject,
        "students": students_data
    })

def staff_enter_grades(request, subject_id):
    """View để nhập điểm cho sinh viên"""
    from student_management_app.models import StudentEnrollment, StudentResult
    
    subject = Subjects.objects.get(id=subject_id)
    
    # Lấy danh sách sinh viên đăng ký môn này
    enrollments = StudentEnrollment.objects.filter(subject_id=subject_id)
    
    students_data = []
    for enrollment in enrollments:
        student = enrollment.student_id
        
        # Lấy điểm của sinh viên (nếu có)
        try:
            result = StudentResult.objects.get(student_id=student.id, subject_id=subject_id)
            # Điểm đã lưu trong DB là điểm sau khi nhân hệ số (0-40, 0-60)
            # Cần chuyển ngược về điểm gốc (0-100) để hiển thị
            assignment_marks = result.subject_assignment_marks  # Điểm sau hệ số (0-40)
            exam_marks = result.subject_exam_marks  # Điểm sau hệ số (0-60)
            assignment_marks_raw = assignment_marks / 0.4 if assignment_marks else None  # Chuyển về 0-100
            exam_marks_raw = exam_marks / 0.6 if exam_marks else None  # Chuyển về 0-100
        except StudentResult.DoesNotExist:
            assignment_marks = None
            exam_marks = None
            assignment_marks_raw = None
            exam_marks_raw = None
        
        students_data.append({
            'id': student.id,
            'admin': student.admin,
            'assignment_marks': assignment_marks,  # Điểm sau hệ số để tính tổng
            'exam_marks': exam_marks,
            'assignment_marks_raw': assignment_marks_raw,  # Điểm gốc để hiển thị
            'exam_marks_raw': exam_marks_raw
        })
    
    return render(request, "staff_template/staff_enter_grades.html", {
        "subject": subject,
        "students": students_data
    })

def staff_save_grades(request):
    """View để lưu điểm cho sinh viên"""
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_my_subjects"))
    
    from student_management_app.models import StudentEnrollment, StudentResult
    
    subject_id = request.POST.get("subject_id")
    
    try:
        subject = Subjects.objects.get(id=subject_id)
        enrollments = StudentEnrollment.objects.filter(subject_id=subject_id)
        
        for enrollment in enrollments:
            student = enrollment.student_id
            assignment_marks_key = f"assignment_marks_{student.id}"
            exam_marks_key = f"exam_marks_{student.id}"
            
            assignment_marks_raw = request.POST.get(assignment_marks_key)
            exam_marks_raw = request.POST.get(exam_marks_key)
            
            # Chỉ lưu nếu có ít nhất một trong hai điểm
            if assignment_marks_raw or exam_marks_raw:
                assignment_marks_raw = float(assignment_marks_raw) if assignment_marks_raw else 0
                exam_marks_raw = float(exam_marks_raw) if exam_marks_raw else 0
                
                # Kiểm tra điểm hợp lệ (0-100)
                if assignment_marks_raw < 0 or assignment_marks_raw > 100:
                    messages.error(request, f"Điểm bài tập phải từ 0-100 cho sinh viên {student.admin.username}")
                    return HttpResponseRedirect(reverse("staff_enter_grades", kwargs={"subject_id": subject_id}))
                
                if exam_marks_raw < 0 or exam_marks_raw > 100:
                    messages.error(request, f"Điểm thi phải từ 0-100 cho sinh viên {student.admin.username}")
                    return HttpResponseRedirect(reverse("staff_enter_grades", kwargs={"subject_id": subject_id}))
                
                # Tính điểm sau khi nhân hệ số để lưu vào DB
                assignment_marks = assignment_marks_raw * 0.4  # Nhân 40%
                exam_marks = exam_marks_raw * 0.6  # Nhân 60%
                
                # Tạo hoặc cập nhật điểm
                result, created = StudentResult.objects.get_or_create(
                    student_id=student,
                    subject_id=subject
                )
                result.subject_assignment_marks = assignment_marks  # Lưu điểm đã nhân hệ số (0-40)
                result.subject_exam_marks = exam_marks  # Lưu điểm đã nhân hệ số (0-60)
                result.save()
        
        messages.success(request, "Lưu điểm thành công!")
        return HttpResponseRedirect(reverse("staff_view_class_students", kwargs={"subject_id": subject_id}))
    
    except Exception as e:
        messages.error(request, f"Lỗi khi lưu điểm: {str(e)}")
        return HttpResponseRedirect(reverse("staff_enter_grades", kwargs={"subject_id": subject_id}))

def staff_manage_description_new(request, subject_id):
    """View để quản lý mô tả học phần"""
    subject = Subjects.objects.get(id=subject_id)
    return render(request, "staff_template/staff_manage_description.html", {"subject": subject})

def staff_save_description(request):
    """View để lưu mô tả học phần"""
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_my_subjects"))
    
    subject_id = request.POST.get("subject_id")
    description = request.POST.get("description")
    
    try:
        subject = Subjects.objects.get(id=subject_id)
        subject.description = description
        
        # Xử lý file upload
        if request.FILES.get('description_file'):
            subject.description_file = request.FILES['description_file']
        
        subject.save()
        messages.success(request, "Lưu mô tả học phần thành công!")
        return HttpResponseRedirect(reverse("staff_manage_description", kwargs={"subject_id": subject_id}))
    
    except Exception as e:
        messages.error(request, f"Lỗi khi lưu mô tả: {str(e)}")
        return HttpResponseRedirect(reverse("staff_manage_description", kwargs={"subject_id": subject_id}))

def staff_send_notification(request):
    """View để hiển thị form gửi thông báo"""
    from student_management_app.models import StudentEnrollment
    
    # Lấy danh sách môn học của giảng viên với số sinh viên
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    subjects_data = []
    
    for subject in subjects:
        student_count = StudentEnrollment.objects.filter(subject_id=subject.id).count()
        subjects_data.append({
            'id': subject.id,
            'subject_code': subject.subject_code,
            'subject_name': subject.subject_name,
            'student_count': student_count
        })
    
    # Lấy lịch sử thông báo đã gửi
    notifications = NotificationStaffs.objects.filter(staff_id=request.user.id).order_by('-created_at')[:10]
    
    return render(request, "staff_template/staff_send_notification.html", {
        "subjects": subjects_data,
        "notifications": notifications
    })

def staff_send_notification_save(request):
    """View để lưu và gửi thông báo"""
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_send_notification"))
    
    from student_management_app.models import StudentEnrollment, NotificationStudent
    
    subject_id = request.POST.get("subject_id")
    message = request.POST.get("message")
    
    try:
        subject = Subjects.objects.get(id=subject_id)
        staff = Staffs.objects.get(admin=request.user.id)
        
        # Tạo notification cho staff
        notification_staff = NotificationStaffs(
            staff_id=staff,
            message=f"Đã gửi thông báo đến môn {subject.subject_name}: {message}"
        )
        notification_staff.save()
        
        # Gửi thông báo đến tất cả sinh viên đăng ký môn này
        enrollments = StudentEnrollment.objects.filter(subject_id=subject_id)
        
        for enrollment in enrollments:
            student = enrollment.student_id
            notification_student = NotificationStudent(
                student_id=student,
                message=f"[{subject.subject_name}] {message}"
            )
            notification_student.save()
        
        messages.success(request, f"Đã gửi thông báo đến {enrollments.count()} sinh viên!")
        return HttpResponseRedirect(reverse("staff_send_notification"))
    
    except Exception as e:
        messages.error(request, f"Lỗi khi gửi thông báo: {str(e)}")
        return HttpResponseRedirect(reverse("staff_send_notification"))

def export_subject_grades(request, subject_id):
    """View để xuất điểm ra Excel"""
    import csv
    from django.http import HttpResponse
    from student_management_app.models import StudentEnrollment, StudentResult
    
    subject = Subjects.objects.get(id=subject_id)
    enrollments = StudentEnrollment.objects.filter(subject_id=subject_id)
    
    # Tạo HTTP response với content type CSV
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="diem_{subject.subject_code}.csv"'
    
    # Thêm BOM để Excel hiển thị đúng tiếng Việt
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(['STT', 'Mã SV', 'Họ và tên', 'Email', 'Điểm BT (0-100)', 'Điểm thi (0-100)', 'BT×40%', 'Thi×60%', 'Tổng điểm', 'Điểm chữ'])
    
    for idx, enrollment in enumerate(enrollments, 1):
        student = enrollment.student_id
        
        # Lấy điểm
        try:
            result = StudentResult.objects.get(student_id=student.id, subject_id=subject_id)
            # Điểm trong DB là sau khi nhân hệ số (0-40, 0-60)
            assignment_marks_weighted = result.subject_assignment_marks if result.subject_assignment_marks else 0
            exam_marks_weighted = result.subject_exam_marks if result.subject_exam_marks else 0
            
            # Chuyển về điểm gốc (0-100)
            assignment_marks_raw = round(assignment_marks_weighted / 0.4, 1) if assignment_marks_weighted else ''
            exam_marks_raw = round(exam_marks_weighted / 0.6, 1) if exam_marks_weighted else ''
            
            # Tổng điểm
            total = assignment_marks_weighted + exam_marks_weighted
            
            # Tính điểm chữ
            if total >= 95:
                grade = 'A+'
            elif total >= 85:
                grade = 'A'
            elif total >= 70:
                grade = 'B'
            elif total >= 55:
                grade = 'C'
            elif total >= 40:
                grade = 'D'
            else:
                grade = 'F'
        except StudentResult.DoesNotExist:
            assignment_marks_raw = ''
            exam_marks_raw = ''
            assignment_marks_weighted = ''
            exam_marks_weighted = ''
            total = ''
            grade = ''
        
        writer.writerow([
            idx,
            student.admin.username,
            f"{student.admin.first_name} {student.admin.last_name}",
            student.admin.email,
            assignment_marks_raw,
            exam_marks_raw,
            f"{assignment_marks_weighted}" if assignment_marks_weighted else '',
            f"{exam_marks_weighted}" if exam_marks_weighted else '',
            total,
            grade
        ])
    
    return response

@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Staffs.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_all_notification(request):
    staff=Staffs.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})

def staff_add_result(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})

def save_student_result(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id=request.POST.get('student_list')
    assignment_marks=request.POST.get('assignment_marks')
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')


    student_obj=Students.objects.get(admin=student_admin_id)
    subject_obj=Subjects.objects.get(id=subject_id)

    try:
        check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_assignment_marks=assignment_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
        else:
            result=StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("staff_add_result"))

@csrf_exempt
def fetch_result_student(request):
    subject_id=request.POST.get('subject_id')
    student_id=request.POST.get('student_id')
    student_obj=Students.objects.get(admin=student_id)
    result=StudentResult.objects.filter(student_id=student_obj.id,subject_id=subject_id).exists()
    if result:
        result=StudentResult.objects.get(student_id=student_obj.id,subject_id=subject_id)
        result_data={"exam_marks":result.subject_exam_marks,"assign_marks":result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")

def start_live_classroom(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/start_live_classroom.html",{"subjects":subjects,"session_years":session_years})

def start_live_classroom_process(request):
    session_year=request.POST.get("session_year")
    subject=request.POST.get("subject")

    subject_obj=Subjects.objects.get(id=subject)
    session_obj=SessionYearModel.object.get(id=session_year)
    checks=OnlineClassRoom.objects.filter(subject=subject_obj,session_years=session_obj,is_active=True).exists()
    if checks:
        data=OnlineClassRoom.objects.get(subject=subject_obj,session_years=session_obj,is_active=True)
        room_pwd=data.room_pwd
        roomname=data.room_name
    else:
        room_pwd=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        roomname=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        staff_obj=Staffs.objects.get(admin=request.user.id)
        onlineClass=OnlineClassRoom(room_name=roomname,room_pwd=room_pwd,subject=subject_obj,session_years=session_obj,started_by=staff_obj,is_active=True)
        onlineClass.save()

    return render(request,"staff_template/live_class_room_start.html",{"username":request.user.username,"password":room_pwd,"roomid":roomname,"subject":subject_obj.subject_name,"session_year":session_obj})


def returnHtmlWidget(request):
    return render(request,"widget.html")


# ============= SUBJECT DESCRIPTION MANAGEMENT =============
def manage_subject_description(request):
    """Quản lý file mô tả môn học của giảng viên"""
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    # Lấy thêm thông tin về số lượng files đã upload cho mỗi subject
    for subject in subjects:
        subject.uploaded_files_count = subject.description_files.count()
    return render(request, "staff_template/manage_subject_description.html", {"subjects": subjects})


def staff_manage_subject_description(request, subject_id):
    """Quản lý file mô tả cho một môn học cụ thể"""
    try:
        subject = Subjects.objects.get(id=subject_id, staff_id=request.user.id)
        description_files = subject.description_files.all().order_by('-uploaded_at')
        
        return render(request, "staff_template/staff_manage_subject_description.html", {
            "subject": subject,
            "description_files": description_files
        })
    except Subjects.DoesNotExist:
        messages.error(request, "Không tìm thấy môn học hoặc bạn không có quyền truy cập")
        return HttpResponseRedirect(reverse("staff_my_subjects"))


def upload_subject_description(request, subject_id):
    """Upload nhiều file PDF mô tả môn học (tối đa 3 files)"""
    if request.method == "POST":
        try:
            subject = Subjects.objects.get(id=subject_id, staff_id=request.user.id)
            
            # DEBUG: In ra để kiểm tra
            print("="*50)
            print(f"DEBUG - POST data keys: {request.POST.keys()}")
            print(f"DEBUG - FILES data keys: {request.FILES.keys()}")
            print(f"DEBUG - Content-Type: {request.content_type}")
            
            # Thử cả hai cách lấy files
            files = request.FILES.getlist('subject_description_files')
            print(f"DEBUG - getlist() returned: {len(files)} files")
            
            # Nếu getlist không có kết quả, thử lấy từng file
            if not files:
                print("DEBUG - Trying alternative method...")
                for key in request.FILES.keys():
                    print(f"DEBUG - Found key in FILES: {key}")
                    file_item = request.FILES[key]
                    files.append(file_item)
            
            print(f"DEBUG - Final file count: {len(files)}")
            for idx, f in enumerate(files):
                print(f"DEBUG - File {idx+1}: {f.name} ({f.size} bytes)")
            print("="*50)
            
            if not files:
                messages.error(request, "Không có file nào được chọn. Vui lòng chọn ít nhất 1 file PDF")
                return HttpResponseRedirect(reverse("manage_subject_description"))
            
            # Giới hạn tối đa 3 files
            if len(files) > 3:
                messages.error(request, f"Bạn đã chọn {len(files)} files. Chỉ được upload tối đa 3 files cùng lúc")
                return HttpResponseRedirect(reverse("manage_subject_description"))
            
            uploaded_count = 0
            skipped_files = []
            fs = FileSystemStorage()
            
            for description_file in files:
                print(f"DEBUG - Processing file: {description_file.name}")
                
                # Kiểm tra file có phải PDF không
                if not description_file.name.lower().endswith('.pdf'):
                    skipped_files.append(description_file.name)
                    continue
                    
                # Lưu file
                filename = fs.save(description_file.name, description_file)
                print(f"DEBUG - Saved file as: {filename}")
                
                # Tạo record trong database
                SubjectDescriptionFile.objects.create(
                    subject=subject,
                    file=filename,
                    file_name=description_file.name
                )
                uploaded_count += 1
            
            if uploaded_count > 0:
                msg = f"✅ Đã upload thành công {uploaded_count} file(s)"
                if skipped_files:
                    msg += f". Bỏ qua {len(skipped_files)} file không phải PDF: {', '.join(skipped_files)}"
                messages.success(request, msg)
            else:
                messages.error(request, "Không tìm thấy file PDF hợp lệ nào")
                
            return HttpResponseRedirect(reverse("manage_subject_description"))
        except Exception as e:
            import traceback
            print(f"DEBUG - Exception: {str(e)}")
            print(f"DEBUG - Traceback: {traceback.format_exc()}")
            messages.error(request, f"Lỗi khi upload files: {str(e)}")
            return HttpResponseRedirect(reverse("manage_subject_description"))
    else:
        return HttpResponse("<h2>Method Not Allowed</h2>")


def delete_subject_description(request, subject_id):
    """Xóa một file mô tả môn học cụ thể"""
    try:
        # subject_id ở đây thực chất là file_id
        file_obj = SubjectDescriptionFile.objects.get(id=subject_id)
        
        # Kiểm tra quyền: chỉ giảng viên của môn học mới có quyền xóa
        if file_obj.subject.staff_id.id != request.user.id:
            messages.error(request, "You don't have permission to delete this file")
            return HttpResponseRedirect(reverse("manage_subject_description"))
        
        # Xóa file vật lý
        if file_obj.file:
            import os
            if os.path.isfile(file_obj.file.path):
                os.remove(file_obj.file.path)
        
        # Xóa record trong database
        file_obj.delete()
        messages.success(request, "Successfully Deleted File")
    except Exception as e:
        messages.error(request, f"Failed to Delete File: {str(e)}")
    
    return HttpResponseRedirect(reverse("manage_subject_description"))
