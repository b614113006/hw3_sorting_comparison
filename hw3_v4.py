import random
import time
import threading
import tkinter as tk
from tkinter import ttk

# ==========================================
# 1. 自訂排序演算法 (精準計數器流速控制，拒絕發抖)
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
        
        # 穩定在 2.1 秒左右前進完畢
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
        
        # 穩定在 2.1 秒左右前進完畢
        progress_dict['Bubble'] = ((n - i + 1) / (n - 1)) * 100
        time.sleep(0.01)

def quick_sort_recursive(data_list, start, end, total_len, progress_dict, counter_list):
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
            # 沒跳過一個元素，計數器就加 1
            counter_list[0] += 1
            if counter_list[0] % 250 == 0:
                current_pct = min(99.0, (counter_list[0] / 1500) * 100)
                progress_dict['Quick'] = current_pct
                time.sleep(0.01) # 精準踩煞車，等一下再出發
                
        while data_list[left] <= data_list[pivot] and left < right:
            left += 1
            counter_list[0] += 1
            if counter_list[0] % 250 == 0:
                current_pct = min(99.0, (counter_list[0] / 1500) * 100)
                progress_dict['Quick'] = current_pct
                time.sleep(0.01) # 精準踩煞車，等一下再出發
                
        if left < right:
            data_list[left], data_list[right] = data_list[right], data_list[left]
            
    data_list[pivot], data_list[right] = data_list[right], data_list[pivot]
    
    # 遞迴處理左右子陣列
    quick_sort_recursive(data_list, start, right - 1, total_len, progress_dict, counter_list)
    quick_sort_recursive(data_list, right + 1, end, total_len, progress_dict, counter_list)

def run_quick_sort(arr, progress_dict):
    """快速排序法執行緒入口"""
    data_list = list(arr)
    n = len(data_list)
    # 使用可變清單作為全域計數器，傳入遞迴中
    counter_list = [0]
    quick_sort_recursive(data_list, 0, n - 1, n, progress_dict, counter_list)
    progress_dict['Quick'] = 100.0  # 完工時乾淨俐落定格在 100%

# ==========================================
# 2. 全域視窗與現代化視覺化 (Tkinter 穩定架構)
# ==========================================

root = tk.Tk()
root.title("Sorting Algorithm Efficiency Comparison (Threaded)")
root.geometry("640x480")
root.configure(bg='#e9ebe0')  # 質感米灰色背景
root.resizable(False, False)

# 共享即時資料結構
progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
status_vars = {"is_running": False}

# 設置 ttk 圓角青藍色樣式
style = ttk.Style()
style.theme_use('clam')
style.configure("Teal.Horizontal.TProgressbar", troughcolor='#cccccc', background='#218c9f', thickness=22, borderwidth=0)

# 大標題
title_label = tk.Label(root, text="Sorting Algorithms Efficiency", font=('Segoe UI', 18), bg='#e9ebe0', fg='#202020')
title_label.pack(pady=(25, 15))

main_frame = tk.Frame(root, bg='#e9ebe0')
main_frame.pack(fill=tk.X, padx=40)

algos = [('Selection Sort', 'Selection'), ('Bubble Sort', 'Bubble'), ('Quick Sort', 'Quick')]
bars = {}
percent_labels = {}

for name, key in algos:
    row = tk.Frame(main_frame, bg='#e9ebe0')
    row.pack(fill=tk.X, pady=6)
    
    lbl = tk.Label(row, text=name, font=('Segoe UI', 12), bg='#e9ebe0', fg='#333333', width=14, anchor='w')
    lbl.pack(side=tk.LEFT)
    
    bar_frame = tk.Frame(row, bg='#e9ebe0')
    bar_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    
    bar = ttk.Progressbar(bar_frame, style="Teal.Horizontal.TProgressbar", orient="horizontal", mode="determinate", length=280)
    bar.pack(fill=tk.X)
    bars[key] = bar
    
    pct_lbl = tk.Label(row, text="0%", font=('Segoe UI', 11, 'bold'), bg='#e9ebe0', fg='#333333', width=5, anchor='e')
    pct_lbl.pack(side=tk.LEFT)
    percent_labels[key] = pct_lbl

