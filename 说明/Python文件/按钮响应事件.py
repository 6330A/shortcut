import tkinter as tk


def increment_counter():
    current_value = int(counter_label["text"])
    new_value = current_value + 1
    counter_label.config(text=str(new_value))


def decrement_counter():
    current_value = int(counter_label["text"])
    new_value = current_value - 1
    counter_label.config(text=str(new_value))


# 创建主窗口
root = tk.Tk()
root.title("计数器")

# 创建文本标签
counter_label = tk.Label(root, text="0", font=("Arial", 24))
counter_label.pack(pady=20)

# 创建按钮
increment_button1 = tk.Button(root, text="加1", command=increment_counter)
increment_button1.pack()

# 创建按钮
increment_button2 = tk.Button(root, text="减1", command=decrement_counter)
increment_button2.pack()

# 运行主循环
root.mainloop()
