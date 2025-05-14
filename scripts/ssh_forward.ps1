# File: ssh_forward.ps1

# Cấu hình hostname đã được định nghĩa trong ~/.ssh/config
$Hostname = "cloud11703157570"

# Danh sách port forwarding theo định dạng "local_port:destination_host:destination_port"
$ForwardPorts = @(
    "5432:localhost:5432",
    "6379:localhost:6379",
    "8080:localhost:8080"
)

# Xây dựng lệnh SSH bắt đầu với option -N (không chạy lệnh từ xa)
$cmd = "ssh -N"

# Lặp qua danh sách port forwarding để nối thêm các tùy chọn -L
foreach ($port in $ForwardPorts) {
    $cmd += " -L $port"
}

# Nối thêm hostname, thông tin user sẽ tự động được lấy từ cấu hình SSH của bạn
$cmd += " $Hostname"

# Hiển thị câu lệnh cuối cùng được xây dựng để phục vụ mục đích debug (có thể ẩn khi sử dụng thực tế)
Write-Host "Executing command: $cmd"

# Thực thi lệnh SSH đã xây dựng
# ssh -N -L 5432:localhost:5432 -L 6379:localhost:6379 -L 8080:localhost:8080 cloud11703157570
Invoke-Expression $cmd
