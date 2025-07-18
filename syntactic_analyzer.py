from collections import deque

class SyntacticAnalyzer:
    """
    Nosso Parser. Ele mantém o estado da "conversa" para lidar com
    perguntas e respostas.
    """
    def __init__(self, grammar, validators):
        self.grammar = grammar
        self.validators = validators
        self.context = {
            'state': 'IDLE',  # Pode ser 'IDLE' ou 'AWAITING_INPUT'
            'awaiting_element': None,
            'incomplete_ast': None
        }

    def parse(self, token_queue: deque):
        """Ponto de entrada do nosso analisador sintático."""
        tokens = list(token_queue)

        # Verifica se estamos esperando uma resposta a uma pergunta anterior
        if self.context['state'] == 'AWAITING_INPUT':
            return self._complete_previous_command(tokens)

        # Se não, tenta analisar um novo comando
        return self._parse_new_command(tokens)

    def _parse_new_command(self, tokens):
        """Analisa um comando do zero."""
        if not tokens:
            return None, "Comando vazio."

        for rule in self.grammar:
            match_result, matched_elements = self._match_pattern(tokens, rule['pattern'])

            if match_result == 'PERFECT_MATCH':
                # Reconheceu a regra e todos os elementos estão presentes
                ast = self._build_ast(rule, matched_elements)
                self.context['state'] = 'IDLE' # Reseta o estado
                return ast, f"Comando reconhecido com sucesso: {rule['rule_name']}"

            if match_result == 'PARTIAL_MATCH':
                # Falta uma palavra, então perguntamos ao usuário
                missing_element_type = rule['pattern'][len(tokens)][0]
                ast = self._build_ast(rule, matched_elements)

                self.context['state'] = 'AWAITING_INPUT'
                self.context['awaiting_element'] = missing_element_type
                self.context['incomplete_ast'] = ast
                
                
                return None, f"Entendi parcialmente. Qual {missing_element_type} você deseja saber?"

        return None, "Não entendi."

    def _complete_previous_command(self, tokens):
        """Tenta completar um comando anterior com a nova entrada do usuário."""
        if not tokens or len(tokens) > 1:
             # O comando falha novamente
            self.context['state'] = 'IDLE' # Reseta para evitar loop de erro
            return None, "Resposta inválida. Por favor, forneça apenas a informação solicitada."

        user_provided_token = tokens[0]
        element_type_needed = self.context['awaiting_element']
        
        # Valida se a resposta do usuário é válida para o tipo de elemento que faltava
        is_valid = False
        if element_type_needed in self.validators:
            validator = self.validators[element_type_needed]
            if callable(validator):
                is_valid = validator(user_provided_token)
            else: # Se for uma lista de opções
                is_valid = user_provided_token in validator

        if is_valid:
            # Completa a AST
            ast = self.context['incomplete_ast']
            element_key = self.context['awaiting_element'].strip('<>').lower()
            ast['elements'][element_key] = user_provided_token
            
            # Reseta o estado e retorna sucesso
            self.context['state'] = 'IDLE'
            return ast, "Comando completado com sucesso!"
        else:
            # A resposta ainda não atende à regra
            self.context['state'] = 'IDLE' # Reseta
            return None, f"A informação '{user_provided_token}' não é um {element_type_needed} válido. Tente novamente."

    def _match_pattern(self, tokens, pattern):
        """Compara uma lista de tokens com um padrão de regra."""
        if len(tokens) > len(pattern):
            # (excesso): Trata como erro por simplicidade
            return 'NO_MATCH', {}

        matched_elements = {}
        for i, token in enumerate(tokens):
            pattern_type, pattern_value = pattern[i]

            if pattern_type == 'KEYWORD':
                if token.lower() != pattern_value.lower():
                    return 'NO_MATCH', {}
            else: # É um não-terminal
                # Simplificação: consideramos qualquer token aqui como o não-terminal.
                # A validação semântica viria depois.
                element_key = pattern_type.strip('<>').lower()
                matched_elements[element_key] = token
        
        if len(tokens) == len(pattern):
            return 'PERFECT_MATCH', matched_elements
        else:
            return 'PARTIAL_MATCH', matched_elements

    def _build_ast(self, rule, matched_elements):
        """Constrói uma Árvore Sintática Abstrata (em formato de dicionário)."""
        logical_operator = 'OR' if 'ou' in rule['rule_name'] else 'AND'

        return {
            'type': rule['type'],
            'rule_name': rule['rule_name'],
            'logical_operator': logical_operator,
            'elements': matched_elements
        }