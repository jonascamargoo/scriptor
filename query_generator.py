def generate_query(ast: dict) -> str:
    """
    Gera uma query estruturada a partir da AST.
    """
    if not ast or 'elements' not in ast or not ast['elements']:
        return "Query Inválida: AST vazia ou malformada."

    # Mapeamento dos elementos da AST para os nomes dos campos da query
    field_mapping = {
        'nome_autor': 'Authors',
        'titulo_documento': 'Document Title',
        'tipo_formato': 'Format',
        'valor_tamanho': 'Size',
        'nome_arquivo': 'File Name',
        'titulo_a': 'Document Title',
        'titulo_b': 'Document Title',
        # Adicione outros mapeamentos conforme crescimento da gramática
    }

    query_parts = []
    for element_key, value in ast['elements'].items():
        # Verifica se o elemento da AST tem um campo correspondente na query
        if element_key in field_mapping:
            field_name = field_mapping[element_key]
            # Formata a parte da query: ("FieldName":"value")
            query_parts.append(f'("{field_name}":"{value}")')

    if not query_parts:
        return "Não foi possível gerar uma query (nenhum elemento mapeado)."

    operator = ast.get('logical_operator', 'AND')
    return f" {operator} ".join(query_parts)

# Qual documento tem título "Relatório Anual" ou título "Tese Final" ?