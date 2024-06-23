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
        "exclusive vacation",
        "high-end gadgets",
        "expensive jewelry",
        "fine art",
        "private island",
        "luxury home",
        "personal chef",
        "private concert",
        "exclusive club membership",
        "custom suit",
        "vintage wine",
        "sports car",
        "diamond ring",
        "private cinema",
        "exclusive spa",
        "golf course membership",
    ],
    "c. Масс-ЗП закредитованные (12)": [
        "economy car",
        "smartphone",
        "laptop",
        "budget vacation",
        "home appliance",
        "furniture",
        "bicycle",
        "budget fashion",
        "tablet",
        "camera",
        "fitness tracker",
        "power bank",
        "headphones",
        "gaming console",
        "books",
        "backpack",
        "workout equipment",
        "kitchen gadgets",
        "TV",
        "home decor",
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
        "home decor",
        "books",
        "kitchen gadgets",
        "workout equipment",
        "budget fashion",
        "budget vacation",
        "furniture",
        "home appliance",
    ],
    "d. Масс-ЗП без согласия БКИ (1,3)": [
        "reliable car",
        "safe investment options",
        "insurance plans",
        "retirement savings",
        "mutual funds",
        "bonds",
        "fixed deposits",
        "pension plans",
        "real estate",
        "life insurance",
        "health insurance",
        "gold",
        "stocks",
        "savings account",
        "emergency fund",
        "government bonds",
        "education plans",
        "family car",
        "home renovation",
        "utility vehicle",
    ],
    "h. Бывшие зарплатники (4,9,10,11)": [
        "investment plans",
        "savings accounts",
        "retirement plans",
        "stocks",
        "bonds",
        "real estate",
        "insurance",
        "mutual funds",
        "gold",
        "pension plans",
        "fixed deposits",
        "emergency fund",
        "health insurance",
        "life insurance",
        "family car",
        "home renovation",
        "education plans",
        "travel packages",
        "luxury items",
        "club memberships",
    ],
    "j. Депозиты в оттоке (0,17)": [
        "alternative investment options",
        "gold",
        "real estate",
        "stocks",
        "bonds",
        "mutual funds",
        "pension plans",
        "fixed deposits",
        "insurance",
        "retirement plans",
        "savings accounts",
        "investment plans",
        "luxury items",
        "emergency fund",
        "health insurance",
        "life insurance",
        "travel packages",
        "education plans",
        "family car",
        "home renovation",
    ],
    "b. Текущие заемщики (14)": [
        "new credit products",
        "debt consolidation options",
        "car loan",
        "home loan",
        "personal loan",
        "credit card",
        "education loan",
        "business loan",
        "mortgage",
        "travel loan",
        "emergency loan",
        "line of credit",
        "auto loan",
        "equipment financing",
        "refinancing",
        "microloan",
        "startup loan",
        "bridge loan",
        "payday loan",
        "investment loan",
    ],
    "e. Супер-аффлуент (-1)": [
        "luxury investments",
        "high-end real estate",
        "premium services",
        "private jet",
        "yacht",
        "luxury car",
        "fine art",
        "exclusive vacation",
        "designer watch",
        "diamond jewelry",
        "personal chef",
        "private concert",
        "exclusive club membership",
        "custom suit",
        "vintage wine",
        "sports car",
        "private island",
        "luxury home",
        "private cinema",
        "exclusive spa",
    ],
    "g. ДК/ЗК до 6 моба (20)": [
        "mobile banking options",
        "online financial services",
        "smartphone",
        "tablet",
        "laptop",
        "budget vacation",
        "home appliance",
        "furniture",
        "bicycle",
        "budget fashion",
        "camera",
        "fitness tracker",
        "power bank",
        "headphones",
        "gaming console",
        "books",
        "backpack",
        "workout equipment",
        "kitchen gadgets",
        "TV",
    ],
    "f. Супер-депозиты (8,16)": [
        "high-yield savings accounts",
        "long-term investments",
        "stocks",
        "bonds",
        "mutual funds",
        "gold",
        "real estate",
        "fixed deposits",
        "pension plans",
        "retirement plans",
        "insurance",
        "savings accounts",
        "investment plans",
        "luxury items",
        "emergency fund",
        "health insurance",
        "life insurance",
        "travel packages",
        "education plans",
        "family car",
    ],
    "i. Бывшие заемщики (2,5,19)": [
        "new loan products",
        "personalized financial services",
        "credit card",
        "personal loan",
        "car loan",
        "home loan",
        "education loan",
        "business loan",
        "mortgage",
        "travel loan",
        "emergency loan",
        "line of credit",
        "auto loan",
        "equipment financing",
        "refinancing",
        "microloan",
        "startup loan",
        "bridge loan",
        "payday loan",
        "investment loan",
    ],
}

# Определение фонов
solid_colors = [
    "#4F6AE8",
    "#CBE6FC",
    "#F6C3A8",
    "#6580F7",
    "#DEDDFC",
    "#663546",
    "#F4F6FA",
]
gradient_colors = [
    ("#8A9EF6", "#445DD3"),
    ("#79B8EE", "#3372B5"),
    ("#B2D8FA", "#9F509B"),
    ("#DEEFFD", "#569BDC"),
    ("#8B9443", "#B0E4CA"),
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
def generate_raw_image(cluster, product_description: str | None = None):
    objects = get_random_objects(cluster)
    objects_prompt = ", ".join(objects)
    prompt = f"{objects_prompt}, 3d, cinematic, blue moody lighting, realistic, official, big, solid white background, colourful with blue elements, banking thematics"
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
async def add_text_to_image(image, title: str, subtitle: str, banner_size, filename):
    position = generate_position(banner_size)
    draw = ImageDraw.Draw(image)
    try:
        try:
            font_size = calc_font_size(banner_size)
            print(f"{font_size} " * 100)
            font = ImageFont.truetype(os.environ["TITLE_FONT_PATH"], int(font_size))
            sub_font = ImageFont.truetype(
                os.environ["DESCRIPTION_FONT_PATH"], int(font_size) - 6
            )
        except Exception:
            log.warning("Loading custom font died")
            font_size = 20
            font = ImageFont.load_default()  # Шрифт по умолчанию
            sub_font = ImageFont.load_default()  # Шрифт по умолчанию
        if title:
            draw.text(position, title, font=font, fill="white")
        if subtitle:
            draw.text(
                (position[0], position[1] + font_size),
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


# Функция для создания фона
def create_background(cluster, width, height):
    if cluster == "a. Супер-ЗП (6,15)" or cluster == "e. Супер-аффлуент (-1)":
        color = "#663546"
        return create_solid_background(color, width, height)
    else:
        if random.random() > 0.5:
            color = random.choice(solid_colors)
            return create_solid_background(color, width, height)
        else:
            color1, color2 = random.choice(gradient_colors)
            return create_gradient_background(color1, color2, width, height)


# Основная функция для генерации баннера
def generate_banner(
    cluster: str,
    filename: str,
    banner_size: tuple[int, int],
    product: str | None = None,
) -> None:
    # Генерация нового изображения
    generated_image = generate_raw_image(cluster, product_description=product)

    # Удаление фона из сгенерированного изображения
    generated_image_nobg = remove_background(generated_image)

    # Создание фона
    background = create_background(cluster, banner_size[1], banner_size[0])

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
