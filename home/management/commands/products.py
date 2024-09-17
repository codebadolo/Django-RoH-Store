import os
import random
from django.core.management.base import BaseCommand
from product.models import Category, Product
from django.utils.text import slugify
from django.db.utils import IntegrityError
from django.conf import settings

# Define the available images from the uploads/images folder
PRODUCT_IMAGES = [
    'uploads/images/asus1_1mbaqhk.jpg', 'uploads/images/desktop2.jfif', 'uploads/images/hp-dektop1.png',
    'uploads/images/office-cahir-black.jpg', 'uploads/images/T-Shirts_black_JCkIFIb.jpg', 
    'uploads/images/T-Shirts-gray.jpg', 'uploads/images/asus_laptop.jpg', 
    'uploads/images/desktop.jpg', 'uploads/images/hp_laptop_d69cahd.jpg', 
    'uploads/images/office-cahir-gray.jpg', 'uploads/images/T-Shirts_black.jpg', 
    'uploads/images/desktop1.jfif', 'uploads/images/elecktronics.png', 
    'uploads/images/office-cahir-black_hsdlFW7.jpg', 'uploads/images/T-Shirts_Electric-blue.jpg', 
    'uploads/images/T-Shirts_Electric-blue_lfBupHo.jpg', 'uploads/images/hp_laptop.jpg', 
    'uploads/images/office-cahir-red.jpg', 'uploads/images/T-Shirts-black_fyBYq6e.jpg',
    'uploads/images/T-Shirts-white.jpg'
]

# Define some example product titles and descriptions
PRODUCT_TITLES = [
    'Smartphone X Pro', 'Laptop Z Series', 'Smart Watch A3', 
    'Wireless Headphones', '4K Ultra TV', 'Bluetooth Speaker',
    'Gaming Console', 'Electric Scooter', 'Camera Pro Max', 'Running Shoes',
    'T-shirt Design', 'Fashion Handbag', 'Dress Model 2024', 'Leather Wallet',
    'Sports Sneakers', 'Headphones Wireless Pro', 'Bluetooth Earbuds', 'Action Camera', 
    'Drone Camera', 'Smart Glasses'
]

PRODUCT_DESCRIPTIONS = [
    'High performance and sleek design.',
    'The best in class for everyday use.',
    'Advanced technology and cutting-edge features.',
    'Durable, efficient, and value for money.',
    'State-of-the-art specifications for modern needs.',
    'Comfortable and stylish clothing for all occasions.',
    'Modern fashion with a perfect fit.'
]

class Command(BaseCommand):
    help = 'Create random products for random categories using available images'

    def handle(self, *args, **kwargs):
        # Fetch all categories
        categories = Category.objects.all()

        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create categories first.'))
            return

        for _ in range(20):  # Change 20 to however many random products you want to create
            # Randomly select a category
            category = random.choice(categories)
            
            # Randomly select a product title, description, and image
            title = random.choice(PRODUCT_TITLES)
            description = random.choice(PRODUCT_DESCRIPTIONS)
            image_name = random.choice(PRODUCT_IMAGES)
            image_path = os.path.join(settings.BASE_DIR, image_name)  # Adjust to actual path

            if not os.path.exists(image_path):
                self.stdout.write(self.style.ERROR(f"Image file does not exist: {image_path}"))
                continue

            # Generate a unique slug
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            # Create the product
            try:
                product = Product.objects.create(
                    category=category,
                    title=title,
                    keywords='electronics, gadget, fashion',
                    description=description,
                    image=image_name,
                    price=random.uniform(50, 1000),  # Random price between $50 and $1000
                    amount=random.randint(10, 100),  # Random stock between 10 and 100
                    minamount=5,
                    variant='None',
                    slug=slug,
                    status='True',
                    detail='This is a random product detail.'
                )
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.title} in category {category.title}'))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(f"Failed to create product: {title}. Slug already exists."))
