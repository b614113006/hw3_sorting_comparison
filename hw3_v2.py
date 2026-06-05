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
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²))
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
    插入排序法：將未排序元素逐一插入到左邊已排序數列的正確位置 (O(n²))
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
        while data[right] >= data[pivot] and left < right:
            right -= 1
        while data[left] <= data[pivot] and left < right:
            left += 1
            
        if left < right:
            data[left], data[right] = data[right], data[left]
            
    data[pivot], data[right] = data[right], data[pivot]
    
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    time.sleep(0.002)
    
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
        self.root.configure(bg='#e9ebe0')  # 質感米灰色背景
        self.root.resizable(False, False)
        
        self.progress = {'Selection': 0.0, 'Insertion': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Insertion': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        # 設置現代化進度條樣式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "Teal.Horizontal.TProgressbar", 
            troughcolor='#cccccc', 
            background='#218c9f', 
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
        
        # 主面板區域
        main_frame = tk.Frame(self.root, bg='#e9ebe0')
        main_frame.pack(fill=tk.X, padx=40)
        
        # 依照指定科目修改：Selection、Insertion、Quick
        algos = [('Selection Sort', 'Selection'), ('Insertion Sort', 'Insertion'), ('Quick Sort', 'Quick')]
        self.bars = {}
        self.percent_labels = {}
        
        for name, key in algos:
            row = tk.Frame(main_frame, bg='#e9ebe0')
            row.pack(fill=tk.X, pady=6)
            
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
            
        self.status_label = tk.Label(self.root, text="Ready", font=('Segoe UI', 12), bg='#e9ebe0', fg='#444444')
        self.status_label.pack(anchor='w', padx=40, pady=(15, 10))
        
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
            
        btn_frame = tk.Frame(self.root, bg='#e9ebe0')
        btn_frame.pack(fill=tk.X, padx=40, pady=(30, 0))
        
        self.start_btn = tk.Button(
            btn_frame, 
            text="Start Simulations (▶)", 
            command=self.start_simulations,
            font=('Segoe UI', 11, 'bold'),
            bg='#1d639b', 
            fg='white',
            activebackground='#257cb3',
            activeforeground='white',
            bd=0, 
            padx=15, 
            pady=6, 
            cursor='hand2'
        )
        self.start_btn.pack(side=tk.LEFT)
        
        quit_btn = tk.Button(
            btn_frame, 
            text="Quit", 
            command=self.root.destroy,
            font=('Segoe UI', 11),
            bg='#a0a0a0', 
            fg='white',
            activebackground='#b5b5b5',
            activeforeground='white',
            bd=0, 
            padx=20, 
            pady=6, 
            cursor='hand2'
        )
        quit_btn.pack(side=tk.RIGHT)
        
        self.refresh_window()
        self.root.mainloop()

    def thread_handler(self, sort_func, algo_label, data_list):
        start_time = time.time()
        sort_func(data_list, self.progress)
        self.runtimes[algo_label] = time.time() - start_time
        self.progress[algo_label] = 100.0

    def start_simulations(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, bg='#cccccc')
        self.status_label.config(text="Running...")
        
        for key in self.progress:
