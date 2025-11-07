"""
Controler - Camada de controle do SGBU

Este arquivo integra os Models com a View.
Gerencia a lógica de negócio e persistência de dados.
"""

from Model.Livro import Livro

class Controler:
    """
    Classe controladora que integra todos os módulos
    """
    
    def __init__(self):
        # Dicionários para armazenar dados em memória (volátil)
        self.livros = {}  # {id: objeto Livro}
        self.proximo_id_livro = 1
        
        # Inicializa com alguns dados de exemplo
        
    
    
    
    # ========== CRUD DE LIVROS ==========
    
    def cadastrar_livro(self, titulo, isbn, autor, categoria, estoque):
        """
        Cadastra um novo livro no sistema
        
        Args:
            titulo (str): Título do livro
            isbn (str): Código ISBN
            autor (str): Nome do autor
            categoria (str): Categoria do livro
            estoque (int): Quantidade em estoque
            
        Returns:
            dict: Dados do livro cadastrado com sucesso
            
        Raises:
            ValueError: Se dados inválidos
        """
        try:
            # Cria objeto Livro (validações são feitas no __init__)
            livro = Livro(titulo, isbn, autor, categoria, estoque)
            
            # Atribui ID único
            livro_id = self.proximo_id_livro
            self.proximo_id_livro += 1
            
            # Armazena no dicionário
            self.livros[livro_id] = livro
            
            return {
                'id': livro_id,
                'titulo': livro.titulo,
                'isbn': livro.isbn,
                'autor': livro.autor,
                'categoria': livro.categoria,
                'estoque': livro.estoque,
                'disponivel': livro.disponivel
            }
        except ValueError as e:
            raise e
    
    def listar_livros(self):
        """
        Lista todos os livros cadastrados
        
        Returns:
            list: Lista de dicionários com dados dos livros
        """
        livros_lista = []
        for livro_id, livro in self.livros.items():
            livros_lista.append({
                'id': livro_id,
                'titulo': livro.titulo,
                'isbn': livro.isbn,
                'autor': livro.autor,
                'categoria': livro.categoria,
                'estoque': livro.estoque,
                'disponivel': livro.disponivel
            })
        return livros_lista
    
    def buscar_livro(self, livro_id):
        """
        Busca um livro pelo ID
        
        Args:
            livro_id (int): ID do livro
            
        Returns:
            dict: Dados do livro ou None se não encontrado
        """
        if livro_id in self.livros:
            livro = self.livros[livro_id]
            return {
                'id': livro_id,
                'titulo': livro.titulo,
                'isbn': livro.isbn,
                'autor': livro.autor,
                'categoria': livro.categoria,
                'estoque': livro.estoque,
                'disponivel': livro.disponivel
            }
        return None
    
    def atualizar_livro(self, livro_id, titulo=None, isbn=None, autor=None, categoria=None, estoque=None):
        """
        Atualiza dados de um livro existente
        
        Args:
            livro_id (int): ID do livro
            titulo, isbn, autor, categoria, estoque: Novos valores (opcionais)
            
        Returns:
            dict: Dados do livro atualizado
            
        Raises:
            ValueError: Se livro não existe ou dados inválidos
        """
        if livro_id not in self.livros:
            raise ValueError(f"Livro com ID {livro_id} não encontrado")
        
        livro = self.livros[livro_id]
        
        # Atualiza apenas campos fornecidos
        if titulo is not None:
            if not titulo or titulo.strip() == "":
                raise ValueError("Titulo é obrigatório")
            livro.titulo = titulo
        
        if isbn is not None:
            if not isbn or isbn.strip() == "":
                raise ValueError("ISBN é obrigatório")
            livro.isbn = isbn
        
        if autor is not None:
            livro.autor = autor
        
        if categoria is not None:
            livro.categoria = categoria
        
        if estoque is not None:
            if estoque < 0:
                raise ValueError("Estoque não pode ser negativo")
            livro.estoque = estoque
            livro.disponivel = estoque > 0
        
        return self.buscar_livro(livro_id)
    
    def remover_livro(self, livro_id):
        """
        Remove um livro do sistema
        
        Args:
            livro_id (int): ID do livro
            
        Returns:
            bool: True se removido com sucesso
            
        Raises:
            ValueError: Se livro não existe
        """
        if livro_id not in self.livros:
            raise ValueError(f"Livro com ID {livro_id} não encontrado")
        
        del self.livros[livro_id]
        return True


# Instância global do controller (singleton)
controler = Controler()