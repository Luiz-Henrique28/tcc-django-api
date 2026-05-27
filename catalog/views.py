from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductCreateUpdateSerializer,
)


# =============================================================================
# Autenticação
# =============================================================================

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Registrar novo usuário e retornar token."""
    name = request.data.get('name', '')
    email = request.data.get('email', '')
    password = request.data.get('password', '')

    if not email or not password:
        return Response(
            {'error': 'Email e senha são obrigatórios.'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email já está em uso.'},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=name,
    )
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'data': {
            'user': {
                'id': user.id,
                'name': user.first_name,
                'email': user.email,
            },
            'token': token.key,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """Autenticar usuário e retornar token."""
    email = request.data.get('email', '')
    password = request.data.get('password', '')

    user = authenticate(username=email, password=password)

    if user is None:
        return Response(
            {'error': 'Credenciais inválidas.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'data': {
            'user': {
                'id': user.id,
                'name': user.first_name,
                'email': user.email,
            },
            'token': token.key,
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """Invalidar token do usuário autenticado."""
    request.user.auth_token.delete()
    return Response({'message': 'Logout realizado com sucesso.'})


# =============================================================================
# Categorias
# =============================================================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Categorias.
    GET: público | POST/PUT/DELETE: autenticado.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'data': serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Categoria removida com sucesso.'},
            status=status.HTTP_200_OK,
        )


# =============================================================================
# Produtos
# =============================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Produtos.
    GET: público (com JOIN na categoria) | POST/PUT/DELETE: autenticado.
    Filtro por categoria via query param: ?category=<id>
    """
    queryset = Product.objects.select_related('categoria').all().order_by('-id')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductListSerializer
        return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            queryset = queryset.filter(categoria_id=category_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        # Return with nested category
        output = ProductListSerializer(
            Product.objects.select_related('categoria').get(pk=product.pk)
        )
        return Response({'data': output.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        output = ProductListSerializer(
            Product.objects.select_related('categoria').get(pk=product.pk)
        )
        return Response({'data': output.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductListSerializer(instance)
        return Response({'data': serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(queryset, many=True)
        return Response({'data': serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Produto removido com sucesso.'},
            status=status.HTTP_200_OK,
        )
