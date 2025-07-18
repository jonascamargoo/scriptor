import sys
import json
import re
from collections import deque
from query_generator import generate_query

# Importa os componentes dos outros módulos
from config import GRAMMAR, NON_TERMINALS_VALIDATORS, GREEN, RED, BLUE, RESET, YELLOW, load_spacy_model
from linguistic_processing import get_tokens_for_parser, update_symbol_table
from syntactic_analyzer import SyntacticAnalyzer

def main_loop():
    """Simula um interpretador de linha de comando usando apenas spaCy."""
    nlp = load_spacy_model()
    if nlp is None:
        sys.exit(1)

    parser = SyntacticAnalyzer(GRAMMAR, NON_TERMINALS_VALIDATORS)
    symbol_table = []

    grammar_keywords = {
        value.lower()
        for rule in GRAMMAR
        for token_type, value in rule['pattern']
        if token_type == 'KEYWORD'
    }
    print(f"Palavras-chave da gramática (não serão removidas): {sorted(list(grammar_keywords))}")

    print("\nInterpretador de Comandos de Documentos (spaCy). Digite 'sair' para terminar.")
    
    while True:
        # 1. Limpa a entrada para remover espaços extras no início/fim
        user_input = input("> ").strip() 
        if user_input.lower() == 'sair':
            break
        
        # 2. Pré-processamento para lidar com aspas
        # Encontra todos os textos entre aspas
        quoted_phrases = re.findall(r'"[^"]*"', user_input)
        # Substitui temporariamente as frases por placeholders
        processed_input = re.sub(r'"[^"]*"', 'PLACEHOLDER', user_input)
        
        
        # --- PROCESSAMENTO UNIFICADO COM SPACY ---
        
        # 3. Processa o texto com placeholders para criar o objeto 'doc'
        doc = nlp(processed_input)

        # 4. Obtém a fila de tokens para o analisador sintático,
        #    e substitui os placeholders de volta pelas frases originais
        token_queue_processed = get_tokens_for_parser(doc, grammar_keywords)
        
        final_token_queue = deque()
        quote_index = 0
        for token in token_queue_processed:
            if token == 'PLACEHOLDER':
                # Remove as aspas externas para o token final
                final_token_queue.append(quoted_phrases[quote_index])
                quote_index += 1
            else:
                final_token_queue.append(token)
        
        # 5. Atualiza a tabela de símbolos (usando o 'doc' original sem placeholders)
        update_symbol_table(nlp(user_input), symbol_table) # Usar o input original aqui

        # 6. Executa a Análise Sintática com a fila de tokens corrigida
        ast, message = parser.parse(final_token_queue)
        
        if ast:
            print(f"{GREEN}--- Análise Sintática OK ---{RESET}")
            if ast:
                print(f"{GREEN}--- Análise Sintática OK ---{RESET}")
                print(f"Mensagem: {message}")
                print(f"Árvore Sintática Abstrata (AST) gerada:")
                print(json.dumps(ast, indent=2, ensure_ascii=False))

                # --- NOVA ETAPA: GERAÇÃO DA QUERY ---
                print(f"\n{BLUE}--- Gerando Query Estruturada ---{RESET}")
                final_query = generate_query(ast)
                print(f"Query Final: {YELLOW}{final_query}{RESET}")
                # ------------------------------------
        else:
            print(f"{RED}--- Erro Sintático ---{RESET}")
            print(f"Mensagem: {message}{RESET}")
            
if __name__ == "__main__":
    main_loop()
    