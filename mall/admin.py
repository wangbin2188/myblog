from django.contrib import admin
from mall.models import Category,Product,ProductItem,RegisterUser,Orders,ShoppingCart,ProductComment

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductItem)
admin.site.register(RegisterUser)
admin.site.register(Orders)
admin.site.register(ShoppingCart)
admin.site.register(ProductComment)
