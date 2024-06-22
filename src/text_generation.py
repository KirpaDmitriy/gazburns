from asyncio import gather

import torch
# from torch import autocast
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2-7B-Instruct", torch_dtype="auto"  # , device_map="auto"
).to("cuda")

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")

torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_flash_sdp(False)


async def generate_func(message: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to("cuda")

    # with autocast("cuda"):
    generated_ids = model.generate(model_inputs.input_ids, max_new_tokens=512)

    generated_ids = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response


async def generate_product_logo(product_desc: str) -> tuple[str, str]:
    # получаем по списку
    product = "банковский продукт"
    product_desc = product_desc.lower()
    list_product = [
        "потребительский кредит",
        "рефинансирование внутреннего  ПК в Газпромбанке",
        "рефинансирование внешнего  ПК в другом банке",
        "кредитная карта",
        "классический автокредит",
        "кредит под залог авто",
        "ипотека",
        "рефинансирование ипотеки",
        "кредит под залог недвижимости",
        "депозит",
        "накопительный счет",
        "дебетовая карта",
        "премиальная карта",
        "брокерский и инвестиционный счет",
        "инвестиционное страхование жизни",
        "накопительное страхование жизни",
        "страхование жизни",
        "страхование жизни",
        "доверительное управление",
        "обезличенный металлический счет",
        "индивидуальный зарплатный проект",
        "обмен валюты",
    ]
    for elem in list_product:
        if elem in product_desc:
            product = elem
            break

    message_title = f"Придумай короткий и интересный слоган, который будет использован на баннере для рекламы  продукта: {product} в банке"
    message_description = f"Дано описание продукта :{product_desc}. Представь, что ты дизайнер и тебе необходимо сделать рекламу этого продукта. Придумай короткий слоган для рекламы, чтобы передать все важные условия продукта."
    name_banner, new_desc = await gather(
        generate_func(message_title), generate_func(message_description)
    )
    return name_banner, new_desc
