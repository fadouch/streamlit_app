import streamlit as st
import base64

page_bg_img = """
<style>
[data-testid="stSidebar"] {
background-image:
url("https://images.unsplash.com/photo-1539622106114-e0df812097e6?q=80&w=1335&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: cover;
}


[data-testid="stSidebarNavLink"] {
background-color:#EEF6F5;
}
</style>"""
st.markdown(page_bg_img, unsafe_allow_html=True)
if __name__ == "__main__":

    # Fonction pour générer le lien de téléchargement du fichier PDF
    def create_download_link(pdf_file, label="Télécharger le PDF"):
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
            b64 = base64.b64encode(pdf_bytes).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_file}" target="_blank">{label}</a>'
        return href

    # Chemin vers le fichier PDF
    pdf_file_path = "Dashboard.pdf"

    # Titre de l'application
    st.title("")
    st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Exporter le contenu de notre  dashboard.</h1>", unsafe_allow_html=True)

    # Bouton de téléchargement
    download_button = st.button("Télécharger le PDF")

    # Afficher le lien de téléchargement lorsque le bouton est cliqué
    if download_button:
        st.markdown(create_download_link(pdf_file_path), unsafe_allow_html=True)
