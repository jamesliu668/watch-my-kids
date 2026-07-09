#!/usr/bin/env python3
import json
import os
import tkinter as tk

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks_config.json")

class ChecklistDialog:
    def __init__(self, root):
        self.root = root
        self.root.title("👀 监控提醒")

        # 全屏覆盖整个屏幕（macOS 原生全屏模式）
        self.root.attributes("-fullscreen", True)

        # 置顶
        self.root.attributes("-topmost", True)

        # 去掉标题栏 → 无法拖动、无法最小化、无法关闭
        self.root.overrideredirect(True)

        # 模态锁定
        self.root.grab_set()
        self.root.focus_force()

        # 是否可以关闭（完成全部任务后设为 True）
        self.can_close = False

        # 禁止通过关闭按钮关闭
        self.root.protocol("WM_DELETE_WINDOW", self.prevent_close)

        # 读取配置文件
        self.tasks = self.load_config()

        # 主容器 - 居中放置内容
        main_frame = tk.Frame(root, bd=2, relief="raised")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=560, height=500)

        # 标题
        tk.Label(main_frame, text="👀 请完成以下所有任务：", font=("Arial", 18, "bold")).pack(pady=(35, 10))

        # 提示
        hint_text = "📌 已完成 ✅   /   未完成 ⬜  (全部完成后按钮才可点击)"
        tk.Label(main_frame, text=hint_text, font=("Arial", 11), fg="#888", wraplength=520).pack(pady=(0, 15))

        # Checklist 项目
        self.vars = []

        frame = tk.Frame(main_frame)
        frame.pack(pady=5, padx=50, fill="both", expand=True)

        for i, task in enumerate(self.tasks):
            text = task["text"]
            completed = task["completed"]

            var = tk.BooleanVar(value=completed)
            cb = tk.Checkbutton(
                frame,
                text=f"{i+1}. {text}",
                variable=var,
                font=("Arial", 14),
                anchor="w",
                padx=10, pady=6,
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
            main_frame, text="⚠️ 请先完成所有任务，全部完成后按钮将自动出现",
            font=("Arial", 12), fg="#888", wraplength=520
        )
        self.hint_label.pack(pady=(15, 10))

        # 底部容器
        self.bottom_frame = tk.Frame(main_frame)
        self.bottom_frame.pack(pady=(0, 25))

        # "好的" 按钮（用 Label 实现）
        self.btn = tk.Label(
            self.bottom_frame, text="好的",
            font=("Arial", 15, "bold"),
            width=12, height=1,
            bg="#4CAF50", fg="white",
            cursor="hand2", relief="raised"
        )
        self.btn.bind("<Button-1>", lambda e: self.ok())

        # 占位空白
        self.placeholder = tk.Label(self.bottom_frame, text="", font=("Arial", 14), width=12, height=1)
        self.placeholder.pack()

        # 定时检查配置文件状态
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

        all_checked = True
        for i, task in enumerate(self.tasks):
            self.vars[i].set(task["completed"])
            if not task["completed"]:
                all_checked = False

        if all_checked:
            self.can_close = True
            self.placeholder.pack_forget()
            self.btn.pack()
            self.hint_label.config(text="✅ 任务全部完成！可以点击关闭了", fg="#4CAF50")
        else:
            self.btn.pack_forget()
            self.placeholder.pack()
            self.hint_label.config(text="⚠️ 请先完成所有任务，全部完成后按钮将自动出现", fg="#888")

        self.root.after(2000, self.refresh_status)

    def prevent_close(self):
        """拦截关闭按钮"""
        pass

    def ok(self):
        """关闭窗口"""
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklistDialog(root)
    root.mainloop()