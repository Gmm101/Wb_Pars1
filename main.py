import requests
import json
from fake_useragent import UserAgent

ua = UserAgent()


def get_seller_id(url):
    headers = {
    "User-Agent": ua.random,
    }
    id_start = url.find("/catalog/") + len("/catalog/")
    id_end = url.find("/detail.aspx")
    product_id = url[id_start:id_end]
    ur2 = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=27&nm={product_id}"
    response = requests.get(ur2, headers=headers)
    seller_id = response.json()["data"]["products"][0]["supplierId"]
    return seller_id


def get_product_info(seller_id):
    headers = {
        "User-Agent": ua.random,
    }
    data = []
    page = 1
    while True:
        url = f"https://catalog.wb.ru/sellers/catalog?TestGroup=no_test&TestID=no_test&appType=1&curr=rub&dest=-1257786&page={page}&sort=popular&spp=27&supplier={seller_id}"
        response = requests.get(url, headers=headers)
        items = response.json()["data"]["products"]
        for i in items:
            name = i.get("name")
            price = i.get("salePriceU")
            rating = i.get("rating")
            id_card = i.get("id")

            data.append(
                {
                    "name": name,
                    "price": price,
                    "rait": rating,
                    "id card": id_card,
                    "Id seller": seller_id,
                    "url": f"https://www.wildberries.ru/catalog/{id_card}/detail.aspx"
                }
            )

        if len(response.json()["data"]["products"]) < 99:
            break
        page += 1
    with open("result.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
