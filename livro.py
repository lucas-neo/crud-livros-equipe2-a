"""
Módulo Livro - [TDD Green]
código MÍNIMO para fazer os testes passarem.
"""
_db_livros = []

def _limpar_db():
    """
    Limpa a base de dados.
    """
    _db_livros.clear()

class Livro:
    
    def __init__(self, titulo, autor, isbn):
        if not titulo:
            raise ValueError("Título é obrigatório")
        if not autor:
            raise ValueError("Autor é obrigatório")
        if not isbn:
            raise ValueError("ISBN é obrigatório")
            
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.status = "disponivel"
    
    def emprestar(self):
        self.status = "emprestado"
    
    def devolver(self):
        self.status = "disponivel"


def criar_livro(titulo, autor, isbn):
    try:
        if buscar_livro_por_isbn(isbn):
             return None
             
        livro = Livro(titulo=titulo, autor=autor, isbn=isbn)
        _db_livros.append(livro)
        return livro
    except ValueError:
        return None

def listar_livros():
    return _db_livros

def buscar_livro_por_isbn(isbn):
    for livro in _db_livros:
        if livro.isbn == isbn:
            return livro
    return None

def atualizar_livro(isbn, novo_titulo, novo_autor):
    livro_encontrado = buscar_livro_por_isbn(isbn)
    
    if livro_encontrado:
        livro_encontrado.titulo = novo_titulo
        livro_encontrado.autor = novo_autor
        return livro_encontrado
    
    return None

def deletar_livro(isbn):

    livro_encontrado = buscar_livro_por_isbn(isbn)
    
    if livro_encontrado:
        _db_livros.remove(livro_encontrado)
        return True 
        
    return False 