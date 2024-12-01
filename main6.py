""" 
Zmiana HSV po stronier uzytkownika

NIE DZIALA (a powinien na czarnych i bialych)
"""

import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def load_image():
    global original_image, processed_image, mask, mask_bright, mask_dark
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        processed_image = original_image.copy()
        create_masks()
        apply_changes()
        update_image()
        update_mask_display()
        update_bright_dark_display()

def create_masks():
    global mask, mask_bright, mask_dark
    hsv = cv2.cvtColor(original_image, cv2.COLOR_RGB2HSV)
    # Maska główna
    lower_color = np.array([h_min_mask.get(), s_min_mask.get(), v_min_mask.get()])
    upper_color = np.array([h_max_mask.get(), s_max_mask.get(), v_max_mask.get()])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Operacje morfologiczne
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Maska jasnych obszarów (V > threshold)
    bright_threshold = bright_threshold_slider.get()
    mask_bright = cv2.inRange(hsv[:, :, 2], bright_threshold, 255)
    mask_bright = cv2.bitwise_and(mask_bright, mask)  # Tylko w obszarze lakieru
    
    # Maska ciemnych obszarów (V < threshold)
    dark_threshold = dark_threshold_slider.get()
    mask_dark = cv2.inRange(hsv[:, :, 2], 0, dark_threshold)
    mask_dark = cv2.bitwise_and(mask_dark, mask)  # Tylko w obszarze lakieru

def apply_changes():
    global processed_image
    if original_image is None:
        return
    # Kopia oryginalnego obrazu
    processed_image = original_image.copy()
    # Pobranie wartości z suwaków HSV
    h_value = h_slider.get()
    s_value = s_slider.get()
    v_value = v_slider.get()
    # Konwersja wybranego koloru do HSV
    selected_hsv = np.array([h_value, s_value, v_value], dtype=np.uint8)
    # Przekształcenie oryginalnego obrazu do HSV
    hsv = cv2.cvtColor(processed_image, cv2.COLOR_RGB2HSV)
    # Zastosowanie maski głównej
    # Zmiana kanałów zgodnie z wyborem użytkownika
    if change_hue_var.get():
        hsv[..., 0][mask > 0] = selected_hsv[0]
    if change_saturation_var.get():
        hsv[..., 1][mask > 0] = selected_hsv[1]
    if change_brightness_var.get():
        hsv[..., 2][mask > 0] = selected_hsv[2]
    # Zwiększenie jasności na jasnych obszarach
    adjust_brightness(hsv, mask_bright, gloss_bright.get(), brighten=True)
    # Zmniejszenie jasności na ciemnych obszarach
    adjust_brightness(hsv, mask_dark, gloss_dark.get(), brighten=False)
    # Konwersja z powrotem do RGB
    processed_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    update_image()

def adjust_brightness(hsv, mask_area, intensity, brighten=True):
    # intensity: 0-100, gdzie 100 to maksymalna zmiana
    factor = intensity / 100.0
    # Pobranie kanału V
    v = hsv[:, :, 2].astype(np.float32)
    # Normalizacja maski
    mask_normalized = mask_area / 255.0
    if brighten:
        # Zwiększenie jasności
        v = v + (255 - v) * factor * mask_normalized
    else:
        # Zmniejszenie jasności
        v = v - v * factor * mask_normalized
    # Klampowanie wartości do [0, 255]
    v = np.clip(v, 0, 255)
    hsv[:, :, 2] = v.astype(np.uint8)

def update_image():
    img = Image.fromarray(processed_image)
    img = img.resize((500, 300), Image.Resampling.LANCZOS)
    imgtk = ImageTk.PhotoImage(image=img)
    image_label.config(image=imgtk)
    image_label.image = imgtk

def update_mask_display():
    if mask is None:
        return
    mask_img = Image.fromarray(mask)
    mask_img = mask_img.resize((250, 150), Image.Resampling.NEAREST)
    masktk = ImageTk.PhotoImage(image=mask_img)
    mask_label.config(image=masktk)
    mask_label.image = masktk

def update_bright_dark_display():
    if mask_bright is None or mask_dark is None:
        return
    # Wyświetlanie maski jasnych obszarów
    mask_bright_img = Image.fromarray(mask_bright)
    mask_bright_img = mask_bright_img.resize((250, 150), Image.Resampling.NEAREST)
    mask_brighttk = ImageTk.PhotoImage(image=mask_bright_img)
    mask_bright_label.config(image=mask_brighttk)
    mask_bright_label.image = mask_brighttk
    # Wyświetlanie maski ciemnych obszarów
    mask_dark_img = Image.fromarray(mask_dark)
    mask_dark_img = mask_dark_img.resize((250, 150), Image.Resampling.NEAREST)
    mask_darktk = ImageTk.PhotoImage(image=mask_dark_img)
    mask_dark_label.config(image=mask_darktk)
    mask_dark_label.image = mask_darktk

def on_gloss_change(val):
    if original_image is not None:
        create_masks()
        apply_changes()
        update_mask_display()
        update_bright_dark_display()

def on_hsv_change(val):
    if original_image is not None:
        create_masks()
        apply_changes()
        update_mask_display()
        update_bright_dark_display()

def on_color_change(val):
    if original_image is not None:
        apply_changes()

# Inicjalizacja zmiennych globalnych
original_image = None
processed_image = None
mask = None
mask_bright = None
mask_dark = None

# Tworzenie GUI
root = Tk()
root.title("Symulator Lakieru Samochodu")

# Ramka na obrazy
images_frame = Frame(root)
images_frame.pack()

