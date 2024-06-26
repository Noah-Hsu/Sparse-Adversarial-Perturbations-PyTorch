import ctypes
import threading
import tkinter as tk
from ctypes import windll
from tkinter import ttk

import numpy as np
import sv_ttk
import subprocess
import PIL
from PIL import Image, ImageTk


class GUI:
    def __init__(self, root, dataset, attack):
        self.root = root
        self.dataSet = dataset
        self.attack = attack
        self.before_images = []
        self.after_images = []
        self.posi_images = []
        self.nege_images = []
        self.batch = 0
        self.inner_canvas = None  # 用于显示图片的 Frame
        self.wait_window = None  # 存储等待窗口的引用
        self.event = threading.Event()  # 用于通知任务结束的事件
        self.label = None
        self.labelframe = None

    def show_dataset(self, frame):
        # 设置数据集下拉框
        tk.Label(frame, text='数据集').pack()
        var = tk.StringVar()
        values = ['UCF-101', '数据集2', '数据集3', '数据集4']
        self.dataSet = ttk.Combobox(frame, textvariable=var, state='readonly', width=16, height=5)
        self.dataSet['values'] = values
        self.dataSet.pack()
        self.dataSet.bind('<<ComboboxSelected>>', self.chosen_dataset)

    def show_attack(self, frame):
        tk.Label(frame, text='方法').pack()
        var = tk.StringVar()
        values = ['SAP', '方法2', '方法3', '方法4', '方法5', '方法6', '方法7', '方法8']
        self.attack = ttk.Combobox(frame, textvariable=var, state='readonly', width=16, height=5)
        self.attack['values'] = values
        self.attack.pack()
        self.attack.bind('<<ComboboxSelected>>', self.chosen_attack)

    def chosen_dataset(self, event):
        print(self.dataSet.current(), self.dataSet.get())
        print(self.attack.current(), self.attack.get())
        if self.dataSet.current() == 0:
            self.attack.config(values=['SAP', '方法2'])
            self.attack.current(0)
        elif self.dataSet.current() == 1:
            self.attack.config(values=['方法2', '方法3'])
            self.attack.current(0)
        elif self.dataSet.current() == 2:
            self.attack.config(values=['方法3', '方法4'])
            self.attack.current(0)
        elif self.dataSet.current() == 3:
            self.attack.config(values=['SAP', '方法4'])
            self.attack.current(0)
        else:
            self.attack.config(values=['test'])
            self.attack.current(0)

    def chosen_attack(self, event):
        print(self.dataSet.current(), self.dataSet.get())
        print(self.attack.current(), self.attack.get())
        # if self.attack.current() == 0:
        #     self.dataSet.config(values=['数据集1', '数据集4'])
        #     self.dataSet.current(0)
        # elif self.attack.current() == 1:
        #     self.dataSet.config(values=['数据集1', '数据集2'])
        #     self.dataSet.current(0)
        # elif self.attack.current() == 2:
        #     self.dataSet.config(values=['数据集2', '数据集3'])
        #     self.dataSet.current(0)
        # elif self.attack.current() == 3:
        #     self.dataSet.config(values=['数据集3', '数据集4'])
        #     self.dataSet.current(0)
        # else:
        #     self.attack.config(values=['test'])

    def confirm(self):
        print(self.dataSet.current(), self.dataSet.get())
        print(self.attack.current(), self.attack.get())
        # self.root.update_idletasks()
        # self.root.withdraw()
        self.open_result()
        if self.dataSet.get() == 'UCF-101' and self.attack.get() == 'SAP':
            1
        else:
            self.open_warning()

    def test(self):
        # 启动一个新线程来执行长时间运行的任务
        thread = threading.Thread(target=self.run_long_task)
        thread.start()

        # 显示等待窗口
        self.open_wait()

    def run_long_task(self):
        # 在这里运行长时间的任务
        subprocess.run(["D:\\APPS\\AnaConda\\envs\\anaconda\\python", "l21_optimization.py",
                        "--input_dir", "../../0Dataset/UCF101/UCF-101-frames",
                        "--split_path", "../../0Dataset/UCF101/ucfTrainTestlist",
                        "--checkpoint_model", "ConvLSTM_150.pth"])
        subprocess.run(["D:\\APPS\\AnaConda\\envs\\anaconda\\python", "calpics.py"])
        # 任务结束后设置事件
        self.event.set()

    def open_wait(self):
        self.wait_window = tk.Toplevel()
        self.wait_window.title("中转")
        self.wait_window.geometry("200x100")
        label = tk.Label(self.wait_window, text="请稍候")
        label.pack()
        # 检查事件是否已经设置，如果设置了就关闭等待窗口
        self.check_event()

    def check_event(self):
        if not self.event.is_set():
            # 如果事件没有设置，则继续等待
            self.wait_window.after(100, self.check_event)
        else:
            # 如果事件已经设置，则关闭等待窗口
            self.wait_window.destroy()

    def open_warning(self):
        new_window = tk.Toplevel()
        new_window.title("警告")
        new_window.geometry("200x100")
        label = tk.Label(new_window, text="暂未实现")
        label.pack()

    def show_batch(self, frame):
        tk.Label(frame, text='训练轮次').pack()
        var = tk.StringVar()
        values = [str(i) for i in range(100)]
        self.batch = ttk.Combobox(frame, textvariable=var, state='readonly', width=16, height=5)
        self.batch['values'] = values
        self.batch.pack()
        self.batch.bind('<<ComboboxSelected>>', self.chosen_batch)  # 绑定到选中条目的方法

    def chosen_batch(self, event):
        self.update_images(self.batch.get())
        self.update_label(self.batch.get())

    def clear_frame_labels(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    def update_label(self, batch):
        self.clear_frame_labels(self.labelframe)
        # 创建新的标签
        tk.Label(self.labelframe, text=f"before：{self.label[100]}\nafter：{self.label[int(batch)]}").pack(side="left")
        # 重新显示标签框架
        self.labelframe.pack(side="top")

    def update_images(self, batch):
        # 清除原有图片
        self.before_images = []
        self.after_images = []
        self.posi_images = []
        self.nege_images = []

        # 加载新图片
        b_dir = "pic/before/0"
        a_dir = "pic/after/0"
        d_dir = "pic/diff/0"
        picsize = (160, 120)

        for i in range(40):
            singleFrame = tk.Frame(self.inner_canvas)  # 注意这里将singleFrame放置在inner_canvas中
            singleFrame.grid(row=1, column=i)

            tk.Label(singleFrame, text=f"第{i + 1}帧").grid(row=0, column=0)

            before_image = ImageTk.PhotoImage(Image.open(f"{b_dir}/{i}.jpg").resize(picsize))
            self.before_images.append(before_image)
            tk.Label(singleFrame, image=before_image).grid(row=1, column=0)

            after_image = ImageTk.PhotoImage(Image.open(f"{a_dir}/{batch}/{i}.jpg").resize(picsize))
            self.after_images.append(after_image)
            tk.Label(singleFrame, image=after_image).grid(row=2, column=0)

            # tk.Label(singleFrame, text=f"beforelabel").grid(row=3, column=0)

            # tk.Label(singleFrame, text=f"afterlabel").grid(row=4, column=0)

            posi_image = ImageTk.PhotoImage(Image.open(f"{d_dir}/{batch}/posi_{i}.jpg").resize(picsize))
            self.posi_images.append(posi_image)
            tk.Label(singleFrame, image=posi_image).grid(row=5, column=0)

            nege_image = ImageTk.PhotoImage(Image.open(f"{d_dir}/{batch}/nege_{i}.jpg").resize(picsize))
            self.nege_images.append(nege_image)
            tk.Label(singleFrame, image=nege_image).grid(row=6, column=0)

    def open_result(self):
        self.label = np.loadtxt("pic/label.txt", dtype=int)
        resultw = tk.Toplevel()
        resultw.title("结果")
        resultw.geometry("800x600")
        # 创建主Canvas
        main_canvas = tk.Canvas(resultw)
        main_canvas.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(resultw, orient="horizontal", command=main_canvas.xview)
        scrollbar.pack(side="bottom", fill="x", padx=10, pady=5, ipadx=20)
        main_canvas.configure(xscrollcommand=scrollbar.set)

        frame = tk.Frame(main_canvas)
        main_canvas.create_window((0, 0), window=frame, anchor="nw")
        self.resultw = resultw
        # 创建批次选择下拉菜单并添加到主Canvas中
        batchFrame = tk.Frame(resultw)
        self.show_batch(batchFrame)
        batchFrame.pack(side="top", fill="x")

        # 获取默认值
        self.batch.current(0)
        batch = self.batch.get()

        # 创建标签显示区域
        self.labelframe = tk.Frame(resultw)
        self.update_label(batch)



        # 创建内部Canvas，用于包含singleFrame
        inner_canvas = tk.Canvas(frame)
        inner_canvas.grid(row=1, column=0)
        self.inner_canvas = inner_canvas
        self.update_images(batch)

        # 更新内部Canvas的滚动区域
        inner_canvas.update_idletasks()
        inner_canvas.configure(scrollregion=inner_canvas.bbox("all"))

        # 将frame的大小调整为适应内容
        frame.update_idletasks()

        # 设置主Canvas的滚动区域
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))

    def show(self):
        # 显示数据集
        dataSetFrame = tk.Frame(self.root)
        dataSetFrame.grid(row=0, column=0)
        self.show_dataset(dataSetFrame)
        self.dataSet.current(0)
        # 显示攻击方法
        attackFrame = tk.Frame(self.root)
        attackFrame.grid(row=0, column=1)
        self.show_attack(attackFrame)
        self.attack.current(0)
        # 显示确认按钮
        confirmFrame = tk.Frame(self.root)
        confirmFrame.grid(row=0, column=2)
        tk.Button(confirmFrame, text='确认', command=self.confirm).pack()
        # 显示测试按钮
        confirmFrame = tk.Frame(self.root)
        confirmFrame.grid(row=1, column=2)
        tk.Button(confirmFrame, text='测试', command=self.test).pack()
        # 显示命令行
        commandFrame = tk.Frame(self.root)
        commandFrame.grid(row=1, column=0, columnspan=3)
        # self.ShowCommand(commandFrame)


root = tk.Tk()

# 主窗口标题
root.title('数据库&方法选择')

ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 获取屏幕的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 设置程序缩放
# 这里的root是你设定的窗口
root.tk.call('tk', 'scaling', ScaleFactor / 75)
# 主窗口大小
root.geometry('400x100')
# root.resizable(width=False, height=False)
gui = GUI(root, None, None)
gui.show()
sv_ttk.set_theme("light")
# 循环显示主窗口
root.mainloop()
