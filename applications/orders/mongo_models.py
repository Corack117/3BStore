from mongoengine import Document, StringField, FloatField, IntField, ListField, EmbeddedDocumentField, DateTimeField, EmbeddedDocument
from datetime import datetime

class ProductMongo(EmbeddedDocument):
    product_id = StringField(required=True)
    name = StringField(required=True)
    unit_price = FloatField(required=True)
    quantity = IntField(required=True)
    subtotal = FloatField(required=True)

class ReturnMongo(EmbeddedDocument):
    product_id = StringField(required=True)
    quantity = IntField(required=True)
    return_date = DateTimeField(default=datetime.now)
    refunded_amount = FloatField(required=True)


class PurchaseMongo(Document):
    purchase_id = StringField(required=True)
    user_id = StringField(required=True)
    products = ListField(EmbeddedDocumentField(ProductMongo))
    total = FloatField(required=True)
    date = DateTimeField(default=datetime.now)
    returns = ListField(EmbeddedDocumentField(ReturnMongo))

    meta = {
        'collection': 'tickets'
    }