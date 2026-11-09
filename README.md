# QUẢN LÝ KHÍ TÀI — Django

Ứng dụng demo quản lý hồ sơ khí tài, mã QR, trạng thái, số lượng, vị trí, bàn giao, kiểm kê và báo cáo Excel.

## Chạy trên máy

Yêu cầu Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Mở http://127.0.0.1:8000. Dữ liệu demo được tạo bằng `seed_demo`; tài khoản quản trị được tạo riêng bằng `createsuperuser`. Không còn mật khẩu quản trị mặc định trong source.

## Deploy lên Render bằng Blueprint

1. Đưa toàn bộ nội dung thư mục dự án (thư mục chứa `manage.py` và `render.yaml`) lên một GitHub repository.
2. Trên Render chọn **New → Blueprint**, kết nối repository và chọn `render.yaml`.
3. Khi Render yêu cầu `ADMIN_PASSWORD`, đặt mật khẩu mạnh tối thiểu 12 ký tự. Không đưa mật khẩu vào GitHub.
4. Chọn Apply. Blueprint tạo Web Service và PostgreSQL, sau đó tự cài thư viện, thu thập static, migrate database, tạo dữ liệu demo và tạo tài khoản quản trị.
5. Khi deploy thành công, mở URL `.onrender.com` do Render cấp. Đăng nhập bằng username `admin` và mật khẩu bạn đã đặt ở bước 3.
6. Vào `/admin/` để quản trị dữ liệu và tài khoản.

## Lưu ý gói miễn phí Render

- Free Web Service tự sleep sau 15 phút không có traffic; lượt truy cập đầu tiên sau khi sleep có thể mất khoảng một phút để khởi động.
- Free Postgres hiện hết hạn sau 30 ngày; hãy nâng cấp trước hạn hoặc sao lưu/chuyển dữ liệu nếu cần giữ lâu dài.
- Không dùng gói miễn phí cho dữ liệu khí tài nhạy cảm hoặc môi trường vận hành thật.

## Chức năng

- Dashboard tổng số hồ sơ, tổng số lượng, đang sử dụng, bảo trì và biểu đồ trạng thái.
- CRUD hồ sơ khí tài, phân loại, serial, số lượng, trạng thái, vị trí, người sử dụng, nguyên giá.
- Tạo mã QR riêng cho từng hồ sơ; trang tra cứu QR công khai chỉ hiển thị thông tin cơ bản.
- Quét QR bằng camera điện thoại hoặc nhập mã để tra cứu. Camera yêu cầu HTTPS trên trình duyệt điện thoại.
- Ghi nhận nhập kho, xuất kho, bàn giao, thu hồi; tự cập nhật số lượng và người sử dụng.
- Kiểm kê, lưu số lượng hệ thống và số lượng thực tế.
- Tìm kiếm, lọc trạng thái, báo cáo và xuất Excel.
- Đăng nhập Django; quản trị tại `/admin/`.

## Ghi chú

Bản này tối ưu cho demo và báo cáo nhanh. Với triển khai thực tế cần bổ sung phân quyền chi tiết, nhật ký thao tác, phê duyệt bàn giao, sao lưu định kỳ, kiểm thử và chính sách bảo mật phù hợp.
