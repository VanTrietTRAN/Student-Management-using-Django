from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create default groups (Staff, Student) and assign sensible permissions"

    def handle(self, *args, **options):
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        student_group, _ = Group.objects.get_or_create(name="Student")

        # Example: allow staff to add/update attendance and results
        staff_perms_codenames = [
            "add_attendance", "change_attendance", "view_attendance",
            "add_attendancereport", "change_attendancereport", "view_attendancereport",
            "add_studentresult", "change_studentresult", "view_studentresult",
            "view_student", "view_subject", "view_course",
        ]

        # Example: allow students to view own attendance/result (kept as view model perms)
        student_perms_codenames = [
            "view_attendance", "view_attendancereport",
            "view_studentresult", "view_subject", "view_course",
        ]

        def assign_perms(group: Group, codenames: list[str]):
            perms = Permission.objects.filter(codename__in=codenames)
            group.permissions.set(perms)
            group.save()

        assign_perms(staff_group, staff_perms_codenames)
        assign_perms(student_group, student_perms_codenames)

        self.stdout.write(self.style.SUCCESS("Default groups and permissions have been set up."))


