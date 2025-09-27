from django.db import models

class Classroom(models.Model):
    """Model cho lớp học"""
    class_name = models.CharField(max_length=20, unique=True, verbose_name="Tên lớp")
    major = models.CharField(max_length=50, verbose_name="Ngành")
    year = models.CharField(max_length=10, verbose_name="Khóa")
    teacher_name = models.CharField(max_length=100, verbose_name="Giảng viên chủ nhiệm")
    room = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phòng học")
    student_count = models.PositiveIntegerField(default=0, verbose_name="Số sinh viên")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang hoạt động', 'Đang hoạt động'),
            ('Tạm dừng', 'Tạm dừng'),
            ('Kết thúc', 'Kết thúc'),
        ],
        default='Đang hoạt động',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'classrooms'
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.class_name