status_label = tk.Label(root, text="Ready", font=('Segoe UI', 12), bg='#e9ebe0', fg='#444444')
status_label.pack(anchor='w', padx=40, pady=(15, 10))

time_heading = tk.Label(root, text="Total runtime (seconds):", font=('Segoe UI', 12, 'bold'), bg='#e9ebe0', fg='#202020')
time_heading.pack(anchor='w', padx=40, pady=(5, 5))

time_labels = {}
time_items = [('Selection Sort:', 'Selection'), ('Bubble Sort:', 'Bubble'), ('Quick Sort:', 'Quick')]

for text_label, key in time_items:
    t_row = tk.Frame(root, bg='#e9ebe0')
    t_row.pack(fill=tk.X, padx=40, pady=2)
    
    name_lbl = tk.Label(t_row, text=text_label, font=('Segoe UI', 11), bg='#e9ebe0', fg='#444444', width=14, anchor='w')
    name_lbl.pack(side=tk.LEFT)
    
    val_lbl = tk.Label(t_row, text="-", font=('Consolas', 11), bg='#e9ebe0', fg='#444444', width=15, anchor='w')
    val_lbl.pack(side=tk.LEFT, padx=20)
    time_labels[key] = val_lbl

def thread_handler(sort_func, algo_label, data_list):
    start_time = time.time()
    sort_func(data_list, progress)
    runtimes[algo_label] = time.time() - start_time
    progress[algo_label] = 100.0

def start_simulations():
    if status_vars["is_running"]:
        return
    status_vars["is_running"] = True
    start_btn.config(state=tk.DISABLED, bg='#cccccc')
    status_label.config(text="Running...")
    
    for key in progress:
        progress[key] = 0.0
        time_labels[key].config(text="-")
        
    test_data = list(range(1, 201))
    random.shuffle(test_data)
    
    # 三條 Thread 同步起跑
    t1 = threading.Thread(target=thread_handler, args=(selection_sort, 'Selection', test_data), daemon=True)
    t2 = threading.Thread(target=thread_handler, args=(bubble_sort, 'Bubble', test_data), daemon=True)
    t3 = threading.Thread(target=thread_handler, args=(run_quick_sort, 'Quick', test_data), daemon=True)
    
    t1.start()
    t2.start()
    t3.start()

def refresh_window():
    """定時主循環：每 20 毫秒刷新重繪一次 UI"""
    for key, bar in bars.items():
        pct = progress[key]
        bar['value'] = pct
        percent_labels[key].config(text=f"{int(pct)}%")
        
        if pct == 100.0 and time_labels[key]['text'] == "-":
            time_labels[key].config(text=f"{runtimes[key]:.6f} s")
            
    if status_vars["is_running"] and all(pct == 100.0 for pct in progress.values()):
        status_vars["is_running"] = False
        status_label.config(text="Ready")
        start_btn.config(state=tk.NORMAL, bg='#1d639b')
        
    root.after(20, refresh_window)

# 按鈕列佈局
btn_frame = tk.Frame(root, bg='#e9ebe0')
btn_frame.pack(fill=tk.X, padx=40, pady=(30, 0))

start_btn = tk.Button(btn_frame, text="Start Simulations (▶)", command=start_simulations, font=('Segoe UI', 11, 'bold'), bg='#1d639b', fg='white', activebackground='#257cb3', activeforeground='white', bd=0, padx=15, pady=6, cursor='hand2')
start_btn.pack(side=tk.LEFT)

quit_btn = tk.Button(btn_frame, text="Quit", command=root.destroy, font=('Segoe UI', 11), bg='#a0a0a0', fg='white', activebackground='#b5b5b5', activeforeground='white', bd=0, padx=20, pady=6, cursor='hand2')
quit_btn.pack(side=tk.RIGHT)

refresh_window()
root.update()
root.mainloop()
