import random
import threading
import time
import tkinter as tk

# ==========================================
# 1. 選擇排序法 (Selection Sort)
# ==========================================
def selection_sort(arr, viz_callback):
    n = len(arr)
    for i in range(n):  # for (i in all elements of array)
        smallest_idx = i
        for j in range(i + 1, n):  # for (j in i+1 to the last element of array)
            if arr[j] < arr[smallest_idx]:  # find smallest values
                smallest_idx = j
            # 紅色代表目前掃描到的柱子，黃色代表目前認定的最小值柱子
            viz_callback(arr, current=j, target=smallest_idx, sorted_up_to=i)
            time.sleep(0.01)
        arr[i], arr[smallest_idx] = arr[smallest_idx], arr[i]  # swap
        viz_callback(arr, current=i, target=smallest_idx, sorted_up_to=i+1)
        time.sleep(0.01)
    viz_callback(arr, done=True)

# ==========================================
# 2. 插入排序法 (Insertion Sort)
# ==========================================
def insertion_sort(arr, viz_callback):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            viz_callback(arr, current=j, target=i, sorted_up_to=i)
            time.sleep(0.01)
        arr[j + 1] = key
        viz_callback(arr, current=j+1, target=i, sorted_up_to=i+1)
        time.sleep(0.01)
    viz_callback(arr, done=True)

# ==========================================
# 3. 快速排序法 (Quick Sort) - 嚴格對齊簡報雙指標法
# ==========================================
def quick_sort_wrapper(arr, viz_callback):
    _quick_sort(arr, 0, len(arr) - 1, viz_callback)
    viz_callback(arr, done=True)

def _quick_sort(arr, start, end, viz_callback):
    if start >= end:  # if (array length <= 1) 終止條件
        return
        
    pivot = start  # 將陣列最開始元素當成基準點
    left = start   # left = start
    right = end    # right = end
    
    while left < right:  # while (left != right)
        # decrease right until (array[right] < array[pivot])
        while left < right and arr[right] >= arr[pivot]:
            right -= 1
            viz_callback(arr, current=right, target=pivot)
            time.sleep(0.005)
            
        # increase left until (array[left] > array[pivot])
        while left < right and arr[left] <= arr[pivot]:
            left += 1
            viz_callback(arr, current=left, target=pivot)
            time.sleep(0.005)
            
        if left < right:
            arr[left], arr[right] = arr[right], arr[left]  # swap(array[left], array[right])
            viz_callback(arr, current=left, target=right)
            time.sleep(0.005)
            
    arr[pivot], arr[right] = arr[right], arr[pivot]  # swap(array[pivot], array[right])
    viz_callback(arr, current=right, target=pivot)
    time.sleep(0.005)
    
    _quick_sort(arr, start, right - 1, viz_callback)  # QuickSort(array, start, pivot - 1)
    _quick_sort(arr, right + 1, end, viz_callback)    # QuickSort(array, pivot + 1, end)


