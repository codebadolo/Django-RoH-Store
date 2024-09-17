from django.core.management.base import BaseCommand
from product.models import Category
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create detailed product categories and subcategories for the e-commerce platform'

    def handle(self, *args, **kwargs):
        def create_category(title, parent=None):
            # Generate a slug from the title
            slug = slugify(title)
            # Check if a category with this slug already exists
            category, created = Category.objects.get_or_create(title=title, parent=parent, slug=slug, defaults={
                'keywords': f'{title}, {parent.title if parent else ""}',
                'description': f'Category for {title}',
                'status': 'True',
            })
            return category

        # Main Category: Electronics
        electronics = create_category("Electronics")

        # Subcategories for Electronics
        phones = create_category("Phones", parent=electronics)
        create_category("Smartphones", parent=phones)
        create_category("Feature Phones", parent=phones)

        accessories = create_category("Accessories", parent=phones)
        create_category("Phone Cases", parent=accessories)
        create_category("Chargers", parent=accessories)

        # Adding Laptops and Subcategories
        laptops = create_category("Laptops", parent=electronics)
        create_category("Gaming Laptops", parent=laptops)
        create_category("Ultrabooks", parent=laptops)

        # Adding TVs and Subcategories
        tvs = create_category("Televisions", parent=electronics)
        create_category("Smart TVs", parent=tvs)

        # Adding Cameras and Subcategories
        cameras = create_category("Cameras", parent=electronics)
        create_category("DSLRs", parent=cameras)

        # Main Category: Clothing
        clothing = create_category("Clothing")

        # Subcategories for Men
        men = create_category("Men", parent=clothing)
        create_category("T-Shirts", parent=men)
        create_category("Jackets", parent=men)

        # Subcategories for Women
        women = create_category("Women", parent=clothing)
        create_category("Dresses", parent=women)
        create_category("Footwear", parent=women)

        self.stdout.write(self.style.SUCCESS('Detailed product categories and subcategories created successfully!'))
