import pytest
from collections import deque

from ..syntactic_analyzer import SyntacticAnalyzer
from ..config import GRAMMAR, NON_TERMINALS_VALIDATORS

# --- Configuração do Pytest (Setup) ---

@pytest.fixture(scope="module")
def optimized_parser():
    """
    Esta é uma "fixture" do pytest. Ela cria e configura o analisador 
    uma única vez e o disponibiliza para todas as funções de teste neste arquivo.
    Isso evita a repetição do código de setup.
    """
    # Lógica de agrupamento da gramática (Passo 1)
    grouped_grammar = {}
    for rule in GRAMMAR:
        first_keyword = rule['pattern'][0][1].lower()
        if first_keyword not in grouped_grammar:
            grouped_grammar[first_keyword] = []
        grouped_grammar[first_keyword].append(rule)
    
    # Supondo que você já modificou o SyntacticAnalyzer para o Passo 2
    parser = SyntacticAnalyzer(grouped_grammar, NON_TERMINALS_VALIDATORS)
    return parser

# --- Testes para a Otimização de Lookahead (Passo 1) ---

def test_lookahead_comando_valido(optimized_parser):
    """
    Testa se o parser otimizado ainda reconhece corretamente um comando válido.
    Verifica se o lookahead não quebrou a funcionalidade básica.
    """
    tokens = deque(['qual', 'documento', 'do', 'autor', '"Jonas"', '?'])
    ast, message = optimized_parser.parse(tokens)
    
    assert ast is not None
    assert ast['rule_name'] == 'pergunta_por_autor'
    assert message.startswith("Comando reconhecido com sucesso")

def test_lookahead_falha_com_comando_invalido(optimized_parser):
    """
    Testa se o lookahead rejeita corretamente um comando que começa
    com uma palavra-chave desconhecida.
    """
    tokens = deque(['onde', 'está', 'o', 'documento', '?']) # "onde" não é um lookahead válido
    ast, message = optimized_parser.parse(tokens)
    
    assert ast is None
    assert message == "Não reconheço este tipo de comando."

# --- Testes para a Flexibilização com Palavras-Chave Opcionais (Passo 2) ---

# Vamos assumir que você atualizou a regra 'pergunta_por_autor' para ser flexível
# 'pattern': [('KEYWORD', 'Qual'), ('OPTIONAL_KEYWORD', 'é'), ('OPTIONAL_KEYWORD', 'o'), ...]

def test_optional_keyword_sem_palavras_opcionais(optimized_parser):
    """
    Testa o caso base: a frase funciona sem as palavras opcionais.
    """
    tokens = deque(['qual', 'documento', 'do', 'autor', '"Jonas"', '?'])
    ast, message = optimized_parser.parse(tokens)
    
    assert ast is not None
    assert ast['rule_name'] == 'pergunta_por_autor_flex' # Usando a nova regra flexível

def test_optional_keyword_com_uma_palavra_opcional(optimized_parser):
    """
    Testa se a frase é reconhecida com UMA das palavras opcionais.
    """
    tokens = deque(['qual', 'o', 'documento', 'do', 'autor', '"Jonas"', '?'])
    ast, message = optimized_parser.parse(tokens)
    
    assert ast is not None
    assert ast['rule_name'] == 'pergunta_por_autor_flex'

def test_optional_keyword_com_todas_palavras_opcionais(optimized_parser):
    """
    Testa se a frase é reconhecida com TODAS as palavras opcionais.
    """
    tokens = deque(['qual', 'é', 'o', 'documento', 'do', 'autor', '"Jonas"', '?'])
    ast, message = optimized_parser.parse(tokens)
    
    assert ast is not None
    assert ast['rule_name'] == 'pergunta_por_autor_flex'

def test_optional_keyword_falha_com_palavra_errada(optimized_parser):
    """
    Testa se o parser ainda falha corretamente se uma palavra que NÃO é
    opcional nem obrigatória for inserida.
    """
    tokens = deque(['qual', 'agora', 'o', 'documento', 'do', 'autor', '"Jonas"', '?'])
    ast, message = optimized_parser.parse(tokens)
    
    assert ast is None
    assert message == "Não entendi." # Ou a mensagem de erro específica do seu parser