# ==========================================
# Tkinter GUI 視覺化介面 (完美對齊老師範例影片)
# ==========================================
class SortingVisualizer:
    def __init__(self, root, data_size=50):
        self.root = root
        self.root.title("演算法效能比較 (Selection vs Insertion vs Quick)")
        self.root.configure(bg="#f0f0f0")
        
        self.data_size = data_size
        # 產生包含 N 個隨機不重複數字
        self.original_data = list(range(5, 5 + data_size * 5, 5))
        random.shuffle(self.original_data)
        
        # 複製三份給不同的演算法
        self.data_selection = list(self.original_data)
        self.data_insertion = list(self.original_data)
        self.data_quick = list(self.original_data)
        
        # 讓畫布寬高配合長條圖呈現細緻外觀
        self.canvas_width = 300
        self.canvas_height = 250
        
        # 建立上方大標題
        main_title = tk.Label(root, text="Sorting Algorithms Performance Comparison", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        main_title.pack(pady=10)
        
        # 橫向排列的三個區域容器
        self.display_frame = tk.Frame(root, bg="#f0f0f0")
        self.display_frame.pack(padx=20)
        
        self.create_canvas_section("Selection Sort", 0)
        self.create_canvas_section("Insertion Sort", 1)
        self.create_canvas_section("Quick Sort (雙指標)", 2)
        
        # 控制按鈕區域 (已修正 padx 參數)
        self.btn_start = tk.Button(root, text="► 開始同步排序 (Multi-threading)", command=self.start_sorting, 
                                  font=("Microsoft JhengHei", 11, "bold"), bg="#2c3e50", fg="white", activebackground="#34495e")
        self.btn_start.pack(pady=15)

    def create_canvas_section(self, title, col):
        frame = tk.LabelFrame(self.display_frame, text=title, font=("Microsoft JhengHei", 10, "bold"), bg="white", padx=5, pady=5)
        frame.pack(side=tk.LEFT, padx=10)
        
        # 建立黑色背景的長條圖畫布
        canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="#1e1e1e", highlightthickness=0)
        canvas.pack()
        
        time_label = tk.Label(frame, text="執行時間: 0.000 秒", font=("Microsoft JhengHei", 10), bg="white", fg="#555")
        time_label.pack(pady=5)
        
        if col == 0:
            self.canvas_sel, self.lbl_sel = canvas, time_label
            self.draw_data(self.canvas_sel, self.data_selection)
        elif col == 1:
            self.canvas_ins, self.lbl_ins = canvas, time_label
            self.draw_data(self.canvas_ins, self.data_insertion)
        elif col == 2:
            self.canvas_qck, self.lbl_qck = canvas, time_label
            self.draw_data(self.canvas_qck, self.data_quick)

    def draw_data(self, canvas, arr, current=-1, target=-1, sorted_up_to=-1, done=False):
        canvas.delete("all")
        
        # 計算每根柱子的寬度與間距
        padding = 1
        bar_width = (self.canvas_width / self.data_size) - padding
        max_val = max(self.original_data)
        
        for i, val in enumerate(arr):
            bar_height = (val / max_val) * (self.canvas_height - 30)
            x0 = i * (bar_width + padding) + padding
            y0 = self.canvas_height - bar_height
            x1 = x0 + bar_width
            y1 = self.canvas_height
            
            # 動態色彩配置
            if done:
                color = "#2ecc71"  # 排序全部完成：亮綠色
            elif i == current:
                color = "#e74c3c"  # 當前活動/比對指標：紅色
            elif i == target:
                color = "#f1c40f"  # 目標/基準/最小值位置：黃色
            elif sorted_up_to != -1 and i < sorted_up_to:
                color = "#27ae60"  # 局部已排序區域：深綠色
            else:
                color = "#3498db"  # 未排序區域：天空藍
                
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def start_sorting(self):
        self.btn_start.config(state=tk.DISABLED, bg="#ccc")
        
        # 同步啟動三個 Thread 執行緒
        t1 = threading.Thread(target=selection_sort, args=(self.data_selection, self.get_callback(self.canvas_sel, self.lbl_sel)))
        t2 = threading.Thread(target=insertion_sort, args=(self.data_insertion, self.get_callback(self.canvas_ins, self.lbl_ins)))
        t3 = threading.Thread(target=quick_sort_wrapper, args=(self.data_quick, self.get_callback(self.canvas_qck, self.lbl_qck)))
        
        t1.start()
        t2.start()
        t3.start()

    def get_callback(self, canvas, label):
        start_time = time.time()
        def callback(arr, current=-1, target=-1, sorted_up_to=-1, done=False):
            elapsed = time.time() - start_time
            # 使用 root.after 確保安全在 Tkinter 主執行緒更新畫面
            self.root.after(0, lambda: self.update_ui(canvas, label, arr, current, target, sorted_up_to, elapsed, done))
