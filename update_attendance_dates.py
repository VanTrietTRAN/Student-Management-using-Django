"""
Script to update attendance dates from 2020 to 2025
Run this script with: python update_attendance_dates.py
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import Attendance, SessionYearModel

def update_attendance_dates():
    """Update all attendance dates from 2020 to 2025"""
    try:
        # Get all attendance records
        attendances = Attendance.objects.all()
        
        print(f"Found {attendances.count()} attendance record(s) in database")
        
        if attendances.count() == 0:
            print("\n✅ No attendance records found. Nothing to update.")
            return
        
        print("\nCurrent attendance dates:")
        for att in attendances[:10]:  # Show first 10
            print(f"  ID {att.id}: {att.attendance_date} (Subject: {att.subject_id.subject_name})")
        if attendances.count() > 10:
            print(f"  ... and {attendances.count() - 10} more records")
        
        # Get the new session year (should be 2025-2026)
        try:
            new_session = SessionYearModel.objects.first()
            print(f"\n📅 Target session year: {new_session.session_start_year} to {new_session.session_end_year}")
        except:
            print("\n❌ No session year found in database!")
            return
        
        # Update attendance dates
        print("\n🔄 Updating attendance dates...")
        updated_count = 0
        
        for att in attendances:
            old_date = att.attendance_date
            
            # Calculate the difference in years (from 2020 to 2025)
            if old_date.year == 2020:
                year_diff = 5  # 2020 -> 2025
            elif old_date.year == 2021:
                year_diff = 4  # 2021 -> 2025
            elif old_date.year == 2022:
                year_diff = 3  # 2022 -> 2025
            elif old_date.year == 2023:
                year_diff = 2  # 2023 -> 2025
            elif old_date.year == 2024:
                year_diff = 1  # 2024 -> 2025
            else:
                year_diff = 0  # Already 2025 or later
            
            if year_diff > 0:
                # Update to 2025 keeping the same month and day
                try:
                    new_date = old_date.replace(year=2025)
                except ValueError:
                    # Handle leap year case (Feb 29)
                    new_date = old_date.replace(year=2025, day=28)
                
                att.attendance_date = new_date
                att.session_year_id = new_session
                att.save()
                updated_count += 1
                
                if updated_count <= 10:  # Show first 10 updates
                    print(f"  ✅ Updated ID {att.id}: {old_date} → {new_date}")
        
        if updated_count > 10:
            print(f"  ... and {updated_count - 10} more records")
        
        print(f"\n✅ Successfully updated {updated_count} attendance record(s)!")
        
        # Show updated dates
        print(f"\nUpdated attendance dates (first 10):")
        attendances = Attendance.objects.all().order_by('-attendance_date')[:10]
        for att in attendances:
            print(f"  ID {att.id}: {att.attendance_date} (Subject: {att.subject_id.subject_name})")
            
    except Exception as e:
        print(f"\n❌ Error updating attendance dates: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("ATTENDANCE DATES UPDATE TOOL - 2025")
    print("=" * 60)
    update_attendance_dates()
    print("=" * 60)
