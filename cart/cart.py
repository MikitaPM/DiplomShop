from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    """
    Добавление продукта в корзину и изменение его кол-ва
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save

    def save(self):
        #Обновление сессии
        self.session[settings.CART_SESSION_ID]= self.cart
        #Отметка сеанса как изменненный
        self.session.modifiend = True

    def remove(self, product):
        """
        Удаление товаров из корзины
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов из корзины и получение продуктов из базы
        """
        product_ids = self.cart.keys()
        #Получение обьектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Общая сумма
        """

        return sum(Decimal(item['price'])* item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modifiend = True
