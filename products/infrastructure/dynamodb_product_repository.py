from typing import Dict, Any
from datetime import date

import boto3

from products.domain.product import Product
from products.domain.product_repository import ProductRepository
from shared.infrastructure.env import env


class DynamoDBProductRepository(ProductRepository):
    def __init__(self):
        dynamodb = boto3.resource("dynamodb")
        self.__table = dynamodb.Table(env.DD_PRODUCT_TABLE_NAME)

    def save(self, product: Product) -> None:
        self.__table.put_item(Item=self.__to_dd_product(product))
    
    def get_all(self) -> list[Product]:
        response = self.__table.scan()
        return [self.__to_domain(dd_product) for dd_product in response["Items"]]
    
    def get_by_id(self, id: str) -> Product | None:
        response = self.__table.get_item(Key={"id": id})
        product = response.get("Item")
        if not product:
            return None
        return self.__to_domain(product)
    
    def update(self, product: Product) -> None:
        self.__table.update_item(
            Key={"id": product.id},
            UpdateExpression="set #name = :name, #stock = :stock, #arriving_date = :arriving_date",
            ExpressionAttributeNames={
                "#name": "name",
                "#stock": "stock",
                "#arriving_date": "arriving_date",
            },
            ExpressionAttributeValues={
                ":name": product.name,
                ":stock": product.stock,
                ":arriving_date": product.arriving_date.isoformat() if product.arriving_date else None,
            },
        )

    def delete(self, id: str) -> None:
        self.__table.delete_item(Key={"id": id})

    def get_by_name(self, name: str) -> Product | None:
        response = self.__table.get_item(Key={"name": name})
        product = response.get("Item")
        if not product:
            return None
        return self.__to_domain(product)

    def __to_dd_product(self, product: Product) -> Dict[str, Any]:
        return {
            "id": product.id,
            "name": product.name,
            "stock": product.stock,
            "arriving_date": product.arriving_date.isoformat() if product.arriving_date else None,
        }
    
    def __to_domain(self, dd_product: Dict[str, Any]) -> Product:
        date_field = date.fromisoformat(dd_product["arriving_date"]) if dd_product["arriving_date"] else None
        
        return Product(
            id=dd_product["id"],
            name=dd_product["name"],
            stock=dd_product["stock"],
            arriving_date=date_field,
        )
