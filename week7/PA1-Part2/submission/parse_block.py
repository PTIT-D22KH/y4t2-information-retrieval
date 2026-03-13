class BSBIIndex(BSBIIndex):            
    def parse_block(self, block_dir_relative):
        """Phân tích file văn bản đã tokenize thành các cặp termID-docID

        Tham số
        ----------
        block_dir_relative : str
            Đường dẫn tương đối đến thư mục chứa các file của khối

        Trả về
        -------
        List[Tuple[Int, Int]]
            Trả về tất cả các cặp td_pairs được trích xuất từ khối

        Nên sử dụng self.term_id_map và self.doc_id_map để lấy termID và docID.
        Chúng được duy trì qua các lần gọi parse_block
        """
        ### Bắt đầu code của bạn
        block_dir = os.path.join(self.data_dir, block_dir_relative)
        term_doc_pair = []
        for filename in os.listdir(block_dir):
            file_path = os.path.join(block_dir, filename)
            relative_path = os.path.join(block_dir_relative, filename)
            doc_id = self.doc_id_map[relative_path]
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    tokens = line.split()
                    for token in tokens:
                        term_id = self.term_id_map[token.strip()]
                        term_doc_pair.append((term_id, doc_id))
        return term_doc_pair
        ### Kết thúc code của bạn
