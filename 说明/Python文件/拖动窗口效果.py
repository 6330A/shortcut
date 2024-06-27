import tkinter as tk

class DraggableWindow:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # 移除窗口边框
        self.x = 0
        self.y = 0

        # 绑定鼠标事件
        self.root.bind("<Button-1>", self.on_left_button_down)
        self.root.bind("<ButtonRelease-1>", self.on_left_button_up)
        self.root.bind("<B1-Motion>", self.on_mouse_move)

    def on_left_button_down(self, event):
        # 记录鼠标当前位置和窗口当前位置的差值
        self.x = event.x
        self.y = event.y

    def on_left_button_up(self, event):
        # 清空鼠标位置信息
        self.x = 0
        self.y = 0

    def on_mouse_move(self, event):
        # 如果鼠标左键被按下，则根据鼠标移动的距离来更新窗口位置
        if self.x != 0 and self.y != 0:
            new_x = self.root.winfo_x() + (event.x - self.x)
            new_y = self.root.winfo_y() + (event.y - self.y)
            self.root.geometry(f"+{new_x}+{new_y}")

if __name__ == "__main__":
    root = tk.Tk()
    window = DraggableWindow(root)
    root.mainloop()
