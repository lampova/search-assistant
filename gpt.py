import json


from conf import client
import re

def extract_json_from_response(response):
    # Находит блок внутри ``````
    match = re.search(r"``````", response, re.DOTALL)
    if match:
        json_text = match.group(1)
    else:
        # Фолбэк — находит первый [ ... ]
        match = re.search(r"(\[.*?\])", response, re.DOTALL)
        json_text = match.group(1) if match else ''
    return json_text


def smart_product_search(product_list: list, search_query: str) -> list:
    print("привет")
    prompt = "Ты — помощник покупателя, который понимает опечатки и ищет максимально выгодные товары.\n"
    prompt += f"Пользователь ищет: {search_query}\n"
    prompt += "Вот список товаров:\n"

    for idx, item in enumerate(product_list, 1):
        prompt += (f"{idx}) Название: {item['product']['name']}\n"
                   f"   Компания: {item['company']['name']}\n"
                   f"   Цена: {item['product']['price']} руб.\n"
                   f"   Расстояние: {item['distance']:.2f} км\n")

    prompt += ("\n Отсортируй подходящие товары от самого выгодного и близкого до самого не выгодного. Учитывай опечатки, похожие слова (напр. солоко = молоко), также покажи подходящие по смыслу или из той же категории(например молочные продукты) с низким приоритетом.\n"
               "Верни результат в формате JSON, как список объектов с полями name, company, price, distance.\n")

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile"
    )
    response = chat_completion.choices[0].message.content
    print("RAW LLM:", response)

    json_text = extract_json_from_response(response)
    try:
        top_products = json.loads(json_text)
    except Exception as e:
        print("JSON parse error:", e)
        top_products = []
    return top_products