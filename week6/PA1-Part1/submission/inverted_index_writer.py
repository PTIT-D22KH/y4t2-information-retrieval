class InvertedIndexWriter(InvertedIndex):
    """"""
    def __enter__(self):
        self.index_file = open(self.index_file_path, 'wb+')              
        return self

    def append(self, term, postings_list):
        """Thêm term và postings_list vào cuối file chỉ mục.
        
        Hàm này thực hiện ba việc:
        1. Mã hóa postings_list sử dụng self.postings_encoding
        2. Lưu metadata dưới dạng self.terms và self.postings_dict
           Lưu ý rằng self.postings_dict ánh xạ termID sang bộ 3 gồm 
           (vị_trí_bắt_đầu_trong_file_index, 
           số_posting_trong_danh_sách, 
           độ_dài_byte_của_danh_sách_posting)
        3. Thêm luồng byte vào file chỉ mục trên đĩa

        Gợi ý: Bạn có thể thấy hữu ích khi đọc tài liệu Python I/O
        (https://docs.python.org/3/tutorial/inputoutput.html) để biết
        thông tin về cách thêm vào cuối file.
        
        Tham số
        ----------
        term:
            term hoặc termID là định danh duy nhất cho term
        postings_list: List[Int]
            Danh sách các docID nơi term xuất hiện
        """
        ### Bắt đầu code của bạn
        encoded_postings_list = self.postings_encoding.encode(sorted(postings_list))
        last_term = self.terms[-1] if len(self.terms) != 0 else None
        start_pos =  (self.postings_dict[last_term][0] + self.postings_dict[last_term][2]) if last_term is not None else 0
        self.postings_dict[term] = (start_pos, len(postings_list), len(encoded_postings_list))
        self.terms.append(term)
        self.index_file.write(encoded_postings_list)

        ### Kết thúc code của bạn
