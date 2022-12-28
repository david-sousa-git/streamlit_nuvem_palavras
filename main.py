import functions_gcp as fgcp
import streamlit as st
import functions_txt as ftxt
from io import StringIO
from PIL import Image 
from datetime import datetime

st.image('https://img.freepik.com/free-vector/cartoon-word-cloud-blue-sky-heaven_107791-6354.jpg?w=2000')
st.title('Nuvem de Palavras')

fileTxt = st.file_uploader(label = "Por favor, suba o arquivo .txt 📝 aqui! ", type=['txt'])


if fileTxt:
    try:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        nome_arquivo = fileTxt.name + dt_string + '.png'
        nome_arquivo = nome_arquivo.replace('/', '_')

        stringio = StringIO(fileTxt.getvalue().decode("utf-8"))
        string_data = stringio.read()
        
        texto_processado = ftxt.pre_processamento(string_data)

        nuvem_txt, buf = ftxt.gerar_nuvem_txt(texto_processado)

        fgcp.upload_blob_from_memory('nuvens_de_palavras', 
                nuvem_txt, 
                nome_arquivo)

        image = Image.open(buf)
        st.image(image, caption='Imagem gerada com sucesso ✅')
    except:
        st.error('Algo deu errado. Tente novamente.', icon="🚨")



                