from tkinter import *
from tkinter import TclError, filedialog, colorchooser, messagebox, ttk
import tkinter.font as tkFont
import os


class MYNotepad:
    def __init__(self, master):
        self.master = master
        master.title("My Notepad")
        try:
            master.wm_iconbitmap("notepad.ico")
        except TclError:
            print("Icon file not found or invalid. Using default icon.")

        # Initialize current file and font
        self.current_file = None
        self.font_style = tkFont.Font(family="Arial", size=12)  # Default font style

        # Creating the text widget
        self.txt = Text(
            master,
            padx=5,
            pady=5,
            wrap=WORD,
            selectbackground="blue",
            bd=2,
            insertwidth=3,
            undo=True,
            font=self.font_style,
        )
        self.txt.pack(fill=BOTH, expand=1)

        # Creating the main menu
        self.main_menu = Menu(master)
        master.config(menu=self.main_menu)

        # Creating the file menu
        self.file_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="FILE", menu=self.file_menu)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.saveas_file)
        self.file_menu.add_command(label="Print", accelerator="Ctrl+P", command=self.print_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        # Creating the edit menu
        self.edit_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="EDIT", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo_file)
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_file)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_file)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete", command=self.delete_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)

        # Creating the format menu
        self.format_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font Style and Size", command=self.font_dialog)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Bold", accelerator="Ctrl+B", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", accelerator="Ctrl+I", command=self.toggle_italic)
        self.format_menu.add_command(label="Underline", accelerator="Ctrl+U", command=self.toggle_underline)

        # Creating the color menu
        self.color_menu = Menu(self.main_menu, tearoff=0)
        self.main_menu.add_cascade(label="Color", menu=self.color_menu)
        self.color_menu.add_command(label="Background Color", command=self.change_back_color)
        self.color_menu.add_command(label="Foreground Color", command=self.change_fore_color)

        # Keyboard shortcuts
        self.master.bind("<Control-n>", lambda event: self.new_file())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-s>", lambda event: self.save_file())
        self.master.bind("<Control-p>", lambda event: self.print_file())
        self.master.bind("<Control-z>", lambda event: self.undo_file())
        self.master.bind("<Control-y>", lambda event: self.redo_file())
        self.master.bind("<Control-x>", lambda event: self.cut_file())
        self.master.bind("<Control-c>", lambda event: self.copy_file())
        self.master.bind("<Control-v>", lambda event: self.paste_file())
        self.master.bind("<Control-b>", lambda event: self.toggle_bold())
        self.master.bind("<Control-i>", lambda event: self.toggle_italic())
        self.master.bind("<Control-u>", lambda event: self.toggle_underline())
        self.master.bind("<Control-a>", lambda event: self.select_all())

    def font_dialog(self):
        """Display a dialog for selecting font style and size."""
        dialog = Toplevel(self.master)
        dialog.title("Font Style and Size")
        dialog.geometry("300x200")
        dialog.transient(self.master)

        # Font styles
        font_styles = ["Regular", "Italic", "Bold", "Bold Italic"]
        style_label = Label(dialog, text="Font style:")
        style_label.pack(pady=5)
        style_combo = ttk.Combobox(dialog, values=font_styles, state="readonly")
        style_combo.pack(pady=5)
        style_combo.current(0)

        # Font sizes
        font_sizes = list(range(8, 72, 2))
        size_label = Label(dialog, text="Size:")
        size_label.pack(pady=5)
        size_combo = ttk.Combobox(dialog, values=font_sizes, state="readonly")
        size_combo.pack(pady=5)
        size_combo.current(2)  # Default size (12)

        # Apply button
        apply_button = Button(dialog, text="Apply", command=lambda: self.apply_font(style_combo.get(), size_combo.get()))
        apply_button.pack(pady=10)

    def apply_font(self, style, size):
        """Apply the selected font style and size."""
        weight = "normal"
        slant = "roman"

        if "Bold" in style:
            weight = "bold"
        if "Italic" in style:
            slant = "italic"

        self.font_style.config(size=int(size), weight=weight, slant=slant)

    def new_file(self):
        self.txt.delete(1.0, END)
        self.current_file = None

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.txt.delete(1.0, END)
            self.txt.insert(END, content)
            self.current_file = file_path

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.txt.get(1.0, END))
        else:
            self.saveas_file()

    def saveas_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.txt.get(1.0, END))
            self.current_file = file_path

    def print_file(self):
        if self.current_file:
            os.startfile(self.current_file, "print")

    def exit_app(self):
        self.master.quit()

    def undo_file(self):
        self.txt.edit_undo()

    def redo_file(self):
        self.txt.edit_redo()

    def cut_file(self):
        self.copy_file()
        self.txt.delete(SEL_FIRST, SEL_LAST)

    def copy_file(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.txt.get(SEL_FIRST, SEL_LAST))

    def paste_file(self):
        self.txt.insert(INSERT, self.master.clipboard_get())

    def delete_text(self):
        self.txt.delete(SEL_FIRST, SEL_LAST)

    def change_back_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.txt.config(bg=color)

    def change_fore_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.txt.config(fg=color)

    def toggle_bold(self):
        current_weight = self.font_style.cget("weight")
        new_weight = "bold" if current_weight != "bold" else "normal"
        self.font_style.config(weight=new_weight)

    def toggle_italic(self):
        current_slant = self.font_style.cget("slant")
        new_slant = "italic" if current_slant != "italic" else "roman"
        self.font_style.config(slant=new_slant)

    def toggle_underline(self):
        current_underline = self.font_style.cget("underline")
        new_underline = 1 if current_underline == 0 else 0
        self.font_style.config(underline=new_underline)

    def select_all(self):
        self.txt.tag_add("sel", "1.0", END)


root = Tk()
app = MYNotepad(root)
root.mainloop()
