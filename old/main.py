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
        mask = create_mask(original_image)
        update_image()

def create_mask(image):
    # Konwersja do HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    cv2.imshow('Obraz hsv', hsv)
    # Zakres kolorów do segmentacji karoserii (można dostosować)
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([179, 50, 255])
    # Górny zakres czerwieni
    #lower_color = np.array([15, 100, 100])
    #upper_color = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Maska morfologiczna dla poprawy jakości
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask

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

def on_gloss_change(val):
    apply_changes()

# Inicjalizacja zmiennych globalnych
original_image = None
processed_image = None
mask = None
selected_color = (0, 0, 255)  # Domyślny kolor czerwony

# Tworzenie GUI
root = Tk()
root.title("Symulator Lakieru Samochodu")

# Ramka na obraz
image_label = Label(root)
image_label.pack()

# Ramka na przyciski
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

root.mainloop()
