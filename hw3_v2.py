import random
import time
import threading
import tkinter as tk

# ==========================================
# 1. 自訂排序演算法 (嚴格遵循投影片邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換
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
    泡泡排序法：逐一比較相鄰元素，將最大者往後「擠」
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
# 2. 視窗與視覺化呈現 (允許使用 Tkinter 處理外殼)
# ==========================================

class SortingHomeworkWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Algorithms Efficiency")
        self.root.geometry("550x400")
        
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        title = tk.Label(self.root, text="Sorting Algorithms Efficiency", font=('Helvetica', 16, 'bold'))
        title.pack(pady=10)
        
        self.canvas = tk.Canvas(self.root, width=500, height=180, bg='white', borderwidth=1, relief="solid")
        self.canvas.pack(pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        self.start_btn = tk.Button(btn_frame, text="Start Simulations", command=self.start_simulations, width=15, font=('Helvetica', 10, 'bold'))
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        quit_btn = tk.Button(btn_frame, text="Quit", command=self.root.destroy, width=10, font=('Helvetica', 10))
        quit_btn.pack(side=tk.LEFT, padx=10)
        
        self.draw_interface()
        self.refresh_window()
        self.root.mainloop()

    def draw_interface(self):
        self.canvas.delete("all")
        
        algos = ['Selection', 'Bubble', 'Quick']
        colors = ['#2ecc71', '#f1c40f', '#3498db']
        
        for i, algo in enumerate(algos):
            y = 30 + i * 55
            pct = self.progress[algo]
            
            self.canvas.create_text(100, y, text=f"{algo} Sort:", font=('Helvetica', 11, 'bold'), anchor='e')
            self.canvas.create_rectangle(110, y - 10, 360, y + 10, outline='gray')
            
            bar_width = 110 + int(250 * (pct / 100))
            if bar_width > 110:
                self.canvas.create_rectangle(110, y - 10, bar_width, y + 10, fill=colors[i], outline='')
                
            self.canvas.create_text(375, y, text=f"{int(pct)}%", font=('Helvetica', 10, 'bold'), anchor='w')
            
            if pct == 100.0:
                status_text = f"{self.runtimes[algo]:.6f} s"
            elif self.is_running:
                status_text = "Running..."
            else:
                status_text = "Pending..."
                
            self.canvas.create_text(425, y, text=status_text, font=('Courier', 10), anchor='w')

    def thread_handler(self, sort_func, algo_label, data_list):
        start_time = time.time()
        sort_func(data_list, self.progress)
        self.runtimes[algo_label] = time.time() - start_time
        self.progress[algo_label] = 100.0

    def start_simulations(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        
        test_data = list(range(1, 201))
        random.shuffle(test_data)
        
        t1 = threading.Thread(target=self.thread_handler, args=(selection_sort, 'Selection', test_data), daemon=True)
        t2 = threading.Thread(target=self.thread_handler, args=(bubble_sort, 'Bubble', test_data), daemon=True)
        t3 = threading.Thread(target=self.thread_handler, args=(run_quick_sort, 'Quick', test_data), daemon=True)
        
        t1.start()
        t2.start()
        t3.start()

    def refresh_window(self):
        self.draw_interface()
        if self.is_running and all(pct == 100.0 for pct in self.progress.values()):
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            
        self.root.after(20, self.refresh_window)

if __name__ == '__main__':
    SortingHomeworkWindow()
