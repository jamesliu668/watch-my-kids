#!/usr/bin/env python3
import json
import os
import tkinter as tk

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks_config.json")

class ChecklistDialog:
    def __init__(self, root):
        self.root = root
        self.root.title("👀 监控提醒")
        self.root.geometry("520x420")

        # 窗口置顶
        self.root.attributes("-topmost", True)

        # 去掉标题栏 → 无法拖动、无法最小化、无法关闭
        self.root.overrideredirect(True)

        # 窗口居中
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 520) // 2
        y = (self.root.winfo_screenheight() - 420) // 2
        self.root.geometry(f"+{x}+{y}")

        # 禁止通过关闭按钮（红 X）关闭窗口（由于标题栏已去掉，此防备用）
        self.root.protocol("WM_DELETE_WINDOW", self.prevent_close)

        # 读取配置文件
        self.tasks = self.load_config()

        # 主容器，加边框视觉效果
        main_frame = tk.Frame(root, bd=2, relief="raised")
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 标题
        tk.Label(main_frame, text="👀 请完成以下所有任务：", font=("Arial", 16, "bold")).pack(pady=(25, 5))

        # 提示
        hint_text = "📌 已完成 ✅   /   未完成 ⬜  (全部完成后按钮才可点击)"
        tk.Label(main_frame, text=hint_text, font=("Arial", 10), fg="#888", wraplength=480).pack(pady=(0, 10))

        # Checklist 项目
        self.vars = []

        frame = tk.Frame(main_frame)
        frame.pack(pady=5, padx=40, fill="both", expand=True)

        for i, task in enumerate(self.tasks):
            text = task["text"]
            completed = task["completed"]

            var = tk.BooleanVar(value=completed)
            cb = tk.Checkbutton(
                frame,
                text=f"{i+1}. {text}",
                variable=var,
                font=("Arial", 13),
                anchor="w",
                padx=10, pady=4,
                state="disabled"
            )
            if completed:
                cb.config(fg="#4CAF50")
            else:
                cb.config(fg="#999")
            cb.pack(fill="x", anchor="w")

            self.vars.append(var)

        # 提示文字
        self.hint_label = tk.Label(
            main_frame, text="⚠️ 请先完成所有任务，全部完成后按钮将自动解锁",
            font=("Arial", 11), fg="#888", wraplength=480
        )
        self.hint_label.pack(pady=(10, 5))

        # 底部容器，用于放置按钮（或空白占位）
        self.bottom_frame = tk.Frame(main_frame)
        self.bottom_frame.pack(pady=(0, 20))

        # "好的" 按钮（用 Label 实现，macOS 下 Button 的 fg 渲染有问题）
        self.btn = tk.Label(
            self.bottom_frame, text="好的",
            font=("Arial", 14, "bold"),
            width=10, height=1,
            bg="#4CAF50", fg="white",
            cursor="hand2", relief="raised"
        )
        self.btn.bind("<Button-1>", lambda e: self.ok())

        # 占位空白，保持布局高度不变
        self.placeholder = tk.Label(self.bottom_frame, text="", font=("Arial", 14), width=10, height=1)
        self.placeholder.pack()

        # 定时检查配置文件状态（每 2 秒刷新一次）
        self.refresh_status()

    def load_config(self):
        """读取配置文件，返回任务列表"""
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return [
                {"text": "完成今天的作业", "completed": False},
                {"text": "整理书桌", "completed": False},
                {"text": "复习今天的课程", "completed": False},
                {"text": "预习明天的内容", "completed": False},
                {"text": "合理安排时间，保护视力", "completed": False},
            ]

    def refresh_status(self):
        """定时重新读取配置文件，刷新界面状态"""
        self.tasks = self.load_config()

        # 更新每个 checkbox 的状态
        all_checked = True
        for i, task in enumerate(self.tasks):
            self.vars[i].set(task["completed"])
            if not task["completed"]:
                all_checked = False

        # 更新按钮：全部完成 → 显示按钮；否则隐藏
        if all_checked:
            self.placeholder.pack_forget()
            self.btn.pack()
            self.hint_label.config(text="✅ 任务全部完成！可以点击关闭了", fg="#4CAF50")
        else:
            self.btn.pack_forget()
            self.placeholder.pack()
            self.hint_label.config(text="⚠️ 请先完成所有任务，全部完成后按钮将自动解锁", fg="#888")

        # 每 2 秒检查一次
        self.root.after(2000, self.refresh_status)

    def prevent_close(self):
        """拦截关闭按钮：禁止点击红 X 关闭窗口"""
        self.hint_label.config(
            text="❌ 任务未全部完成，不能关闭！请先完成任务 ✅",
            fg="red"
        )
        self.root.attributes("-alpha", 0.7)
        self.root.after(200, lambda: self.root.attributes("-alpha", 1.0))

    def ok(self):
        """关闭窗口"""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklistDialog(root)
    root.mainloop()