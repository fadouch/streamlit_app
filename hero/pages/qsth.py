import streamlit as st
import subprocess
import base64
def convert_to_cog(input_path, output_path):
    # Utilisez la commande rio cogeo create pour convertir le GeoTIFF en COG
    subprocess.run([
        "rio",
        "cogeo",
        "create",
        input_path,
        output_path,
        "--co",
        "overview_level=6"
    ])

def main():
    st.title("Conversion de GeoTIFF en COG")

    # Sélection du fichier GeoTIFF à convertir
    uploaded_file = st.file_uploader("Téléchargez votre fichier GeoTIFF", type=["tif"])

    if uploaded_file is not None:
        st.write("Fichier GeoTIFF sélectionné :", uploaded_file.name)

        # Afficher un bouton pour lancer la conversion
        if st.button("Convertir en COG"):
            try:
                # Sauvegarder le fichier GeoTIFF téléchargé
                with open("uploaded_geotiff.tif", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Chemin d'entrée pour le fichier GeoTIFF téléchargé
                input_geotiff = "uploaded_geotiff.tif"

                # Chemin de sortie pour le fichier COG généré
                output_cog = "converted_cog.tif"

                # Convertir le GeoTIFF en COG
                convert_to_cog(input_geotiff, output_cog)

                # Afficher le lien de téléchargement pour le COG généré
                st.success("Conversion réussie ! Téléchargez le COG généré.")
                st.markdown(get_binary_file_downloader_html(output_cog), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Erreur lors de la conversion : {str(e)}")

def get_binary_file_downloader_html(bin_file, file_label='Télécharger COG'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}">Cliquez ici pour télécharger</a>'
    return href

if __name__ == "__main__":
    main()
