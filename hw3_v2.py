import random
import time
import threading
import tkinter as tk

# ==========================================
# 1. 自訂排序演算法 (嚴格遵循投影片教學邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²)) [cite: 605]
    """
    n = len(arr)
    data = list(arr)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        
        # 計算百分比並更新
        progress_dict['Selection'] = ((i + 1) / n) * 100
        time.sleep(0.01)

def bubble_sort(arr, progress_dict):
    """
    泡泡排序法：逐一比較相鄰元素，將最大者往後「擠」 (O(n²)) [cite: 746, 747]
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
    快速排序法核心遞迴：雙指標朝中間移動（嚴格遵循投影片第12頁虛擬碼邏輯） [cite: 1410]
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
    
    # 動態估算進度
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
# 2. 自製畫布 GUI 視覺化介面 (不使用任何內建圖形元件)
# ==========================================

class SortingVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Algorithm Efficiency Comparison")
        self.root.geometry("550x400")
        self.root.resizable(False, False)
        
        # 共用資料結構
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        # 標題
        title = tk.Label(self.root, text="Sorting Algorithms Efficiency", font=('Helvetica', 16, 'bold'))
        title.pack(pady=10)
        
        # 【核心：自製純手繪畫布】
        # 我們不用任何 Progressbar 元件，全部在這個畫布上用數學座標畫出來！
        self.canvas = tk.Canvas(self.root, width=500, height=180, bg='white', highlightthickness=1, highlightbackground='#ccc')
        self.canvas.pack(pady=10)
        
        # 初始化畫布文字與空白條
        self.draw_custom_graphics()
        
        # 按鈕區域
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        self.start_btn = tk.Button(btn_frame, text="Start Simulations", command=self.start_simulations, width=15, font=('Helvetica', 10, 'bold'))
        self.start_btn.pack(side=tk.LEFT, x=10)
        
        quit_btn = tk.Button(btn_frame, text="Quit", command=self.root.quit, width=10, font=('Helvetica', 10))
        quit_btn.pack(side=tk.LEFT, x=10)
        
        # 啟動定時刷新畫面
        self.update_view()

    def draw_custom_graphics(self):
        """完全手動計算座標，繪製進度條與時間文字"""
        self.canvas.delete("all")  # 清空舊畫面
        
        labels = ['Selection', 'Bubble', 'Quick']
        colors = ['#2ecc71', '#f1c40f', '#3498db']  # 綠、黃、藍
        
        for i, label in enumerate(labels):
            y_offset = 25 + i * 50
            pct = self.progress[label]
            
            # 1. 繪製標籤文字
            self.canvas.create_text(60, y_offset, text=f"{label}:", font=('Helvetica', 11, 'bold'), anchor='e')
            
            # 2. 繪製進度條外框 (固定寬度 300 像素)
            self.canvas.create_rectangle(80, y_offset - 10, 380, y_offset + 10, outline='#bdc3c7', width=1)
            
            # 3. 根據當前百分比計算內部填充寬度並繪製
            fill_width = 80 + int(300 * (pct / 100))
            if fill_width > 80:
                self.canvas.create_rectangle(80, y_offset - 10, fill_width, y_offset + 10, fill=colors[i], outline='')
                
            # 4. 繪製百分比數字
            self.canvas.create_text(400, y_offset, text=f"{int(pct)}%", font=('Helvetica', 10), anchor='w')
            
            # 5. 繪製即時執行時間
            time_str = f"Pending..." if not self.is_running and pct == 0 else f"Running..."
            if pct == 100:
                time_str = f"{self.runtimes[label]:.6f} s"
            self.canvas.create_text(440, y_offset, text=time_str, font=('Courier', 10), anchor='w')

    def thread_wrapper(self, sort_func, label, arr):
        start_time = time.time()
        sort_func(arr, self.progress)
        self.runtimes[label] = time.time() - start_time
        self.progress[label] = 100.0

    def start_simulations(self):
        if self.is_running:
            return
        self.is_running = True
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        
        # 產出 N=200 個隨機不重複數字
        base_list = list(range(1, 201))
        random.shuffle(base_list)
        
        # 三個獨立執行緒同步跑排序
        t1 = threading.Thread(target=self.thread_wrapper, args=(selection_sort, 'Selection', base_list), daemon=True)
        t2 = threading.Thread(target=self.thread_wrapper, args=(bubble_sort, 'Bubble', base_list), daemon=True)
        t3 = threading.Thread(target=self.thread_wrapper, args=(run_quick_sort, 'Quick', base_list), daemon=True)
        
        t1.start()
        t2.start()
        t3.start()

    def update_view(self):
        """定時重新渲染畫布 (每 20 毫秒一次)"""
        self.draw_custom_graphics()
        
        # 檢查是否所有 Thread 都跑完了
        if self.is_running and all(pct == 100.0 for pct in self.progress.values()):
            self.is_running = False
            
        self.root.after(20, self.update_view)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = SortingVisualizer()
    app.run()
