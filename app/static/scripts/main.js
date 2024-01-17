function confirmPayment() {
  // Hiển thị hộp thoại xác nhận
  var isConfirmed = confirm("Bạn có chắc chắn muốn thanh toán không?");

  // Kiểm tra kết quả xác nhận
  if (isConfirmed) {
    // Nếu người dùng chọn "OK", chuyển hướng đến trang thanh toán thành công
    window.location.href = "{{ url_for('index') }}";
  } else {
    // Ngược lại, không làm gì hoặc có thể thực hiện các hành động khác
    console.log("Người dùng đã hủy thanh toán.");
  }
}