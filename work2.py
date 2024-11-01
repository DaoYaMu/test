import sys
import json
import os
from datetime import datetime
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QLineEdit, QPushButton, \
    QLabel, QCheckBox, QTextEdit, QMessageBox
from PySide2.QtCore import Qt, QTimer


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI Components
        self.setWindowTitle("每日待办事项工具")
        self.resize(400, 600)

        # Main layout and container widget
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Date display
        self.date_label = QLabel(f"日期：{datetime.now().strftime('%Y-%m-%d')}")
        self.date_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.date_label)

        # Todo list widget
        self.todo_list = QListWidget()
        main_layout.addWidget(self.todo_list)

        # Input for new todo
        self.new_todo_input = QLineEdit()
        self.new_todo_input.setPlaceholderText("输入新的待办事项...")
        main_layout.addWidget(self.new_todo_input)

        # Buttons
        add_button = QPushButton("添加")
        delete_button = QPushButton("删除选中项")
        main_layout.addWidget(add_button)
        main_layout.addWidget(delete_button)

        # Checkbox for marking status
        self.status_checkbox = QCheckBox("标记为已完成")
        main_layout.addWidget(self.status_checkbox)

        # Notes area
        self.notes_area = QTextEdit()
        self.notes_area.setPlaceholderText("输入备注...")
        main_layout.addWidget(self.notes_area)

        # Bind events
        add_button.clicked.connect(self.add_todo)
        delete_button.clicked.connect(self.delete_selected_todo)
        self.todo_list.itemClicked.connect(self.load_selected_todo)
        self.status_checkbox.stateChanged.connect(self.update_status)
        self.new_todo_input.returnPressed.connect(self.add_todo)
        self.notes_area.textChanged.connect(self.save_to_json)

        # Load existing todos
        self.todos = {}
        self.json_file_path = os.path.join(os.path.dirname(__file__), 'todos.json')
        self.load_from_json()

    def add_todo(self):
        text = self.new_todo_input.text().strip()
        if text:
            # Create new todo entry
            todo_id = str(datetime.now().timestamp())
            self.todos[todo_id] = {
                "text": text,
                "completed": False,
                "notes": ""
            }
            self.update_todo_list()
            self.save_to_json()
            self.new_todo_input.clear()

    def delete_selected_todo(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            todo_id = current_item.data(Qt.UserRole)
            if todo_id in self.todos:
                del self.todos[todo_id]
                self.update_todo_list()
                self.save_to_json()
                self.notes_area.clear()
                self.status_checkbox.setChecked(False)

    def load_selected_todo(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            todo_id = current_item.data(Qt.UserRole)
            todo = self.todos.get(todo_id, {})
            self.new_todo_input.setText(todo.get("text", ""))
            self.status_checkbox.setChecked(todo.get("completed", False))
            self.notes_area.setPlainText(todo.get("notes", ""))

    def update_status(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            todo_id = current_item.data(Qt.UserRole)
            if todo_id in self.todos:
                self.todos[todo_id]["completed"] = self.status_checkbox.isChecked()
                self.update_todo_list()
                self.save_to_json()

    def update_todo_list(self):
        self.todo_list.clear()
        for todo_id, todo in self.todos.items():
            text = todo["text"]
            if todo["completed"]:
                text += " [已完成]"
            item = self.todo_list.addItem(text)
            item.setData(Qt.UserRole, todo_id)

    def save_to_json(self):
        # Save all todos to JSON file
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, indent=4, ensure_ascii=False)
        except IOError as e:
            QMessageBox.critical(self, "保存错误", f"无法保存文件: {e}")

    def load_from_json(self):
        # Load todos from JSON file if exists
        if os.path.exists(self.json_file_path):
            try:
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
                self.update_todo_list()
            except IOError as e:
                QMessageBox.critical(self, "加载错误", f"无法加载文件: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())