image_label = Label(images_frame)
image_label.pack(side=LEFT, padx=10, pady=10)

mask_label = Label(images_frame, text="Maska Główna")
mask_label.pack(side=LEFT, padx=10, pady=10)

mask_bright_label = Label(images_frame, text="Maska Jasnych Obszarów")
mask_bright_label.pack(side=LEFT, padx=10, pady=10)

mask_dark_label = Label(images_frame, text="Maska Ciemnych Obszarów")
mask_dark_label.pack(side=LEFT, padx=10, pady=10)

# Ramka na przyciski i kontrolki
controls_frame = Frame(root)
controls_frame.pack(pady=10)

load_button = Button(controls_frame, text="Wczytaj Obraz", command=load_image)
load_button.grid(row=0, column=0, padx=5)

# Suwaki dla wyboru koloru w HSV
color_frame = LabelFrame(controls_frame, text="Wybór Koloru (HSV)")
color_frame.grid(row=0, column=1, padx=5, columnspan=3)

h_slider = Scale(color_frame, from_=0, to=179, orient=HORIZONTAL, label="Hue", command=on_color_change)
h_slider.set(0)
h_slider.pack(side=LEFT, padx=5)

s_slider = Scale(color_frame, from_=0, to=255, orient=HORIZONTAL, label="Saturation", command=on_color_change)
s_slider.set(255)
s_slider.pack(side=LEFT, padx=5)

v_slider = Scale(color_frame, from_=0, to=255, orient=HORIZONTAL, label="Brightness", command=on_color_change)
v_slider.set(255)
v_slider.pack(side=LEFT, padx=5)

# Checkboxy do wyboru, które kanały zmieniać
options_frame = LabelFrame(controls_frame, text="Opcje Zmiany")
options_frame.grid(row=0, column=4, padx=5, columnspan=2)

change_hue_var = IntVar(value=1)
change_saturation_var = IntVar(value=0)
change_brightness_var = IntVar(value=0)

change_hue_cb = Checkbutton(options_frame, text="Zmień Hue", variable=change_hue_var, command=apply_changes)
change_hue_cb.pack(anchor=W)

change_saturation_cb = Checkbutton(options_frame, text="Zmień Saturation", variable=change_saturation_var, command=apply_changes)
change_saturation_cb.pack(anchor=W)

change_brightness_cb = Checkbutton(options_frame, text="Zmień Brightness", variable=change_brightness_var, command=apply_changes)
change_brightness_cb.pack(anchor=W)

# Suwak do regulacji połysku dla jasnych obszarów
gloss_bright_label = Label(controls_frame, text="Połysk Jasnych:")
gloss_bright_label.grid(row=1, column=0, padx=5)

gloss_bright = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=on_gloss_change)
gloss_bright.set(50)
gloss_bright.grid(row=1, column=1, padx=5)

# Suwak do regulacji połysku dla ciemnych obszarów
gloss_dark_label = Label(controls_frame, text="Połysk Ciemnych:")
gloss_dark_label.grid(row=1, column=2, padx=5)

gloss_dark = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=on_gloss_change)
gloss_dark.set(50)
gloss_dark.grid(row=1, column=3, padx=5)

# Ramki do regulacji HSV dla maski
hsv_frame = LabelFrame(root, text="Regulacja HSV Maski")
hsv_frame.pack(padx=10, pady=10)

# Suwak dla Hue Maski
h_min_mask = Scale(hsv_frame, from_=0, to=179, orient=HORIZONTAL, label="Hue Min", command=on_hsv_change)
h_min_mask.set(0)
h_min_mask.grid(row=0, column=0, padx=5, pady=5)

h_max_mask = Scale(hsv_frame, from_=0, to=179, orient=HORIZONTAL, label="Hue Max", command=on_hsv_change)
h_max_mask.set(179)
h_max_mask.grid(row=0, column=1, padx=5, pady=5)

# Suwak dla Saturation Maski
s_min_mask = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Saturation Min", command=on_hsv_change)
s_min_mask.set(50)
s_min_mask.grid(row=1, column=0, padx=5, pady=5)

s_max_mask = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Saturation Max", command=on_hsv_change)
s_max_mask.set(255)
s_max_mask.grid(row=1, column=1, padx=5, pady=5)

# Suwak dla Value Maski
v_min_mask = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Value Min", command=on_hsv_change)
v_min_mask.set(50)
v_min_mask.grid(row=2, column=0, padx=5, pady=5)

v_max_mask = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Value Max", command=on_hsv_change)
v_max_mask.set(255)
v_max_mask.grid(row=2, column=1, padx=5, pady=5)

# Suwak do ustawienia progu jasnych obszarów
bright_threshold_label = Label(hsv_frame, text="Próg Jasnych (V):")
bright_threshold_label.grid(row=3, column=0, padx=5, pady=5)

bright_threshold_slider = Scale(hsv_frame, from_=128, to=255, orient=HORIZONTAL, label="Próg Jasnych", command=on_hsv_change)
bright_threshold_slider.set(180)
bright_threshold_slider.grid(row=3, column=1, padx=5, pady=5)

# Suwak do ustawienia progu ciemnych obszarów
dark_threshold_label = Label(hsv_frame, text="Próg Ciemnych (V):")
dark_threshold_label.grid(row=4, column=0, padx=5, pady=5)

dark_threshold_slider = Scale(hsv_frame, from_=0, to=127, orient=HORIZONTAL, label="Próg Ciemnych", command=on_hsv_change)
dark_threshold_slider.set(80)
dark_threshold_slider.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
