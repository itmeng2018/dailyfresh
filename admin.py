from django.contrib import admin
from django.core.cache import cache
from goods.models import GoodsType, IndexPromotionBanner, IndexGoodsBanner, IndexTypeGoodsBanner, Goods, GoodsSKU, \
    GoodsImage


admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsType)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexPromotionBanner)
admin.site.register(IndexTypeGoodsBanner)