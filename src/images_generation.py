import os
import random

import numpy as np
import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
from torch import autocast

from src.logger import app_logger

log = app_logger(__name__)

pipeline = AutoPipelineForText2Image.from_pretrained(
    "kandinsky-community/kandinsky-2-1", torch_dtype=torch.float16
).to("cuda")
pipeline.enable_model_cpu_offload()

# Определение кластеров и возможных объектов для каждого кластера
clusters = {
    "a. Супер-ЗП (6,15)": [
        "luxury car",
        "yacht",
        "private jet",
        "designer watch",
        "fine art",
        "private island",
        "luxury home",
        "golf clubs",
        "vintage wine bottle",
        "diamond ring",
        "sports car",
        "custom suit",
    ],
    "c. Масс-ЗП закредитованные (12)": [
        "economy car",
        "smartphone",
        "laptop",
        "travel suitcase",
        "home appliance",
        "furniture",
        "bicycle",
        "budget fashion items",
        "tablet",
        "camera",
        "fitness tracker",
        "headphones",
        "gaming console",
        "backpack",
        "TV",
        "books",
        "kitchen gadgets",
    ],
    "k. Без продукта (7,13,18)": [
        "car",
        "smartphone",
        "travel suitcase",
        "laptop",
        "bicycle",
        "camera",
        "tablet",
        "fitness tracker",
        "gaming console",
        "headphones",
        "backpack",
        "TV",
        "books",
        "kitchen gadgets",
        "furniture",
        "home appliance",
    ],
    "d. Масс-ЗП без согласия БКИ (1,3)": [
        "reliable car",
        "documents",
        "insurance policy",
        "gold bars",
        "real estate",
        "life insurance",
        "health insurance",
        "stocks",
        "savings passbook",
        "emergency fund",
        "education plan",
        "family car",
        "home renovation tools",
    ],
    "h. Бывшие зарплатники (4,9,10,11)": [
        "investment documents",
        "savings passbook",
        "retirement plan",
        "stocks",
        "bonds",
        "real estate",
        "insurance policy",
        "gold bars",
        "family car",
        "home renovation tools",
        "education plan",
        "travel package",
    ],
    "j. Депозиты в оттоке (0,17)": [
        "investment options",
        "gold bars",
        "real estate",
        "stocks",
        "bonds",
        "mutual fund documents",
        "pension plan",
        "fixed deposits",
        "insurance policy",
        "savings passbook",
        "luxury items",
        "emergency fund",
        "travel package",
        "education plan",
        "family car",
    ],
    "b. Текущие заемщики (14)": [
        "car loan documents",
        "home loan documents",
        "personal loan documents",
        "credit card",
        "business loan documents",
        "mortgage documents",
        "travel loan documents",
        "emergency loan documents",
        "line of credit",
        "auto loan documents",
    ],
    "e. Супер-аффлуент (-1)": [
        "luxury investments",
        "high-end real estate",
        "private jet",
        "yacht",
        "luxury car",
        "fine art",
        "designer watch",
        "diamond jewelry",
        "sports car",
        "private island",
        "luxury home",
    ],
    "g. ДК/ЗК до 6 моба (20)": [
        "mobile banking setup",
        "smartphone",
        "tablet",
        "laptop",
        "home appliance",
        "furniture",
        "bicycle",
        "budget fashion items",
        "camera",
        "fitness tracker",
        "power bank",
        "headphones",
        "gaming console",
        "backpack",
        "kitchen gadgets",
        "TV",
    ],
    "f. Супер-депозиты (8,16)": [
        "high-yield savings passbook",
        "long-term investments",
        "stocks",
        "bonds",
        "mutual fund documents",
        "gold bars",
        "real estate",
        "fixed deposits",
        "pension plan",
        "insurance policy",
        "luxury items",
        "travel package",
        "education plan",
        "family car",
    ],
    "i. Бывшие заемщики (2,5,19)": [
        "personal loan documents",
        "credit card",
        "car and documents",
        "home and documents",
        "bachelor hat and documents",
        "business chart and documents",
        "money stack and documents",
        "documents, ticket, plane, palms",
        "medicine logo and documents",
        "line of credit",
        "auto loan documents",
    ],
}

# Определение фонов
solid_colors = [
    ("#4F6AE8", "medium blue"),
    ("#CBE6FC", "pale (mostly white) blue"),
    ("#F6C3A8", "salmon pink"),
    ("#6580F7", "royal blue"),
    ("#DEDDFC", "lavender"),
    ("#663546", "dark wine colour"),
    ("#F4F6FA", "light gray"),
]

