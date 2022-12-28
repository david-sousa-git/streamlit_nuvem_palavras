# pip install spacy
# python -m spacy download pt
import spacy
pln = spacy.load('pt_core_news_sm')
import re
import string
# pip install wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

###################################################################################################
stop_words = spacy.lang.pt.stop_words.STOP_WORDS
# palavras que não tem significado para as frases

###################################################################################################
def pre_processamento(texto):
  texto = texto.lower()
  
  texto = re.sub(r'@[A-Za-z0-9$-_@.&+]+', ' ', texto)
    # começa com @
    # seguido do nome de usuário: A-Z | a-z | 0-9 | $ | - | _ | @ | .| & | +
    # +, pois pode ter mais de um caractere
    # substuir por espaço em branco

  texto = re.sub(r'https?://[A-Za-z0-9./]+', ' ', texto)
  # ?, pois pode ou não ter o s

  texto = re.sub(r'[+-]?[0-9.]', ' ', texto)
  # retirando os números

  texto = re.sub(r' +', ' ', texto)
  # quando encontra mais de um espaço em branco, substituir por apenas 1

  documento = pln(texto)
  lista = []

  for palavra in documento:  # 'David corre correndo' -> ['David', 'correr']
      lista.append(palavra.lemma_)
      # Lematização. Tem como objetivo reduzir uma palavra à sua forma base e agrupar diferentes formas da mesma palavra.
      # Por exemplo, as palavras “correr", "corre" e "correu" são todas formas da palavra "correr"

  lista = [palavra for palavra in lista if 
            palavra not in stop_words and 
            palavra not in string.punctuation and 
            palavra != '-PRON-' and
            ' ' not in palavra
          ]
  # removendo as stop_words e as pontuações
  # removendo a palavra -PRON- que a lematização coloca quando não encontra um lemma : PRONOME

  textos_positivos_unica_string = ' '.join([str(elemento) for elemento in lista])
  # juntando com espaço em branco

  return textos_positivos_unica_string

def gerar_nuvem_txt(texto_processado):
  plt.figure(figsize=(120, 60))
  fig = plt.imshow(WordCloud().generate(texto_processado))

  buf = io.BytesIO()
  fig.figure.savefig(buf, format='png')

  buf.seek(0)

  return buf.getvalue(), buf