import random
import time
import threading
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. 自訂排序演算法 (核心重點：嚴格遵循投影片邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (投影片第3-4頁邏輯)
    """
    n = len(arr)
    data = list(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        
        progress_dict['Selection'] = ((i + 1) / n) * 100
        time.sleep(0.01)

def insertion_sort(arr, progress_dict):
    """
    插入排序法：將未排序元素逐一插入到左邊已排序數列的正確位置
    """
    n = len(arr)
    data = list(arr)
    
    for i in range(1, n):
        key_val = data[i]
        j = i - 1
        while j >= 0 and data[j] > key_val:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key_val
        
        progress_dict['Insertion'] = (i / (n - 1)) * 100
        time.sleep(0.01)

def quick_sort_recursive(data, start, end, total_len, progress_dict):
    """
    快速排序法核心遞迴：雙指標朝中間移動（嚴格遵循投影片第12頁虛擬碼邏輯）
    """
    if start >= end:
        return
        
    pivot = start
    left = start
    right = end
    
    while left != right:
        # 右指標向左移動，直到數值小於基準點
        while data[right] >= data[pivot] and left < right:
            right -= 1
        # 左指標向右移動，直到數值大於基準點
        while data[left] <= data[pivot] and left < right:
            left += 1
            
        if left < right:
            data[left], data[right] = data[right], data[left]
            
    # 左右指標相撞，交換基準點與相撞處數值
    data[pivot], data[right] = data[right], data[pivot]
    
    # 動態估算進度 (以已切分完畢的比例計算)
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    time.sleep(0.002)
    
    # 遞迴處理左右子陣列
    quick_sort_recursive(data, start, right - 1, total_len, progress_dict)
    quick_sort_recursive(data, right + 1, end, total_len, progress_dict)

def run_quick_sort(arr, progress_dict):
    data = list(arr)
    n = len(data)
    quick_sort_recursive(data, 0, n - 1, n, progress_dict)
    progress_dict['Quick'] = 100.0

# ==========================================
# 2. 現代化視窗與視覺化呈現 (使用內建系統樣式)
# ==========================================

class SortingHomeworkWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Algorithm Efficiency Comparison (Threaded)")
        self.root.geometry("640x480")
        self.root.configure(bg='#e9ebe0')  # 圖
