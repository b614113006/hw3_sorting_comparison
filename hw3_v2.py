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
    time.sleep(0.002)  # 稍微延遲讓 Quick Sort 有動畫漸進感
    
    # 遞迴處理左右子陣列
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
        btn_
