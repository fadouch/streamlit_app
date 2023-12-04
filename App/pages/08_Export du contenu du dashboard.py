import streamlit as st
import base64

# Fonction pour générer le lien de téléchargement du fichier PDF
def create_download_link(pdf_file, label="Télécharger le PDF"):
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_file}" target="_blank">{label}</a>'
    return href

# Chemin vers le fichier PDF
pdf_file_path = "dashboard_geoanalytique_2023-08-01_Type d'Événement.pdf"

# Titre de l'application
st.title("")
st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Exporter le contenu de notre  dashboard.</h1>", unsafe_allow_html=True)

# Bouton de téléchargement
download_button = st.button("Télécharger le PDF")

# Afficher le lien de téléchargement lorsque le bouton est cliqué
if download_button:
    st.markdown(create_download_link(pdf_file_path), unsafe_allow_html=True)
