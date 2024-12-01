import cv2
import numpy as np

# Wczytanie obrazu
image = cv2.imread('images/maluch.png')
original = image.copy()

# Konwersja do skali szarości
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Wygładzenie obrazu (redukcja szumów)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 1. Detekcja krawędzi metodą Canny
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)


# 2. Znalezienie konturów
contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Utworzenie pustej maski
mask = np.zeros_like(gray)


# 3. Filtracja konturów na podstawie powierzchni i proporcji
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 5000:  # Próg powierzchni do dostosowania
        # Obliczenie prostokąta otaczającego kontur
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        if 0.5 < aspect_ratio < 2.5:  # Przykładowe proporcje dla samochodu
            # Narysowanie konturu na masce
            cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

# Zapisanie maski lub wyświetlenie wyniku
cv2.imwrite('car_mask.jpg', mask)
cv2.imshow('Edges', edges)
cv2.imshow('Mask', mask)
cv2.waitKey(20000)