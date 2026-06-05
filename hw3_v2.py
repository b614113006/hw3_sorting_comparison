import random
import time
import threading
import sys

# ==========================================
# 1. 自訂排序演算法 (嚴格遵循投影片教學邏輯)
# ==========================================

def selection_sort(arr, progress_dict):
    """
    選擇排序法：反覆從未排序數列中找最小值，與左邊數字交換 (O(n²))
    """
    n = len(arr)
    # 複製一份避免影響其他執行緒
    data = list(arr) 
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        # 交換數值
        data[i], data[min_idx] = data[min_idx], data[i]
        
        # 更新進度百分比
        progress_dict['Selection'] = int(((i + 1) / n) * 100)
        time.sleep(0.005)  # 稍微延遲以便在終端機觀察動畫效果

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
        
        # 更新進度百分比 (投影片邏輯：做完一輪擠出一個最大值)
        progress_dict['Bubble'] = int(((n - i + 1) / (n - 1)) * 100)
        time.sleep(0.005)

def quick_sort_recursive(arr, start, end, total_len, progress_dict):
    """
    快速排序法核心遞迴：雙指標朝中間移動、交換、切分左右子陣列 (投影片第12頁虛擬碼邏輯)
    """
    if start >= end:
        return
        
    pivot = start
    left = start
    right = end
    
    while left != right:
        # 右指標往左移動，直到找到比基準點小的數值
        while data_qs[right] >= data_qs[pivot] and left < right:
            right -= 1
        # 左指標往右移動，直到找到比基準點大的數值
        while data_qs[left] <= data_qs[pivot] and left < right:
            left += 1
            
        if left < right:
            data_qs[left], data_qs[right] = data_qs[right], data_qs[left]
            
    # 左右指標相撞，交換基準點與相撞處數值
    data_qs[pivot], data_qs[right] = data_qs[right], data_qs[pivot]
    
    # 估算 Quick Sort 的進度 (以已定位的 pivot 數量或切分深度模擬)
    # 為了讓進度條平滑，這裡依據切分範圍比例動態更新
    current_sorted = total_len - (end - start)
    progress_dict['Quick'] = min(99, int((current_sorted / total_len) * 100))
    
    # 遞迴跑左右子陣列
    quick_sort_recursive(arr, start, right - 1, total_len, progress_dict)
    quick_sort_recursive(arr, right + 1, end, total_len, progress_dict)

def run_quick_sort(arr, progress_dict):
    """
    快速排序法執行緒入口
    """
    global data_qs
    data_qs = list(arr)
    n = len(data_qs)
    quick_sort_recursive(data_qs, 0, n - 1, n, progress_dict)
    progress_dict['Quick'] = 100

# ==========================================
# 2. 執行緒管理與終端機視覺化 (TUI)
# ==========================================

def draw_progress_bar(label, percentage, color_code):
    """
    在終端機繪製精美的進度條
    """
    bar_length = 30
    filled_length = int(round(bar_length * percentage / 100))
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    # 使用 ANSI 顏色編碼美化介面
    return f"{label:<10} [\033[{color_code}m{bar}\033[0m] {percentage:>3}%"

def main():
    print("=" * 50)
    print("     Sorting Algorithms Efficiency Comparison     ")
    print("=" * 50)
    
    # 讓使用者自訂隨機不重複數字的數量 N
    try:
        N = int(input("請輸入要測試的隨機不重複數字數量 N (建議 100-300): "))
    except ValueError:
        print("輸入錯誤，預設為 200")
        N = 200
        
    print(f"\n正在產出 {N} 個隨機不重複數字...")
    # 模擬隨機不重覆數字，不使用系統排序函式
    base_list = list(range(1, N + 1))
    random.shuffle(base_list)
    print("資料準備就緒，準備啟動三個獨立 Thread 同步執行！")
    input("按 Enter 鍵開始模擬...")

    # 記錄各演算法進度與執行時間
    progress = {'Selection': 0, 'Bubble': 0, 'Quick': 0}
    runtimes = {'Selection': 0.0, 'Bubble': 0.0, 'Quick': 0.0}
    
    # 定義執行緒包裝函式，以便精準紀錄時間
    def thread_wrapper(sort_func, label):
        start_time = time.time()
        if label == 'Quick':
            sort_func(base_list, progress)
        else:
            sort_func(base_list, progress)
        runtimes[label] = time.time() - start_time
        progress[label] = 100  # 確保結束時必定為 100%

    # 建立 3 個獨立的 Thread
    t1 = threading.Thread(target=thread_wrapper, args=(selection_sort, 'Selection'))
    t2 = threading.Thread(target=thread_wrapper, args=(bubble_sort, 'Bubble'))
    t3 = threading.Thread(target=thread_wrapper, args=(run_quick_sort, 'Quick'))

    # 啟動所有執行緒 (同步進行)
    t1.start()
    t2.start()
    t3.start()

    # 終端機動態更新視覺化畫面
    sys.stdout.write("\033[?25l")  # 隱藏終端機游標
    try:
        while t1.is_alive() or t2.is_alive() or t3.is_alive():
            # 回到畫面最上方重新繪製 (實現動畫效果)
            sys.stdout.write("\r" + " " * 60 + "\n" * 4) 
            sys.stdout.write("\033[4A") 
            
            sys.stdout.write(draw_progress_bar("Selection", progress['Selection'], "32") + "\n") # 綠色
            sys.stdout.write(draw_progress_bar("Bubble", progress['Bubble'], "33") + "\n")    # 黃色
            sys.stdout.write(draw_progress_bar("Quick", progress['Quick'], "36") + "\n")     # 青色
            sys.stdout.flush()
            time.sleep(0.05)
            
        # 最終確保所有人都顯示 100%
        sys.stdout.write("\033[3A")
        sys.stdout.write(draw_progress_bar("Selection", 100, "32") + "\n")
        sys.stdout.write(draw_progress_bar("Bubble", 100, "33") + "\n")
        sys.stdout.write(draw_progress_bar("Quick", 100, "36") + "\n")
        sys.stdout.flush()
        
    finally:
        sys.stdout.write("\033[?25h")  # 恢復終端機游標

    # 等待所有執行緒安全結束
    t1.join()
    t2.join()
    t3.join()

    # 印出最終效能統計結果
    print("\n" + "=" * 50)
    print("                 Total Runtime (seconds)         ")
    print("=" * 50)
    print(f"Selection Sort : {runtimes['Selection']:.6f} s")
    print(f"Bubble Sort    : {runtimes['Bubble']:.6f} s")
    print(f"Quick Sort     : {runtimes['Quick']:.6f} s")
    print("=" * 50)
    print("模擬完成！請將此結果錄製為動態 GIF 並上傳至 GitHub 繳交。")

if __name__ == '__main__':
    main()
