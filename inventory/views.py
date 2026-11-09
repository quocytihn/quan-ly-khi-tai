import base64, io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from openpyxl import Workbook
import qrcode
from .models import Asset, Category, Location, Transaction, Stocktake
from .forms import AssetForm, TransactionForm, StocktakeForm

@login_required
def dashboard(request):
    assets = Asset.objects.all()
    status_data = [{'label': label, 'count': assets.filter(status=key).count()} for key,label in Asset.STATUS]
    context = {'total_assets': assets.count(), 'total_quantity': assets.aggregate(v=Sum('quantity'))['v'] or 0,
      'in_use': assets.filter(status='IN_USE').count(), 'maintenance': assets.filter(status='MAINTENANCE').count(),
      'categories': Category.objects.count(), 'locations': Location.objects.count(),
      'recent': assets[:6], 'recent_transactions': Transaction.objects.select_related('asset')[:6],
      'status_data': status_data}
    return render(request,'inventory/dashboard.html',context)

@login_required
def asset_list(request):
    q=request.GET.get('q','').strip(); status=request.GET.get('status','')
    assets=Asset.objects.select_related('category','location')
    if q: assets=assets.filter(Q(code__icontains=q)|Q(name__icontains=q)|Q(serial_number__icontains=q)|Q(category__name__icontains=q))
    if status: assets=assets.filter(status=status)
    return render(request,'inventory/asset_list.html',{'assets':assets,'q':q,'status':status,'statuses':Asset.STATUS})

@login_required
def asset_create(request):
    form=AssetForm(request.POST or None)
    if form.is_valid():
        obj=form.save(); messages.success(request,'Đã thêm hồ sơ khí tài.'); return redirect('asset_detail',pk=obj.pk)
    return render(request,'inventory/asset_form.html',{'form':form,'title':'Thêm khí tài'})

@login_required
def asset_edit(request,pk):
    obj=get_object_or_404(Asset,pk=pk); form=AssetForm(request.POST or None,instance=obj)
    if form.is_valid(): form.save(); messages.success(request,'Đã cập nhật hồ sơ.'); return redirect('asset_detail',pk=obj.pk)
    return render(request,'inventory/asset_form.html',{'form':form,'title':'Cập nhật khí tài'})

@login_required
def asset_detail(request,pk):
    obj=get_object_or_404(Asset.objects.select_related('category','location'),pk=pk)
    return render(request,'inventory/asset_detail.html',{'asset':obj,'transactions':obj.transactions.all()[:10]})

@login_required
def asset_delete(request,pk):
    obj=get_object_or_404(Asset,pk=pk)
    if request.method=='POST': obj.delete(); messages.success(request,'Đã xóa hồ sơ.'); return redirect('asset_list')
    return render(request,'inventory/confirm_delete.html',{'object':obj})

@login_required
def asset_qr(request,pk):
    obj=get_object_or_404(Asset,pk=pk)
    url=request.build_absolute_uri(f'/scan/?code={obj.code}')
    img=qrcode.make(url); buf=io.BytesIO(); img.save(buf,format='PNG')
    encoded=base64.b64encode(buf.getvalue()).decode()
    return render(request,'inventory/qr.html',{'asset':obj,'qr_data':encoded,'scan_url':url})

def scan(request):
    code=request.GET.get('code','').strip()
    asset=Asset.objects.filter(Q(code=code)|Q(qr_token__iexact=code)).first() if code else None
    return render(request,'inventory/scan.html',{'asset':asset,'code':code})

@login_required
def transactions(request):
    return render(request,'inventory/transactions.html',{'transactions':Transaction.objects.select_related('asset','performed_by')[:200]})

@login_required
def transaction_create(request):
    form=TransactionForm(request.POST or None)
    if form.is_valid():
        tx=form.save(commit=False); tx.performed_by=request.user
        asset=tx.asset
        if tx.action=='IMPORT': asset.quantity += tx.quantity
        elif tx.action in ('EXPORT','HANDOVER'):
            if tx.quantity>asset.quantity: form.add_error('quantity','Số lượng giao/xuất vượt quá số lượng hiện có.')
            else:
                asset.quantity -= tx.quantity
                if tx.action=='HANDOVER': asset.status='IN_USE'; asset.assigned_to=tx.to_person
        elif tx.action=='RETURN':
            asset.quantity += tx.quantity; asset.status='IN_STOCK'; asset.assigned_to=''
        elif tx.action=='ADJUST':
            asset.quantity = tx.quantity
        if not form.errors:
            asset.save(); tx.save(); messages.success(request,'Đã ghi nhận nghiệp vụ.'); return redirect('transactions')
    return render(request,'inventory/transaction_form.html',{'form':form})

@login_required
def stocktake(request):
    form=StocktakeForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False); obj.expected_quantity=obj.asset.quantity; obj.checked_by=request.user; obj.save()
        messages.success(request,'Đã lưu kết quả kiểm kê.'); return redirect('stocktake')
    records=Stocktake.objects.select_related('asset','checked_by')[:100]
    return render(request,'inventory/stocktake.html',{'form':form,'records':records})

@login_required
def reports(request):
    assets=Asset.objects.select_related('category','location')
    return render(request,'inventory/reports.html',{'assets':assets,'total_value':sum(a.price*a.quantity for a in assets),'total_quantity':sum(a.quantity for a in assets)})

@login_required
def export_excel(request):
    wb=Workbook(); ws=wb.active; ws.title='Danh sach khi tai'
    ws.append(['Mã','Tên khí tài','Chủng loại','Serial','Số lượng','Đơn vị','Trạng thái','Vị trí','Người sử dụng','Nguyên giá'])
    for a in Asset.objects.select_related('category','location'):
        ws.append([a.code,a.name,a.category.name,a.serial_number,a.quantity,a.unit,a.get_status_display(),a.location.name if a.location else '',a.assigned_to,float(a.price)])
    response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition']='attachment; filename="bao_cao_khi_tai.xlsx"'; wb.save(response); return response
