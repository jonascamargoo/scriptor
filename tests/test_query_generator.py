from query_generator import generate_query

def test_generate_query_for_author_and_title():
    """
    Testa a geração de uma query com o operador lógico AND.
    """
    # 1. Prepara uma AST (Árvore Sintática Abstrata) de exemplo
    ast = {
        'type': 'pergunta',
        'rule_name': 'pergunta_autor_e_titulo',
        'logical_operator': 'AND',
        'elements': {
            'nome_autor': '"Jonas Camargo"',
            'titulo_documento': '"Tese Final"'
        }
    }
    
    # 2. Define o resultado esperado
    expected_query = '("Authors":"Jonas Camargo") AND ("Document Title":"Tese Final")'
    
    # 3. Executa a função e verifica o resultado
    generated_query = generate_query(ast)
    assert generated_query.strip() == expected_query

def test_generate_query_for_title_or_title():
    """
    Testa a geração de uma query com o operador lógico OR.
    """
    # 1. Prepara uma AST de exemplo
    ast = {
        'type': 'pergunta',
        'rule_name': 'pergunta_titulo_ou_titulo',
        'logical_operator': 'OR',
        'elements': {
            'titulo_a': '"Relatório Anual"',
            'titulo_b': '"Tese Final"'
        }
    }
    
    # 2. Define o resultado esperado
    expected_query = '("Document Title":"Relatório Anual") OR ("Document Title":"Tese Final")'

    # 3. Executa a função e verifica o resultado
    generated_query = generate_query(ast)
    assert generated_query.strip() == expected_query

def test_generate_query_with_empty_ast():
    """
    Testa o comportamento com uma AST vazia.
    """
    ast = {}
    expected_message = "Query Inválida: AST vazia ou malformada."
    generated_query = generate_query(ast)
    assert generated_query == expected_message