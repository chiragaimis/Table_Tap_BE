from django.core.management.base import BaseCommand
from api.Product.model import Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed categories and products for Smart E-Commerce Platform'

    def handle(self, *args, **kwargs):
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Fashion', 'description': 'Clothing and accessories'},
            {'name': 'Groceries', 'description': 'Food and daily essentials'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {cat_data['name']}"))

        # Create products
        products_data = [
            {'name': 'Smartphone X1', 'category': 'Electronics', 'price': '599.99', 'stock': 50, 'description': 'Latest smartphone with advanced features'},
            {'name': 'Laptop Pro 15', 'category': 'Electronics', 'price': '1299.99', 'stock': 30, 'description': 'High-performance laptop for professionals'},
            {'name': 'Wireless Earbuds', 'category': 'Electronics', 'price': '89.99', 'stock': 100, 'description': 'Premium wireless earbuds with noise cancellation'},
            {'name': 'Smart Watch', 'category': 'Electronics', 'price': '249.99', 'stock': 75, 'description': 'Fitness tracking smartwatch'},
            {'name': 'Tablet 10 inch', 'category': 'Electronics', 'price': '399.99', 'stock': 40, 'description': 'Portable tablet for work and entertainment'},
            
            {'name': 'Men T-Shirt', 'category': 'Fashion', 'price': '19.99', 'stock': 200, 'description': 'Comfortable cotton t-shirt'},
            {'name': 'Women Dress', 'category': 'Fashion', 'price': '49.99', 'stock': 150, 'description': 'Elegant summer dress'},
            {'name': 'Jeans', 'category': 'Fashion', 'price': '39.99', 'stock': 180, 'description': 'Classic denim jeans'},
            {'name': 'Sneakers', 'category': 'Fashion', 'price': '79.99', 'stock': 120, 'description': 'Comfortable sports sneakers'},
            {'name': 'Backpack', 'category': 'Fashion', 'price': '34.99', 'stock': 90, 'description': 'Durable travel backpack'},
            
            {'name': 'Organic Apples', 'category': 'Groceries', 'price': '4.99', 'stock': 500, 'description': 'Fresh organic apples'},
            {'name': 'Whole Wheat Bread', 'category': 'Groceries', 'price': '2.99', 'stock': 300, 'description': 'Healthy whole wheat bread'},
            {'name': 'Milk 1L', 'category': 'Groceries', 'price': '3.49', 'stock': 400, 'description': 'Fresh dairy milk'},
            {'name': 'Eggs 12 pack', 'category': 'Groceries', 'price': '5.99', 'stock': 250, 'description': 'Farm fresh eggs'},
            {'name': 'Rice 5kg', 'category': 'Groceries', 'price': '12.99', 'stock': 150, 'description': 'Premium basmati rice'},
        ]

        for prod_data in products_data:
            if not Product.objects.filter(name=prod_data['name']).exists():
                Product.objects.create(
                    name=prod_data['name'],
                    category=categories[prod_data['category']],
                    price=Decimal(prod_data['price']),
                    stock_quantity=prod_data['stock'],
                    description=prod_data['description'],
                    image=f'https://via.placeholder.com/400x400?text={prod_data["name"].replace(" ", "+")}',
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f"Created product: {prod_data['name']}"))

        self.stdout.write(self.style.SUCCESS('Products seeded successfully'))
