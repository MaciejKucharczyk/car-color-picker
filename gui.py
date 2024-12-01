from tkinter import *
from main import *

def gui():
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

    color_button = Button(controls_frame, text="Wybierz Kolor", command=choose_color)
    color_button.grid(row=0, column=1, padx=5)

    # Suwak do regulacji połysku dla jasnych obszarów
    gloss_bright_label = Label(controls_frame, text="Połysk Jasnych:")
    gloss_bright_label.grid(row=0, column=2, padx=5)

    gloss_bright = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=on_gloss_change)
    gloss_bright.set(50)
    gloss_bright.grid(row=0, column=3, padx=5)

    # Suwak do regulacji połysku dla ciemnych obszarów
    gloss_dark_label = Label(controls_frame, text="Połysk Ciemnych:")
    gloss_dark_label.grid(row=0, column=4, padx=5)

    gloss_dark = Scale(controls_frame, from_=0, to=100, orient=HORIZONTAL, command=on_gloss_change)
    gloss_dark.set(50)
    gloss_dark.grid(row=0, column=5, padx=5)

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
    