# Đoạn code này có thể đặt trong bất kỳ module Python nào, không yêu cầu IPython
# đang chạy sẵn. Nó chỉ tạo lớp con magics nhưng chưa khởi tạo đối tượng.
from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.core.magics.osm import OSMagics

@magics_class
class AutogradingMagics(Magics):
    @cell_magic
    def tee(self, line, cell):
        osm = OSMagics()
        self.shell.run_cell(cell)
        osm.writefile(line, cell)

# Để thực sự sử dụng các magic này, bạn phải đăng ký chúng với một
# phiên IPython đang chạy.

def load_ipython_extension(ipython):
    """
    Bất kỳ file module nào định nghĩa hàm có tên `load_ipython_extension`
    đều có thể được tải thông qua `%load_ext module.path` hoặc được cấu hình
    để IPython tự động tải khi khởi động.
    """
    # Bạn có thể đăng ký class mà không cần khởi tạo đối tượng. IPython sẽ
    # tự gọi constructor mặc định.
    ipython.register_magics(AutogradingMagics)
