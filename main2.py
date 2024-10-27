import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk

def load_image():
    global original_image, processed_image, mask
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        processed_image = original_image.copy()
        create_mask()
        update_image()
        update_mask_display()

def create_mask():
    global mask
    hsv = cv2.cvtColor(original_image, cv2.COLOR_RGB2HSV)
    # Używamy aktualnych wartości z suwaków
    lower_color = np.array([h_min.get(), s_min.get(), v_min.get()])
    upper_color = np.array([h_max.get(), s_max.get(), v_max.get()])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Maska morfologiczna dla poprawy jakości
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

def choose_color():
    global selected_color
    color = askcolor()[0]
    if color:
        selected_color = (int(color[0]), int(color[1]), int(color[2]))
        apply_changes()

def apply_changes():
    global processed_image
    if original_image is None:
        return
    # Kopia oryginalnego obrazu
    processed_image = original_image.copy()
    # Konwersja wybranego koloru do HSV
    selected_hsv = cv2.cvtColor(np.uint8([[selected_color]]), cv2.COLOR_RGB2HSV)[0][0]
    # Przekształcenie oryginalnego obrazu do HSV
    hsv = cv2.cvtColor(processed_image, cv2.COLOR_RGB2HSV)
    # Zastosowanie maski
    hsv[mask > 0] = selected_hsv
    # Konwersja z powrotem do RGB
    processed_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    # Regulacja połysku/matowości
    adjust_gloss()
    update_image()

def adjust_gloss():
    global processed_image
    if gloss_value.get() == 0:
        return
    # Prosta symulacja połysku poprzez dodanie rozmycia i mieszanie
    gloss_intensity = gloss_value.get() / 100
    blurred = cv2.GaussianBlur(processed_image, (15, 15), 0)
    processed_image = cv2.addWeighted(processed_image, 1 - gloss_intensity, blurred, gloss_intensity, 0)

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

def on_gloss_change(val):
    apply_changes()

def on_hsv_change(val):
    if original_image is not None:
        create_mask()
        apply_changes()
        update_mask_display()

# Inicjalizacja zmiennych globalnych
original_image = None
processed_image = None
mask = None
selected_color = (0, 0, 255)  # Domyślny kolor czerwony

# Tworzenie GUI
root = Tk()
root.title("Symulator Lakieru Samochodu")

# Ramka na obrazy
images_frame = Frame(root)
images_frame.pack()

image_label = Label(images_frame)
image_label.pack(side=LEFT, padx=10, pady=10)

mask_label = Label(images_frame)
mask_label.pack(side=RIGHT, padx=10, pady=10)

# Ramka na przyciski i kontrolki
controls_frame = Frame(root)
controls_frame.pack(pady=10)

load_button = Button(controls_frame, text="Wczytaj Obraz", command=load_image)
load_button.grid(row=0, column=0, padx=5)

color_button = Button(controls_frame, text="Wybierz Kolor", command=choose_color)
color_button.grid(row=0, column=1, padx=5)

# Suwak do regulacji połysku
gloss_label = Label(controls_frame, text="Połysk:")
gloss_label.grid(row=0, column=2, padx=5)

gloss_value = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=on_gloss_change)
gloss_value.set(50)
gloss_value.grid(row=0, column=3, padx=5)

# Ramki do regulacji HSV
hsv_frame = LabelFrame(root, text="Regulacja HSV")
hsv_frame.pack(padx=10, pady=10)

# Suwak dla Hue
h_min = Scale(hsv_frame, from_=0, to=179, orient=HORIZONTAL, label="Hue Min", command=on_hsv_change)
h_min.set(0)
h_min.grid(row=0, column=0, padx=5, pady=5)

h_max = Scale(hsv_frame, from_=0, to=179, orient=HORIZONTAL, label="Hue Max", command=on_hsv_change)
h_max.set(179)
h_max.grid(row=0, column=1, padx=5, pady=5)

# Suwak dla Saturation
s_min = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Saturation Min", command=on_hsv_change)
s_min.set(50)
s_min.grid(row=1, column=0, padx=5, pady=5)

s_max = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Saturation Max", command=on_hsv_change)
s_max.set(255)
s_max.grid(row=1, column=1, padx=5, pady=5)

# Suwak dla Value
v_min = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Value Min", command=on_hsv_change)
v_min.set(50)
v_min.grid(row=2, column=0, padx=5, pady=5)

v_max = Scale(hsv_frame, from_=0, to=255, orient=HORIZONTAL, label="Value Max", command=on_hsv_change)
v_max.set(255)
v_max.grid(row=2, column=1, padx=5, pady=5)

root.mainloop()
