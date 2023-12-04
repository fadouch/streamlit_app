import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import os

# Charger les images de carte pour une date spécifique et un phénomène donné
def load_map(date, phenomenon, day_offset):
    # Générer le chemin du fichier en fonction du phénomène et de l'offset du jour
    path = f"cartes intepolees/{date}_{phenomenon}_{day_offset}_cog.tif"
    
    try:
        # Vérifier si le fichier existe
        if os.path.exists(path):
            return path
        else:
            return None
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image : {str(e)}")
        return None

# Fonction principale Streamlit
def main():
    st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Application de Cartes Météo</h1>", unsafe_allow_html=True)

    # Introduction
    st.caption(
    "Explorez les variations spatiales des événements météorologiques tels que l'humidité, la température "
    "et les précipitations à travers le temps. Utilisez les options de sélection pour choisir la date, "
    "le phénomène météorologique et naviguez entre les différents jours. Les cartes sont générées à partir "
    "de données interpolées, offrant ainsi une visualisation dynamique et informative."
    )

    # Sélection de la date
    selected_date = st.selectbox("Sélectionner la date", ["2023-07-01", "2023-08-01", "2023-09-01"])

    # Sélection du phénomène
    selected_phenomenon = st.selectbox("Sélectionner le phénomène", ["humidity", "precipitation", "temperature"])

    # Slider pour la navigation entre les cartes
    day_offset = st.slider("Sélectionner le jour (aujourd'hui = 0, hier = -1, etc.)", -6, 0, 0)

    # Calcul de la date basée sur le décalage
    selected_date_index = selected_date  # Ajustez si nécessaire

    # Charger et afficher l'image pour le jour sélectionné
    carte_image = load_map(selected_date_index, selected_phenomenon, day_offset)

    # Créer la carte Leafmap avec le centre sur le Maroc et un zoom plus faible
    m = leafmap.Map(height=600, center=[31.7917, -7.0926], zoom=8)

    # Ajouter l'image à la carte
    if carte_image is not None:
        layer_name = "Image 1"
        m.add_raster(carte_image, colormap="terrain", layer_name=layer_name)

        # Ajouter une légende avec un dégradé de couleurs
        if selected_phenomenon == "temperature":
            colors = ["#fff51a", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15","#67000d"]
            m.add_colorbar(colors=colors, vmin=0, vmax=50, layer_name=layer_name, caption="Température (°C)")
        elif selected_phenomenon == "precipitation":
            colors = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"]
            m.add_colorbar(colors=colors, vmin=0, vmax=20, layer_name=layer_name, caption="Précipitations (mm)")
        elif selected_phenomenon == "humidity":
            colors = ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"]
            m.add_colorbar(colors=colors, vmin=0, vmax=100, layer_name=layer_name, caption="Humidité (%)")
        
    else:
        st.error("Carte non trouvée pour la date, le phénomène et l'offset du jour sélectionnés.")

    # Afficher la carte avec Streamlit
    folium_static(m)

if __name__ == "__main__":
    main()
