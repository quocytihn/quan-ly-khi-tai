from django.core.management.base import BaseCommand
from inventory.models import Category, Location, Asset
class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu để trình diễn hệ thống'
    def handle(self,*args,**kwargs):
        cats={n:Category.objects.get_or_create(name=n)[0] for n in ['Thiết bị thông tin','Dụng cụ kỹ thuật','Phương tiện','Thiết bị hỗ trợ']}
        locs={n:Location.objects.get_or_create(name=n)[0] for n in ['Kho A1','Phòng kỹ thuật','Đội sử dụng']}
        samples=[('KT-001','Máy bộ đàm cầm tay', 'Thiết bị thông tin',12,'IN_STOCK','Kho A1'),('KT-002','Ống nhòm quan sát','Dụng cụ kỹ thuật',5,'IN_USE','Đội sử dụng'),('KT-003','Máy đo chuyên dụng','Thiết bị hỗ trợ',3,'MAINTENANCE','Phòng kỹ thuật'),('KT-004','Bộ thiết bị liên lạc','Thiết bị thông tin',8,'IN_STOCK','Kho A1'),('KT-005','Thiết bị định vị','Thiết bị hỗ trợ',4,'IN_USE','Đội sử dụng')]
        for code,name,cat,qty,status,loc in samples:
            Asset.objects.get_or_create(code=code,defaults={'name':name,'category':cats[cat],'quantity':qty,'status':status,'location':locs[loc]})
        self.stdout.write(self.style.SUCCESS('Đã tạo dữ liệu demo.'))
