from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Account)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(ProductReview)
admin.site.register(StockInfo)
admin.site.register(UserInfo)

admin.site.site_title = '桃饱商城管理'
admin.site.site_header = '桃饱商城管理'
