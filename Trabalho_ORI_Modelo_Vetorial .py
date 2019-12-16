# UNIVERSIDADE FEDERAL DE UBERLÂNDIA - UFU
# Organização e Recuperação da informação - Professor Wendel Melo #
# Guilherme Henrique de Araújo Santos - 11721BSI220
# Gustavo Henrique Ferreira Reis Costa - 11721BSI222 

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#

# CÓDIGO FONTE - MODELO VETORIAL:

import nltk # Importando o pacote NLTK para poder usar seus recursos na aplicação.
import json # Importado o pacote JSON para converter dicionário em texto
import sys # Importando o pacote SYS para poder ler os argumentos por linha de comando
import math # Importando o pacote MATH para poder fazer as operações de ponderamento que usam logarítmo
import operator # Pacote utilizado para imprimir um dicionário na ordem inversa

# Função que trará o cálculo do IDF que é o log (Número total de arquivos / Número de arquivos que contém o termo passado
def calcula_IDF (dicionario, dicionario_IDF):
    for z in dicionario:
        Ni = len(dicionario[z]) 
        IDF = math.log10(len(dict_listarq)/Ni) 
        dicionario_IDF[z] = IDF 

# Essa função irá fazer o cáculo do TF x IDF 
# TF = 1 + log (Frequência de um termo em um determinado documento)
# Percorre um dicionário, um índice invertido
# Armazena o valor do IDF do termo do dicionário
# Percorre o "índice" novamente, pegando apenas o nome do arquivo
# Se este arquivo não estiver no dicionário de TF_IDF, colocar
# Pegar a frequência do termo
# Calcular seu TF_IDF
def calcula_TF_IDF(dicionario, dicionario_IDF, dicionario_TF_IDF, listaArquivos):
    for termo in dicionario.keys():
            
        valor_IDF = dicionario_IDF[termo]

        for numero_arquivo in dicionario[termo]:
            nome_arquivo = listaArquivos[numero_arquivo-1]
            if nome_arquivo not in dicionario_TF_IDF:
                dicionario_TF_IDF[ nome_arquivo ] = {}
            
            frequencia = dicionario[termo][numero_arquivo]
            dicionario_TF_IDF[nome_arquivo][ termo ] =  (1 + math.log10(frequencia) ) * valor_IDF

stopwords = nltk.corpus.stopwords.words # Lista de stopwords
stopwords = nltk.corpus.stopwords.words("portuguese") # Pegando as stopwords em português
stopwords.sort() # Ordenando as stopwords por ordem alfabética 

# Declaração de variáveis:
dict_listarq = {} 
contador = 0 
dicionario_indice = {} 
dIDF = {} 
meu_tf_idf = {} 
dicionario_indice_consulta_final = {} 
dconsulta_final_TF_IDF = {}
similaridade = {}
numerador = {}
denominador = {}
soma_consulta = 0
listconsulta_final = [sys.argv[2]]
consulta_sem_radical = []


with open(sys.argv[1],"r") as arquivobase: # Abertura do arquivo base.txt pelo argumento passado na linha de comando setado com a opção de leitura
    base = arquivobase.read() # Leitura dos dados do arquivo que mostrará a minha base de documentos disponíveis
    listarq = base.split("\n") # A função split me permite retirar todo o conteúdo especificado dentro do parênteses, no caso estamos tirando todos os enters "\n" e colocamos dentro de uma lista


