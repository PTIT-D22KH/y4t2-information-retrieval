class CompressedPostings:
    #Nếu bạn cần thêm phương thức trợ giúp, thêm ở đây
    ### Bắt đầu code của bạn
    @staticmethod
    def _variable_byte_encoding(n: int) -> List[bytes]:
        result_bytes = []
        while True:
            result_bytes.insert(0, n % 128)
            n //= 128
            if n == 0:
                break
        result_bytes[-1] |= 128
        return result_bytes
    ### Kết thúc code của bạn

    @staticmethod
    def encode(postings_list):
        """Mã hóa `postings_list` sử dụng mã hóa khoảng cách (gap encoding) 
        với mã hóa byte biến đổi cho mỗi khoảng cách

        Tham số
        ----------
        postings_list: List[int]
            Danh sách posting cần mã hóa

        Trả về
        -------
        bytes: 
            Biểu diễn byte của danh sách posting đã nén 
            (được tạo bởi hàm `array.tobytes`)
        """
        ### Bắt đầu code của bạn
        result_bytes = []
        previous = 0
        for doc_id in postings_list:
            gap = doc_id - previous
            previous = doc_id
            byte = CompressedPostings._variable_byte_encoding(gap)
            result_bytes.extend(byte)
        return array.array('B', result_bytes).tobytes()
        ### Kết thúc code của bạn


    @staticmethod
    def decode(encoded_postings_list):
        """Giải mã biểu diễn byte của danh sách posting đã nén

        Tham số
        ----------
        encoded_postings_list: bytes
            Biểu diễn byte được tạo bởi `CompressedPostings.encode` 

        Trả về
        -------
        List[int]
            Danh sách posting đã giải mã (mỗi posting là một docId)
        """
        ### Bắt đầu code của bạn
        decoded_postings_list = array.array('B')
        decoded_postings_list.frombytes(encoded_postings_list)
        numbers = []
        n = 0
        for i, byte in enumerate(decoded_postings_list):
            if byte < 128:
                n = 128 * n + byte
            else:
                n = 128 * n + byte - 128
                numbers.append(n)
                n = 0
        prefix_sum = 0
        res = []
        for num in numbers:
            prefix_sum += num
            res.append(prefix_sum)
        return res
        ### Kết thúc code của bạn
