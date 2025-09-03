class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = 1
        else:
            self.cart[product_id] += 1
        self.save()

    def decrease(self, product_id):
        product_id = str(product_id)

        if self.cart[product_id] - 1 == 0:
            self.remove(product_id)
        else:
            self.cart[product_id] -= 1
        self.save()



    def save(self):
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()


    def items(self):
        from .models import Product
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart_items = []
        for product in products:
            quantity = self.cart[str(product.id)]
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': quantity * product.price
            })
        return cart_items

    def total_price(self):
        return sum(item['total_price'] for item in self.items())
