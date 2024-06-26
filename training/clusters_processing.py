import json
import os
import re

import numpy as np
import pandas as pd
import torch
from lavis.models import load_model_and_preprocess
from PIL import Image

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-7B-Instruct", torch_dtype="auto", device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")


def generate_func(message):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)
    generated_ids = [
        output_ids[len(input_ids) :]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


# получаем описание изображения на английском
def get_img_description(name_img):
    raw_image = Image.open(name_img).convert("RGB")
    model, vis_processors, _ = load_model_and_preprocess(
        name="blip_caption", model_type="base_coco", is_eval=True, device=device
    )
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    description = model.generate({"image": image})
    return description[0]


# получаем кейсы, где может быть использован баннер
def get_example_of_use(desc):
    message = f"Есть баннер, которые используются в банке для рекламы различных продуктов и предложение. По его описанию {desc} распиши подробно примеры в формате списка, где он может быть использован"

    return generate_func(message)


# получаем теги по кейсам
def get_tags_from_example(example_uses):
    message = f"Дан список {example_uses}, переделай его в теги ключевых слов и выведи списком с разделением через запятую"
    reply = generate_func(message)
    list_reply = reply.split(", ")
    return list_reply


image_desc_matching = dict()
image_example_matching = dict()
image_tag_matching = dict()
for file_name in banner_list_name:
    img_path = dir_path + "/" + file_name
    desc = get_img_description(img_path)
    image_desc_matching[file_name] = desc
    example = get_example_of_use(desc)
    image_example_matching[file_name] = example
    tags = get_tags_from_example(example)
    new_list = []
    for elem in tags:
        elem = re.sub(r"[^\w\s]", "", elem)
        elem = (
            elem.strip().replace("Список ключевых слов:", "").replace("Мой ответ:", "")
        )
        new_list.append(elem)
    image_tag_matching[file_name] = tags