gradient_colors = [
    (("#8A9EF6", "#445DD3"), ("periwinkle blue", "deeper blue")),
    (("#79B8EE", "#3372B5"), ("azure", "cobalt blue")),
    (("#B2D8FA", "#9F509B"), ("pale blue", "muted plum")),
    (("#DEEFFD", "#569BDC"), ("light blue", "standard blue")),
    (("#8B9443", "#B0E4CA"), ("olive green", "soft teal")),
]

# Определение текстов для типов продуктов
product_texts = {
    "Классический потребительский кредит": '"Ваша возможность - наш выбор!"',
    "Рефинансирование внутреннего ПК в Газпромбанке": '"Безграничное содержимое, всегда рядом"',
    "Кредитная карта": '"Ваша кредитная карта, в банке - ваш ресурс!"',
    "Ипотека (обычная, льготная, ИТ, дальневосточная и тд)": '"Надежность - ключ к успеху - наш продукт! Покупайте дома с нас!"',
    "Премиальная карта": '"Без границ - в вашем карте!"',
    "Страхование жизни": '"Банк - ваш защитник, гарантия вашего благополучия!"',
    "Обмен валюты": '"Без границ - наш новый баланс!"',
    "Индивидуальный зарплатный проект": '"Разработайте свою будущую карьеру - с нашим индивидуальным зарплатным проектом!"',
}


# Функция для выбора случайных объектов из списка
def get_random_objects(cluster):
    if cluster not in clusters:
        cluster = "k. Без продукта (7,13,18)"
    objects = random.sample(clusters[cluster], k=random.randint(1, 3))
    return objects


# Функция для создания сплошного фона
def create_solid_background(color, width, height):
    base = Image.new("RGBA", (width, height), color)
    return base


# Функция для создания градиентного фона
def create_gradient_background(color1, color2, width, height):
    base = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(base)
    for i in range(height):
        ratio = i / height
        r = int(int(color1[1:3], 16) * (1 - ratio) + int(int(color2[1:3], 16) * ratio))
        g = int(int(color1[3:5], 16) * (1 - ratio) + int(int(color2[3:5], 16) * ratio))
        b = int(int(color1[5:], 16) * (1 - ratio) + int(int(color2[5:], 16) * ratio))
        draw.line((0, i, width, i), fill=(r, g, b))
    return base


# Функция для генерации изображения
def generate_raw_image(
    cluster,
    product_description: str | None = None,
    color_topic_1: str | None = None,
    color_topic_2: str | None = None,
):
    objects = get_random_objects(cluster)
    objects_prompt = ", ".join(objects)
    prompt = f"{objects_prompt}, 3d, cinematic, blue moody lighting, realistic, official, big, solid white background, colourful with {color_topic_1} elements, banking thematics"
    if product_description:
        prompt += f" for advertising the following product: {product_description}"
    negative_prompt = "low quality, bad quality, cartoon, futuristic, text"
    log.info("Prompt: %s. Negative prompt: %s", prompt, negative_prompt)
    with autocast("cuda"):
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


# Функция для масштабирования изображения
def scale_image(image, target_height):
    aspect_ratio = image.width / image.height
    new_height = int(target_height * 0.95)
    new_width = int(new_height * aspect_ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)


# Функция для объединения изображений
def combine_images(banner_image, generated_image, position):
    banner_image.paste(generated_image, position, generated_image)
    return banner_image


