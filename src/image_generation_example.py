import numpy as np
import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image, ImageDraw, ImageFont
from rembg import remove

pipeline = AutoPipelineForText2Image.from_pretrained(
    "kandinsky-community/kandinsky-2-1", torch_dtype=torch.float16
).to("cuda")
pipeline.enable_model_cpu_offload()

# Определение рекомендаций на основе кластеров
recommendations = {
    "a. Супер-ЗП (6,15)": "luxury car, yacht, private jet",
    "c. Масс-ЗП закредитованные (12)": "economy car, smartphone, travel suitcase",
    "k. Без продукта (7,13,18)": "consumer loan, car, smartphone, travel suitcase",
    "d. Масс-ЗП без согласия БКИ (1,3)": "reliable car, safe investment options",
    "h. Бывшие зарплатники (4,9,10,11)": "investment plans, savings accounts",
    "j. Депозиты в оттоке (0,17)": "alternative investment options, gold, real estate",
    "b. Текущие заемщики (14)": "new credit products, debt consolidation options",
    "e. Супер-аффлуент (-1)": "luxury investments, high-end real estate, premium services",
    "g. ДК/ЗК до 6 моба (20)": "mobile banking options, online financial services",
    "f. Супер-депозиты (8,16)": "high-yield savings accounts, long-term investments",
    "i. Бывшие заемщики (2,5,19)": "new loan products, personalized financial services",
}


# Функция для генерации изображения
def generate_image(cluster):
    prompt = f"3d image of {recommendations[cluster]}, cinematic, moody white lighting, official"
    negative_prompt = "low quality, bad quality, funny, detailed"
    image = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        prior_guidance_scale=1.0,
        guidance_scale=4.0,
        height=768,
        width=768,
    ).images[0]
    return image


# Функция для удаления фона
def remove_background(image):
    image_np = np.array(image)
    image_np_nobg = remove(image_np)
    return Image.fromarray(image_np_nobg)


# Функция для создания градиентного фона
def create_gradient_background(width, height):
    base = Image.new("RGBA", (width, height), (255, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    for i in range(height):
        r = int(219 * (i / height))
        g = int(80 * (i / height))
        b = int(152 * (i / height))
        draw.line((0, i, width, i), fill=(r, g, b, 255))
    return base


# Функция для масштабирования изображения
def scale_image(image, target_height):
    aspect_ratio = image.width / image.height
    new_height = int(target_height * 0.8)
    new_width = int(new_height * aspect_ratio)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


# Функция для объединения изображений
def combine_images(banner_image, generated_image, position):
    banner_image.paste(generated_image, position, generated_image)
    return banner_image


# Функция для добавления текста на изображение
def add_text_to_image(image, text):
    draw = ImageDraw.Draw(image)
    font = (
        ImageFont.load_default()
    )  # Вы можете заменить на другой шрифт при необходимости
    text_position = (50, 50)
    draw.text(text_position, text, font=font, fill="white")
    return image


# Основная функция для генерации баннера
def generate_banner(cluster, product=None):
    # Генерация нового изображения
    generated_image = generate_image(cluster)
    # Удаление фона из сгенерированного изображения
    generated_image_nobg = remove_background(generated_image)

    # Создание градиентного фона размером 200x1200 пикселей
    gradient_background = create_gradient_background(1200, 200)

    # Масштабирование сгенерированного изображения до 80% от высоты баннера
    scaled_image = scale_image(generated_image_nobg, 200)

    # Объединение изображений
    final_image = combine_images(
        gradient_background, scaled_image, (1050, 20)
    )  # Позиция может быть скорректирована
    final_image.save("final_combined_banner.png")
    # Добавление текста на изображение
    # random_text_key = random.choice(list(texts.keys()))
    # random_text = texts[random_text_key]
    # final_image_with_text = add_text_to_image(final_image, random_text)

    # Сохранение результата
    # final_image_with_text.save('final_combined_banner_with_text.png')

    # Отображение результата
    # final_image_with_text.show()


# Вызов функции для генерации баннера с учетом заданного кластера
cluster = "k. Без продукта (7,13,18)"
generate_banner(cluster)
