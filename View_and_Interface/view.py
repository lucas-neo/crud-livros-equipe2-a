from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa o controller
from controler import controler


def _esc(v):
    """Escapa valores HTML para evitar XSS"""
    return escape("" if v is None else str(v))


class BibliotecaView(BaseHTTPRequestHandler):
    """
    Servidor HTTP que controla todas as telas do SGBU via Python.
    """

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/livros':
            self.render_livros()
        elif path == '/livros/novo':
            self.render_form_livro()
        elif path.startswith('/livros/editar/'):
            livro_id = int(path.split('/')[-1])
            self.render_form_editar_livro(livro_id)
        elif path.startswith('/livros/deletar/'):
            livro_id = int(path.split('/')[-1])
            self.deletar_livro(livro_id)
        elif path == '/cadastro':
            self.render_cadastro()
        elif path == '/emprestimos':
            self.render_emprestimos()
        elif path == '/relatorios':
            self.render_relatorios()
        else:
            self.send_error(404, "Página não encontrada")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        # Lê dados do formulário
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(body)
        
        # Converte lista em valor único
        data = {k: v[0] if v else '' for k, v in data.items()}
        
        if path == '/livros/salvar':
            self.processar_livro(data)
        elif path == '/livros/atualizar':
            self.atualizar_livro(data)
        else:
            self.send_error(404, "Rota não encontrada")

    # ========== RENDERIZAÇÃO - MÓDULO 2: LIVROS ==========
    
    def render_livros(self):
        """Renderiza lista de livros usando o controller"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            # Busca livros do controller
            livros = controler.listar_livros()
            
            if livros:
                conteudo = '''
                    <div class="actions">
                        <h2>Catálogo de Livros</h2>
                        <a href="/livros/novo" class="btn btn-primary">+ Novo Livro</a>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Título</th>
                                <th>ISBN</th>
                                <th>Autor</th>
                                <th>Categoria</th>
                                <th>Estoque</th>
                                <th>Status</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                '''
                
                for livro in livros:
                    status_badge = "Disponível" if livro['disponivel'] else "Indisponível"
                    conteudo += f'''
                        <tr>
                            <td>{_esc(livro['id'])}</td>
                            <td>{_esc(livro['titulo'])}</td>
                            <td>{_esc(livro['isbn'])}</td>
                            <td>{_esc(livro['autor'])}</td>
                            <td>{_esc(livro['categoria'])}</td>
                            <td>{_esc(livro['estoque'])}</td>
                            <td><span class="badge">{status_badge}</span></td>
                            <td class="actions">
                                <a href="/livros/editar/{livro['id']}" class="btn btn-sm">Editar</a>
                                <a href="/livros/deletar/{livro['id']}" class="btn btn-sm btn-danger" 
                                   onclick="return confirm('Tem certeza que deseja excluir?')">Excluir</a>
                            </td>
                        </tr>
                    '''
                
                conteudo += '''
                        </tbody>
                    </table>
                '''
            else:
                conteudo = '''
                    <div class="actions">
                        <h2>Catálogo de Livros</h2>
                        <a href="/livros/novo" class="btn btn-primary">+ Novo Livro</a>
                    </div>
                    <div class="alert alert-info">
                        Nenhum livro cadastrado ainda. Clique em "+ Novo Livro" para começar.
                    </div>
                '''
        
        except Exception as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro:</strong> {_esc(str(e))}
                </div>
            '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_livro(self):
        """Renderiza formulário de novo livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="actions">
                <h2>Cadastrar Novo Livro</h2>
            </div>
            <form method="POST" action="/livros/salvar" class="form">
                <div class="form-group">
                    <label>Título *</label>
                    <input type="text" name="titulo" required>
                </div>
                <div class="form-group">
                    <label>ISBN *</label>
                    <input type="text" name="isbn" required>
                </div>
                <div class="form-group">
                    <label>Autor *</label>
                    <input type="text" name="autor" required>
                </div>
                <div class="form-group">
                    <label>Categoria *</label>
                    <select name="categoria" required>
                        <option value="">Selecione...</option>
                        <option value="Técnico">Técnico</option>
                        <option value="Ficção">Ficção</option>
                        <option value="Não-ficção">Não-ficção</option>
                        <option value="Romance">Romance</option>
                        <option value="Biografia">Biografia</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Estoque *</label>
                    <input type="number" name="estoque" min="0" required>
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-primary">Cadastrar</button>
                    <a href="/livros" class="btn">Cancelar</a>
                </div>
            </form>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def processar_livro(self, data):
        """Processa cadastro de novo livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            # Chama o controller para cadastrar
            livro = controler.cadastrar_livro(
                titulo=data.get('titulo', ''),
                isbn=data.get('isbn', ''),
                autor=data.get('autor', ''),
                categoria=data.get('categoria', ''),
                estoque=int(data.get('estoque', 0))
            )
            
            conteudo = f'''
                <div class="alert alert-success">
                    <strong>Sucesso!</strong> Livro "{_esc(livro['titulo'])}" cadastrado com sucesso!
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Ver Todos os Livros</a>
                    <a href="/livros/novo" class="btn">Cadastrar Outro</a>
                </div>
            '''
        
        except ValueError as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro de Validação:</strong> {_esc(str(e))}
                </div>
                <div class="form-actions">
                    <a href="/livros/novo" class="btn btn-primary">Tentar Novamente</a>
                    <a href="/livros" class="btn">Voltar</a>
                </div>
            '''
        except Exception as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro:</strong> {_esc(str(e))}
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Voltar</a>
                </div>
            '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_form_editar_livro(self, livro_id):
        """Renderiza formulário de edição de livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            livro = controler.buscar_livro(livro_id)
            
            if not livro:
                conteudo = '''
                    <div class="alert alert-danger">
                        <strong>Erro:</strong> Livro não encontrado.
                    </div>
                    <div class="form-actions">
                        <a href="/livros" class="btn btn-primary">Voltar</a>
                    </div>
                '''
            else:
                conteudo = f'''
                    <div class="actions">
                        <h2>Editar Livro</h2>
                    </div>
                    <form method="POST" action="/livros/atualizar" class="form">
                        <input type="hidden" name="id" value="{livro['id']}">
                        <div class="form-group">
                            <label>Título *</label>
                            <input type="text" name="titulo" value="{_esc(livro['titulo'])}" required>
                        </div>
                        <div class="form-group">
                            <label>ISBN *</label>
                            <input type="text" name="isbn" value="{_esc(livro['isbn'])}" required>
                        </div>
                        <div class="form-group">
                            <label>Autor *</label>
                            <input type="text" name="autor" value="{_esc(livro['autor'])}" required>
                        </div>
                        <div class="form-group">
                            <label>Categoria *</label>
                            <select name="categoria" required>
                                <option value="Técnico" {"selected" if livro['categoria'] == "Técnico" else ""}>Técnico</option>
                                <option value="Ficção" {"selected" if livro['categoria'] == "Ficção" else ""}>Ficção</option>
                                <option value="Não-ficção" {"selected" if livro['categoria'] == "Não-ficção" else ""}>Não-ficção</option>
                                <option value="Romance" {"selected" if livro['categoria'] == "Romance" else ""}>Romance</option>
                                <option value="Biografia" {"selected" if livro['categoria'] == "Biografia" else ""}>Biografia</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Estoque *</label>
                            <input type="number" name="estoque" value="{livro['estoque']}" min="0" required>
                        </div>
                        <div class="form-actions">
                            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                            <a href="/livros" class="btn">Cancelar</a>
                        </div>
                    </form>
                '''
        
        except Exception as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro:</strong> {_esc(str(e))}
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Voltar</a>
                </div>
            '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def atualizar_livro(self, data):
        """Processa atualização de livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            livro_id = int(data.get('id', 0))
            
            livro = controler.atualizar_livro(
                livro_id=livro_id,
                titulo=data.get('titulo'),
                isbn=data.get('isbn'),
                autor=data.get('autor'),
                categoria=data.get('categoria'),
                estoque=int(data.get('estoque', 0))
            )
            
            conteudo = f'''
                <div class="alert alert-success">
                    <strong>Sucesso!</strong> Livro "{_esc(livro['titulo'])}" atualizado com sucesso!
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Ver Todos os Livros</a>
                </div>
            '''
        
        except ValueError as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro de Validação:</strong> {_esc(str(e))}
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Voltar</a>
                </div>
            '''
        except Exception as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro:</strong> {_esc(str(e))}
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Voltar</a>
                </div>
            '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def deletar_livro(self, livro_id):
        """Deleta um livro"""
        with open("View_and_Interface/crud_livros.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        try:
            controler.remover_livro(livro_id)
            
            conteudo = '''
                <div class="alert alert-success">
                    <strong>Sucesso!</strong> Livro removido com sucesso!
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Ver Todos os Livros</a>
                </div>
            '''
        
        except ValueError as e:
            conteudo = f'''
                <div class="alert alert-danger">
                    <strong>Erro:</strong> {_esc(str(e))}
                </div>
                <div class="form-actions">
                    <a href="/livros" class="btn btn-primary">Voltar</a>
                </div>
            '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    # ========== OUTRAS ROTAS (cadastro, emprestimos, relatorios) ==========
    
    def render_cadastro(self):
        """Renderiza página de cadastro de usuários"""
        with open("View_and_Interface/cadastro.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="alert alert-info">
                <strong>Módulo 1 - Cadastro de Usuários</strong><br>
                Funcionalidade não implementada. Os alunos devem implementar usando TDD.
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_emprestimos(self):
        """Renderiza página de empréstimos"""
        with open("View_and_Interface/emprestimos.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="alert alert-info">
                <strong>Módulo 3 - Empréstimos e Devoluções</strong><br>
                Funcionalidade não implementada. Os alunos devem implementar usando TDD.
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    def render_relatorios(self):
        """Renderiza página de relatórios"""
        with open("View_and_Interface/relatorios.html", "r", encoding="utf-8") as f:
            html = f.read()
        
        conteudo = '''
            <div class="alert alert-info">
                <strong>Módulo 4 - Relatórios</strong><br>
                Funcionalidade não implementada. Os alunos devem implementar usando TDD.
            </div>
        '''
        
        html = html.replace('<!--CONTEUDO-->', conteudo)
        self.send_html(html)
    
    # ========== HELPERS ==========
    
    def send_html(self, html):
        """Envia resposta HTML"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


def run_server(port=8000):
    """Inicia o servidor HTTP"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BibliotecaView)
    print(f'🚀 Servidor SGBU rodando em http://localhost:{port}')
    print(f'📚 Acesse: http://localhost:{port}/livros')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()