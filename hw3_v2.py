import random
import time
import threading
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. 自訂排序演算法 (嚴格遵循投影片與作業規範)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換
    """
    n = len(arr)
    data_list = list(arr)  # 複製一份避免執行緒互相干擾
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data_list[j] < data_list[min_idx]:
                min_idx = j
        data_list[i], data_list[min_idx] = data_list[min_idx], data_list[i]
        
        # 即時更新進度
        progress_dict['Selection'] = ((i + 1) / n) * 100
        time.sleep(0.01)

def insertion_sort(arr, progress_dict):
    """
    插入排序法：將未排序元素逐一插入到左邊已排序數列的正確位置
    """
    n = len(arr)
    data_list = list(arr)
    
    for i in range(1, n):
        key_val = data_list[i]
        j = i - 1
        while j >= 0 and data_list[j] > key_val:
            data_list[j + 1] = data_list[j]
            j -= 1
        data_list[j + 1] = key_val
        
        # 即時更新進度
        progress_dict['Insertion'] = (i / (n - 1)) * 100
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
        # 右指標向左移動，直到數值小於基準點
        while data_list[right] >= data_list[pivot] and left < right:
            right -= 1
        # 左指標向右移動，直到數值大於基準點
        while data_list[left] <= data_list[pivot] and left < right:
            left += 1
            
        if left < right:
            data_list[left], data_list[right] = data_list[right], data_list[left]
            
    # 左右指標相撞，交換基準點與相撞處數值
    data_list[pivot], data_list[right] = data_list[right], data_list[pivot]
    
    # 動態估算進度 (以已切分完畢的比例計算)
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    time.sleep(0.002)
    
    # 遞迴處理左右子陣列
    quick_sort_recursive(data_list, start, right - 1, total_len, progress_dict)
    quick_sort_recursive(data_list, right + 1, end, total_len, progress_dict)

def run_quick_sort(arr, progress_dict):
    """快速排序法執行緒入口"""
    data_list = list(arr)
    n = len(data_list)
    quick_sort_recursive(data_list, 0, n - 1, n, progress_dict)
    progress_dict['Quick'] = 100.0  # 確保完成時衝到 100%

# ==========================================
# 2. 現代化視窗與視覺化呈現 (Tkinter 與 圓角樣式)
# ==========================================

class SortingHomeworkWindow:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Sorting Algorithm Efficiency Comparison (Threaded)")
        self.root.geometry("640x480")
        self.root.configure(bg='#e9ebe0')  # 質感米灰色背景
        self.root.resizable(False, False)
        
        # 即時數據共享結構
        self.progress = {'Selection': 0.0, 'Insertion': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Insertion': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        # 設置 ttk 圓角與主題色彩樣式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "Teal.Horizontal.TProgressbar", 
            troughcolor='#cccccc', 
            background='#218c9f',  # 質感青藍色
            thickness=22, 
            borderwidth=0
        )
        
        # 頂部大標題
        title_label = tk.Label(
            self.root, 
            text="Sorting Algorithms Efficiency", 
            font=('Segoe UI', 18), 
            bg='#e9ebe0', 
            fg='#202020'
        )
        title_label.pack(pady=(25, 15))
        
        # 主框架面板 (排版靠左，預留足夠寬度防止文字被裁切)
        main_frame = tk.Frame(self.root, bg='#e9ebe0')
        main_frame.pack(fill=tk.X, padx=40)
        
        algos = [('Selection Sort', 'Selection'), ('Insertion Sort', 'Insertion'), ('Quick Sort', 'Quick')]
        self.bars = {}
        self.percent_labels = {}
        
        for name, key in algos:
            row = tk.Frame(main_frame, bg='#e9ebe0')
            row.pack(fill=tk.X, pady=6)
            
            # 演算法名稱固定寬度，確保完美對齊且不被擋住
            lbl = tk.Label(row, text=name, font=('Segoe UI', 12), bg='#e9ebe0', fg='#333333', width=14, anchor='w')
            lbl.pack(side=tk.LEFT)
            
            bar_frame = tk.Frame(row, bg='#e9ebe0')
            bar_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            bar = ttk.Progressbar(bar_frame, style="Teal.Horizontal.TProgressbar", orient="horizontal", mode="determinate", length=280)
            bar.pack(fill=tk.X)
            self.bars[key] = bar
            
            pct_lbl = tk.Label(row, text="0%", font=('Segoe UI', 11, 'bold'), bg='#e9ebe0', fg='#333333', width=5, anchor='e')
            pct_lbl.pack(side=tk.LEFT)
            self.percent_labels[key] = pct_lbl
            
        # 狀態標籤 (Ready / Running...)
        self.status_label = tk.Label(self.root, text="Ready", font=('Segoe UI', 12), bg='#e9ebe0', fg='#444444')
        self.status_label.pack(anchor='w', padx=40, pady=(15, 10))
        
        # 底部耗時面板大標題
        time_heading = tk.Label(self.root, text="Total runtime (seconds):", font=('Segoe UI', 12, 'bold'), bg='#e9ebe0', fg='#202020')
        time_heading.pack(anchor='w', padx=40, pady=(5, 5))
        
        self.time_labels = {}
        time_items = [('Selection Sort:', 'Selection'), ('Insertion Sort:', 'Insertion'), ('Quick Sort:', 'Quick')]
        
        for text_label, key in time_items:
            t_row = tk.Frame(self.root, bg='#e9ebe0')
            t_row.pack(fill=tk.X, padx=40, pady=2)
            
            name_lbl = tk.Label(t_row, text=text_label, font=('Segoe UI', 11), bg='#e9ebe0', fg='#444444', width=14, anchor='w')
            name_lbl.pack(side=tk.LEFT)
            
            val_lbl = tk.Label(t_row, text="-", font=('Consolas', 11), bg='#e9ebe0', fg='#444444', width=15, anchor='w')
            val_lbl.pack(side=tk.LEFT, padx=20)
            self.time_labels[key] = val_lbl
