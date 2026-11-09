import uuid
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('Tên chủng loại', max_length=120, unique=True)
    description = models.TextField('Mô tả', blank=True)
    def __str__(self): return self.name

class Location(models.Model):
    name = models.CharField('Tên vị trí', max_length=150, unique=True)
    description = models.CharField('Mô tả', max_length=255, blank=True)
    def __str__(self): return self.name

class Asset(models.Model):
    STATUS = [('IN_STOCK','Trong kho'),('IN_USE','Đang sử dụng'),('MAINTENANCE','Bảo trì'),('LIQUIDATED','Thanh lý'),('LOST','Thất lạc')]
    code = models.CharField('Mã khí tài', max_length=40, unique=True)
    name = models.CharField('Tên khí tài', max_length=180)
    category = models.ForeignKey(Category, verbose_name='Chủng loại', on_delete=models.PROTECT, related_name='assets')
    serial_number = models.CharField('Số serial', max_length=100, blank=True)
    quantity = models.PositiveIntegerField('Số lượng', default=1)
    unit = models.CharField('Đơn vị tính', max_length=30, default='cái')
    status = models.CharField('Trạng thái', max_length=20, choices=STATUS, default='IN_STOCK')
    location = models.ForeignKey(Location, verbose_name='Vị trí', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.CharField('Người đang sử dụng', max_length=120, blank=True)
    purchase_date = models.DateField('Ngày nhập', null=True, blank=True)
    price = models.DecimalField('Nguyên giá', max_digits=14, decimal_places=0, default=0)
    description = models.TextField('Ghi chú', blank=True)
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.code} - {self.name}'

class Transaction(models.Model):
    TYPES = [('IMPORT','Nhập kho'),('EXPORT','Xuất kho'),('HANDOVER','Bàn giao'),('RETURN','Thu hồi'),('ADJUST','Điều chỉnh')]
    asset = models.ForeignKey(Asset, verbose_name='Khí tài', on_delete=models.CASCADE, related_name='transactions')
    action = models.CharField('Nghiệp vụ', max_length=20, choices=TYPES)
    quantity = models.PositiveIntegerField('Số lượng', default=1)
    from_person = models.CharField('Người giao', max_length=120, blank=True)
    to_person = models.CharField('Người nhận', max_length=120, blank=True)
    note = models.TextField('Ghi chú', blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']

class Stocktake(models.Model):
    asset = models.ForeignKey(Asset, verbose_name='Khí tài', on_delete=models.CASCADE)
    expected_quantity = models.PositiveIntegerField('Số lượng hệ thống')
    actual_quantity = models.PositiveIntegerField('Số lượng thực tế')
    note = models.CharField('Ghi chú', max_length=255, blank=True)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
