import cv2
import numpy as np

# Wczytanie obrazu
image = cv2.imread('merc.jpg')
image_resized = cv2.resize(image, (600, 400))  # Zmiana rozmiaru dla łatwiejszego przetwarzania

# Konwersja do przestrzeni kolorów HSV (opcjonalne, ale może być bardziej efektywne)
image_hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

# Przekształcenie obrazu do macierzy 2D
pixels = image_hsv.reshape((-1, 3))
pixels = np.float32(pixels)  # Konwersja do float32, wymagana przez k-means

# Parametry k-means
k = 3  # Liczba klastrów (dostosuj w zależności od obrazu)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
_, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Konwersja wyników k-means do obrazu
centers = np.uint8(centers)  # Powrót do typu uint8
segmented_image = centers[labels.flatten()]
segmented_image = segmented_image.reshape(image_resized.shape)

# Wybór klastra odpowiadającego samochodowi
selected_cluster = 2  # Wybierz indeks klastra (może wymagać dostosowania po wizualizacji)
mask = (labels.reshape(image_resized.shape[:2]) == selected_cluster).astype(np.uint8) * 255

# Usunięcie szumów za pomocą operacji morfologicznych
kernel = np.ones((5, 5), np.uint8)
mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Wyodrębnienie samochodu z obrazu
car_only = cv2.bitwise_and(image_resized, image_resized, mask=mask_cleaned)

# Wyświetlenie wyników
cv2.imshow('Oryginalny obraz', image_resized)
cv2.imshow('Segmentowany obraz', segmented_image)
cv2.imshow('Maska', mask_cleaned)
cv2.imshow('Samochod', car_only)
cv2.waitKey(0)
cv2.destroyAllWindows()
