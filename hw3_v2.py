import random
import time
import threading
import tkinter as tk

# ==========================================
# 1. 自訂排序演算法 (核心學習重點：嚴格遵循投影片邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²))
    """
    n = len(arr)
    data = list(arr)  # 複製一份避免執行緒互相干擾
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        
        # 計算並更新進度百分比
        progress_dict['Selection'] = ((i + 1) / n) * 100
        time.sleep(0.01)  # 稍微延遲讓進度條動畫明顯

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
        # 右指標向左移動，直到數值小於基準點 [cite: 1410]
        while data[right] >= data[pivot] and left < right:
            right -= 1
        # 左指標向右移動，直到數值大於基準點 [cite: 1410]
        while data[left] <= data[pivot] and left < right:
            left += 1
            
        if left < right:
            data[left], data[right] = data[right], data[left]  # [cite: 1410]
            
    # 左右指標相撞，交換基準點與相撞處數值 [cite: 1411]
    data[pivot], data[right] = data[right], data[pivot]
    
    # 動態估算進度 (以已切分完畢的比例計算)
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99.0, (current_sorted / total_len) * 100)
    time.sleep(0.002)  # 稍微延遲讓 Quick Sort 有動畫漸進感
    
    # 遞迴處理左右子陣列 [cite: 1411]
    quick_sort_recursive(data, start, right - 1, total_len, progress_dict)
    quick_sort_recursive(data, right + 1, end, total_len, progress_dict)

def run_quick_sort(arr, progress_dict):
    data = list(arr)
    n = len(data)
    quick_sort_recursive(data, 0, n - 1, n, progress_dict)
    progress_dict['Quick'] = 100.0  # 結束時確保為 100%

# ==========================================
# 2. 視窗與視覺化呈現 (允許使用 Tkinter 處理外殼)
# ==========================================

class SortingHomeworkWindow:
    def __init__(self):
        # 建立主視窗 (彈跳視窗)
        self.root = tk.Tk()
        self.root.title("Sorting Algorithms Efficiency")
        self.root.geometry("550x400")
        
        # 即時數據共享結構
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.is_running = False
        
        # 視窗標題文字
        title = tk.Label(self.root, text="Sorting Algorithms Efficiency", font=('Helvetica', 16, 'bold'))
        title.pack(pady=10)
        
        # 核心畫布：用來手動繪製進度條與時間
        self.canvas = tk.Canvas(self.root, width=500, height=180, bg='white', borderwidth=1, relief="solid")
        self.canvas.pack(pady=10)
        
        # 繪製初始狀態
        self.draw_interface()
        
        # 按鈕區域 (跟老師一樣有開始與關閉視窗的鍵)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)
        
        # 開始模擬鍵
        self.start_btn = tk.Button(btn_frame, text="Start Simulations", command=self.start_simulations, width=15, font=('Helvetica', 10, 'bold'))
        self.start_btn.pack(side=tk.LEFT, x=10)
        
        # 關閉視窗鍵
        quit_btn = tk.Button(btn_frame, text="Quit", command=self.root.destroy, width=10, font=('Helvetica', 10))
        quit_btn.pack(side=tk.LEFT, x=10)
        
        # 啟動每 20 毫秒刷新畫面的循環
        self.refresh_window()

    def draw_interface(self):
        """完全由程式碼手動計算座標，將演算法效能進度『畫』在畫布上"""
        self.canvas.delete("all")  # 擦除舊畫面
        
        algos = ['Selection', 'Bubble', 'Quick']
        colors = ['#2ecc71', '#f1c40f', '#3498db']  # 綠、黃、藍
        
        for i, algo in enumerate(algos):
            y = 30 + i * 55  # 計算每一列的 y 軸位置
            pct = self.progress[algo]
            
            # 1. 畫演算法文字
            self.canvas.create_text(100, y, text=f"{algo} Sort:", font=('Helvetica', 11, 'bold'), anchor='e')
            
            # 2. 畫進度條外框 (寬度 250 像素)
            self.canvas.create_rectangle(110, y - 10, 360, y + 10, outline='gray')
            
            # 3. 根據當前百分比計算進度條長度並著色
            bar_width = 110 + int(250 * (pct / 100))
            if bar_width > 110:
                self.canvas.create_rectangle(110, y - 10, bar_width, y + 10, fill=colors[i], outline='')
                
            # 4. 畫百分比數字
            self.canvas.create_text(375, y, text=f"{int(pct)}%", font=('Helvetica', 10, 'bold'), anchor='w')
            
            # 5. 顯示即時狀態或最終耗時
            if pct == 100.0:
                status_text = f"{self.runtimes[algo]:.6f} s"
            elif self.is_running:
                status_text = "Running..."
            else:
                status_text = "Pending..."
                
            self.canvas.create_text(425, y, text=status_text, font=('Courier', 10), anchor='w')

    def thread_handler(self, sort_func, algo_label, data_list):
        """執行緒包裝：精準測量演算法執行總時間"""
        start_time = time.time()
        sort_func(data_list, self.progress)
        self.runtimes[algo_label] = time.time() - start_time
        self.progress[algo_label] = 100.0

    def start_simulations(self):
        """點擊『Start Simulations』鍵時觸發的多執行緒效能比較"""
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)  # 執行中禁用開始鍵
        
        # 資料重設
        self.progress = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        self.runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
        
        # 2. 模擬隨機產出包含 N 個隨機不重覆數字 (此處設 N=200)
        test_data = list(range(1, 201))
        random.shuffle(test_data)
        
        # 3. 使用三個 thread，獨立跑排序演算法，達到同步進行效能視覺化
        t1 = threading.Thread(target=self.thread_handler, args=(selection_sort, 'Selection', test_data), daemon=True)
        t2 = threading.Thread(target=self.thread_handler, args=(bubble_sort, 'Bubble', test_data), daemon=True)
        t3 = threading.Thread(target=self.thread_handler, args=(run_quick_sort, 'Quick', test_data), daemon=True)
        
        # 同步啟動
        t1.start()
        t2.start()
        t3.start()

    def refresh_window(self):
        """定時重新繪製畫布內容，達到動態視覺化效果"""
        self.draw_interface()
        
        # 如果三個 Thread 都抵達 100%，恢復開始鍵
        if self.is_running and all(pct == 100.0 for pct in self.progress.values()):
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            
        # 每 20 毫秒重複執行此刷新機制
        self.root.after(20, self.refresh_window)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = SortingHomeworkWindow()
    app.run()
