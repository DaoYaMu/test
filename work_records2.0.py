import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any


class WorkRecordApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("每日工作记录v2.0 by Roy")
        self.root.geometry("800x600")

        # 设置主题样式
        self.style = ttk.Style()
        self.style.configure("Task.TButton", padding=5)
        self.style.configure("Delete.TButton", padding=5)

        # 初始化数据
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.data = self.load_data()
        self.init_current_date_data()

        # 创建主框架
        self.create_main_layout()
        self.refresh_tasks()

    def get_application_path(self) -> str:
        """获取应用程序路径，兼容打包后的exe"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    @property
    def file_path(self) -> str:
        """获取数据文件路径"""
        return os.path.join(self.get_application_path(), 'work_records.json')

    def ensure_file_directory(self) -> None:
        """确保文件目录存在"""
        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建数据目录: {e}")

    def load_data(self) -> Dict[str, Any]:
        """加载历史记录"""
        self.ensure_file_directory()
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return {}
        except Exception as e:
            messagebox.showerror("加载错误", f"无法加载数据文件: {e}")
            return {}

    def save_data(self) -> None:
        """保存数据"""
        self.ensure_file_directory()
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("保存错误", f"无法保存数据: {e}")

    def init_current_date_data(self) -> None:
        """Initialize data for the current date and carry over incomplete tasks from previous days."""
        if self.current_date not in self.data:
            self.data[self.current_date] = {'tasks': [], 'notes': ''}

            # Traverse backward to find and carry over incomplete tasks from previous dates
            date = datetime.now() - timedelta(days=1)
            seen_tasks = set(task['text'] for task in self.data[self.current_date]['tasks'])

            # Gather incomplete tasks until we run out of recorded days
            while date.strftime('%Y-%m-%d') in self.data:
                date_str = date.strftime('%Y-%m-%d')
                previous_tasks = self.data[date_str]['tasks']

                for task in previous_tasks:
                    if not task['status'] and task['text'] not in seen_tasks:
                        # Add incomplete task only if it's unique for the day
                        self.data[self.current_date]['tasks'].append(task.copy())
                        seen_tasks.add(task['text'])

                # Move one day further back
                date -= timedelta(days=1)

    def create_main_layout(self) -> None:
        """创建主要布局"""
        # 创建顶部框架
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill='x', padx=10, pady=5)

        # 日期显示
        date_label = ttk.Label(
            top_frame,
            text=f"日期: {self.current_date}",
            font=("Arial", 12, "bold")
        )
        date_label.pack(side='left')

        # 查看历史按钮
        history_btn = ttk.Button(
            top_frame,
            text="查看历史记录",
            command=self.view_history,
            style="Task.TButton"
        )
        history_btn.pack(side='right')

        # 创建主容器
        main_container = ttk.PanedWindow(self.root, orient='horizontal')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)

        # 左侧待办事项区域
        tasks_container = ttk.Frame(main_container)
        main_container.add(tasks_container, weight=1)

        # 待办事项输入区域
        input_frame = ttk.Frame(tasks_container)
        input_frame.pack(fill='x', pady=5)

        self.task_entry = ttk.Entry(input_frame)
        self.task_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        add_btn = ttk.Button(
            input_frame,
            text="添加待办事项",
            command=self.add_task,
            style="Task.TButton"
        )
        add_btn.pack(side='right')

        # 待办事项列表区域
        tasks_frame = ttk.Frame(tasks_container)
        tasks_frame.pack(fill='both', expand=True)

        # 创建带滚动条的画布
        self.canvas = tk.Canvas(tasks_frame)
        scrollbar = ttk.Scrollbar(tasks_frame, orient="vertical", command=self.canvas.yview)
        self.tasks_frame = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # 布局滚动区域
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")

        # 绑定调整大小事件
        self.tasks_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # 右侧工作记录区域
        notes_container = ttk.Frame(main_container)
        main_container.add(notes_container, weight=1)

        notes_label = ttk.Label(notes_container, text="今日工作记录", font=("Arial", 10, "bold"))
        notes_label.pack(pady=5)

        self.notes_text = scrolledtext.ScrolledText(notes_container, wrap=tk.WORD, height=10)
        self.notes_text.pack(fill='both', expand=True)
        self.notes_text.insert("1.0", self.data[self.current_date].get('notes', ''))
        self.notes_text.bind("<KeyRelease>", self.on_notes_change)

    def on_frame_configure(self, event=None):
        """更新画布的滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """当画布大小改变时，调整内部框架的宽度"""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def add_task(self) -> None:
        """添加新任务"""
        task_text = self.task_entry.get().strip()
        if task_text:
            self.data[self.current_date]['tasks'].append({
                'text': task_text,
                'status': False,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            self.save_data()
            self.task_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("输入错误", "请先输入待办事项内容")

    def update_task_status(self, index: int) -> None:
        """更新任务状态"""
        try:
            self.data[self.current_date]['tasks'][index]['status'] = \
                not self.data[self.current_date]['tasks'][index]['status']
            self.save_data()
            self.refresh_tasks()
        except Exception as e:
            messagebox.showerror("错误", f"更新任务状态失败: {e}")

    def delete_task(self, index: int) -> None:
        """删除任务"""
        if messagebox.askyesno("确认", "确定要删除这个任务吗？"):
            try:
                del self.data[self.current_date]['tasks'][index]
                self.save_data()
                self.refresh_tasks()
            except Exception as e:
                messagebox.showerror("错误", f"删除任务失败: {e}")

    def refresh_tasks(self) -> None:
        """刷新任务列表"""
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for idx, task in enumerate(self.data[self.current_date]['tasks']):
            task_frame = ttk.Frame(self.tasks_frame)
            task_frame.pack(fill='x', pady=2)

            # 状态图标
            status_text = "✔" if task['status'] else "□"
            status_btn = ttk.Button(
                task_frame,
                text=status_text,
                width=3,
                command=lambda i=idx: self.update_task_status(i)
            )
            status_btn.pack(side='left', padx=(0, 5))

            # 任务内容
            task_text = task['text']
            if task['status']:
                task_label = ttk.Label(
                    task_frame,
                    text=task_text,
                    font=("Arial", 9, "overstrike")
                )
            else:
                task_label = ttk.Label(
                    task_frame,
                    text=task_text,
                    font=("Arial", 9)
                )
            task_label.pack(side='left', fill='x', expand=True)

            # 删除按钮
            delete_btn = ttk.Button(
                task_frame,
                text="X",
                width=2,
                command=lambda i=idx: self.delete_task(i),
                style="Delete.TButton"
            )
            delete_btn.pack(side='right')

    def on_notes_change(self, event=None) -> None:
        """处理备注内容变更"""
        self.data[self.current_date]['notes'] = self.notes_text.get("1.0", tk.END).strip()
        self.save_data()

    def view_history(self) -> None:
        """查看历史记录"""
        history_window = tk.Toplevel(self.root)
        history_window.title("历史记录")
        history_window.geometry("600x400")

        # 创建日期选择器
        date_frame = ttk.Frame(history_window, padding="5")
        date_frame.pack(fill='x')

        dates = sorted(self.data.keys(), reverse=True)
        date_var = tk.StringVar(value=dates[0] if dates else self.current_date)

        date_combo = ttk.Combobox(
            date_frame,
            textvariable=date_var,
            values=dates,
            state="readonly"
        )
        date_combo.pack(side='left', padx=5)

        # 创建内容显示区域
        content_frame = ttk.Frame(history_window, padding="5")
        content_frame.pack(fill='both', expand=True)

        history_text = scrolledtext.ScrolledText(
            content_frame,
            wrap='word',
            font=("Arial", 10)
        )
        history_text.pack(fill='both', expand=True)

        def update_history_view(*args):
            selected_date = date_var.get()
            if selected_date in self.data:
                history_text.delete("1.0", tk.END)
                record = self.data[selected_date]

                # 添加任务列表
                history_text.insert(tk.END, "待办事项:\n", "header")
                for task in record['tasks']:
                    status = '✔' if task['status'] else '❌'
                    history_text.insert(tk.END, f"{status} {task['text']}\n")

                # 添加备注
                history_text.insert(tk.END, "\n备注:\n", "header")
                history_text.insert(tk.END, record['notes'])

                # 设置标题样式
                history_text.tag_configure("header", font=("Arial", 10, "bold"))

        date_combo.bind('<<ComboboxSelected>>', update_history_view)
        update_history_view()


def main():
    root = tk.Tk()
    app = WorkRecordApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()