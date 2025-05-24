import tkinter
from tkinter import *
import editor_logic as edl

MAX_WIDTH = 800
MAX_HEIGHT = 600

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
    info_label.config(text="Выделите область мышью...")


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
    info_label.config(text="")

def undo_action():
    edl.undo()
    update_canvas()



# --- GUI ---
window = Tk()
window.title("Фоторедактор")
window.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}")
window.resizable(False, False)

menu_bar = tkinter.Menu(window)
file_menu = tkinter.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить как", command=save_as)
menu_bar.add_cascade(label="Файл", menu=file_menu)
window.config(menu=menu_bar)

side_panel = Frame(window, width=170, bg="#f0f0f0")
side_panel.pack(side=LEFT, fill=Y, padx=10, pady=10)

button_width = 25
Button(side_panel, text="Повернуть", command=rotate, width=button_width).pack(pady=5)
Button(side_panel, text="Ч/Б", command=black_and_white, width=button_width).pack(pady=5)
Button(side_panel, text="Отразить", command=flip, width=button_width).pack(pady=5)
Button(side_panel, text="Сепия", command=sepia, width=button_width).pack(pady=5)
Button(side_panel, text="Инверсия", command=invert, width=button_width).pack(pady=5)
Button(side_panel, text="Яркость", command=brightness, width=button_width).pack(pady=5)
Button(side_panel, text="Четкость", command=sharpness, width=button_width).pack(pady=5)
Button(side_panel, text="Насыщенность", command=color, width=button_width).pack(pady=5)
Button(side_panel, text="Обрезка", command=start_crop, width=button_width).pack(pady=5)
Button(side_panel, text="Отменить", command=undo_action, width=button_width).pack(pady=5)

info_label = Label(side_panel, text="", bg="#f0f0f0", wraplength=120)
info_label.pack()

image_frame = Frame(window, bg="gray")
image_frame.pack(side=LEFT, fill=BOTH, expand=True)

canvas = Canvas(image_frame, bg="gray", cursor="")
canvas.pack(fill=BOTH, expand=True)

canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)

window.mainloop()
