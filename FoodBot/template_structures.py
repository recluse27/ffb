import time


def PRODUCT_LIST(items):
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": "Buy",
                            "type": "postback",
                            "payload": "get_product/" + str(PRODUCTS.index(item))
                        }
                    ]
                } for item in items]
        }
    }


def RECEIPT_TEMPLATE(item):
    return {
        "type": "template",
        "payload": {
            "template_type": "receipt",
            "recipient_name": "Stephane Crozatier",
            "order_number": round(time.time()),
            "currency": "UAH",
            "payment_method": "Credit Card",
            "order_url": "",
            "timestamp": round(time.time()),
            "elements": [
                RECEIPT_ELEMENT_TEMPLATE(item=item)
            ],
            "summary": {
                "total_cost": item['price']
            }
        }
    }


def RECEIPT_ELEMENT_TEMPLATE(item):
    return {
        "title": item['title'],
        "quantity": 1,
        "price": item['price'],
        "currency": "UAH",
        "image_url": item['image_url']
    }


def QUICK_REPLIES_MENU():
    return {
        "content_type": "text",
        "title": "Menu",
        "payload": "get_all_products"
    }


def QUICK_REPLIES_GET_MORE(_from, _to):
    return {
        "content_type": "text",
        "title": "Get more",
        "payload": "get_more/{_from}-{_to}".format(_from=_from,
                                                   _to=_to)
    }

def QUICK_REPLIES_REPEAT():
    return {
        "content_type": "text",
        "title": "Repeat",
        "payload": "get_more/0-4"
    }


PRODUCTS = [{"title": "Classic Fries",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Fries-Small-Medium.png?$THUMBNAIL_MEDIUM$",
             "price": 15},
            {"title": "Big Mac",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Big-Mac.png?$THUMBNAIL_MEDIUM$",
             "price": 30},
            {"title": "Coca-Cola",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Coca-Cola-Classic-Small.png?$THUMBNAIL_MEDIUM$",
             "price": 10},
            {"title": "Double Royal Cheesburger",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Double-Quarter-Pounder-with-Cheese.png?$THUMBNAIL_MEDIUM$",
             "price": 20},
            {"title": "Maple Bacon Dijon Crispy Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-maplebacondijon-crispychicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "price": 20},
            {"title": "Sweet BBQ Bacon Crispy Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-sweetbbqbacon-crispychicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "price": 19},
            {"title": "Picoguac Grilled Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-picoguac-grilledchicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "price": 22},
            {"title": "Chicken McNuggets",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Chicken-McNuggets-4pc.png?$THUMBNAIL_MEDIUM$",
             "price": 16},
            {"title": "Artisan Grilled Chicken Sandwich",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Artisan-Grilled-Chicken-Sandwich.png?$THUMBNAIL_MEDIUM$",
             "price": 25},
            {"title": "Premium Bacon Ranch Salad with Grilled Chicken",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Premium-Bacon-Ranch-Salad-with-Grilled-Chicken.png?$THUMBNAIL_MEDIUM$",
             "price": 17},
            {"title": "Premium Bacon Ranch Salad with Buttermilk Crispy Chicken",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Premium-Bacon-Ranch-Salad-with-Buttermilk-Crispy-Chicken.png?$THUMBNAIL_MEDIUM$",
             "price": 17},
            {"title": "Premium Southwest Salad with Grilled Chicken",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Premium-Southwest-Salad-with-Grilled-Chicken.png?$THUMBNAIL_MEDIUM$",
             "price": 17},
            {"title": "Chocolate McCafe Shake",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Chocolate-McCafe-Shake-Medium.png?$THUMBNAIL_MEDIUM$",
             "price": 12},
            {"title": "Strawberry McCafe Shake",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Strawberry-McCafe-Shake-Medium.png?$THUMBNAIL_MEDIUM$",
             "price": 12},
            {"title": "Vanilla McCafe Shake",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Vanilla-McCafe-Shake-Medium.png?$THUMBNAIL_MEDIUM$",
             "price": 12},
            {"title": "Sweet BBQ Bacon Grilled Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-sweetbbqbacon-grilledchicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "price": 22}]
