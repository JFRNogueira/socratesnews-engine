import streamlit as st
from ebooklib import epub
from fpdf import FPDF
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
import base64

def epub_to_pdf(epub_file_path, pdf_file_path):
    # Carregar o livro EPUB
    book = epub.read_epub(epub_file_path)

    # Inicializar o PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Adicionar conteúdo do EPUB ao PDF
    for item in book.get_items():
        if item.get_type() == epub.EpubHtml:  # Processar apenas itens do tipo HTML
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text()  # Extrair texto sem tags HTML
            pdf.add_page()
            pdf.multi_cell(0, 10, text)

    # Salvar o PDF
    pdf.output(pdf_file_path)

# Função para criar link de download
def create_download_link(file_path, file_name):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{file_name}">Clique aqui para baixar o PDF</a>'

def main():
    st.title("Conversor de EPUB para PDF")

    st.write("Carregue um arquivo no formato EPUB e converta-o para PDF.")

    epub_file = st.file_uploader("Selecione um arquivo EPUB", type=["epub"])

    if epub_file is not None:
        with NamedTemporaryFile(delete=False, suffix=".epub") as temp_epub:
            temp_epub.write(epub_file.read())
            temp_epub_path = temp_epub.name

        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf_path = temp_pdf.name

        if st.button("Converter para PDF"):
            try:
                epub_to_pdf(temp_epub_path, temp_pdf_path)
                st.success("Conversão concluída com sucesso!")

                download_link = create_download_link(temp_pdf_path, "arquivo_convertido.pdf")
                st.markdown(download_link, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Ocorreu um erro durante a conversão: {e}")

if __name__ == "__main__":
    main()
