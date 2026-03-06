class IdMap:
    """Lớp trợ giúp để lưu trữ ánh xạ từ chuỗi sang id."""
    def __init__(self):
        self.str_to_id = {}
        self.id_to_str = []
        
    def __len__(self):
        """Trả về số lượng term được lưu trong IdMap"""
        return len(self.id_to_str)
        
    def _get_str(self, i):
        """Trả về chuỗi tương ứng với id (`i`) cho trước."""
        ### Bắt đầu code của bạn
        return self.id_to_str[i]
        ### Kết thúc code của bạn
        
    def _get_id(self, s):
        """Trả về id tương ứng với chuỗi (`s`). 
        Nếu `s` chưa có trong IdMap, gán một id mới và trả về id mới đó.
        """
        ### Bắt đầu code của bạn
        if s not in self.str_to_id:
            current_id = len(self.id_to_str)
            self.str_to_id[s] = current_id
            self.id_to_str.append(s)
            return current_id
        else:
            return self.str_to_id[s]
        ### Kết thúc code của bạn
            
    def __getitem__(self, key):
        """Nếu `key` là số nguyên, sử dụng _get_str; 
           Nếu `key` là chuỗi, sử dụng _get_id;"""
        if type(key) is int:
            return self._get_str(key)
        elif type(key) is str:
            return self._get_id(key)
        else:
            raise TypeError
