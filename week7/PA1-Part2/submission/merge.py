
import heapq
class BSBIIndex(BSBIIndex):
    def merge(self, indices, merged_index):
        """Hợp nhất nhiều chỉ mục đảo thành một chỉ mục duy nhất

        Tham số
        ----------
        indices: List[InvertedIndexIterator]
            Danh sách các đối tượng InvertedIndexIterator, mỗi đối tượng 
            đại diện cho một chỉ mục đảo có thể duyệt cho một khối
        merged_index: InvertedIndexWriter
            Một đối tượng InvertedIndexWriter để ghi từng danh sách 
            posting đã hợp nhất
        """
        ### Bắt đầu code của bạn

        ### Kết thúc code của bạn
