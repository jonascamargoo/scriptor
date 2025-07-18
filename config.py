import spacy

# Cores para o console
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Definição da gramática formal
GRAMMAR = [
    {
        'rule_name': 'pergunta_localizacao_documento',
        'type': 'pergunta',
        'pattern': [
            ('KEYWORD', 'Qual'),
            ('KEYWORD', 'documento'),
            ('KEYWORD', 'está'),
            ('KEYWORD', 'no'),
            ('<TITULO_DOCUMENTO>', 'titulo_documento'),
            ('KEYWORD', '?')
        ]
    },
    {
        'rule_name': 'pergunta_por_autor',
        'type': 'pergunta',
        'pattern': [
            ('KEYWORD', 'Qual'),
            ('KEYWORD', 'documento'),
            ('KEYWORD', 'do'),
            ('KEYWORD', 'autor'),
            ('<NOME_AUTOR>', 'nome_autor'),
            ('KEYWORD', '?')
        ]
    },
    {
        'rule_name': 'atribuicao_autor',
        'type': 'atribuicao',
        'pattern': [
            ('KEYWORD', 'O'),
            ('KEYWORD', 'autor'),
            ('KEYWORD', 'é'),
            ('<NOME_AUTOR>', 'nome_autor'),
            ('KEYWORD', '.')
        ]
    },
    {
        'rule_name': 'pergunta_tamanho_documento',
        'type': 'pergunta',
        'pattern': [
            ('KEYWORD', 'Qual'),
            ('KEYWORD', 'tamanho'),
            ('KEYWORD', 'tem'),
            ('<NOME_ARQUIVO>', 'nome_arquivo'),
            ('KEYWORD', '?')
        ]
    },
    {
        'rule_name': 'pergunta_titulo_documento',
        'type': 'pergunta',
        'pattern': [
            ('KEYWORD', 'Qual'),
            ('KEYWORD', 'documento'),
            ('KEYWORD', 'tem'),
            ('<TITULO_DOCUMENTO>', 'titulo_documento'),
            ('KEYWORD', '?')
        ]
    },
    {
        'rule_name': 'atribuicao_formato',
        'type': 'atribuicao',
        'pattern': [
            ('KEYWORD', 'O'),
            ('KEYWORD', 'formato'),
            ('KEYWORD', 'é'),
            ('<TIPO_FORMATO>', 'tipo_formato'),
            ('KEYWORD', '.')
        ]
    },
    {
        'rule_name': 'atribuicao_tamanho_minimo',
        'type': 'atribuicao',
        'pattern': [
            ('KEYWORD', 'Quero'),
            ('KEYWORD', 'tamanho'),
            ('KEYWORD', 'maior'),
            ('KEYWORD', 'que'),
            ('<VALOR_TAMANHO>', 'valor_tamanho'),
            ('KEYWORD', '.')
        ]
    }, 
    {
        'rule_name': 'pergunta_autor_e_titulo',
        'type': 'pergunta',
        'pattern': [
            ('KEYWORD', 'Qual'),
            ('KEYWORD', 'documento'),
            ('KEYWORD', 'do'),
            ('KEYWORD', 'autor'),
            ('<NOME_AUTOR>', 'nome_autor'),
            ('KEYWORD', 'com'),
            ('KEYWORD', 'título'),
            ('<TITULO_DOCUMENTO>', 'titulo_documento'),
            ('KEYWORD', '?')
        ]
    }   
]

# Validadores para os não-terminais da gramática
NON_TERMINALS_VALIDATORS = {
    '<TIPO_FORMATO>': ['.pdf', '.txt', '.docx', 'jpeg'],
    '<NOME_ARQUIVO>': ['relatorio.docx', 'imagem.jpeg', 'documento1'],
    '<TITULO_DOCUMENTO>': ['"Relatório Anual"', '"Notas de Aula"'],
    '<VALOR_TAMANHO>': lambda x: x.isdigit(),
    '<NOME_AUTOR>': lambda x: x.startswith('"') and x.endswith('"')
}



def load_spacy_model(model_name="pt_core_news_sm"):
    """
    Tenta carregar um modelo spaCy. Se não estiver instalado,
    instrui como instalar e encerra o programa.
    """
    try:
        nlp = spacy.load(model_name)
        print(f"{GREEN}Modelo spaCy '{model_name}' carregado com sucesso.{RESET}")
        return nlp
    except OSError:
        print(f"{RED}Erro: Modelo spaCy '{model_name}' não encontrado.{RESET}")
        print(f"{YELLOW}Por favor, instale o modelo executando o comando abaixo e tente novamente:{RESET}")
        print(f"python -m spacy download {model_name}")
        return None
    except ImportError:
        print(f"{RED}Erro: Biblioteca spaCy não encontrada. Instale com 'pip install spacy'.{RESET}")
        return None
    
    
    
    # Qual documento do autor "Jonas Camargo" com título "Relatório Final" ?