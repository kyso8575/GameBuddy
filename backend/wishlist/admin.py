from django.contrib import admin
from .models import Wishlist

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'game', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'game__name')
    raw_id_fields = ('user', 'game')
    date_hierarchy = 'created_at'
