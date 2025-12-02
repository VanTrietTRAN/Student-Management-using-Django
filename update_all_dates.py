"""
Comprehensive script to update ALL dates in the system to 2025-2026
Run this script with: python update_all_dates.py
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import (
    Students, Staffs, Subjects, Attendance, AttendanceReport,
    LeaveReportStudent, LeaveReportStaff, StudentResult,
    OnlineClassRoom, Schedule, SessionYearModel
)

def shift_date_to_2025(old_date):
    """Shift any date to 2025 keeping month and day"""
    if not old_date:
        return old_date
    
    year_diff = 2025 - old_date.year
    
    if year_diff <= 0:
        return old_date  # Already 2025 or later
    
    try:
        return old_date.replace(year=2025)
    except ValueError:
        # Handle leap year (Feb 29)
        return old_date.replace(year=2025, day=28)

def update_all_system_dates():
    """Update all dates in the system to align with 2025-2026"""
    try:
        print("\n" + "="*60)
        print("COMPREHENSIVE DATE UPDATE - 2025-2026")
        print("="*60)
        
        # 1. Update Schedules
        print("\n📅 Updating Schedules...")
        schedules = Schedule.objects.all()
        updated_schedules = 0
        for schedule in schedules:
            if schedule.session_year_id.session_start_year.year < 2025:
                session_2025 = SessionYearModel.objects.first()
                schedule.session_year_id = session_2025
                schedule.save()
                updated_schedules += 1
        print(f"   ✅ Updated {updated_schedules} schedule(s)")
        
        # 2. Update Leave Reports (Students)
        print("\n📅 Updating Student Leave Reports...")
        leave_students = LeaveReportStudent.objects.all()
        updated_leaves_students = 0
        for leave in leave_students:
            old_created = leave.created_at
            if old_created.year < 2025:
                # Update created_at and updated_at
                new_date = shift_date_to_2025(old_created)
                LeaveReportStudent.objects.filter(id=leave.id).update(
                    created_at=new_date,
                    updated_at=new_date
                )
                updated_leaves_students += 1
        print(f"   ✅ Updated {updated_leaves_students} student leave report(s)")
        
        # 3. Update Leave Reports (Staff)
        print("\n📅 Updating Staff Leave Reports...")
        leave_staffs = LeaveReportStaff.objects.all()
        updated_leaves_staffs = 0
        for leave in leave_staffs:
            old_created = leave.created_at
            if old_created.year < 2025:
                new_date = shift_date_to_2025(old_created)
                LeaveReportStaff.objects.filter(id=leave.id).update(
                    created_at=new_date,
                    updated_at=new_date
                )
                updated_leaves_staffs += 1
        print(f"   ✅ Updated {updated_leaves_staffs} staff leave report(s)")
        
        # 4. Update Student Results
        print("\n📅 Updating Student Results...")
        results = StudentResult.objects.all()
        updated_results = 0
        for result in results:
            if result.created_at.year < 2025:
                new_date = shift_date_to_2025(result.created_at)
                StudentResult.objects.filter(id=result.id).update(
                    created_at=new_date,
                    updated_at=new_date
                )
                updated_results += 1
        print(f"   ✅ Updated {updated_results} student result(s)")
        
        # 5. Update Online Classrooms
        print("\n📅 Updating Online Classrooms...")
        classrooms = OnlineClassRoom.objects.all()
        updated_classrooms = 0
        for classroom in classrooms:
            changed = False
            if classroom.session_years.session_start_year.year < 2025:
                session_2025 = SessionYearModel.objects.first()
                classroom.session_years = session_2025
                changed = True
            if classroom.created_on.year < 2025:
                new_date = shift_date_to_2025(classroom.created_on)
                OnlineClassRoom.objects.filter(id=classroom.id).update(created_on=new_date)
                changed = True
            if changed:
                updated_classrooms += 1
        print(f"   ✅ Updated {updated_classrooms} online classroom(s)")
        
        # 6. Update Students created_at
        print("\n📅 Updating Student Records...")
        students = Students.objects.all()
        updated_students = 0
        for student in students:
            changed = False
            if student.created_at.year < 2025:
                new_date = shift_date_to_2025(student.created_at)
                Students.objects.filter(id=student.id).update(
                    created_at=new_date,
                    updated_at=new_date
                )
                changed = True
            if student.session_year_id.session_start_year.year < 2025:
                session_2025 = SessionYearModel.objects.first()
                Students.objects.filter(id=student.id).update(session_year_id=session_2025)
                changed = True
            if changed:
                updated_students += 1
        print(f"   ✅ Updated {updated_students} student record(s)")
        
        # 7. Update Staffs created_at
        print("\n📅 Updating Staff Records...")
        staffs = Staffs.objects.all()
        updated_staffs = 0
        for staff in staffs:
            if staff.created_at.year < 2025:
                new_date = shift_date_to_2025(staff.created_at)
                Staffs.objects.filter(id=staff.id).update(
                    created_at=new_date,
                    updated_at=new_date
                )
                updated_staffs += 1
        print(f"   ✅ Updated {updated_staffs} staff record(s)")
        
        # Summary
        print("\n" + "="*60)
        print("📊 UPDATE SUMMARY:")
        print("="*60)
        print(f"   Schedules:              {updated_schedules}")
        print(f"   Student Leave Reports:  {updated_leaves_students}")
        print(f"   Staff Leave Reports:    {updated_leaves_staffs}")
        print(f"   Student Results:        {updated_results}")
        print(f"   Online Classrooms:      {updated_classrooms}")
        print(f"   Student Records:        {updated_students}")
        print(f"   Staff Records:          {updated_staffs}")
        print("="*60)
        print("✅ ALL DATES UPDATED SUCCESSFULLY TO 2025-2026!")
        print("="*60 + "\n")
            
    except Exception as e:
        print(f"\n❌ Error updating dates: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_all_system_dates()
