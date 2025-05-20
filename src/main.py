from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

original_image = None
display_image = None
current_tk_image = None

MAX_WIDTH = 800
MAX_HEIGHT = 600


def update_display():
    global display_image, current_tk_image

    if not original_image:
        return

    display_image = original_image.copy()
    img_width, img_height = display_image.size
    scale = min((MAX_WIDTH - 100) / img_width, (MAX_HEIGHT - 100) / img_height, 1.0)

    if scale < 1.0:
        display_image = display_image.resize((int(img_width * scale), int(img_height * scale)), Image.LANCZOS)

    current_tk_image = ImageTk.PhotoImage(display_image)
    place_for_image.configure(image=current_tk_image)
    place_for_image.image = current_tk_image


def open_file():
    global original_image
    path = filedialog.askopenfilename()
    if not path:
        return
    original_image = Image.open(path)
    update_display()


def rotate():
    global original_image
    if original_image:
        original_image = original_image.transpose(Image.ROTATE_90)
        update_display()


def black_and_white():
    global original_image
    if original_image:
        original_image = original_image.convert("L")
        update_display()


def flip():
    global original_image
    if original_image:
        original_image = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        update_display()


def save_as():
    if original_image:
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            original_image.save(path)


def sepia():
    global original_image
    if original_image:
        if original_image.mode != "RGB":
            original_image = original_image.convert("RGB")
        sepia_image = original_image.copy()
        pixels = sepia_image.load()

        for y in range(sepia_image.height):
            for x in range(sepia_image.width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))

        original_image = sepia_image
        update_display()


# --- GUI setup ---
window = Tk()
window.title("Фоторедактор")
window.geometry(f"{MAX_WIDTH}x{MAX_HEIGHT}")
window.resizable(False, False)

# Левая панель с кнопками
side_panel = Frame(window, width=150, bg="#f0f0f0")
side_panel.pack(side=LEFT, fill=Y, padx=10, pady=10)

Button(side_panel, text="Открыть", command=open_file, width=15).pack(pady=5)
Button(side_panel, text="Повернуть", command=rotate, width=15).pack(pady=5)
Button(side_panel, text="Ч/Б", command=black_and_white, width=15).pack(pady=5)
Button(side_panel, text="Отразить", command=flip, width=15).pack(pady=5)
Button(side_panel, text="Сепия", command=sepia, width=15).pack(pady=5)
Button(side_panel, text="Сохранить как", command=save_as, width=15).pack(pady=5)

# Область для изображения
image_frame = Frame(window, bg="gray")
image_frame.pack(side=LEFT, fill=BOTH, expand=True)

place_for_image = Label(image_frame, bg="gray")
place_for_image.pack(expand=True)

mainloop()
