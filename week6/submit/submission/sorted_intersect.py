def sorted_intersect(list1, list2):
    """Giao hai danh sách đã sắp xếp (tăng dần) và trả về kết quả đã sắp xếp

    Tham số
    ----------
    list1: List[Comparable]
    list2: List[Comparable]
        Các danh sách đã sắp xếp cần giao

    Trả về
    -------
    List[Comparable]
        Giao đã sắp xếp        
    """
    ### Bắt đầu code của bạn
    i, j = 0, 0
    result = []
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return result
    ### Kết thúc code của bạn
