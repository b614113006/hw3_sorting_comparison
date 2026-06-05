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
            viz_callback(arr, current=j, target=smallest_idx)
            time.sleep(0.01)
        arr[i], arr[smallest_idx] = arr[smallest_idx], arr[i]  # swap
        viz_callback(arr, current=i, target=smallest_idx)
        time.sleep(0.01)
    viz_callback(arr, done=True)

# ==========================================
# 2. 泡泡排序法 (Bubble Sort)
# ==========================================
def bubble_sort(arr, viz_callback):
    n = len(arr)
    for i in range(n, 0, -1):  # for (i from n to 1)
        for j in range(0, i - 1):  # for (j in 0 to i-1)
            if arr[j] > arr[j + 1]:  # if (array[j] > array[j+1])
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # swap
            viz_callback(arr, current=j, target=j+1)
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
            time.sleep(0.01)
            
        # increase left until (array[left] > array[pivot])
        while left < right and arr[left] <= arr[pivot]:
            left += 1
            viz_callback(arr, current=left, target=pivot)
            time.sleep(0.01)
            
        if left < right:
            arr[left], arr[right] = arr[right], arr[left]  # swap(array[left], array[right])
            viz_callback(arr, current=left, target=right)
            time.sleep(0.01)
            
    arr[pivot], arr[right] = arr[right], arr[pivot]  # swap(array[pivot], array[right])
    viz_callback(arr, current=right, target=pivot)
    time.sleep(0.01)
    
    _quick_sort(arr, start, right - 1, viz_callback)  # QuickSort(array, start, pivot - 1)
    _quick_sort(arr, right + 1, end, viz_callback)    # QuickSort(array, pivot + 1, end)


# ==========================================
# Tkinter GUI 視覺化介面
# ==========================================
class SortingVisualizer:
    def __init__(self, root, data_size=40):
        self.root = root
        self.root.title("演算法效能比較 (Selection vs Bubble vs Quick)")
        
        self.data_size = data_size
        # 產出包含 N 個隨機不重覆數字
        self.original_data = list(range(10, 10 + data_size * 5, 5))
        random.shuffle(self.original_data)
        
        # 複製三份給不同的演算法
        self.data_selection = list(self.original_data)
        self.data_bubble = list(self.original_data)
        self.data_quick = list(self.original_data)
        
        # 建立三個畫布
        self.canvas_width = 250
        self.canvas_height = 200
        
        self.create_canvas_section("Selection Sort", 0)
        self.create_canvas_section("Bubble Sort", 1)
        self.create_canvas_section("Quick Sort (雙指標)", 2)
        
        # 開始按鈕
        self.btn_start = tk.Button(root, text="開始同步排序 (Multi-threading)", command=self.start_sorting, font=("Arial", 12))
        self.btn_start.pack(pady=10)

    def create_canvas_section(self, title, col):
        frame = tk.LabelFrame(self.root, text=title, font=("Arial", 10, "bold"))
        frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        canvas.pack()
        
        time_label = tk.Label(frame, text="時間: 0.000s", font=("Arial", 10))
        time_label.pack(pady=2)
        
        if col == 0:
            self.canvas_sel, self.lbl_sel = canvas, time_label
            self.draw_data(self.canvas_sel, self.data_selection)
        elif col == 1:
            self.canvas_bub, self.lbl_bub = canvas, time_label
            self.draw_data(self.canvas_bub, self.data_bubble)
        elif col == 2:
            self.canvas_qck, self.lbl_qck = canvas, time_label
            self.draw_data(self.canvas_qck, self.data_quick)

    def draw_data(self, canvas, arr, current=-1, target=-1, done=False):
        canvas.delete("all")
        bar_width = self.canvas_width / self.data_size
        max_val = max(self.original_data)
        
        for i, val in enumerate(arr):
            bar_height = (val / max_val) * (self.canvas_height - 20)
            x0 = i * bar_width
            y0 = self.canvas_height - bar_height
            x1 = (i + 1) * bar_width
            y1 = self.canvas_height
            
            if done:
                color = "#2ecc71"
            elif i == current:
                color = "#e74c3c"
            elif i == target:
                color = "#f1c40f"
            else:
                color = "#3498db"
                
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def start_sorting(self):
        self.btn_start.config(state=tk.DISABLED)
        
        # 建立三個 Thread 獨立跑排序
        t1 = threading.Thread(target=selection_sort, args=(self.data_selection, self.get_callback(self.canvas_sel, self.lbl_sel)))
        t2 = threading.Thread(target=bubble_sort, args=(self.data_bubble, self.get_callback(self.canvas_bub, self.lbl_bub)))
        t3 = threading.Thread(target=quick_sort_wrapper, args=(self.data_quick, self.get_callback(self.canvas_qck, self.lbl_qck)))
        
        t1.start()
        t2.start()
        t3.start()

    def get_callback(self, canvas, label):
        start_time = time.time()
        def callback(arr, current=-1, target=-1, done=False):
            elapsed = time.time() - start_time
            self.root.after(0, lambda: self.update_ui(canvas, label, arr, current, target, elapsed, done))
        return callback

    def update_ui(self, canvas, label, arr, current, target, elapsed, done):
        self.draw_data(canvas, arr, current, target, done)
        label.config(text=f"時間: {elapsed:.3f}s")

if __name__ == "__main__":
    window = tk.Tk()
    app = SortingVisualizer(window, data_size=40)
    window.mainloop()
