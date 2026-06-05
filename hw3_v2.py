import random
import time
import threading
import tkinter as tk

# ==========================================
# 1. 自訂排序演算法 (嚴格遵循投影片教學邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²))
    """
    n = len(arr)
    data = list(arr)  # 複製一份避免互相干擾
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        # 交換數值
        data[i], data[min_idx] = data[min_idx], data[i]
        
        # 計算當前進度百分比
        progress_dict['Selection'] = ((i + 1) / n) * 100
        time.sleep(0.01)  # 微調延遲讓動畫更流暢

def bubble_sort(arr, progress_dict):
    """
    泡泡排序法：逐一比較相鄰元素，將最大者往後「擠」 (O(n²))
    """
    n = len(arr)
    data = list(arr)
    
    for i in range(n, 1, -1):
        for j in range(0, i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
        
        # 更新進度百分比 (做完一輪擠出一個最大值)
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
    
    # 動態估算進度 (以已切分完畢的陣列比例來計算)
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    time.sleep(0.002)  # Quick Sort 太快了，微調延遲以便視覺化觀察
    
    # 遞迴跑左右子陣列
    quick_sort_recursive(data, start, right - 1, total_len, progress_dict)
    quick_sort_recursive(data, right + 1, end, total_len, progress_dict)

def run_quick_sort(arr, progress_dict):
    """快速排序法入口"""
    data = list(arr)
    n = len(data)
    quick_sort_recursive(data, 0, n - 1, n, progress_dict)
    progress_dict['Quick'] = 100.0  # 確保最終必定為 100%

# ==========================================
# 2. Tkinter 美觀介面與多執行緒視覺化
# ==========================================

class SortingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Algorithms Efficiency Comparison")
        self.root.geometry("560x420")
        self.root.configure(bg='#f5f6fa')  # 現代感淡雅背景色
        self.root.resizable(False, False)
        
        # 資料紀錄
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        # 介面標題
        title_label = tk.Label(
            self.root, 
            text="Sorting Algorithms Efficiency", 
            font=('Segoe UI', 18, 'bold'), 
            bg='#f5f6fa', 
            fg='#2f3640'
        )
        title_label.pack(pady=15)
        
        # 自製圖形化 Canvas（完全不使用內建進度條元件）
        self.canvas = tk.Canvas(
            self.root, 
            width=520, 
            height=200, 
            bg='#ffffff', 
            highlightthickness=1, 
            highlightbackground='#dcdde1'
        )
        self.canvas.pack(pady=10)
        
        # 初始化繪製
        self.render_graphics()
        
        # 按鈕控制區域
        btn_frame = tk.Frame(self.root, bg='#f5f6fa')
        btn_frame.pack(pady=20)
        
        self.start_btn = tk.Button(
            btn_frame, 
            text="Start Simulations", 
            command=self.start_simulations, 
            width=16, 
            height=1,
            font=('Segoe UI', 11, 'bold'),
            bg='#44bd32',  # 綠色按鈕
            fg='white',
            activebackground='#4cd137',
            activeforeground='white',
            relief=tk.FLAT
        )
        self.start_btn.pack(side=tk.LEFT, x=15)
        
        quit_btn = tk.Button(
            btn_frame, 
            text="Quit", 
            command=self.root.quit, 
            width=10, 
            height=1,
            font=('Segoe UI', 11),
            bg='#718093',  # 灰色按鈕
            fg='white',
            activebackground='#a4b0be',
            activeforeground='white',
            relief=tk.FLAT
        )
        quit_btn.pack(side=tk.LEFT, x=15)
        
        # 啟動定時刷新核心 (每 20 毫秒刷新一次視窗)
        self.refresh_loop()

    def render_graphics(self):
        """核心：透過數學座標在 Canvas 上純手繪所有文字與長條進度圖"""
        self.canvas.delete("all")  # 擦除舊畫面重新繪製
        
        algorithms = ['Selection', 'Bubble', 'Quick']
        # 質感配色：薄荷綠、向日葵黃、晴空藍
        colors = ['#2cdde1', '#f1c40f', '#3498db'] 
        
        for i, algo in enumerate(algorithms):
            y = 35 + i * 60  # 計算每一列的垂直間距
            pct = self.progress[algo]
            
            # 1. 繪製演算法名稱
            self.canvas.create_text(95, y, text=f"{algo} Sort:", font=('Segoe UI', 11, 'bold'), anchor='e', fill='#353b48')
            
            # 2. 繪製圓角效果進度條背景框 (寬度固定 280 像素)
            self.canvas.create_rectangle(110, y - 12, 390, y + 12, fill='#f5f6fa', outline='#dcdde1', width=1)
            
            # 3. 根據即時百分比計算填充長度並塗色
            bar_end_x = 110 + int(280 * (pct / 100))
            if bar_end_x > 110:
                self.canvas.create_rectangle(110, y - 12, bar_end_x, y + 12, fill=colors[i], outline='')
                
            # 4. 顯示即時百分比數字
            self.canvas.create_text(405, y, text=f"{int(pct)}%", font=('Segoe UI', 10, 'bold'), anchor='w', fill='#2f3640')
            
            # 5. 顯示即時執行耗時
            if pct == 100.0:
                time_text = f"{self.runtimes[algo]:.6f} s"
                text_color = '#2f3640'
            elif self.is_running:
                time_text = "Running..."
                text_color = '#718093'
            else:
                time_text = "Pending..."
                text_color = '#718093'
                
            self.canvas.create_text(450, y, text=time_text, font=('Consolas', 10), anchor='w', fill=text_color)

    def thread_wrapper(self, sort_func, algo_label, input_data):
        """包裝執行緒以精準量測時間"""
        start_time = time.time()
        sort_func(input_data, self.progress)
        self.runtimes[algo_label] = time.time() - start_time
        self.progress[algo_label] = 100.0

    def start_simulations(self):
        """按下按鈕時，啟動三個獨立的 Thread 進行效能爭霸"""
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED, bg='#dcdde1')  # 執行中禁用按鈕
        
        # 重設所有數據
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        
        # 模擬產出 N=200 個隨機不重複數字
        test_data = list(range(1, 201))
        random.shuffle(test_data)
        
        # 分別為三個演算法建立獨立的 Thread (同步跑效能)
        t1 = threading.Thread(target=self.thread_wrapper, args=(selection_sort, 'Selection', test_data), daemon=True)
        t2 = threading.Thread(target=self.thread_wrapper, args=(bubble_sort, 'Bubble', test_data), daemon=True)
        t3 = threading.Thread(target=self.thread_wrapper, args=(run_quick_sort, 'Quick', test_data), daemon=True)
        
        # 啟動 Thread
        t1.start()
        t2.start()
        t3.start()

    def refresh_loop(self):
        """定時循環：每 20 毫秒重新渲染一次 Canvas 畫面"""
        self.render_graphics()
        
        # 檢查是否所有執行緒都安全抵達終點
        if self.is_running and all(pct == 100.0 for pct in self.progress.values()):
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL, bg='#44bd32')  # 恢復按鈕可用
            
        self.root.after(20, self.refresh_loop)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = SortingApp()
    app.run()
