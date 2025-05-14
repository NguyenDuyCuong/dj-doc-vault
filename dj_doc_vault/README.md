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


---
# **Steps to Run Projects**

1. **Forward Ports từ Server qua SSH:**  
   Dùng SSH để forward các cổng cần thiết từ server để truy cập dịch vụ từ xa.

2. **Chạy Frontend:**  
   Sử dụng lệnh sau để khởi động frontend với Tailwind:
   ```bash
   python src/manage.py tailwind start
   ```

3. **Chạy Backend:**  
   Khởi động backend bằng Django với lệnh:
   ```bash
   python src/manage.py runserver
   ```

4. **Forward Domain từ Ngrok:**  
   Nếu bạn cần tạo đường dẫn public qua Ngrok, sử dụng:
   ```bash
   ngrok http 8000
   ```

Các bước này giúp bạn nhanh chóng thiết lập môi trường phát triển cho dự án của mình. Nếu cần thêm hỗ trợ hoặc muốn tinh chỉnh thêm, hãy cho tôi biết nhé! 🚀
