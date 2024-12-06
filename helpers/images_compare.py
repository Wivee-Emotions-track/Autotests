import cv2
import numpy as np


def compare_image(path_to_image, path_to_reference):
    reference_image = cv2.imread(path_to_reference)
    canvas_image = cv2.imread(path_to_image)

    difference = cv2.absdiff(reference_image, canvas_image)
    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_difference, 50, 255, cv2.THRESH_BINARY)

    # Если нет отличий, сумма всех пикселей в threshold должна быть равна 0
    if np.sum(threshold) == 0:
        return True
    else:
        return False

def get_coordinates_of_found_element(path_to_background, path_to_image, background_element):
    # Загрузка изображений
    canvas_image = cv2.imread(path_to_background)
    template = cv2.imread(path_to_image)  # Эталон элемента, который нужно найти

    # Сопоставление шаблонов
    result = cv2.matchTemplate(canvas_image, template, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Проверить, нашли ли элемент
    threshold = 0.8  # Уровень совпадения
    if max_val >= threshold:
        print("Элемент найден!")
        top_left = max_loc
        template_height, template_width = template.shape[:2]

        # Определить центр найденного элемента
        center_x = top_left[0] + template_width // 2
        center_y = top_left[1] + template_height // 2
    else:
        raise Exception("Элемент не найден.")
    canvas_bounding_box = background_element.bounding_box()  # Получение размеров канвы

    click_x = canvas_bounding_box["x"] + center_x
    click_y = canvas_bounding_box["y"] + center_y
    return click_x, click_y