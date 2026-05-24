from django.db import models


class Category(models.Model):
    """Categoria de produto."""
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return self.nome


class Product(models.Model):
    """Produto do catálogo."""
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    categoria = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='produtos',
        db_column='categoria_id',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['id']

    def __str__(self):
        return self.nome
