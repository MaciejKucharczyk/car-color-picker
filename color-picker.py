import cv2
import numpy as np
from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageTk

def hsv_to_rgb(h, s, v):
    """Konwertuje kolor z HSV na RGB."""
    color = np.uint8([[[h, s, v]]])
    rgb = cv2.cvtColor(color, cv2.COLOR_HSV2RGB)[0][0]
    return tuple(rgb)

def update_color_display(event=None):
    """Aktualizuje wyświetlany kolor na podstawie wartości HSV."""
    h = hue_scale.get()
    s = saturation_scale.get()
    v = value_scale.get()
    
    rgb = hsv_to_rgb(h, s, v)
    color_display.config(bg='#%02x%02x%02x' % rgb)
    rgb_label.config(text=f'RGB: {rgb}')
    hsv_label.config(text=f'HSV: ({h}, {s}, {v})')

def save_color():
    """Zapisuje aktualny kolor HSV i RGB."""
    h = hue_scale.get()
    s = saturation_scale.get()
    v = value_scale.get()
    rgb = hsv_to_rgb(h, s, v)
    print(f'Zapisany kolor - HSV: ({h}, {s}, {v}), RGB: {rgb}')

# Tworzenie głównego okna
root = Tk()
root.title("HSV Color Picker")
root.geometry("400x400")
root.resizable(False, False)

# Ramka na suwaki
sliders_frame = Frame(root)
sliders_frame.pack(pady=20)

# Suwak dla Hue
hue_label = Label(sliders_frame, text="Hue (H):")
hue_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')
hue_scale = Scale(sliders_frame, from_=0, to=179, orient=HORIZONTAL, command=update_color_display)
hue_scale.set(0)
hue_scale.grid(row=0, column=1, padx=5, pady=5)

# Suwak dla Saturation
saturation_label = Label(sliders_frame, text="Saturation (S):")
saturation_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')
saturation_scale = Scale(sliders_frame, from_=0, to=255, orient=HORIZONTAL, command=update_color_display)
saturation_scale.set(0)
saturation_scale.grid(row=1, column=1, padx=5, pady=5)

# Suwak dla Value
value_label = Label(sliders_frame, text="Value (V):")
value_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')
value_scale = Scale(sliders_frame, from_=0, to=255, orient=HORIZONTAL, command=update_color_display)
value_scale.set(0)
value_scale.grid(row=2, column=1, padx=5, pady=5)

# Ramka na wyświetlany kolor
color_frame = Frame(root, bd=2, relief=GROOVE)
color_frame.pack(pady=10)

color_display = Label(color_frame, bg="#000000", width=20, height=10)
color_display.pack(padx=10, pady=10)

# Ramka na etykiety RGB i HSV
labels_frame = Frame(root)
labels_frame.pack(pady=5)

rgb_label = Label(labels_frame, text="RGB: (0, 0, 0)")
rgb_label.pack()

hsv_label = Label(labels_frame, text="HSV: (0, 0, 0)")
hsv_label.pack()

# Przycisk zapisu koloru
save_button = Button(root, text="Zapisz Kolor", command=save_color)
save_button.pack(pady=10)

# Inicjalizacja wyświetlenia koloru
update_color_display()

root.mainloop()
