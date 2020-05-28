import cv2

image = cv2.imread(r"D:\Python\OpenCV_my_tests\test.JPG", cv2.IMREAD_GRAYSCALE)  # Загружаем изображения как grayscale
width = 500  # Задаём ширину изображения в пикселях.
height = int(image.shape[0] * float(width) / image.shape[1])  # Пропорционально пересчитанная высота изображения
dim = (width, height)
median = 200  # граничное среднее значение цвета для пересчета в black and white изображение
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # Пересчитываем изображение в нужные нам размеры
ret, resized_b_and_w = cv2.threshold(resized, median, 255, cv2.THRESH_BINARY)  # Пересчитываем изображение в black and white
window_gray = "Исходное изображение в оттенках серого"
window_black = "Пересчитанное в чёрно-белое изображение"
cv2.namedWindow(window_gray)
cv2.namedWindow(window_black)
cv2.moveWindow(window_gray, 400, 20)
cv2.moveWindow(window_black, 400, 350)
cv2.imshow(window_gray, resized)  # Выводим на монитор исходное grayscale изображение
cv2.imshow(window_black, resized_b_and_w)  # Выводим на монитор получившееся black and white изображение
non_zero_pixels = cv2.countNonZero(resized_b_and_w)  # Подсчитываем количество белых пикселей
black_pixels_percent = 100 - (non_zero_pixels * 100 / (width * height))
print("Процент заполнения листа печатными элементами :", black_pixels_percent)

cv2.waitKey(0)

