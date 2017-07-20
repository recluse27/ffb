import time

PRODUCT_LIST = lambda items: {
    "type": "template",
    "payload": {
        "template_type": "list",
        "elements": [
            {
                "title": item['title'],
                "subtitle": str(item['price']) + ' UAH',
                "image_url": item['image_url'],
                "default_action": {
                    "type": "postback",
                    "payload": {"type": "get_receipt",
                                "item_name": item['title']}
                },
                "buttons": [
                    {
                        "title": "Buy",
                        "type": "postback",
                        "payload": {"type": "get_receipt",
                                    "item_name": item['title']}
                    }
                ]
            } for item in items]
    }
}
RECEIPT_TEMPLATE = lambda item: {
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
        "address": {
            "street_1": "1 Hacker Way",
            "city": "Menlo Park",
            "postal_code": "94025",
            "state": "CA",
            "country": "US"
        },
        "summary": {
            "total_cost": item['price']
        }
    }
}

RECEIPT_ELEMENT_TEMPLATE = lambda item: {
    "title": item['title'],
    "quantity": 1,
    "price": item['price'],
    "currency": "UAH",
    "image_url": item['image_url']
}

QUICK_REPLIES = {
    "content_type": "text",
    "title": "Menu",
    "payload": {"type": "get_products"}
}

PRODUCTS = [{"title": "Classic Fries",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/desktop/t-mcdonalds-Fries-Small-Medium.png?$THUMBNAIL_MEDIUM$",
             "price": 15},
            {"title": "Big Mac",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/desktop/t-mcdonalds-Big-Mac.png?$THUMBNAIL_MEDIUM$",
             "price": 30},
            {"title": "Coca-Cola",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/desktop/t-mcdonalds-Coca-Cola-Classic-Small.png?$THUMBNAIL_MEDIUM$",
             "price": 10},
            {"title": "Double Royal Cheesburger",
             "image_url": "https://www.mcdonalds.com/is/image/content/dam/usa/nutrition/items/regular/desktop/t-mcdonalds-Double-Quarter-Pounder-with-Cheese.png?$THUMBNAIL_MEDIUM$",
             "price": 20}]
