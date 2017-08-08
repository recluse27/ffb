import time


def CATEGORY_LIST():
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "image_url": item['image_url'],
                    "buttons": [
                        {
                            "title": item['title'],
                            "type": "postback",
                            "payload": "get_category/" + item['title']
                        }
                    ]
                } for item in PRODUCT_CATEGORIES]
        }
    }


def GET_BASKET(items):
    return {
        "type": "template",
        "payload": {
            "template_type": "list",
            "elements": [
                {
                    "title": item['title'],
                    "subtitle": str(item['price']) + ' UAH',
                    "image_url": item['image_url'],
                } for item in items]
        }
    }


def PRODUCT_LIST(items, category=None):
    filtered_items = list(filter(lambda product: product['category'] == category, items))

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
                            "title": "Add",
                            "type": "postback",
                            "payload": "add_product/" + str(PRODUCTS.index(item))
                        }
                    ]
                } for item in filtered_items]
        }
    }


def RECEIPT_TEMPLATE(items):
    return {
        "type": "template",
        "payload": {
            "template_type": "receipt",
            "recipient_name": "User",
            "order_number": round(time.time()),
            "currency": "UAH",
            "payment_method": "Credit Card",
            "order_url": "",
            "timestamp": round(time.time()),
            "elements": [
                RECEIPT_ELEMENT_TEMPLATE(item=item)
                for item in items
            ],
            "summary": {
                "total_cost": sum(item['price'] for item in items)
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


def QUICK_REPLIES_GET_MORE(category, _from, _to):
    return {
        "content_type": "text",
        "title": "Get more",
        "payload": "get_more/{category}/{_from}-{_to}".format(category=category,
                                                              _from=_from,
                                                              _to=_to)
    }


def QUICK_REPLIES_REPEAT(category):
    return {
        "content_type": "text",
        "title": "Repeat",
        "payload": "get_more/{category}/0-4".format(category=category)
    }


def QUICK_REPLIES_CATEGORIES():
    return {
        "content_type": "text",
        "title": "Categories",
        "payload": "get_categories"
    }


def QUICK_REPLIES_GET_BASKET():
    return {
        "content_type": "text",
        "title": "Get basket",
        "payload": "get_basket"
    }


def QUICK_REPLIES_CHECKOUT():
    return {
        "content_type": "text",
        "title": "Checkout",
        "payload": "checkout"
    }


PRODUCTS = [{"title": "Classic Fries",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Fries-Small-Medium.png?$THUMBNAIL_MEDIUM$",
             "category": "Other",
             "price": 15},
            {"title": "Big Mac",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Big-Mac.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 30},
            {"title": "Coca-Cola",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Coca-Cola-Classic-Small.png?$THUMBNAIL_MEDIUM$",
             "category": "Drinks",
             "price": 10},
            {"title": "Double Royal Cheesburger",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Double-Quarter-Pounder-with-Cheese.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 20},
            {"title": "Maple Bacon Dijon Crispy Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-maplebacondijon-crispychicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 20},
            {"title": "Sweet BBQ Bacon Crispy Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-sweetbbqbacon-crispychicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 19},
            {"title": "Picoguac Grilled Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-picoguac-grilledchicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 22},
            {"title": "Chicken McNuggets",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Chicken-McNuggets-4pc.png?$THUMBNAIL_MEDIUM$",
             "category": "Other",
             "price": 16},
            {"title": "Artisan Grilled Chicken Sandwich",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Artisan-Grilled-Chicken-Sandwich.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 25},
            {"title": "Premium Bacon Ranch Salad with Grilled Chicken",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Premium-Bacon-Ranch-Salad-with-Grilled-Chicken.png?$THUMBNAIL_MEDIUM$",
             "category": "Salads",
             "price": 17},
            {"title": "Premium Bacon Ranch Salad with Buttermilk Crispy Chicken",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Premium-Bacon-Ranch-Salad-with-Buttermilk-Crispy-Chicken.png?$THUMBNAIL_MEDIUM$",
             "category": "Salads",
             "price": 17},
            {"title": "Premium Southwest Salad with Grilled Chicken",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Premium-Southwest-Salad-with-Grilled-Chicken.png?$THUMBNAIL_MEDIUM$",
             "category": "Salads",
             "price": 17},
            {"title": "Chocolate McCafe Shake",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Chocolate-McCafe-Shake-Medium.png?$THUMBNAIL_MEDIUM$",
             "category": "Drinks",
             "price": 12},
            {"title": "Strawberry McCafe Shake",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Strawberry-McCafe-Shake-Medium.png?$THUMBNAIL_MEDIUM$",
             "category": "Drinks",
             "price": 12},
            {"title": "Vanilla McCafe Shake",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-Vanilla-McCafe-Shake-Medium.png?$THUMBNAIL_MEDIUM$",
             "category": "Drinks",
             "price": 12},
            {"title": "Sweet BBQ Bacon Grilled Chicken Artisan",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                          "desktop/t-mcdonalds-sweetbbqbacon-grilledchicken-artisan.png?$THUMBNAIL_MEDIUM$",
             "category": "Burgers",
             "price": 22}]

PRODUCT_CATEGORIES = [
    {'title': 'Drinks', 'image_url': "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                                     "desktop/t-mcdonalds-Coca-Cola-Classic-Small.png?$THUMBNAIL_MEDIUM$"},
    {'title': 'Burgers', 'image_url': "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                                      "desktop/t-mcdonalds-Double-Quarter-Pounder-with-Cheese.png?$THUMBNAIL_MEDIUM$"},
    {'title': 'Salads', 'image_url': "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                                     "desktop/t-mcdonalds-Premium-Southwest-Salad-with-Grilled-Chicken.png?$THUMBNAIL_MEDIUM$"},
    {'title': 'Other', 'image_url': "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/"
                                    "desktop/t-mcdonalds-Fries-Small-Medium.png?$THUMBNAIL_MEDIUM$"}]
