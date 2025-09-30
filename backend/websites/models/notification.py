from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    content = models.TextField(verbose_name="Nội dung")
    target_role = models.CharField(
        max_length=50,
        choices=[
            ('Toàn trường', 'Toàn trường'),
            ('Khoa CNTT', 'Khoa CNTT'),
            ('Khoa KTPM', 'Khoa KTPM'),
            ('Khoa ATTT', 'Khoa ATTT'),
            ('CNTT21A', 'Lớp CNTT21A'),
            ('CNTT21B', 'Lớp CNTT21B'),
        ],
        default='Toàn trường',
        verbose_name="Đối tượng"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc")

    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.target_role}"