from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'preco', 'estoque', 'categoria', 'criado_em']
    list_filter = ['categoria']
    search_fields = ['nome']
