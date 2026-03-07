class BSBIIndex(BSBIIndex):
    def invert_write(self, td_pairs, index):
        """Đảo ngược td_pairs thành danh sách posting và ghi chúng vào chỉ mục cho trước
        
        Tham số
        ----------
        td_pairs: List[Tuple[Int, Int]]
            Danh sách các cặp termID-docID
        index: InvertedIndexWriter
            Chỉ mục đảo trên đĩa tương ứng với khối       
        """
        ### Bắt đầu code của bạn
        td_pairs = sorted(td_pairs, key = lambda x : self.term_id_map[x[0]])
        postings = []
        last_term = ""
        for pair in td_pairs:
            if pair[0] != last_term:
                if last_term != '':
                    index.append(last_term, list(set(postings)))
                postings = []
                postings.append(pair[1])
                last_term = pair[0]
            else:
                postings.append(pair[1])
        if last_term:
            index.append(last_term, list(set(postings)))

        ## Kết thúc code của bạn
