import tkinter as tk
import json
import keyboard

# 定义常量 窗口尺寸，展示行数和列数
LEFT_WIDTH = 200
RIGHT_WIDTH = 400
WINDOW_WIDTH = LEFT_WIDTH + RIGHT_WIDTH
WINDOW_HEIGHT = 300
LABEL_ROWS = 8
LABEL_COLUMNS = 2

# 设置窗口移动的
x = 0
y = 0

# 显示窗口
is_visible = True

# 时间响应变量
selected = 0
currentPage = 0
pages = 0

# 响应页面变量
start_index = 0
end_index = 0

# 定义不同列对应的字体
SHORTCUT_FONT = "微软雅黑 14 bold"
DESCRIBE_FONT = "微软雅黑 12"
BUTTON_FONT = "微软雅黑 14 bold"
PAGE_FONT = "微软雅黑 10 bold"
FONTS = [SHORTCUT_FONT, DESCRIBE_FONT]

# 创建主窗口
root = tk.Tk()

# 不显示标题等，关闭窗口请点击左上角,和热键的隐藏不再冲突
root.overrideredirect(True)

# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置窗口位置 固定大小
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{screen_width - WINDOW_WIDTH - 20}+{screen_height - WINDOW_HEIGHT - 90}")
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)

# 使用 Python 读取 JSON 文件，并解析其中的信息
with open('ShortCut.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
SoftWares = list(data.keys())


def toggle_window():
    global is_visible
    if is_visible:
        root.withdraw()  # 隐藏窗口
    else:
        root.deiconify()  # 显示窗口
    is_visible = not is_visible


keyboard.add_hotkey("ctrl + \\", toggle_window)


def showShortcut():
    global selected
    global currentPage
    global pages
    global start_index
    global end_index

    root.attributes('-topmost', True)
    shortcuts = data[SoftWares[selected]]
    pages, remainder = divmod(len(shortcuts), LABEL_ROWS)
    if remainder > 0:  # 如果有余数，则商需要加一
        pages += 1

    # 计算起始索引和结束索引
    start_index = currentPage * LABEL_ROWS
    end_index = min((currentPage + 1) * LABEL_ROWS, len(shortcuts))

    # 获取对应范围的值并赋值给 labels
    for index, rows in enumerate(shortcuts[start_index:end_index]):
        # 键名必须与json一致
        labels[index][0]["text"] = rows["快捷键"]
        labels[index][1]["text"] = rows["描述"]
    for i in range(end_index - start_index, LABEL_ROWS):
        labels[i][1]["text"] = ""
        labels[i][0]["text"] = ""
    page_label.config(text=f"{currentPage + 1}/{pages}")


def closeExe():
    root.destroy()


def switchSoftware():
    global selected
    global currentPage
    global start_index
    global end_index
    # 点击切换按钮时，selected + 1 循环遍历， currentPage = 0
    selected = (selected + 1) % len(SoftWares)
    currentPage = 0
    btn_close.config(text=SoftWares[selected])  # 修改所查软件

    showShortcut()


def changePage(event):
    # currentPage 范围 [0 - pages), 滚轮切换控制currentPage不会超出范围
    global currentPage
    global pages
    if event.delta > 0 and currentPage > 0:  # 上滚
        currentPage = currentPage - 1
        showShortcut()
    elif event.delta < 0 and currentPage < pages - 1:
        currentPage = currentPage + 1
        showShortcut()
    else:
        pass


def on_enter(event):
    event.widget.config(fg="#002060")  # 鼠标进入时的背景颜色


def on_leave(event):
    event.widget.config(fg="#365daa")  # 鼠标离开时恢复背景颜色


def on_label_click(event):
    global x, y
    x, y = event.x, event.y


def on_label_motion(event):
    global x, y
    if x != 0 and y != 0:
        new_x = root.winfo_x() + (event.x - x)
        new_y = root.winfo_y() + (event.y - y)
        root.geometry(f"+{new_x}+{new_y}")


def on_left_button_release(event):
    # 清空鼠标位置信息
    global x, y
    x, y = 0, 0


# 绑定滚轮事件
root.bind("<MouseWheel>", changePage)

# 两个按钮，左边显示当前软件，点击关闭窗口
# 右边切换软件,关闭功能暂时关闭吧,不知道添加什么功能
btn_close = tk.Button(root, text=SoftWares[selected], anchor="w", command=closeExe, font=BUTTON_FONT, fg="#365daa",
                      bd=0, highlightthickness=0, bg="#f1f3f9")
btn_change = tk.Button(root, text="↻", anchor="w", command=switchSoftware, font=BUTTON_FONT, fg="#365daa", bd=0,
                       highlightthickness=0, bg="#f1f3f9")
page_label = tk.Label(root, text="currentPage+1/pages", anchor="e", bg="#365daa", font=PAGE_FONT, fg="white",
                      highlightbackground="white")
btn_close.bind("<Enter>", on_enter)
btn_close.bind("<Leave>", on_leave)

btn_change.bind("<Enter>", on_enter)
btn_change.bind("<Leave>", on_leave)

# 按钮放置在第一行
btn_close.grid(row=0, column=0, sticky="nsew")
btn_change.grid(row=0, column=1, sticky="nsew")

# 页面放在左下角
page_label.grid(row=LABEL_ROWS + 1, column=0, columnspan=2, sticky="nsew")

# 创建标签并设置字体
labels = [[tk.Label(root, anchor="w", bg="#365daa", font=FONTS[col], fg="white") for col in range(LABEL_COLUMNS)] for _
          in
          range(LABEL_ROWS)]

# 放置文本标签
for row in range(LABEL_ROWS):
    for col in range(LABEL_COLUMNS):
        labels[row][col].grid(row=row + 1, column=col, sticky="nsew")
        labels[row][col].bind("<Button-1>", on_label_click)
        labels[row][col].bind("<B1-Motion>", on_label_motion)
        labels[row][col].bind("<ButtonRelease-1>", on_left_button_release)

# 设置网格布局权重
for col in range(LABEL_COLUMNS):
    root.grid_columnconfigure(col, minsize=LEFT_WIDTH if col == 0 else RIGHT_WIDTH)
for row in range(LABEL_ROWS + 2):
    root.grid_rowconfigure(row, weight=1)
showShortcut()

root.mainloop()
