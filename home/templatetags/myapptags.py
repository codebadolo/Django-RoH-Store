from django import template
from django.db.models import Sum
from django.urls import reverse
from django.utils.text import slugify  # Add this import
from mysite import settings
from order.models import ShopCart
from product.models import Category
from django import template
from django.db.models import Sum
from django.urls import reverse
from product.models import Category

register = template.Library()

@register.simple_tag
def categorylist():
    return Category.objects.all()

@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count



@register.simple_tag
def categoryTree(id=0, menu=''):
    # Fetch main categories or subcategories based on the id
    if id <= 0:
        query = Category.objects.filter(parent_id__isnull=True).order_by("id")
    else:
        query = Category.objects.filter(parent_id=id)

    querycount = query.count()

    if querycount > 0:
        for rs in query:
            subcount = Category.objects.filter(parent_id=rs.id).count()
            if subcount > 0:
                menu += '\t<li class="dropdown side-dropdown">\n'
                menu += '\t<a class ="dropdown-toggle" data-toggle="dropdown" aria-expanded="true">' + rs.title + '<i class="fa fa-angle-right"></i></a>\n'
                menu += '\t\t<div class="custom-menu">\n'
                menu += '\t\t\t<ul class="list-links">\n'
                menu += categoryTree(int(rs.id), '')
                menu += '\t\t\t</ul>\n'
                menu += '\t\t</div>\n'
                menu += "\t</li>\n\n"
            else:
                menu += '\t\t\t\t<li><a href="' + reverse('category_products', args=(rs.id, rs.slug)) + '">' + rs.title + '</a></li>\n'
    return menu
