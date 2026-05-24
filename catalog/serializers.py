from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para Categoria."""

    class Meta:
        model = Category
        fields = ['id', 'nome', 'descricao']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de Produtos (com categoria aninhada)."""
    categoria = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'categoria', 'criado_em', 'atualizado_em']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para criação/atualização de Produtos (recebe categoria_id)."""
    categoria_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'nome', 'descricao', 'preco', 'estoque', 'categoria_id', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate_categoria_id(self, value):
        if not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError('Categoria não encontrada.')
        return value

    def create(self, validated_data):
        categoria_id = validated_data.pop('categoria_id')
        validated_data['categoria_id'] = categoria_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        categoria_id = validated_data.pop('categoria_id', None)
        if categoria_id is not None:
            validated_data['categoria_id'] = categoria_id
        return super().update(instance, validated_data)
