import random
import time
import threading
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. 自訂排序演算法 (核心重點：精準鎖定 Selection, Bubble, Quick)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²))
    """
    n = len(arr)
    data_list = list(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data_list[j] < data_list[min_idx]:
                min_idx = j
        data_list[i], data_list[min_idx] = data_list[min_idx], data_list[i]
        
        # 即時更新 Selection Sort 進度並保持可觀察的延遲
        progress_dict['Selection'] = ((i + 1) / n) * 100
        time.sleep(0.01)

def bubble_sort(arr, progress_dict):
    """
    泡泡排序法：逐一比較相鄰元素，將最大者往後「擠」 (O(n²))
    """
    n = len(arr)
    data_list = list(arr)
    for i in range(n, 1, -1):
        for j in range(0, i - 1):
            if data_list[j] > data_list[j + 1]:
                data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
        
        # 即時更新 Bubble Sort 進度 (每做完一輪擠出一個最大值)
        progress_dict['Bubble'] = ((n - i + 1) / (n - 1)) * 100
        time.sleep(0.01)

def quick_sort_recursive(data_list, start, end, total_len, progress_dict):
    """
    快速排序法核心遞迴：雙指標朝中間移動（嚴格遵循投影片第12頁虛擬碼邏輯）
    """
    if start >= end:
        return
    pivot = start
    left = start
    right = end
    while left != right:
        while data_list[right] >= data_list[pivot] and left < right:
            right -= 1
        while data_list[left] <= data_list[pivot] and left < right:
            left += 1
        if left < right:
            data_list[left], data_list[right] = data_list[right], data_list[left]
    data_list[pivot], data_list[right] = data_list[right], data_list[pivot]
    
    # 保持 $O(n \log n)$ 速度封印解除狀態，無 sleep 延遲
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    
    quick_sort_recursive(data_list, start, right - 1, total_len, progress_dict)
    quick_sort_recursive(data_list, right + 1, end, total_len, progress_dict)

def run_quick_sort(arr, progress_dict):
    """快速排序法執行緒入口"""
    data_list = list(arr)
    n = len(data_list)
    quick_sort_recursive(data_list, 0, n - 1, n, progress_dict)
    progress_dict['Quick'] = 100.0  # 完成時瞬間充滿

# ==========================================
# 2. 全域視窗與現代化視覺化 (Tkinter 與 圓角樣式)
# ==========================================

root = tk.Tk()
root.title("Sorting Algorithm Efficiency Comparison (Threaded)")
root.geometry("640x480")
root.configure(bg='#e9ebe0')  # 柔和現代感米灰色背景
root.resizable(False, False)

# 共享即時資料結構
progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
status_vars = {"is_running": False}

# 設置 ttk 元件外觀風格 (質感青藍色)
style = ttk.Style()
style.theme_use('clam')
style.configure("Teal.Horizontal.TProgressbar", troughcolor='#cccccc', background='#218c9f', thickness=22, borderwidth=0)

# 頂部大標題
title_label = tk.Label(root, text="Sorting Algorithms Efficiency", font=('Segoe UI', 18), bg='#e9ebe0', fg='#202020')
title_label.pack(pady=(25, 15))

# 主面板框架 (排版全部靠左垂直對齊)
main_frame = tk.Frame(root, bg='#e9ebe0')
main_frame.pack(fill=tk.X, padx=40)

# 建立進度條元件
algos = [('Selection Sort', 'Selection'), ('Bubble Sort', 'Bubble'), ('Quick Sort', 'Quick')]
bars = {}
percent_labels = {}

for name, key in algos:
    row = tk.Frame(main_frame, bg='#e9ebe0')
    row.pack(fill=tk.X, pady=6)
