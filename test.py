## -- coding: utf-8 --
import cv2
import pdf2image

images = pdf2image.convert_from_bytes(open(r"D:\Python\test.pdf", 'rb').read())
images[0].save(r"D:\Python\test_pdf.JPG", 'JPEG')

image = cv2.imread(r"D:\Python\test_pdf.JPG", cv2.IMREAD_GRAYSCALE)  # Загружаем изображения как grayscale
width = 500  # Задаём ширину изображения в пикселях.
height = int(image.shape[0] * float(width) / image.shape[1])  # Пропорционально пересчитанная высота изображения
dim = (width, height)
median = 100  # Граничное среднее значение цвета для перовода изображения цветовую систему black and white
resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # Пересчитываем изображение в нужные нам размеры
ret, resized_b_and_w = cv2.threshold(resized, median, 255, cv2.THRESH_BINARY)  # Пересчитываем изображение в black and white
window_gray = u"Исходное изображение в оттенках серого"
window_black = u"Пересчитанное в чёрно-белое изображение"
cv2.namedWindow(window_gray)
cv2.namedWindow(window_black)
cv2.moveWindow(window_gray, 50, 40)
cv2.moveWindow(window_black, 555, 40)
cv2.imshow(window_gray, resized)  # Выводим на монитор исходное grayscale изображение
cv2.imshow(window_black, resized_b_and_w)  # Выводим на монитор получившееся black and white изображение
non_zero_pixels = cv2.countNonZero(resized_b_and_w)  # Подсчитываем количество белых пикселей
black_pixels_percent = round(100 - (non_zero_pixels * 100 / (width * height)))
print("Процент заполнения листа печатными элементами:", black_pixels_percent, "%")

cv2.waitKey(0)
