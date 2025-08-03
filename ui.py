import streamlit as st
import re
from collections import deque
from config import GRAMMAR, NON_TERMINALS_VALIDATORS, load_spacy_model
from linguistic_processing import get_tokens_for_parser, update_symbol_table
from syntactic_analyzer import SyntacticAnalyzer
from query_generator import generate_query

# --- Funções de Apoio e Lógica do Interpretador ---

@st.cache_resource
def load_dependencies():
    """Carrega o modelo spaCy e o parser uma única vez para otimizar a performance."""
    nlp_model = load_spacy_model()
    if nlp_model is None:
        st.error("O modelo spaCy não pôde ser carregado. Siga as instruções no terminal.")
        st.stop()
    
    grouped_grammar = {}
    for rule in GRAMMAR:
        first_keyword = rule['pattern'][0][1].lower()
        if first_keyword not in grouped_grammar:
            grouped_grammar[first_keyword] = []
        grouped_grammar[first_keyword].append(rule)

    parser = SyntacticAnalyzer(grouped_grammar, NON_TERMINALS_VALIDATORS)
    
    # Extrai palavras-chave da gramática
    grammar_keywords = {
        value.lower()
        for rule in GRAMMAR
        for token_type, value in rule['pattern']
        if token_type == 'KEYWORD'
    }
    return nlp_model, parser, grammar_keywords

def generate_example_inputs():
    """
    Gera frases de exemplo limpas a partir da gramática para fins didáticos,
    sem espaço extra antes da pontuação final.
    """
    examples = []
    for rule in GRAMMAR:
        example_parts = []
        for token_type, value in rule['pattern']:
            if token_type == 'KEYWORD':
                example_parts.append(value)
            else:
                example_parts.append(f"<{value}>")

        full_example = " ".join(example_parts)
        clean_example = re.sub(r'\s+([?.])', r'\1', full_example)
        examples.append(clean_example)
        
    return examples




def run_interpreter(user_input, nlp, parser, grammar_keywords):
    """Executa o pipeline completo do interpretador."""
    user_input = re.sub(r'([?.])', r' \1', user_input)
    # Lógica de pré-processamento para aspas
    quoted_phrases = re.findall(r'"[^"]*"', user_input)
    processed_input = re.sub(r'"[^"]*"', 'PLACEHOLDER', user_input)
    
    doc = nlp(processed_input)
    
    token_queue_processed = get_tokens_for_parser(doc, grammar_keywords)
    
    final_token_queue = deque()
    quote_index = 0
    for token in token_queue_processed:
        if token == 'PLACEHOLDER' and quote_index < len(quoted_phrases):
            final_token_queue.append(quoted_phrases[quote_index])
            quote_index += 1
        else:
            final_token_queue.append(token)
            
    # Executa a análise sintática
    ast, message = parser.parse(final_token_queue)
    return ast, message

# --- Interface Gráfica com Streamlit ---

st.set_page_config(page_title="Interpretador de Comandos", layout="wide")

st.title("🔎 Protótipo de Interpretador de Linguagem Natural")
st.markdown("""
Esta interface demonstra as fases de um interpretador de linguagem natural. 
Digite um comando em português no campo abaixo para ver a **Árvore Sintática Abstrata (AST)** e a **Query Estruturada** final que seriam enviadas a um sistema de busca.
""")

# Carrega dependências de forma otimizada
nlp, parser, keywords = load_dependencies()

# Botão Didático com Exemplos de Comandos
with st.expander("Clique aqui para ver exemplos de comandos válidos"):
    st.info("Seu interpretador reconhece padrões baseados na seguinte gramática:")
    example_list = generate_example_inputs()
    for ex in example_list:
        st.code(ex, language="text")
    st.warning("Lembre-se de substituir os termos entre `<...>` por valores reais (ex: `<nome_autor>` por `\"Jonas Camargo\"`).")


# Input do usuário
user_input = st.text_input("Digite seu comando aqui:", placeholder='Qual documento do autor "Jonas Camargo" ?')

if user_input:
    # Executa o interpretador quando o usuário digita algo
    ast, message = run_interpreter(user_input.strip(), nlp, parser, keywords)

    st.divider()

    if ast:
        st.success(f"Comando reconhecido com sucesso! ({message})")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌳 Árvore Sintática Abstrata (AST)")
            st.json(ast)

        with col2:
            st.subheader("🔍 Query Estruturada Gerada")
            final_query = generate_query(ast)
            st.code(final_query, language="sql")
            
    else:
        st.error(f"Não foi possível interpretar o comando. ({message})")