from django.db import models

class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True, verbose_name="Mã môn học")
    subject_name = models.CharField(max_length=100, verbose_name="Tên môn học")
    credits = models.IntegerField(verbose_name="Số tín chỉ")
    major = models.CharField(max_length=50, verbose_name="Ngành")
    type = models.CharField(
        max_length=20,
        choices=[
            ('Bắt buộc', 'Bắt buộc'),
            ('Tự chọn', 'Tự chọn'),
            ('Thực tập', 'Thực tập'),
        ],
        default='Bắt buộc',
        verbose_name="Loại môn"
    )
    semester = models.CharField(max_length=10, verbose_name="Học kỳ")
    teacher_name = models.CharField(max_length=100, verbose_name="Giảng viên")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Đang mở', 'Đang mở'),
            ('Tạm đóng', 'Tạm đóng'),
            ('Kết thúc', 'Kết thúc'),
        ],
        default='Đang mở',
        verbose_name="Trạng thái"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
        ordering = ['subject_code']

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"