def generate_position(banner_size: tuple[int, int]) -> tuple[int, int]:
    if banner_size == (216, 1184):
        text_position = (50, 50)
    elif banner_size == (380, 380):
        text_position = (50, 10)
    elif banner_size == (640, 1160):
        text_position = (50, banner_size[0] // 2 - 50)
    else:
        text_position = (50, 50)
    return text_position


def calc_font_size(banner_size) -> int:
    return int(max(banner_size[0] / 7, banner_size[1] / 7))


# Функция для добавления текста на изображение
# async def add_text_to_image(image, title: str, subtitle: str, banner_size, filename):
#     position = generate_position(banner_size)
#     draw = ImageDraw.Draw(image)
#     try:
#         try:
#             font_size = calc_font_size(banner_size)
#             log.info(f"Font size: {font_size}")
#             font = ImageFont.truetype(os.environ["TITLE_FONT_PATH"], int(font_size))
#             sub_font = ImageFont.truetype(
#                 os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
#             )
#         except Exception as error:
#             log.warning("Loading custom font died with %s", error)
#             font_size = 20
#             font = ImageFont.load_default()  # Шрифт по умолчанию
#             sub_font = ImageFont.load_default()  # Шрифт по умолчанию
#         if title:
#             draw.text(position, title, font=font, fill="white")
#         if subtitle:
#             draw.text(
#                 (position[0], position[1] + font_size),
#                 subtitle,
#                 font=sub_font,
#                 fill="white",
#             )
#         image.save(f"{os.environ['PICTURES_FOLDER']}/{filename}.png")
#     except UnicodeEncodeError:
#         # Если возникла ошибка, значит текст содержит символы, не поддерживаемые шрифтом по умолчанию
#         log.error(
#             "Ошибка кодировки. Пожалуйста, используйте шрифт, поддерживающий кириллицу."
#         )
#     return image


# Функция для создания фона
def create_background(cluster, width, height):
    if cluster == "a. Супер-ЗП (6,15)" or cluster == "e. Супер-аффлуент (-1)":
        color = "#663546"
        return create_solid_background(color, width, height), "red"
    else:
        if random.random() > 0.5:
            color, color_name = random.choice(solid_colors)
            return create_solid_background(color, width, height), color_name
        else:
            colors, colors_names = random.choice(gradient_colors)
            color1, color2 = colors_names
            return (
                create_gradient_background(color1, color2, width, height),
                colors_names,
            )


# Основная функция для генерации баннера
def generate_banner(
    cluster: str,
    filename: str,
    banner_size: tuple[int, int],
    product: str | None = None,
) -> None:
    # Создание фона
    background, color_topic = create_background(cluster, banner_size[1], banner_size[0])
    if isinstance(color_topic, tuple):
        color_topic_1, color_topic_2 = color_topic
    else:
        color_topic_1, color_topic_2 = color_topic, None

    # Генерация нового изображения
    generated_image = generate_raw_image(
        cluster,
        product_description=product,
        color_topic_1=color_topic_1,
        color_topic_2=color_topic_2,
    )

    # Удаление фона из сгенерированного изображения
    generated_image_nobg = remove_background(generated_image)
    generated_image_nobg.save(f"{os.environ['PICTURES_FOLDER']}/{filename}_object.png")

    # Масштабирование сгенерированного изображения
    scaled_image = scale_image(generated_image_nobg, banner_size[0])

    # Определение позиции текста и изображения в зависимости от размера баннера
    if banner_size == (216, 1184):
        image_position = (
            banner_size[1] - scaled_image.width - 50,
            (banner_size[0] - scaled_image.height) // 2,
        )
    elif banner_size == (380, 380):
        image_position = (
            (banner_size[1] - scaled_image.width) // 2,
            (banner_size[0] - scaled_image.height) // 2 + 50,
        )
    elif banner_size == (640, 1160):
        image_position = (
            banner_size[1] - scaled_image.width - 50,
            banner_size[0] - scaled_image.height - 50,
        )
    else:
        image_position = (
            banner_size[1] - scaled_image.width,
            banner_size[0] - scaled_image.height,
        )

    # Объединение изображений
    final_image = combine_images(background, scaled_image, image_position)
    final_image.save(f"{os.environ['PICTURES_FOLDER']}/{filename}.png")


# Функция для генерации баннера с учетом извлечённого классификатором кластера
async def generate_image(
    segment: str,
    filename: str,
    banner_size: tuple[int, int],
    product: str | None = None,
) -> None:
    generate_banner(
        segment, product=product, banner_size=banner_size, filename=filename
    )


def get_size_text(draw, position, text, font):
    text_bbox = draw.textbbox(position, text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    return text_width, text_height


async def add_text_to_image(
    image,
    title: str,
    subtitle: str,
    banner_size,
    filename,
    object_size: tuple[int, int],
):
    if banner_size == (216, 1184):
        image_position = (
            banner_size[1] - object_size[0] - 50,
            (banner_size[0] - object_size[1]) // 2,
        )
    elif banner_size == (380, 380):
        image_position = (
            (banner_size[1] - object_size[0]) // 2,
            (banner_size[0] - object_size[1]) // 2 + 50,
        )
    elif banner_size == (640, 1160):
        image_position = (
            banner_size[1] - object_size[0] - 50,
            banner_size[0] - object_size[1] - 50,
        )
    else:
        image_position = (
            banner_size[1] - object_size[0],
            banner_size[0] - object_size[1],
        )

    position = generate_position(banner_size)
    draw = ImageDraw.Draw(image)
    try:
        try:
            if banner_size == (216, 1184):
                font_size = calc_font_size(banner_size)
                font = ImageFont.truetype(os.environ["TITLE_FONT_PATH"], int(font_size))
                text_width, text_height = get_size_text(draw, position, title, font)
                while text_width > image_position[0] - position[0]:
                    font_size -= 5
                    font = ImageFont.truetype(
                        os.environ["TITLE_FONT_PATH"], int(font_size)
                    )
                    text_width, text_height = get_size_text(draw, position, title, font)
                font_size = calc_font_size(banner_size)
                sub_font = ImageFont.truetype(
                    os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                )

                text_width, text_height = get_size_text(
                    draw, position, subtitle, sub_font
                )
                while text_width > image_position[0] - position[0]:
                    font_size -= 5
                    sub_font = ImageFont.truetype(
                        os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                    )
                    text_width, text_height = get_size_text(
                        draw, position, subtitle, sub_font
                    )
            elif banner_size == (380, 380):
                font_size = calc_font_size(banner_size)
                font = ImageFont.truetype(os.environ["TITLE_FONT_PATH"], int(font_size))
                text_width, text_height = get_size_text(draw, position, title, font)
                while text_width > banner_size[1] - 5:
                    font_size -= 1
                    font = ImageFont.truetype(
                        os.environ["TITLE_FONT_PATH"], int(font_size)
                    )
                    text_width, text_height = get_size_text(draw, position, title, font)

                font_size = calc_font_size(banner_size)
                sub_font = ImageFont.truetype(
                    os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                )
                text_width, text_height = get_size_text(
                    draw, position, subtitle, sub_font
                )

                while text_width > banner_size[1] - 5:
                    font_size -= 1
                    sub_font = ImageFont.truetype(
                        os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                    )
                    text_width, text_height = get_size_text(
                        draw, position, subtitle, sub_font
                    )

            elif banner_size == (640, 1160):
                font_size = calc_font_size(banner_size)
                font = ImageFont.truetype(os.environ["TITLE_FONT_PATH"], int(font_size))
                text_width, text_height = get_size_text(draw, position, title, font)
                while text_width > banner_size[1] - 50:
                    font_size -= 5
                    font = ImageFont.truetype(
                        os.environ["TITLE_FONT_PATH"], int(font_size)
                    )
                    text_width, text_height = get_size_text(draw, position, title, font)

                font_size = calc_font_size(banner_size)
                sub_font = ImageFont.truetype(
                    os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                )

                text_width, text_height = get_size_text(
                    draw, position, subtitle, sub_font
                )
                while text_width > image_position[0]:
                    font_size -= 5
                    sub_font = ImageFont.truetype(
                        os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                    )
                    text_width, text_height = get_size_text(
                        draw, position, subtitle, sub_font
                    )
            else:
                font_size = calc_font_size(banner_size)
                log.info(f"Font size: {font_size}")
                font = ImageFont.truetype(os.environ["TITLE_FONT_PATH"], int(font_size))
                sub_font = ImageFont.truetype(
                    os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
                )
        except Exception as error:
            log.error("Loading fonts died: %s", error)
            font_size = 20
            font = ImageFont.load_default()  # Шрифт по умолчанию
            sub_font = ImageFont.load_default()  # Шрифт по умолчанию

        if title:
            if banner_size == (216, 1184):
                draw.text(position, title, font=font, fill="white")
            elif banner_size == (640, 1160):
                draw.text((50, 50), title, font=font, fill="white")
            elif banner_size == (380, 380):
                draw.text((5, 5), title, font=font, fill="white")
            else:
                draw.text((20, 20), title, font=font, fill="white")

        if subtitle:
            if banner_size == (216, 1184):
                draw.text(
                    (position[0], position[1] + banner_size[0] / 10 + font_size),
                    subtitle,
                    font=sub_font,
                    fill="white",
                )
            elif banner_size == (640, 1160):
                draw.text(
                    (50, 50 + banner_size[0] / 10 + font_size),
                    subtitle,
                    font=sub_font,
                    fill="white",
                )
            elif banner_size == (380, 380):
                draw.text(
                    (5, 5 + banner_size[0] / 10 + font_size),
                    subtitle,
                    font=sub_font,
                    fill="white",
                )
            else:
                draw.text(
                    (20, 20 + font_size * 2),
                    subtitle,
                    font=sub_font,
                    fill="white",
                )

        image.save(f"{os.environ['PICTURES_FOLDER']}/{filename}.png")

    except UnicodeEncodeError:
        # Если возникла ошибка, значит текст содержит символы, не поддерживаемые шрифтом по умолчанию
        print(
            "Ошибка кодировки. Пожалуйста, используйте шрифт, поддерживающий кириллицу."
        )

    return image
