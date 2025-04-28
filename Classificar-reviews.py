import spacy
import language_tool_python

# Inicializando o modelo de português e o corretor gramatical
nlp = spacy.load('pt_core_news_sm')
tool = language_tool_python.LanguageTool('pt-BR')

# Listas de tokens
tokens_positivos = [
    "ótimo", "excelente", "incrível", "fantástico", "maravilhoso", "perfeito",
    "bom", "adorável", "agradável", "eficiente", "rápido", "prático",
    "funcional", "aconchegante", "caprichado", "personalizado", "profissional",
    "organizado", "inovador", "top", "show", "massa", "bonito", "elegante",
    "confiável", "resistente", "durável", "forte", "leve", "ágil", "preciso",
    "versátil", "detalhado", "atencioso", "sensacional", "espetacular", "melhor",
    "intuitivo", "relevante", "valioso", "especial", "exclusivo", "completo",
    "efetivo", "suave", "simpático", "dedicado", "ágil", "topzera", "bala", "firmeza", "brabo", "nota dez"
]


tokens_negativos = [
    "ruim", "horrível", "péssimo", "terrível", "decepcionante", "lento",
    "ineficiente", "problemático", "fraco", "desgastado", "defeituoso",
    "instável", "malfeito", "amador", "desleixado", "confuso", "complicado",
    "desorganizado", "caro", "inútil", "desnecessário", "fajuto", "vagabundo",
    "quebrado", "frustrante","mau", "fraco","arrepender", "demorado", "arrastado", "bizarro",
    "chato", "aborrecido", "ridículo", "sem graça", "sem sentido",
    "lixo", "porcaria", "zoado", "fuleiro", "meia boca", "furado",
    "bugado", "problemático", "trambolho", "porre"
]


tokens_neutros = [
    "ok", "regular", "mediano", "normal", "simples", "básico", "usual",
    "comum", "razoável", "padrão", "esperado", "mínimo", "satisfatório",
    "moderado", "neutro", "consistente", "previsível", "genérico",
    "ordinário", "aceitável", "convencional", "linear", "tradicional",
    "frequente", "repetitivo", "rotineiro", "controlado", "adequado",
    "estável", "pragmático", "objetivo", "simplesinho"
]


palavras_reversoras = ["mas", "porém", "entretanto", "todavia", "no entanto"]

def corrigir_gramatica(texto):
    """Corrige automaticamente o texto usando LanguageTool"""
    matches = tool.check(texto)
    texto_corrigido = language_tool_python.utils.correct(texto, matches)
    return texto_corrigido

def preprocessar(texto):
    """Corrige, lematiza e gera tokens do texto"""
    print(f"\nTexto original: {texto}")
    texto_corrigido = corrigir_gramatica(texto)
    print(f"Texto corrigido: {texto_corrigido}")
    
    texto_corrigido = texto_corrigido.lower()  # Coloca tudo minúsculo
    doc = nlp(texto_corrigido)

    tokens = []
    for token in doc:
        if not token.is_punct and not token.is_space:  # Ignora pontuação e espaço
            tokens.append(token.lemma_)  # Lema do token
    
    print(f"Tokens obtidos após pré-processamento: {tokens}")
    return tokens

def classificar_opiniao(texto):
    """Classifica a opinião baseada nos tokens"""
    tokens = preprocessar(texto)
    positivos = 0
    negativos = 0
    neutros = 0
    sentimento_reverso = False
    tokens_usados_para_classificacao = []

    for token in tokens:
        if token in palavras_reversoras:
            sentimento_reverso = True
            continue

        if token in tokens_positivos:
            tokens_usados_para_classificacao.append(token)
            if sentimento_reverso:
                negativos += 1
            else:
                positivos += 1
        elif token in tokens_negativos:
            tokens_usados_para_classificacao.append(token)
            if sentimento_reverso:
                positivos += 1
            else:
                negativos += 1
        elif token in tokens_neutros:
            tokens_usados_para_classificacao.append(token)
            neutros += 1

    print(f"Tokens usados para a classificação: {tokens_usados_para_classificacao}")

    if positivos > negativos:
        return "Opinião POSITIVA"
    elif negativos > positivos:
        return "Opinião NEGATIVA"
    elif positivos == negativos and (positivos > 0 or negativos > 0):
        return "Opinião NEUTRA (Conflito de sentimentos)"
    else:
        return "Opinião NEUTRA (Sem sentimento detectado)"

# Exemplo de uso:
comentarios = [
    "Produto veio com um lado zoado ,xiando.",
    "É até bonito, meu filho adorou as luzes, mas só serve de enfeite, não sai som….",
    "Perfeito!. Material excelente!. Som, perfeito!. Meu filho amouuu. Usando ele no xbox-s. E ainda veio um brinde.",
    "O som do aparelho é horrível.",
    "Ótimo produto pelo preço. Está me atendendo perfeitamente e, utilizo o dia todo. Se quiser desligar o led, basta não conectar o usb.",
    "Pra começar, um lado já veio sem funcionar, desconfortável, muitos ruídos do som por mal acabamento nessa parte, pensei que fosse um ótimo custo benefício vendo as avaliações, mas da minha parte me arrependi totalmente e não indico a compra",
    "Produto bem mediano.",
    "Nao funciona com a função de head set para falar é horrível, sim sai muito baixo.",
    "Aperta bem as orelhas, mas atende bem pelo valor. Isola bem os ruídos durante chamadas.",
    "Horrível som ruim material ruim desconfortavel não esperava muito mas tbm não esperava tão pouco.",
    "Possuo outro modelo da mesma marca (que é muito bom). Mas este modelo específico oferece menos conforto por causa da espuma do fone.",
    "Pelo preço até q não é tão ruim."
]

for comentario in comentarios:
    print("\n" + "="*60)
    resultado = classificar_opiniao(comentario)
    print(f"Classificação final: {resultado}")
