import cv2
import numpy as np
from tkinter import filedialog
from tkinter import Tk

# Globalne zmienne
original_image = None
processed_image = None
selected_color = None
selected_point = None
masks = {}

def load_image():
    global original_image, processed_image
    # Wczytaj obraz za pomocą okna dialogowego
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = cv2.imread(file_path)
        processed_image = original_image.copy()
        show_image()

def show_image():
    global processed_image
    cv2.imshow("Click on the car to select color", processed_image)
    cv2.setMouseCallback("Click on the car to select color", select_color)

def select_color(event, x, y, flags, param):
    global original_image, selected_color, selected_point, masks
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_point = (x, y)
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
        selected_color = hsv_image[y, x]
        print(f"Selected HSV Color: {selected_color} at {selected_point}")
        # Zaznaczenie wybranego punktu na obrazie
        cv2.circle(processed_image, selected_point, 5, (0, 255, 0), -1)
        create_masks()
        show_masks()

def create_masks():
    global original_image, selected_color, selected_point, masks
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # Granice dla koloru z uwzględnieniem odchyleń
    h = selected_color[0]
    s = selected_color[1]
    v = selected_color[2]

    lower_bound = np.array([h, max(0, s - 0.3 * s), max(0, v - 0.3 * v)], dtype=np.uint8)
    upper_bound = np.array([h, min(255, s + 0.3 * s), min(255, v + 0.3 * v)], dtype=np.uint8)

    # Maska na podstawie wybranego koloru
    color_mask = cv2.inRange(hsv, lower_bound, upper_bound)
    print(f"Color Mask Sum: {np.sum(color_mask)}")  # Debug: Sprawdź, czy maska nie jest pusta

    # Operacje morfologiczne dla lepszej jakości maski
    kernel = np.ones((5, 5), np.uint8)
    color_mask_cleaned = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)

    # Segmentacja K-means
    k_means_mask = segment_with_k_means(original_image, selected_point)

    # Połącz maski (segmentacja + kolor)
    combined_mask = combine_masks(k_means_mask, color_mask_cleaned, weight=0.7)

    # Zapisz maski w słowniku
    masks["color_mask"] = color_mask_cleaned
    masks["k_means_mask"] = k_means_mask
    masks["combined_mask"] = combined_mask

def segment_with_k_means(image, selected_point):
    # Rozmiar zmniejszony do 600x400 dla wydajności
    resized = cv2.resize(image, (600, 400))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    pixels = hsv.reshape((-1, 3))
    pixels = np.float32(pixels)

    k = 3  # Liczba klastrów
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, _ = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Dopasowanie punktu do odpowiedniego klastra
    resized_point = (int(selected_point[0] * 600 / image.shape[1]), int(selected_point[1] * 400 / image.shape[0]))
    selected_cluster = labels[resized_point[1] * 600 + resized_point[0]]
    print(f"Selected Cluster: {selected_cluster}")  # Debug: Wybrany klaster

    # Maska dla wybranego klastra
    mask = (labels.reshape((400, 600)) == selected_cluster).astype(np.uint8) * 255

    # Dopasowanie maski do oryginalnego rozmiaru obrazu
    original_size = original_image.shape[:2]
    mask_resized = cv2.resize(mask, (original_size[1], original_size[0]), interpolation=cv2.INTER_NEAREST)

    return mask_resized

def combine_masks(segment_mask, color_mask, weight=0.7):
    """
    Łączy maskę segmentacji i maskę koloru:
    - segment_mask: maska segmentacji (bazowa).
    - color_mask: maska koloru (filtr).
    - weight: waga maski koloru (domyślnie 0.7).
    """
    # Normalizacja masek do wartości [0, 1]
    segment_norm = segment_mask.astype(np.float32) / 255.0
    color_norm = color_mask.astype(np.float32) / 255.0

    # Łączenie masek
    combined = segment_norm * (1 - weight) + color_norm * weight

    # Próg, aby uwzględnić tylko istotne piksele
    combined = (combined > 0.5).astype(np.uint8) * 255

    return combined

def show_masks():
    global masks
    if "color_mask" in masks:
        cv2.imshow("Color Mask", masks["color_mask"])
    if "k_means_mask" in masks:
        cv2.imshow("K-Means Mask", masks["k_means_mask"])
    if "combined_mask" in masks:
        combined_mask = masks["combined_mask"]
        result = cv2.bitwise_and(original_image, original_image, mask=combined_mask)
        print(f"Combined Mask Sum: {np.sum(combined_mask)}")  # Debug: Sprawdź, czy połączona maska nie jest pusta
        cv2.imshow("Combined Mask", combined_mask)
        cv2.imshow("Detected Car", result)

# GUI do wczytania obrazu
root = Tk()
root.withdraw()  # Ukryj główne okno tkinter
load_image()

cv2.waitKey(0)
cv2.destroyAllWindows()
