from dataclasses import dataclass


@dataclass
class Product:
    name: str
    thumbnail_url: str
    price: int
    info_url: str
