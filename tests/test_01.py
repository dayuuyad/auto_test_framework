# 生成一个冒泡排序的测试方法
import os


def test_bubble_sort():
    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = [11, 12, 22, 25, 34, 64, 90]
    assert bubble_sort(arr) == sorted_arr

    
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    print(arr)        
    return arr


# def test_delete_cache():
#     def clean_cache() -> None:
#         """删除所有缓存文件"""
#         path = r"d:\traecode\pytest-auto-api-master\cache\contract-qzbzb_case.json"
#         os.remove(path)
#         print(f"{path}是否存在：{os.path.exists(path)}")
    
#     clean_cache()