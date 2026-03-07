class BSBIIndex(BSBIIndex):
    def retrieve(self, query):
        """Truy xuất các tài liệu tương ứng với truy vấn kết hợp

        Tham số
        ----------
        query: str
            Danh sách các token truy vấn phân cách bằng dấu cách

        Kết quả
        ------
        List[str]
            Danh sách tài liệu đã sắp xếp chứa mỗi token truy vấn. 
            Trả về rỗng nếu không tìm thấy tài liệu.

        KHÔNG nên ném lỗi cho các term không có trong tập dữ liệu
        """
        if len(self.term_id_map) == 0 or len(self.doc_id_map) == 0:
            self.load()

        ### Bắt đầu code của bạn
        query_tokens = [token.strip() for token in query.split()]
        heap = []
        with InvertedIndexMapper(self.index_name, directory = self.output_dir, postings_encoding=self.postings_encoding) as mapper:
            for token in query_tokens:
                postings = mapper[self.term_id_map[token]]
                heapq.heappush(heap, (len(postings), postings))
            while (len(heap)) > 1:
                list1 = heapq.heappop(heap)[1]
                list2 = heapq.heappop(heap)[1]
                temp  = sorted_intersect(list1, list2)
                heapq.heappush(heap, (len(temp), temp))
        result = [self.doc_id_map[doc_id] for doc_id in heap[0][1]]
        return result
        ### Kết thúc code của bạn
