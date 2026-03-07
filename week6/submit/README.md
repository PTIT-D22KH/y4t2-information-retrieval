Hướng dẫn bắt đầu
==================

Cài đặt Conda
--------------
Chúng ta sẽ sử dụng Conda để có được bộ cài đặt chuẩn của Python và các gói hữu ích liên quan. Nếu bạn chưa sử dụng, hãy cài đặt theo hướng dẫn dành cho từng nền tảng tại [trang cài đặt Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Tạo môi trường mới
-------------------
Chúng tôi đã cung cấp file cấu hình môi trường cho bài tập này.
Để tạo môi trường mới với các gói cần thiết, chạy lệnh

     conda env create -f environment.yml


Lệnh này sẽ tạo một môi trường mới có tên int14158-pa1. Bạn có thể kích hoạt nó bằng lệnh

     conda activate int14158-pa1

Khi hoàn thành bài tập, bạn có thể tắt môi trường bằng lệnh

     conda deactivate

Nếu bạn dùng conda phiên bản v4.4 trở lên, hãy sử dụng `conda activate int14158-pa1` và tương tự `conda deactivate`


Mở Jupyter Notebook
--------------------
Chúng ta sẽ sử dụng Jupyter Notebook để làm bài tập. Bạn có thể bắt đầu phiên làm việc mới bằng lệnh

      jupyter notebook

Lệnh này sẽ khởi động một máy chủ cục bộ mà bạn có thể kết nối bằng trình duyệt.
