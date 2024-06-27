import tkinter as tk
import json
import keyboard

LEFT_WIDTH = 200
RIGHT_WIDTH = 400
WINDOW_WIDTH = LEFT_WIDTH + RIGHT_WIDTH
WINDOW_HEIGHT = 300
LABEL_ROWS = 8
LABEL_COLUMNS = 2

x = 0
y = 0

is_visible = True

selected = 0
currentPage = 0
pages = 0

start_index = 0
end_index = 0

SHORTCUT_FONT = "微软雅黑 14 bold"
DESCRIBE_FONT = "微软雅黑 12"
BUTTON_FONT = "微软雅黑 14 bold"
PAGE_FONT = "微软雅黑 10 bold"
FONTS = [SHORTCUT_FONT, DESCRIBE_FONT]

root = tk.Tk()

root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{screen_width - WINDOW_WIDTH - 20}+{screen_height - WINDOW_HEIGHT - 90}")
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)

with open('ShortCut.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
SoftWares = list(data.keys())


def toggle_window():
    global is_visible
    if is_visible:
        root.withdraw()
    else:
        root.deiconify()
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
    if remainder > 0:
        pages += 1

    start_index = currentPage * LABEL_ROWS
    end_index = min((currentPage + 1) * LABEL_ROWS, len(shortcuts))

    for index, rows in enumerate(shortcuts[start_index:end_index]):
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
    selected = (selected + 1) % len(SoftWares)
    currentPage = 0
    btn_close.config(text=SoftWares[selected])

    showShortcut()


def changePage(event):
    global currentPage
    global pages
    if event.delta > 0 and currentPage > 0:
        currentPage = currentPage - 1
        showShortcut()
    elif event.delta < 0 and currentPage < pages - 1:
        currentPage = currentPage + 1
        showShortcut()
    else:
        pass


def on_enter(event):
    event.widget.config(fg="#002060")


def on_leave(event):
    event.widget.config(fg="#365daa")


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
    global x, y
    x, y = 0, 0


root.bind("<MouseWheel>", changePage)

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

btn_close.grid(row=0, column=0, sticky="nsew")
btn_change.grid(row=0, column=1, sticky="nsew")

page_label.grid(row=LABEL_ROWS + 1, column=0, columnspan=2, sticky="nsew")

labels = [[tk.Label(root, anchor="w", bg="#365daa", font=FONTS[col], fg="white") for col in range(LABEL_COLUMNS)] for _
          in
          range(LABEL_ROWS)]

for row in range(LABEL_ROWS):
    for col in range(LABEL_COLUMNS):
        labels[row][col].grid(row=row + 1, column=col, sticky="nsew")
        labels[row][col].bind("<Button-1>", on_label_click)
        labels[row][col].bind("<B1-Motion>", on_label_motion)
        labels[row][col].bind("<ButtonRelease-1>", on_left_button_release)

for col in range(LABEL_COLUMNS):
    root.grid_columnconfigure(col, minsize=LEFT_WIDTH if col == 0 else RIGHT_WIDTH)
for row in range(LABEL_ROWS + 2):
    root.grid_rowconfigure(row, weight=1)
showShortcut()

root.mainloop()
