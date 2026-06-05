import random
import threading
import time
import os

# 全局延遲設定（秒），用來調整動畫速度
DELAY = 0.01

# ==========================================
# 1. 選擇排序法 (Selection Sort)
# ==========================================
def selection_sort(arr, viz_callback):
    """
    對齊簡報：雙層 for 迴圈，反覆從未排序區找最小值與左邊交換
    """
    n = len(arr)
    # i 從 0 到 n-1 (all elements)
    for i in range(n):  # [cite: 737]
        smallest_idx = i
        # j 從 i+1 到最後一個元素
        for j in range(i + 1, n):  # [cite: 738]
            if arr[j] < arr[smallest_idx]:
                smallest_idx = j
            # 每一次比對都可以觸發視覺化回傳
            viz_callback(arr, current=j, target=smallest_idx)
            time.sleep(DELAY)
            
        # 將最小值與第 i 個數值交換
        arr[i], arr[smallest_idx] = arr[smallest_idx], arr[i]  # [cite: 738]
        viz_callback(arr, current=i, target=smallest_idx)
        time.sleep(DELAY)
    return arr

# ==========================================
# 2. 泡泡排序法 (Bubble Sort)
# ==========================================
def bubble_sort(arr, viz_callback):
    """
    對齊簡報：i 從 n 遞減到 1，j 從 0 到 i-1，兩兩比較把最大值擠到後面
    """
    n = len(arr)
    # i from n to 1
    for i in range(n, 0, -1):  # [cite: 999]
        # j in 0 to i-1
        for j in range(0, i - 1):  # [cite: 1001]
            if arr[j] > arr[j + 1]:  # [cite: 1002]
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # [cite: 1003]
            # 實時觸發視覺化
            viz_callback(arr, current=j, target=j+1)
            time.sleep(DELAY)
    return arr

# ==========================================
# 3. 快速排序法 (Quick Sort) - 嚴格對齊簡報雙指標法
# ==========================================
def quick_sort_wrapper(arr, viz_callback):
    """
    包裝函式，用來啟動遞迴
    """
    _quick_sort(arr, 0, len(arr) - 1, viz_callback)
    return arr

def _quick_sort(arr, start, end, viz_callback):
    """
    對齊簡報：選第一個元素為 pivot，left/right 指標向中間靠攏
    """
    # 終止條件：子陣列長度小於等於 1
    if start >= end:  # [cite: 1403, 1406]
        return
        
    pivot = start  # 將陣列最開始元素當成基準點 [cite: 1060, 1407]
    left = start   # [cite: 1408]
    right = end    # [cite: 1409]
    
    # while (left != right)
    while left < right:  # [cite: 1410]
        # 往左移動右指標，直到碰到小於基準點者
        while left < right and arr[right] >= arr[pivot]:  # [cite: 1210, 1411]
            right -= 1
            viz_callback(arr, current=right, target=pivot)
            time.sleep(DELAY)
            
        # 往右移動左指標，直到碰到大於基準點者
        while left < right and arr[left] <= arr[pivot]:  # [cite: 1212, 1411]
            left += 1
            viz_callback(arr, current=left, target=pivot)
            time.sleep(DELAY)
            
        # 交換左指標和右指標內容
        if left < right:  # [cite: 1182, 1235]
            arr[left], arr[right] = arr[right], arr[left]  # [cite: 1411]
            viz_callback(arr, current=left, target=right)
            time.sleep(DELAY)
            
    # 移動到左右指標碰在一起，此時終止，交換基準點與相撞處的值
    arr[pivot], arr[right] = arr[right], arr[pivot]  # [cite: 1280, 1306, 1412]
    viz_callback(arr, current=right, target=pivot)
    time.sleep(DELAY)
    
    # 遞迴跑左右兩邊的子陣列
    _quick_sort(arr, start, right - 1, viz_callback)  # [cite: 1388, 1412]
    _quick_sort(arr, right + 1, end, viz_callback)    # [cite: 1388, 1412]
