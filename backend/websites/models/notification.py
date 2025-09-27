from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    """Model cho thông báo"""
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    content = models.TextField(verbose_name="Nội dung")
    sender = models.CharField(max_length=100, verbose_name="Người gửi")
    target = models.CharField(max_length=100, verbose_name="Đối tượng nhận")
    is_important = models.BooleanField(default=False, verbose_name="Quan trọng")
    is_read = models.BooleanField(default=False, verbose_name="Đã đọc")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        db_table = 'notifications'
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
