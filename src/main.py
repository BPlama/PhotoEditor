import os
import sys
import tkinter as tk
from tkinter import PhotoImage
import customtkinter
import editor_logic as edl
from idlelib.tooltip import Hovertip


MAX_WIDTH = 1000
MAX_HEIGHT = 700

start_x = start_y = 0
rect_id = None
cropping_mode = False
offset_x = offset_y = 0


def update_canvas():
    global current_tk_image, offset_x, offset_y
    canvas_w = canvas.winfo_width()
    canvas_h = canvas.winfo_height()

    img, sx, sy, offsets = edl.get_display_image(canvas_w, canvas_h)
    if img:
        current_tk_image = img
        offset_x, offset_y = offsets
        canvas.delete("all")
        canvas.create_image(canvas_w // 2, canvas_h // 2, anchor="center", image=current_tk_image)


def open_file():
    edl.open_file()
    update_canvas()


def save_as():
    edl.save_as()


def rotate():
    edl.rotate()
    update_canvas()


def black_and_white():
    edl.black_and_white()
    update_canvas()


def flip():
    edl.flip()
    update_canvas()


def sepia():
    edl.sepia()
    update_canvas()


def invert():
    edl.invert()
    update_canvas()


def brightness():
    edl.brightness_upscale()
    update_canvas()


def sharpness():
    edl.sharpness_upscale()
    update_canvas()


def color():
    edl.color_upscale()
    update_canvas()


def start_crop():
    global cropping_mode
    cropping_mode = True
    canvas.config(cursor="cross")
    info_label.configure(text="Выделите область мышью...", font=my_font)


def on_press(event):
    global start_x, start_y, rect_id
    if not cropping_mode:
        return
    start_x, start_y = event.x, event.y
    rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')


def on_drag(event):
    if cropping_mode and rect_id:
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)


def on_release(event):
    global cropping_mode, rect_id
    if not cropping_mode or not rect_id:
        return

    x1 = min(start_x, event.x) - offset_x
    y1 = min(start_y, event.y) - offset_y
    x2 = max(start_x, event.x) - offset_x
    y2 = max(start_y, event.y) - offset_y

    if x2 - x1 > 5 and y2 - y1 > 5:
        crop_box = (
            int(x1 * edl.scale_x),
            int(y1 * edl.scale_y),
            int(x2 * edl.scale_x),
            int(y2 * edl.scale_y)
        )
        edl.crop_image(crop_box)
        update_canvas()

    cropping_mode = False
    canvas.config(cursor="")
    info_label.configure(text="")


def undo_action():
    edl.undo()
    update_canvas()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

icon_path = resource_path('assets/Icon/editor_logo_white.ico')

# --- GUI INIT ---
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.title("Фоторедактор")
window.iconbitmap(resource_path('assets/Icon/editor_logo_white.ico'))
window.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}")
window.resizable(False, False)

my_font = customtkinter.CTkFont(family="Verdana", size=12, weight="bold")

# Меню

menu_style = {
    "background": "#242632",
    "activebackground": "#3A3B45"
}

menu_frame = tk.Frame(window, bg="#242632", height=30)
menu_frame.pack(side="top", fill="x")

# Кнопка "Файл"
file_btn = tk.Menubutton(
    menu_frame,
    text="Файл",
    **menu_style,
    fg="white",
    relief="flat",
    bd=0,
    font=my_font
)
file_btn.pack(side="left", padx=10)

# Выпадающее меню для "Файл"
file_dropdown = tk.Menu(
    file_btn,
    **menu_style,
    fg="white",
    tearoff=0,
    font=my_font
)

file_dropdown.add_command(label="Открыть", command=open_file, **menu_style)
file_dropdown.add_command(label="Сохранить как", command=save_as, **menu_style)

file_btn.configure(menu=file_dropdown)

# Боковая панель
side_panel = customtkinter.CTkFrame(window, width=200, fg_color="#1a1a1a")
side_panel.pack(side="left", fill="y", padx=10, pady=10)

