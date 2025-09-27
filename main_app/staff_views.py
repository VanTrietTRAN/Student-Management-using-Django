import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_students = Student.objects.filter(course=staff.course).count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    subjects = Subject.objects.filter(staff=staff)
    total_subject = subjects.count()
    attendance_list = Attendance.objects.filter(subject__in=subjects)
    total_attendance = attendance_list.count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name)
        attendance_list.append(attendance_count)
    context = {
        'page_title': 'Staff Panel - ' + str(staff.admin.last_name) + ' (' + str(staff.course) + ')',
        'total_students': total_students,
        'total_attendance': total_attendance,
        'total_leave': total_leave,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list
    }
    return render(request, 'staff_template/home_content.html', context)




def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None,instance=staff)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = staff.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                staff.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "staff_template/staff_view_profile.html", context)

    return render(request, "staff_template/staff_view_profile.html", context)


@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def staff_view_notification(request):
    staff = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationStaff.objects.filter(staff=staff)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "staff_template/staff_view_notification.html", context)




# ===== NEW STAFF FEATURES =====

def staff_manage_students(request):
    """Quản lý danh sách sinh viên - hiển thị, thêm, sửa, xóa"""
    staff = get_object_or_404(Staff, admin=request.user)
    students = Student.objects.filter(course=staff.course)
    context = {
        'page_title': 'Manage Students',
        'students': students,
        'staff': staff
    }
    return render(request, 'staff_template/staff_manage_students.html', context)


def staff_add_student(request):
    """Thêm sinh viên mới"""
    staff = get_object_or_404(Staff, admin=request.user)
    form = StudentForm(request.POST or None, request.FILES or None)
    context = {
        'form': form,
        'page_title': 'Add Student',
        'staff': staff
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                user = CustomUser.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    user_type=3,
                    gender=form.cleaned_data['gender'],
                    address=form.cleaned_data['address'],
                    profile_pic=form.cleaned_data['profile_pic']
                )
                student = Student.objects.create(
                    admin=user,
                    course=staff.course,
                    session=form.cleaned_data['session']
                )
                messages.success(request, "Student added successfully!")
                return redirect('staff_manage_students')
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
        else:
            messages.error(request, "Form has errors!")
    return render(request, 'staff_template/staff_add_student.html', context)


def staff_edit_student(request, student_id):
    """Sửa thông tin sinh viên"""
    staff = get_object_or_404(Staff, admin=request.user)
    student = get_object_or_404(Student, id=student_id, course=staff.course)
    form = StudentEditForm(request.POST or None, request.FILES or None, instance=student)
    context = {
        'form': form,
        'page_title': 'Edit Student',
        'student': student,
        'staff': staff
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                user = student.admin
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.gender = form.cleaned_data['gender']
                user.address = form.cleaned_data['address']
                
                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])
                
                if form.cleaned_data['profile_pic']:
                    user.profile_pic = form.cleaned_data['profile_pic']
                
                user.save()
                student.session = form.cleaned_data['session']
                student.save()
                messages.success(request, "Student updated successfully!")
                return redirect('staff_manage_students')
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
        else:
            messages.error(request, "Form has errors!")
    return render(request, 'staff_template/staff_edit_student.html', context)


def staff_delete_student(request, student_id):
    """Xóa sinh viên"""
    staff = get_object_or_404(Staff, admin=request.user)
    student = get_object_or_404(Student, id=student_id, course=staff.course)
    try:
        student.admin.delete()  # This will also delete the student due to CASCADE
        messages.success(request, "Student deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")
    return redirect('staff_manage_students')


