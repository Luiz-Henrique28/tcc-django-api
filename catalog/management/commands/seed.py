"""
Seed command — popula o banco com 20 categorias e 1000 produtos.
Usa random seed fixo para reprodutibilidade (mesmo dados em ambos os frameworks).
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


# Seed fixo para reprodutibilidade
RANDOM_SEED = 42

CATEGORIES = [
    ('Eletrônicos', 'Dispositivos eletrônicos e gadgets'),
    ('Livros', 'Livros físicos e digitais'),
    ('Roupas', 'Vestuário masculino e feminino'),
    ('Calçados', 'Sapatos, tênis e sandálias'),
    ('Esportes', 'Artigos esportivos e fitness'),
    ('Casa e Jardim', 'Itens para casa e decoração'),
    ('Automotivo', 'Peças e acessórios automotivos'),
    ('Brinquedos', 'Brinquedos e jogos infantis'),
    ('Saúde', 'Produtos de saúde e bem-estar'),
    ('Beleza', 'Cosméticos e cuidados pessoais'),
    ('Alimentos', 'Alimentos e bebidas'),
    ('Ferramentas', 'Ferramentas manuais e elétricas'),
    ('Papelaria', 'Material de escritório e escolar'),
    ('Pet Shop', 'Produtos para animais de estimação'),
    ('Informática', 'Computadores e periféricos'),
    ('Games', 'Jogos e consoles de videogame'),
    ('Música', 'Instrumentos musicais e acessórios'),
    ('Móveis', 'Móveis para casa e escritório'),
    ('Bebês', 'Produtos para bebês e crianças'),
    ('Camping', 'Equipamentos para camping e aventura'),
]

PRODUCT_ADJECTIVES = [
    'Premium', 'Ultra', 'Pro', 'Max', 'Lite', 'Plus', 'Super', 'Mega',
    'Mini', 'Classic', 'Digital', 'Smart', 'Power', 'Elite', 'Master',
]

PRODUCT_NOUNS = {
    'Eletrônicos': ['Smartphone', 'Tablet', 'Fone de Ouvido', 'Smartwatch', 'Câmera', 'Caixa de Som', 'Carregador', 'Cabo USB'],
    'Livros': ['Romance', 'Manual Técnico', 'Biografia', 'Ficção Científica', 'Quadrinhos', 'Dicionário', 'Atlas', 'Enciclopédia'],
    'Roupas': ['Camiseta', 'Calça Jeans', 'Jaqueta', 'Vestido', 'Bermuda', 'Moletom', 'Camisa Social', 'Saia'],
    'Calçados': ['Tênis Esportivo', 'Sapato Social', 'Sandália', 'Bota', 'Chinelo', 'Sapatênis', 'Mocassim', 'Tamanco'],
    'Esportes': ['Bola de Futebol', 'Raquete', 'Haltere', 'Esteira', 'Tapete Yoga', 'Luva de Boxe', 'Bicicleta', 'Rede de Vôlei'],
    'Casa e Jardim': ['Vaso Decorativo', 'Luminária', 'Tapete', 'Cortina', 'Regador', 'Almofada', 'Quadro', 'Relógio de Parede'],
    'Automotivo': ['Pneu', 'Óleo Motor', 'Filtro de Ar', 'Lâmpada LED', 'Tapete Carro', 'Cera Automotiva', 'Antena', 'Buzina'],
    'Brinquedos': ['Boneca', 'Carrinho', 'Quebra-Cabeça', 'Lego', 'Pelúcia', 'Jogo de Tabuleiro', 'Pião', 'Fantasia'],
    'Saúde': ['Vitamina C', 'Termômetro', 'Balança', 'Medidor de Pressão', 'Protetor Solar', 'Band-Aid', 'Colírio', 'Massageador'],
    'Beleza': ['Perfume', 'Batom', 'Shampoo', 'Creme Facial', 'Esmalte', 'Rímel', 'Base', 'Hidratante'],
    'Alimentos': ['Café Especial', 'Azeite Extra Virgem', 'Chocolate', 'Granola', 'Mel Orgânico', 'Chá Importado', 'Castanha', 'Geleia'],
    'Ferramentas': ['Furadeira', 'Chave de Fenda', 'Martelo', 'Alicate', 'Serra', 'Trena', 'Nível', 'Parafusadeira'],
    'Papelaria': ['Caderno', 'Caneta', 'Lápis', 'Borracha', 'Agenda', 'Marcador', 'Régua', 'Grampeador'],
    'Pet Shop': ['Ração Premium', 'Coleira', 'Brinquedo Pet', 'Cama Pet', 'Shampoo Pet', 'Comedouro', 'Arranhador', 'Guia Retrátil'],
    'Informática': ['Monitor', 'Teclado Mecânico', 'Mouse Gamer', 'SSD', 'Memória RAM', 'Placa de Vídeo', 'Webcam', 'Hub USB'],
    'Games': ['Controle Gamer', 'Headset Gamer', 'Console', 'Jogo RPG', 'Mousepad XL', 'Cadeira Gamer', 'Volante', 'Arcade Stick'],
    'Música': ['Violão', 'Guitarra', 'Teclado Musical', 'Bateria', 'Microfone', 'Amplificador', 'Ukulele', 'Flauta'],
    'Móveis': ['Mesa de Escritório', 'Cadeira Ergonômica', 'Estante', 'Sofá', 'Cama Box', 'Guarda-Roupa', 'Cômoda', 'Rack TV'],
    'Bebês': ['Carrinho de Bebê', 'Mamadeira', 'Fralda', 'Berço', 'Chupeta', 'Babá Eletrônica', 'Body', 'Mordedor'],
    'Camping': ['Barraca', 'Saco de Dormir', 'Lanterna', 'Cantil', 'Fogareiro', 'Mochila 50L', 'Isolante Térmico', 'Bússola'],
}


class Command(BaseCommand):
    help = 'Popula o banco com 20 categorias e 1000 produtos (seed fixo).'

    def handle(self, *args, **options):
        random.seed(RANDOM_SEED)

        self.stdout.write('Limpando dados existentes...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Criar categorias
        self.stdout.write('Criando 20 categorias...')
        categories = []
        for nome, descricao in CATEGORIES:
            cat = Category.objects.create(nome=nome, descricao=descricao)
            categories.append(cat)

        # Criar 1000 produtos
        self.stdout.write('Criando 1000 produtos...')
        products = []
        for i in range(1000):
            categoria = random.choice(categories)
            cat_name = categoria.nome
            noun = random.choice(PRODUCT_NOUNS[cat_name])
            adjective = random.choice(PRODUCT_ADJECTIVES)
            nome = f'{noun} {adjective} {i + 1}'
            descricao = f'Descrição do produto {nome} na categoria {cat_name}.'
            preco = Decimal(str(round(random.uniform(9.99, 9999.99), 2)))
            estoque = random.randint(0, 500)

            products.append(Product(
                nome=nome,
                descricao=descricao,
                preco=preco,
                estoque=estoque,
                categoria=categoria,
            ))

        Product.objects.bulk_create(products)

        self.stdout.write(self.style.SUCCESS(
            f'Seed concluído: {len(categories)} categorias e {len(products)} produtos criados.'
        ))
