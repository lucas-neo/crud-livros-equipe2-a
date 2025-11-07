import sys
sys.path.append('..')
import pytest
from Model.Livro import Livro

def test_criar_livro_com_sucesso():

    titulo = "Dacio e a Biblioteca"
    isbn = "978-3-16-148410-0"
    autor = "Dacio Machado"
    categoria = "Ficção"
    estoque = 5

    livro = Livro(titulo, isbn, autor, categoria, estoque)

    assert livro.titulo == "Dacio e a Biblioteca"
    assert livro.isbn == "978-3-16-148410-0"
    assert livro.autor == "Dacio Machado"
    assert livro.categoria == "Ficção"
    assert livro.estoque == 5
    assert livro.disponivel == True

def test_criar_livro_sem_titulo():
    with pytest.raises(ValueError, match="Titulo é obrigatório"):
         Livro("", "123", "Autor", "Categoria", 5)

def test_criar_livro_sem_isbn():
    """[TDD RED] Teste criar livro sem ISBN"""
    with pytest.raises(ValueError, match="ISBN é obrigatório"):
        Livro("Titulo", "", "Autor", "Categoria", 5)

def test_criar_livro_com_estoque_negativo():
    """[TDD RED] Teste estoque negativo"""
    with pytest.raises(ValueError, match="Estoque não pode ser negativo"):
        Livro("Titulo", "123", "Autor", "Categoria", -1)