# Стиль кнопок
btn_style = {
    "width": 60,
    "text_color": "white",
    "fg_color": "#2E2F3A",
    "hover_color": "#3D3E4A",
    "border_width": 1,
    "border_color": "#3D3E4A",
    "font": my_font
}

# Загрузка иконок
rotate_icon = PhotoImage(file="assets/ButtonIcons/rotate.png")
bw_icon = PhotoImage(file="assets/ButtonIcons/black_and_white.png")
flip_icon = PhotoImage(file="assets/ButtonIcons/flip.png")
sepia_icon = PhotoImage(file="assets/ButtonIcons/sepia.png")
inversion_icon = PhotoImage(file="assets/ButtonIcons/inversion.png")
brightness_icon = PhotoImage(file="assets/ButtonIcons/brightness.png")
sharpness_icon = PhotoImage(file="assets/ButtonIcons/sharpness.png")
color_icon = PhotoImage(file="assets/ButtonIcons/color.png")
crop_icon = PhotoImage(file="assets/ButtonIcons/crop.png")
undo_icon = PhotoImage(file="assets/ButtonIcons/undo.png")

# Кнопки с описаниями
buttons = [
    {
        "name": "Повернуть",
        "command": rotate,
        "icon": rotate_icon,
        "description": "Поворот изображения на 90° по часовой стрелке"
    },
    {
        "name": "Ч/Б",
        "command": black_and_white,
        "icon": bw_icon,
        "description": "Преобразование цветного изображения в черно-белое"
    },
    {
        "name": "Отразить",
        "command": flip,
        "icon": flip_icon,
        "description": "Зеркальное отражение изображения по горизонтали"
    },
    {
        "name": "Сепия",
        "command": sepia,
        "icon": sepia_icon,
        "description": "Наложение сепийного фильтра (ретро эффект)"
    },
    {
        "name": "Инверсия",
        "command": invert,
        "icon": inversion_icon,
        "description": "Инверсия цветов изображения (негатив)"
    },
    {
        "name": "Яркость",
        "command": brightness,
        "icon": brightness_icon,
        "description": "Регулировка яркости изображения (+20%)"
    },
    {
        "name": "Четкость",
        "command": sharpness,
        "icon": sharpness_icon,
        "description": "Увеличение резкости изображения"
    },
    {
        "name": "Насыщенность",
        "command": color,
        "icon": color_icon,
        "description": "Увелечения насыщенности цветов"
    },
    {
        "name": "Обрезка",
        "command": start_crop,
        "icon": crop_icon,
        "description": "Обрезка изображения (выделите область)"
    },
    {
        "name": "Отменить",
        "command": undo_action,
        "icon": undo_icon,
        "description": "Отмена последнего действия"
    }
]


# Класс для красивого тултипа
class ToolTip(customtkinter.CTkToplevel):
    def __init__(self, widget, text):
        super().__init__()
        self.widget = widget
        self.text = text
        self.withdraw()
        self.overrideredirect(True)

        self.label = customtkinter.CTkLabel(
            self,
            text=self.text,
            corner_radius=6,
            fg_color="#2E2F3A",
            text_color="white",
            padx=10,
            pady=5,
            wraplength=200
        )
        self.label.pack()

        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty()
        self.geometry(f"+{x}+{y}")
        self.deiconify()

    def hide(self, event):
        self.withdraw()


# Создаем кнопки с подсказками
for btn_info in buttons:
    btn = customtkinter.CTkButton(
        side_panel,
        text="",
        command=btn_info["command"],
        **btn_style,
        image=btn_info["icon"]
    )
    btn.pack(pady=5)

    # Создаем подсказку с описанием
    ToolTip(btn, f"{btn_info['name']}\n\n{btn_info['description']}")

info_label = customtkinter.CTkLabel(side_panel, text="", text_color="white", wraplength=120)
info_label.pack(pady=5)

# Canvas + контейнер для него
image_frame = tk.Frame(window, bg="#1d1d27", highlightthickness=1, highlightbackground="#444")
image_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

canvas = tk.Canvas(image_frame, bg="#1d1d27", bd=0, highlightthickness=0, relief="flat", cursor="")
canvas.pack(fill="both", expand=True)

canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)

window.mainloop()
