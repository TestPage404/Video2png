import cv2, os, hashlib
from PIL import Image

def extract_frames(video_path, output_path, frame_interval=1):
    # Открываем видеофайл
    cap = cv2.VideoCapture(video_path)
    count = 0

    while cap.isOpened():
        # Считываем кадр из видео
        ret, frame = cap.read()

        # Если достигнут конец видео, завершаем цикл
        if not ret:
            break

        # Извлекаем кадр каждый frame_interval-ый кадр
        if count % frame_interval == 0:
            frame_output_path = f"{output_path}\\frame_{count}.jpg"
            cv2.imwrite(frame_output_path, frame)
            print(f"Извлечен кадр: {frame_output_path}")

        count += 1

    # Закрываем видеофайл
    cap.release()
    cv2.destroyAllWindows()

def image_hash(image_path, hash_size=8):
    image = Image.open(image_path)
    resized_image = image.resize((hash_size + 1, hash_size), Image.LANCZOS)
    grayscale_image = resized_image.convert("L")
    pixels = list(grayscale_image.getdata())
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = grayscale_image.getpixel((col, row))
            pixel_right = grayscale_image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, "0"))
            decimal_value = 0
    return "".join(hex_string)

def delete_duplicates(folder_path):
    image_hashes = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                file_hash = image_hash(file_path)
                if file_hash not in image_hashes:
                    image_hashes[file_hash] = file_path
                else:
                    os.remove(file_path)
                    print(f"Удален повторяющийся файл: {file_path}")

def crop_image(input_image_path, output_image_path):
    image = Image.open(input_image_path)
    left = 250  # левая координата обрезки
    top = 70  # верхняя координата обрезки
    right = 1030  # правая координата обрезки
    bottom = 570  # нижняя координата обрезки
    cropped_image = image.crop((left, top, right, bottom))
    cropped_image.save(output_image_path)


if __name__ == "__main__":
    file_name = '1. Основы работы с ESR.mp4'
    video_path = f"d:\\Eltex\\{file_name}"
    output_path = f"d:\\Eltex\\{file_name.split()[0]}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    frame_interval = 1  # Извлекать каждый кадр
    extract_frames(video_path, output_path, frame_interval)
    delete_duplicates(output_path)
    for root,dirs,files in os.walk(output_path):
        for file in files:
            input_image_path = f"{output_path}\\{file}"
            crop_image(input_image_path, input_image_path)
