class InvertedIndexMapper(InvertedIndex):
    def __getitem__(self, key):
        return self._get_postings_list(key)
    
    def _get_postings_list(self, term):
        """Lấy danh sách posting (các docId) cho `term`.
        
        Hàm này không nên duyệt qua file chỉ mục.
        Tức là, nó chỉ cần đọc các byte từ file chỉ mục 
        tương ứng với danh sách posting cho term được yêu cầu.
        """
        ### Bắt đầu code của bạn
        postings_start, posting_num, posting_bytes = self.postings_dict[term]
        self.index_file.seek(postings_start, 0)
        postings_binary = self.index_file.read(posting_bytes)
        postings = self.postings_encoding.decode(postings_binary)
        return postings
        ### Kết thúc code của bạn
