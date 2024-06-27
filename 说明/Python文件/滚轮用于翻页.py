import tkinter as tk


def increment_counter(event):
    current_value = int(counter_label["text"])
    if event.delta > 0:  # 滚轮上滚
        new_value = current_value + 1
    else:  # 滚轮下滚
        new_value = current_value - 1
    counter_label.config(text=str(new_value))


# 创建主窗口
root = tk.Tk()
root.title("计数器")

# 创建文本标签
counter_label = tk.Label(root, text="0", font=("Arial", 24))
counter_label.pack(pady=20)

# 绑定鼠标滚轮事件
root.bind("<MouseWheel>", increment_counter)

# 运行主循环
root.mainloop()
