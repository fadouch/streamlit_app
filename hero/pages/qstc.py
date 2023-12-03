import streamlit as st
import base64
import leafmap

# Sélection de la date et de l'attribut
selected_date = st.selectbox("Sélectionner la date", ["2023-07-01", "2023-08-01", "2023-09-01"])
selected_attribute = st.selectbox("Timelapse", ["temperature", "precipitation", "humidity"])

# Construction du chemin des images en fonction de la sélection de l'utilisateur
if selected_attribute == "humidity":
    images = f'pages/cartes intepolees_cog/{selected_date}_humidity_*_cog.tif'
elif selected_attribute == "precipitation":
    images = f'pages/cartes intepolees_cog/{selected_date}_precipitation_*_cog.tif'
elif selected_attribute == "temperature":
    images = f'pages/cartes intepolees_cog/{selected_date}_temperature_*_cog.tif'
else:
    st.write("Sélection non prise en charge.")

# Génération du timelapse avec leafmap
leafmap.create_timelapse(
    images,
    out_gif='carte.gif',
    bands=[0, 1, 2],
    fps=10,
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

# Affichage du timelapse généré
width = 600
st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(open("carte.gif", "rb").read()).decode()}" alt="timelapse" width="{width}">', unsafe_allow_html=True)
