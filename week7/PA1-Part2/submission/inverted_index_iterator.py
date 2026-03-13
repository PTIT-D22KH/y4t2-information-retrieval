class InvertedIndexIterator(InvertedIndex):
    """"""
    def __enter__(self):
        """Thêm initialization_hook vào hàm __enter__ của lớp cha
        """
        super().__enter__()
        self._initialization_hook()
        return self

    def _initialization_hook(self):
        """Sử dụng hàm này để khởi tạo iterator
        """
        ### Bắt đầu code của bạn
        self.start = 0
        self.length = len(self.postings_dict.keys())
        ### Kết thúc code của bạn

    def __iter__(self): 
        return self

    def __next__(self):
        """Trả về cặp (term, postings_list) tiếp theo trong chỉ mục.

        Lưu ý: Hàm này chỉ nên đọc một lượng nhỏ dữ liệu từ 
        file chỉ mục. Cụ thể, bạn không nên cố gắng giữ toàn bộ 
        file chỉ mục trong bộ nhớ.
        """
        ### Bắt đầu code của bạn
        if self.start < self.length:
            term_id = self.term_iter.__next__()
            start_pos, len_postings, len_bytes_postings = self.postings_dict[term_id]
            postings_binary = self.index_file.read(len_bytes_postings)
            postings = self.postings_encoding.decode(postings_binary)
            self.start += 1
            return (term_id, postings)
        else:
            raise StopIteration
        ### Kết thúc code của bạn

    def delete_from_disk(self):
        """Đánh dấu chỉ mục để xóa khi thoát. Hữu ích cho chỉ mục tạm thời
        """
        self.delete_upon_exit = True

    def __exit__(self, exception_type, exception_value, traceback):
        """Xóa file chỉ mục khi thoát context cùng với 
        các hàm __exit__ của lớp cha"""
        self.index_file.close()
        if hasattr(self, 'delete_upon_exit') and self.delete_upon_exit:
            os.remove(self.index_file_path)
            os.remove(self.metadata_file_path)
        else:
            with open(self.metadata_file_path, 'wb') as f:
                pkl.dump([self.postings_dict, self.terms], f)
