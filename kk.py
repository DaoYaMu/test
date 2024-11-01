import os
import tkinter as tk
from tkinter import filedialog, messagebox
import warnings

# 忽略 libpng 相关的警告
warnings.filterwarnings("ignore", category=UserWarning, message=".*iCCP.*")


def rename_files():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    old_text = old_text_entry.get()
    new_text = new_text_entry.get()

    if not old_text:
        messagebox.showerror("错误", "请输入要替换的字符")
        return

    files_renamed = 0
    for filename in os.listdir(folder_path):
        if old_text in filename:
            new_filename = filename.replace(old_text, new_text)
            old_file = os.path.join(folder_path, filename)
            new_file = os.path.join(folder_path, new_filename)
            os.rename(old_file, new_file)
            files_renamed += 1

    messagebox.showinfo("完成", f"重命名完成，共修改了 {files_renamed} 个文件")


# 创建主窗口
root = tk.Tk()
root.title("文件名重命名工具")

# 创建输入框和标签
tk.Label(root, text="替换字符").grid(row=0, column=0, padx=10, pady=10)
old_text_entry = tk.Entry(root)
old_text_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="新字符").grid(row=1, column=0, padx=10, pady=10)
new_text_entry = tk.Entry(root)
new_text_entry.grid(row=1, column=1, padx=10, pady=10)

# 创建重命名按钮
rename_button = tk.Button(root, text="选择文件夹并重命名", command=rename_files)
rename_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# 启动主循环
root.mainloop()
