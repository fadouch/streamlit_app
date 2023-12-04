import streamlit as st
import base64
import leafmap

# Titre de la page
st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Analyse des Données Météorologiques par les timelapses.</h1>", unsafe_allow_html=True)

st.caption("Explorez des timelapses interactifs offrant une visualisation dynamique des conditions météorologiques sur une période de 7 jours. "
         "Nos timelapses utilisent des cartes interpolées basées sur la méthode IDW pour fournir une représentation spatiale lissée des données météorologiques au Maroc.")


# Sélection de la date et de l'attribut

selected_date = st.selectbox("Sélectionner la date", ["2023-08-01", "2023-09-01", "2023-07-01"])
selected_attribute = st.selectbox("Choisissez le type de données à visualiser", ["temperature", "precipitation", "humidity"])

# Construction du chemin des images en fonction de la sélection de l'utilisateur
if selected_attribute == "humidity":
    images = f'cartes intepolees/{selected_date}_humidity*.tif'
elif selected_attribute == "precipitation":
    images = f'cartes intepolees/{selected_date}_precipitation*.tif'
elif selected_attribute == "temperature":
    images = f'cartes intepolees/{selected_date}_temperature*.tif'
else:
    st.write("Sélection non prise en charge.")

# Génération du timelapse avec leafmap
leafmap.create_timelapse(
    images,
    out_gif='carte.gif',
    bands=[0, 1, 2],
    fps=4,
    progress_bar_color='blue',
    add_text=True,
    text_xy=('3%', '3%'),  
    text_sequence=-6,
    font_size=50,
    font_color='white',
    mp4=False,
    reduce_size=False,
    transparent_background=True,
)

st.write("")
st.write("**Le timelapse correspondant** :")

# Affichage du timelapse généré
width = 600
st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(open("carte.gif", "rb").read()).decode()}" alt="timelapse" width="{width}">', unsafe_allow_html=True)

