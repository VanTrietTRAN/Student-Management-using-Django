"""
Script to update session year from 2024-2025 to 2025-2026
Run this script with: python update_session_year.py
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_system.settings')
django.setup()

from student_management_app.models import SessionYearModel
from datetime import datetime

def update_session_years():
    """Update all session years to 2025-2026"""
    try:
        # Get all session years
        sessions = SessionYearModel.objects.all()
        
        print(f"Found {sessions.count()} session year(s) in database")
        print("\nCurrent session years:")
        for session in sessions:
            print(f"  ID {session.id}: {session.session_start_year} to {session.session_end_year}")
        
        if sessions.count() == 0:
            # Create new session year if none exists
            print("\nNo session years found. Creating 2025-2026...")
            new_session = SessionYearModel(
                session_start_year=datetime(2025, 1, 1).date(),
                session_end_year=datetime(2026, 12, 31).date()
            )
            new_session.save()
            print(f"✅ Created new session year: 2025-2026 (ID: {new_session.id})")
        else:
            # Update existing session years
            print("\n🔄 Updating session years to 2025-2026...")
            for session in sessions:
                old_start = session.session_start_year
                old_end = session.session_end_year
                
                session.session_start_year = datetime(2025, 1, 1).date()
                session.session_end_year = datetime(2026, 12, 31).date()
                session.save()
                
                print(f"✅ Updated ID {session.id}: {old_start} - {old_end} → 2025-01-01 - 2026-12-31")
        
        print("\n✅ Session year update completed successfully!")
        print(f"\nUpdated session years:")
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            print(f"  ID {session.id}: {session.session_start_year} to {session.session_end_year}")
            
    except Exception as e:
        print(f"\n❌ Error updating session years: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("SESSION YEAR UPDATE TOOL - 2025-2026")
    print("=" * 60)
    update_session_years()
    print("=" * 60)
