from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageOps

MAX_WIDTH = 800
MAX_HEIGHT = 600

# Глобальные переменные для обработки
original_image = None
display_image = None
scale_x = 1.0
scale_y = 1.0
image_offset_x = 0
image_offset_y = 0


def open_file():
    global original_image
    image_files = r"*.jpg *.jpeg *.png"
    path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Photo files", image_files)])
    if path:
        original_image = Image.open(path)
    return original_image


def save_as():
    if original_image:
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            original_image.save(path)


def rotate():
    global original_image
    if original_image:
        push_to_history()
        original_image = original_image.transpose(Image.ROTATE_90)


def black_and_white():
    global original_image
    if original_image:
        push_to_history()
        original_image = original_image.convert("L")


def flip():
    global original_image
    if original_image:
        push_to_history()
        original_image = original_image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


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
        push_to_history()
        original_image = sepia_image


def invert():
    global original_image
    if original_image:
        if original_image.mode != "RGB":
            original_image = original_image.convert("RGB")
        push_to_history()
        original_image = ImageOps.invert(original_image)


def brightness_upscale(factor=1.2):
    global original_image
    if original_image:
        enhancer = ImageEnhance.Brightness(original_image)
        push_to_history()
        original_image = enhancer.enhance(factor)


def sharpness_upscale(factor=2):
    global original_image
    if original_image:
        enhancer = ImageEnhance.Sharpness(original_image)
        push_to_history()
        original_image = enhancer.enhance(factor)


def color_upscale(factor=1.5):
    global original_image
    if original_image:
        enhancer = ImageEnhance.Color(original_image)
        push_to_history()
        original_image = enhancer.enhance(factor)


def crop_image(crop_box):
    global original_image
    if original_image:
        push_to_history()
        original_image = original_image.crop(crop_box)


def get_original_image():
    return original_image


def get_display_image(canvas_w, canvas_h):
    global display_image, scale_x, scale_y, image_offset_x, image_offset_y
    if not original_image:
        return None, None, None, None

    display_image = original_image.copy()
    img_w, img_h = display_image.size

    scale = min(canvas_w / img_w, canvas_h / img_h, 1.0)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    scale_x = img_w / new_w
    scale_y = img_h / new_h

    if scale < 1.0:
        display_image = display_image.resize((new_w, new_h), Image.LANCZOS)

    image_offset_x = canvas_w // 2 - new_w // 2
    image_offset_y = canvas_h // 2 - new_h // 2

    return ImageTk.PhotoImage(display_image), scale_x, scale_y, (image_offset_x, image_offset_y)


history_stack = []


def push_to_history():
    global history_stack, original_image
    if original_image:
        history_stack.append(original_image.copy())
        if len(history_stack) > 30:
            history_stack.pop(0)


def undo():
    global original_image
    if history_stack:
        original_image = history_stack.pop()