# Criação de um laço para percorrer a lista que contém as "referências" para minha base de dados
for k in range (0, len(listarq)): 

    contador += 1 # Incremento o contador para armazenar o próximo arquivo posteriormente

    if contador not in dict_listarq: # Se contador não existir no dicionário
        dict_listarq[contador] = listarq[k] # Dicionário coloca o contador como sua chave e seu valor inicial é dado como o nome do arquivo no qual ele se encontra
    dict_listarq[contador] = listarq[k] # Se for encontrado também executará essa ação
    

    arqY = open(listarq[k], "r") # Criando uma variável de leitura para abrir o arquivo da posição "k"
    readY = arqY.read().lower() # A variável readY irá ler o arquivo da posição k e passar todas as suas letras para minúsculas.
    # A função replace abaixo pegará toda <origem> (Primeiro "caracter ou palavras") e trocar pelo <destino> (Sengundo "caracter ou palavra")
    readY = readY.replace("?"," ")
    readY = readY.replace(",", " ")
    readY = readY.replace(".", " ")
    readY = readY.replace("!", " ")
    readY = readY.replace("...", " ")
    readY = readY.replace("\n", " ")

    # Realizar a tokenização do conteúdo readY, ou seja, separar cada caractere ou string por vírgulas dentro de uma lista
    palavras = nltk.word_tokenize(readY) # Palavras contém uma lista tokenizada
    
    palavras_not_stopwords = [] # Criação de uma lista para armazenar os documentos da base sem "stopwords"
    palavras_not_rad = [] # Criação de uma lista para armazenar os documentos da base com apenas os radicais

    # Criação de outro laço para percorrer a lista do conteúdo da base tokenizado
    for k in range(0, len(palavras)):
 
        if(palavras[k] not in stopwords): # Se a palavra ou caracter da posição k na lista palavras não for "stopwords" (variável criada)
            palavras_not_stopwords.append(palavras[k]) # Utilizo a função append para acrescentar a "palavra" dentro da minha lista de palavras sem stopwords

    # Criação de um laço para percorrer a minha lista de palavras do documento sem stopwords
    for k in range(0, len(palavras_not_stopwords)):
        stemmer = nltk.stem.RSLPStemmer() # Criação de uma variável que permite que eu possa tirar os radicais das palavras
        palavras_not_rad.append(stemmer.stem(palavras_not_stopwords[k])) # Colocando as palavras sem as stopwords e com seus radicais extraídos na lista palavras_not_rad
               
    # Este for percorre os índices do dicionário dict_listarq, onde temos que pegar os números de cada documentos, no caso que estão no índice
    #for c in dict_listarq.keys():
    #    valores = c # Colocando uma variável para armazenar o valor dos índices que serão o número referente a cada documento
    
    valores = contador

    # Laço percorrendo a lista com as palavras sem radicais e sem stopwords
    for c in range (0, len(palavras_not_rad)):
        if palavras_not_rad[c] not in dicionario_indice: # Se a palavras não estiver no índice invertido
            dicionario_indice[palavras_not_rad[c]] = {} # Crio um dicionário vazio, que armazenará futuramente {"arquivo" : "quantidade de vezes que a palavra aparece"}
        
        dicionario_indice[palavras_not_rad[c]][valores] = palavras_not_rad.count(palavras_not_rad[c]) # Coloco o arquivo que ela está que é a variável que foi criada logo acima (valores) e conto a quantidade de vezes que a palavra aparece no vetor com os radicais e sem stopwords  

    arqY.close() # Fechando arquivo com conteúdo informativo, ou seja, o arquivo da base que está sendo lido no momento



# Chamada das funções que serão executadas para a ponderação dos termos
calcula_IDF(dicionario_indice, dIDF)
calcula_TF_IDF(dicionario_indice, dIDF, meu_tf_idf, listarq)
    

# Criação do arquivo pesos.txt
# Armazena-se o conteúdo que o arquivo conterá
# Faz-se o layout de como irá aparecer no arquivo utilizando replace
with open ("pesos.txt", "w") as pesos:
    for percorrer in meu_tf_idf:
        armazena_conteudo_arquivo = percorrer + str (meu_tf_idf[percorrer])
        txtPesos = armazena_conteudo_arquivo.replace(",","").replace(":", ",").replace("{" , ": ").replace("'", "").replace("}","").replace(", ", ",") + "\n"
        pesos.write(txtPesos)

# Abertura do arquivo consulta passado na linha de comando
# Passa o conteúdo da consulta para minúsculo e retira-se os operadores de AND
with open(sys.argv[2], 'r') as arqConsulta: 
    consulta_lida = arqConsulta.read().lower() 
consulta_final = consulta_lida.replace('&','').replace("\n", " ")
consulta_tokenizada = nltk.word_tokenize(consulta_final)

