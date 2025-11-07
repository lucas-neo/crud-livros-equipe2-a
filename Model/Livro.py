"""
Model: Livro
Módulo 2 - Catálogo de Livros

Este arquivo deve ser implementado pelos alunos usando TDD (Test Driven Development).

Requisitos:
- Classe Livro com atributos: id, isbn, titulo, autores, categoria, sinopse, ano, editora, estoque, status
- Validações:
  * ISBN não pode ser vazio e deve seguir formato válido
  * Título deve ter pelo menos 1 caractere
  * Estoque não pode ser negativo
  * Status deve ser 'disponivel', 'emprestado' ou 'manutencao'
  * Categoria deve ser válida

Exemplos de testes a implementar:
- test_criar_livro_valido()
- test_criar_livro_isbn_invalido()
- test_criar_livro_estoque_negativo()
- test_alterar_status_livro()
- test_validar_disponibilidade()
"""

class Livro:
    def __init__(self, titulo, isbn, autor, categoria, estoque):
        if not titulo or titulo.strip() =="":
            raise ValueError("Titulo é obrigatório")
        if not isbn or isbn.strip() == "":
            raise ValueError ("ISBN é obrigatório")
        if estoque < 0:
            raise ValueError ("Estoque não pode ser negativo")
        self.titulo = titulo
        self.isbn = isbn
        self.autor = autor
        self.categoria = categoria
        self.estoque = estoque
        self.disponivel = estoque > 0
        pass