def staff_students_grades(request):
    """Trang nhập điểm trực tiếp trên bảng danh sách sinh viên"""
    staff = get_object_or_404(Staff, admin=request.user)
    students = Student.objects.filter(course=staff.course)
    subjects = Subject.objects.filter(staff=staff)
    courses = Course.objects.all()
    sessions = Session.objects.all()
    
    print(f"Staff: {staff}")
    print(f"Staff course: {staff.course}")
    print(f"Students count: {students.count()}")
    print(f"Subjects count: {subjects.count()}")
    print(f"All courses count: {courses.count()}")
    
    # Handle AJAX request for getting students by course
    if request.method == 'GET' and request.GET.get('course_id'):
        course_id = request.GET.get('course_id')
        print(f"AJAX request received for course_id: {course_id}")
        
        try:
            course = get_object_or_404(Course, id=course_id)
            print(f"Course found: {course.name}")
            
            # Get all students in the selected course
            students = Student.objects.filter(course=course)
            print(f"Found {students.count()} students for course {course.name}")
            
            # Debug: print all students
            for student in students:
                print(f"Student: {student.admin.last_name}, {student.admin.first_name} - {student.admin.email}")
            
            grades_data = []
            for student in students:
                grades_data.append({
                    'student_id': student.id,
                    'name': f"{student.admin.last_name}, {student.admin.first_name}",
                    'email': student.admin.email,
                    'course': course.name,
                    'test_score': 0,
                    'exam_score': 0,
                    'total': 0
                })
            
            print(f"Returning {len(grades_data)} student records")
            return JsonResponse({'success': True, 'data': grades_data})
        except Exception as e:
            print(f"Error in staff_students_grades: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)})
    
    # If no course_id, return all students for testing
    if request.method == 'GET' and request.GET.get('test') == 'true':
        grades_data = []
        for student in students:
            grades_data.append({
                'student_id': student.id,
                'name': f"{student.admin.last_name}, {student.admin.first_name}",
                'email': student.admin.email,
                'test_score': 0,
                'exam_score': 0,
                'total': 0
            })
        return JsonResponse({'success': True, 'data': grades_data})
    
    context = {
        'page_title': 'Student Grades Management',
        'students': students,
        'subjects': subjects,
        'courses': courses,
        'sessions': sessions,
        'staff': staff
    }
    return render(request, 'staff_template/staff_students_grades.html', context)


@csrf_exempt
def staff_save_grade(request):
    """Lưu điểm sinh viên (AJAX)"""
    if request.method == 'POST':
        try:
            student_id = request.POST.get('student_id')
            subject_id = request.POST.get('subject_id')
            test_score = request.POST.get('test_score', 0)
            exam_score = request.POST.get('exam_score', 0)
            
            student = get_object_or_404(Student, id=student_id)
            subject = get_object_or_404(Subject, id=subject_id)
            
            # Kiểm tra xem staff có quyền dạy môn này không
            staff = get_object_or_404(Staff, admin=request.user)
            if subject.staff != staff:
                return JsonResponse({'success': False, 'message': 'Unauthorized'})
            
            result, created = StudentResult.objects.get_or_create(
                student=student,
                subject=subject,
                defaults={'test': test_score, 'exam': exam_score}
            )
            
            if not created:
                result.test = test_score
                result.exam = exam_score
                result.save()
            
            return JsonResponse({'success': True, 'message': 'Grade saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def staff_create_notification(request):
    """Tạo thông báo mới"""
    staff = get_object_or_404(Staff, admin=request.user)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        target_type = request.POST.get('target_type')  # 'all', 'course', 'specific'
        target_course = request.POST.get('target_course')
        specific_students = request.POST.getlist('specific_students')
        
        try:
            if target_type == 'all':
                # Gửi cho tất cả sinh viên
                students = Student.objects.all()
                for student in students:
                    NotificationStudent.objects.create(
                        student=student,
                        message=message
                    )
            elif target_type == 'course':
                # Gửi cho sinh viên trong khóa học
                course = get_object_or_404(Course, id=target_course)
                students = Student.objects.filter(course=course)
                for student in students:
                    NotificationStudent.objects.create(
                        student=student,
                        message=message
                    )
            elif target_type == 'specific':
                # Gửi cho sinh viên cụ thể
                for student_id in specific_students:
                    student = get_object_or_404(Student, id=student_id)
                    NotificationStudent.objects.create(
                        student=student,
                        message=message
                    )
            
            messages.success(request, "Notification sent successfully!")
            return redirect('staff_create_notification')
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")
    
    # Lấy danh sách sinh viên trong khóa học của staff
    students = Student.objects.filter(course=staff.course)
    courses = Course.objects.all()
    
    context = {
        'page_title': 'Create Notification',
        'students': students,
        'courses': courses,
        'staff': staff
    }
    return render(request, 'staff_template/staff_create_notification.html', context)


def staff_edit_profile(request):
    """Trang sửa thông tin cá nhân của staff (tối ưu hóa)"""
    staff = get_object_or_404(Staff, admin=request.user)
    user = staff.admin
    
    # Initialize form with user data
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'gender': user.gender,
        'address': user.address,
    }
    
    form = StaffEditForm(request.POST or None, request.FILES or None, initial=initial_data)
    context = {
        'form': form,
        'page_title': 'Edit Profile',
        'staff': staff
    }
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.gender = form.cleaned_data['gender']
                user.address = form.cleaned_data['address']
                
                if form.cleaned_data['password']:
                    user.set_password(form.cleaned_data['password'])
                
                if form.cleaned_data['profile_pic']:
                    user.profile_pic = form.cleaned_data['profile_pic']
                
                user.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('staff_edit_profile')
            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
        else:
            messages.error(request, "Form has errors!")
    
    return render(request, 'staff_template/staff_edit_profile.html', context)