# Esse laço anda na consulta e verifica se o termo é apenas um caractere, se não for
# Ele tira o radical do termo
# Se for apenas um caractere ele apenas adiciona o conteúdo no vetor
# Ele também verifica se existe o termo digitado na consulta dentro da base, se existir
# Ocorre tudo normalmente, se não existir ele termina enviando um arquivo resposta para o usuário
for andando_na_consulta in consulta_tokenizada:
    radical = nltk.stem.RSLPStemmer()
    if (len(andando_na_consulta) > 1):
        consulta_sem_radical.append(radical.stem(andando_na_consulta))
    
    if (len(andando_na_consulta) <= 1):
        consulta_sem_radical.append(andando_na_consulta)

    if radical.stem(andando_na_consulta) not in dicionario_indice:
        arquivo = open('resposta.txt', 'w')
        arquivo.writelines("O termo " + "'" + andando_na_consulta + "'" + " contido na consulta não existe na base de documentos")
        arquivo.close()
        sys.exit()

# Cria um índice invertido para a consulta
for entra_na_consulta_final in consulta_sem_radical:
    if sys.argv[2] not in dicionario_indice_consulta_final:
        dicionario_indice_consulta_final[entra_na_consulta_final] = {}
    dicionario_indice_consulta_final[entra_na_consulta_final][1]= consulta_sem_radical.count(entra_na_consulta_final)

# Calculta o TF_IDF da consulta
calcula_TF_IDF(dicionario_indice_consulta_final, dIDF, dconsulta_final_TF_IDF, listconsulta_final)


#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
            #*#*#*#*#*#*#*#*#*#------ CALCULANDO A SIMILARIDADE ------- #*#*#*#*#*#*#*#*#*#

for percorre_consulta in dconsulta_final_TF_IDF:
    for consulta_chave, consulta_valor in dconsulta_final_TF_IDF[percorre_consulta].items():
        consulta_valor_quadrado = math.pow(consulta_valor,2)
        soma_consulta = soma_consulta + consulta_valor_quadrado
    raiz_consulta = math.sqrt(soma_consulta)

for percorre_arquivos in meu_tf_idf:
    soma = 0
    soma2 = 0
    for percorre_consulta in dconsulta_final_TF_IDF:
        for termo_chave, tf_idf_termo_chave in meu_tf_idf[percorre_arquivos].items():
            for consulta_chave, consulta_valor in dconsulta_final_TF_IDF[percorre_consulta].items():
                if consulta_chave == termo_chave:
                    multipesos = consulta_valor*tf_idf_termo_chave
                    soma = soma + multipesos
                numerador[percorre_arquivos] = soma

            tf_idf_termo_chave_quadrado = math.pow(tf_idf_termo_chave,2)
            soma2 = soma2 + tf_idf_termo_chave_quadrado
        raizarq = math.sqrt(soma2)
        denominador[percorre_arquivos] = raizarq * raiz_consulta
        similaridade[percorre_arquivos] = numerador[percorre_arquivos]/denominador[percorre_arquivos]

            #*#*#*#*#*#*#*#*#*#------ CALCULANDO A SIMILARIDADE ------- #*#*#*#*#*#*#*#*#*#
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*


# Ordenando a similaridade do maior para o menor em um vetor que contém o nome do arquivo e sua similaridade com a consulta
sim = sorted (similaridade.items(), key=operator.itemgetter(1), reverse=True)

# Criando o arquivo resposta.txt, que deve mostrar a quantidade de arquivos que correspondem a consulta
# Bem como, seus nomes e suas similaridades com a consulta
# A variável válidos, são todos os documentos similares à consulta, porém se essa similaridade for menor que 0.001, válidos decrementa
# validos é a quantidade de arquivos que respondem a minha consulta de uma maneira mais eficaz 
validos = len(sim)
with open('resposta.txt', 'w') as resposta:
    for s in sim:
        if s[1] < 0.001:
            validos-= 1
    resposta.write(str(validos))
    for s in sim:
        if s[1] >= 0.001:
            resposta.write("\n" + s[0] + " " + str(s[1]))