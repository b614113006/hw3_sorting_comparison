import random
import time
import threading
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. 自訂排序演算法 (核心學習重點：嚴格遵循投影片邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²)) [cite: 2173, 2307]
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

def bubble_sort(arr, progress_dict):
    """
    泡泡排序法：逐一比較相鄰元素，將最大者往後「擠」 (O(n²)) [cite: 2314, 2580]
    """
    n = len(arr)
    data = list(arr)
    
    for i in range(n, 1, -1):
        for j in range(0, i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
        
        progress_dict['Bubble'] = ((n - i + 1) / (n - 1)) * 100
        time.sleep(0.01)

def quick_sort_recursive(data, start, end, total_len, progress_dict):
    """
    快速排序法核心遞迴：雙指標朝中間移動（嚴格遵循投影片第12頁虛擬碼邏輯） [cite: 2978]
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
            data[left], data[right] = data[right], data[left] [cite: 2978]
            
    data[pivot], data[right] = data[right], data[pivot] [cite: 2979]
    
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    time.sleep(0.002)
    
    quick_sort_recursive(data, start, right - 1, total_len, progress_dict) [cite: 2979]
    quick_sort_recursive(data, right + 1, end, total_len, progress_dict) [cite: 2979]

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
        self.root.configure(bg='#e9ebe0')  # 圖二：柔和淺灰色/米色背景
        self.root.resizable(False, False)
        
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        # 設置 ttk 元件的現代化圓角質感外觀 (Style)
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用支援自訂色彩的基礎主題
        
        # 訂製青藍色圓角進度條樣式
        self.style.configure(
            "Teal.Horizontal.TProgressbar", 
            troughcolor='#cccccc',    # 進度條未滿的灰色軌道
            background='#218c9f',     # 圖二：層次感青藍色填滿
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
        
        # --- 演算法主面板區域 (排版全部靠左，預留足夠寬度防止文字被擋) ---
        main_frame = tk.Frame(self.root, bg='#e9ebe0')
        main_frame.pack(fill=tk.X, padx=40)
        
        algos = [('Selection Sort', 'Selection'), ('Bubble Sort', 'Bubble'), ('Quick Sort', 'Quick')]
        self.bars = {}
        self.percent_labels = {}
        
        for i, (name, key) in enumerate(algos):
            row = tk.Frame(main_frame, bg='#e9ebe0')
            row.pack(fill=tk.X, pady=6)
            
            # 演算法名稱標籤 (靠左固定寬度，字體加粗分明，絕不裁切)
            lbl = tk.Label(row, text=name, font=('Segoe UI', 12), bg='#e9ebe0', fg='#333333', width=14, anchor='w')
            lbl.pack(side=tk.LEFT)
            
            # 圓角進度條外框裝飾
            bar_frame = tk.Frame(row, bg='#e9ebe0')
            bar_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            # 內建現代化進度條
            bar = ttk.Progressbar(bar_frame, style="Teal.Horizontal.TProgressbar", orient="horizontal", mode="determinate", length=280)
            bar.pack(fill=tk.X)
            self.bars[key] = bar
            
            # 即時進度百分比文字數字 (預設 0%)
            pct_lbl = tk.Label(row, text="0%", font=('Segoe UI', 11, 'bold'), bg='#e9ebe0', fg='#333333', width=5, anchor='e')
            pct_lbl.pack(side=tk.LEFT)
            self.percent_labels[key] = pct_lbl
            
        # 狀態文字標籤 (Ready / Running...)
        self.status_label = tk.Label(self.root, text="Ready", font=('Segoe UI', 12), bg='#e9ebe0', fg='#444444')
        self.status_label.pack(anchor='w', padx=40, pady=(15, 10))
        
        # --- 底部統計時間區塊 ---
        time_heading = tk.Label(self.root, text="Total runtime (seconds):", font=('Segoe UI', 12, 'bold'), bg='#e9ebe0', fg='#202020')
        time_heading.pack(anchor='w', padx=40, pady=(5, 5))
        
        self.time_labels = {}
        time_items = [('Selection Sort:', 'Selection'), ('Bubble Sort:', 'Bubble'), ('Quick Sort:', 'Quick')]
        
        for text_label, key in time_items:
            t_row = tk.Frame(self.root, bg='#e9ebe0')
            t_row.pack(fill=tk.X, padx=40, pady=2)
            
            name_lbl = tk.Label(t_row, text=text_label, font=('Segoe UI', 11), bg='#e9ebe0', fg='#444444', width=14, anchor='w')
            name_lbl.pack(side=tk.LEFT)
            
            val_lbl = tk.Label(t_row, text="-", font=('Consolas', 11), bg='#e9ebe0', fg='#444444', width=15, anchor='w')
            val_lbl.pack(side=tk.LEFT, padx=20)
            self.time_labels[key] = val_lbl
            
        # --- 按鈕控制列 ---
        btn_frame = tk.Frame(self.root, bg='#e9ebe0')
        btn_frame.pack(fill=tk.X, padx=40, pady=(30, 0))
        
        # 開始模擬按鈕 (加上直觀的播放圖示 ❪▶❫，深藍色質感圓角外觀)
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
        
        # 關閉視窗按鈕 (灰色現代扁平化外觀)
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
        
        # 啟動事件刷新循環
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
        
        # 重置數值與時間短橫線
        for key in self.progress:
            self.progress[key] = 0.0
            self.time_labels[key].config(text="-")
            
        test_data = list(range(1, 201))
        random.shuffle(test_data)
        
        # 三執行緒同步運算比較 [cite: 1749]
        t1 = threading.Thread(target=self.thread_handler, args=(selection_sort, 'Selection', test_data), daemon=True)
        t2 = threading.Thread(target=self.thread_handler, args=(bubble_sort, 'Bubble', test_data), daemon=True)
        t3 = threading.Thread(target=self.thread_handler, args=(run_quick_sort, 'Quick', test_data), daemon=True)
        
        t1.start()
        t2.start()
        t3.start()

    def refresh_window(self):
        # 動態更新進度條長度與旁邊的百分比標籤
        for key, bar in self.bars.items():
            pct = self.progress[key]
            bar['value'] = pct
            self.percent_labels[key].config(text=f"{int(pct)}%")
            
            # 若該演算法完成，把左側橫線換成精準耗時秒數
            if pct == 100.0 and self.time_labels[key]['text'] == "-":
                self.time_labels[key].config(text=f"{self.runtimes[key]:.6f} s")
                
        # 檢查是否全數跑完
        if self.is_running and all(pct == 100.0 for pct in self.progress.values()):
            self.is_running = False
            self.status_label.config(text="Ready")
            self.start_btn.config(state=tk.NORMAL, bg='#1d639b')
            
        self.root.after(20, self.refresh_window)

if __name__ == '__main__':
    SortingHomeworkWindow()
