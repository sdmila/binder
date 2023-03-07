import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import webbrowser

class About(tk.Toplevel):
    is_open = False

    def __init__(self, parent):
        if About.is_open:
            return
        About.is_open = True
        super().__init__(parent)
        self.overrideredirect(True)
        self.resizable(False, False)
        self.transient(parent)
        self.geometry(
            "+{}+{}".format(
                parent.winfo_rootx() + parent.winfo_width() // 2 - 100,
                parent.winfo_rooty() + parent.winfo_height() // 2 - 150
            )
        )
        self.wait_visibility()
        self.grab_set()
        
        name_label = tk.Label(
            self,
            text="Binder"
        )
        name_label.pack(padx=10, pady=10)

        version_label = tk.Label(
            self,
            text="Version: 0.0.1",
            anchor="w"
        )
        version_label.pack(padx=10)

        license_label = tk.Label(
            self,
            text="License: GPLv3",
            anchor="w"
        )
        license_label.pack(padx=10)

        close_button = tk.Button(
            self,
            text="Close",
            command=self.close
        )
        close_button.pack(pady=10)
        
        self.wait_window()

    def close(self):
        About.is_open = False
        self.destroy()

class App:
    def __init__(self, main):
        self.main = main
        self.main.title("Binder")
        self.create_menu_bar()
        self.create_notebook()
        self.open_readme()
        self.current_file_path = None

    def open_readme(self):
        readme_file = "README.md"
        readme_path = os.path.join(os.getcwd(), readme_file)
        if os.path.exists(readme_path):
            self.open_file(readme_path)

    def create_menu_bar(self):
        self.menu_bar = tk.Menu(self.main)
        self.define_file_menu()
        self.define_edit_menu()
        self.define_help_menu()
        self.main.config(menu = self.menu_bar)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main)
        self.notebook.pack(
            expand = True,
            fill = 'both')
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def on_tab_changed(self, event):
        current_tab = self.notebook.select()
        file_name = self.notebook.tab(current_tab, "text")
        if file_name == "Untitled":
            self.main.title("Untitled - Binder")
        else:
            file_path = os.path.join(self.current_directory, file_name)
            self.main.title(file_path + " - Binder")

    def define_file_menu(self):
        file_menu = tk.Menu(
            self.menu_bar,
            tearoff=0
        )
        file_menu.add_command(
            label = "New",
            accelerator = "Ctrl+N",
            command = self.new_file
        )
        file_menu.add_command(
            label = "Open...",
            accelerator = "Ctrl+O",
            command = self.open_file
        )
        file_menu.add_command(
            label = "Save",
            accelerator = "Ctrl+S",
            command = self.save_file
        )
        file_menu.add_command(
            label = "Save As...",
            accelerator = "Ctrl+Shift+S",
            command = self.save_file_as
        )
        file_menu.add_separator()
        file_menu.add_command(
            label = "Close",
            accelerator = "Ctrl+W",
            command = self.close
        )
        file_menu.add_command(
            label = "Close All",
            accelerator = "Ctrl+Shift+W",
            command = self.close_all
        )
        file_menu.add_separator()
        file_menu.add_command(
            label = "Exit",
            accelerator = "Alt+F4",
            command = self.main.quit
        )
        self.menu_bar.add_cascade(
            label = "File",
            menu = file_menu
        )
        self.main.bind("<Control-n>", lambda event: self.new_file())
        self.main.bind("<Control-o>", lambda event: self.open_file())
        self.main.bind("<Control-s>", lambda event: self.save_file())
        self.main.bind("<Control-S>", lambda event: self.save_file_as())
        self.main.bind("<Control-w>", lambda event: self.close())
        self.main.bind("<Control-W>", lambda event: self.close_all())
        self.main.bind("<Alt-F4>", lambda event: self.main.quit())

    def new_file(self):
        new_tab = ttk.Frame(self.notebook)
        text_field = tk.Text(new_tab)
        text_field.pack(
            fill="both", 
            expand = True)
        self.notebook.add(new_tab, text = "Untitled")
        self.notebook.select(new_tab)

    def open_file(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename(
                filetypes = [
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                title = "Open"
            )
        if file_path:
            self.current_directory = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            with open(file_path, "r") as file:
                content = file.read()
            new_tab = ttk.Frame(self.notebook)
            text_field = tk.Text(new_tab)
            text_field.pack(
                fill="both",
                expand=True
            )
            text_field.insert("1.0", content)
            self.notebook.add(new_tab, text=file_name)
            self.notebook.select(new_tab)
            self.main.title(file_path + " - Binder")


    def save_file(self):
        current_tab = self.notebook.select()
        file_name = self.notebook.tab(current_tab, "text")
        if file_name == "Untitled":
            self.save_file_as()
        else:
            file_path = os.path.join(self.current_directory, file_name)
            with open(file_path, "w") as file:
                text_field = self.notebook.nametowidget(current_tab).winfo_children()[0]
                file.write(text_field.get("1.0", "end-1c"))
                self.main.title(file_path + " - Binder")

    def save_file_as(self):
        file_path = tk.filedialog.asksaveasfilename(
            filetypes = [
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title = "Save As"
        )
        if file_path:
            self.current_directory = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            with open(file_path, "w") as file:
                current_tab = self.notebook.select()
                text_field = self.notebook.nametowidget(current_tab).winfo_children()[0]
                file.write(text_field.get("1.0", "end-1c"))
            self.notebook.tab(
                self.notebook.select(),
                text = file_name
            )
            self.main.title(file_path + " - Binder")

    def close(self):
        current_tab = self.notebook.select()
        if current_tab:
            if self.notebook.index('end') == 1:
                self.new_file()
            self.notebook.forget(current_tab)

    def close_all(self):
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.new_file()

    def define_edit_menu(self):
        edit_menu = tk.Menu(
            self.menu_bar,
            tearoff=0
        )
        edit_menu.add_command(
            label = "Cut",
            accelerator = "Ctrl+X",
            command = self.cut
        )
        edit_menu.add_command(
            label = "Copy",
            accelerator = "Ctrl+C",
            command = self.copy
        )
        edit_menu.add_command(
            label = "Paste",
            accelerator = "Ctrl+V",
            command = self.paste
        )
        self.menu_bar.add_cascade(
            label = "Edit",
            menu = edit_menu
        )  
        self.main.bind("<Control-x>", lambda event: self.cut())
        self.main.bind("<Control-c>", lambda event: self.copy())
        self.main.bind("<Control-v>", lambda event: self.paste())

    def cut(self):
        current_tab = self.notebook.select()
        text_field = self.notebook.nametowidget(current_tab).winfo_children()[0]
        text = text_field.get("sel.first", "sel.last")
        self.main.clipboard_clear()
        self.main.clipboard_append(text)
        text_field.delete("sel.first", "sel.last")

    def copy(self):
        current_tab = self.notebook.select()
        text_field = self.notebook.nametowidget(current_tab).winfo_children()[0]
        text = text_field.get("sel.first", "sel.last")
        self.main.clipboard_clear()
        self.main.clipboard_append(text)

    def paste(self):
        current_tab = self.notebook.select()
        text_field = self.notebook.nametowidget(current_tab).winfo_children()[0]
        if text_field.tag_ranges("sel"):
            text_field.delete("sel.first", "sel.last")
        text_field.insert("insert", self.main.clipboard_get())

    def define_help_menu(self):
        help_menu = tk.Menu(
            self.menu_bar,
            tearoff=0
        )
        help_menu.add_command(
            label = "GitHub Repository",
            command = self.open_github_repository
        )
        help_menu.add_separator()
        help_menu.add_command(
            label = "About",
            accelerator = "F1",
            command = self.show_about_dialog
        )
        self.menu_bar.add_cascade(
            label = "Help",
            menu = help_menu
        )
        self.main.bind("<F1>", lambda event: self.show_about_dialog())

    def open_github_repository(self):
        webbrowser.open('https://www.github.com/sdmila/binder/')

    def show_about_dialog(self):
        About(self.main)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()