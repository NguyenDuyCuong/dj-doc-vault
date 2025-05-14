# Chạy Django với Ngrok

Ngrok giúp bạn dễ dàng tạo một URL công khai để truy cập vào server Django chạy trên máy cục bộ. Điều này đặc biệt hữu ích khi bạn cần kiểm tra webhook hoặc chia sẻ ứng dụng mà không cần triển khai lên máy chủ.

## Hướng dẫn nhanh:
1. **Cài đặt ngrok** nếu chưa có:  
   ```sh
   pip install pyngrok
   ```
2. **Thêm `.ngrok.io` vào `ALLOWED_HOSTS`** trong `settings.py`.
3. **Khởi động server Django:**  
   ```sh
   python manage.py runserver
   ```
4. **Mở đường hầm ngrok:**  
   ```sh
   ngrok http 8000
   ```
5. **Sử dụng URL ngrok** để truy cập ứng dụng hoặc kiểm thử API.
