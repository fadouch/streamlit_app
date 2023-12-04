import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import os
from folium import plugins
import folium

# Créez la carte Leafmap
m = leafmap.Map(height=600, center=[39.4948, -108.5492], zoom=12)

# Charger les images de carte pour une date spécifique et un phénomène donné
def load_map(date, phenomenon, day_offset):
    try:
        # Générer les chemins des fichiers en fonction de la date, du phénomène et de l'offset du jour
        path1 = f"cartes intepolees/{date}_{phenomenon}_{day_offset}_cog.tif"
        path2 = f"cartes intepolees/{date}_{phenomenon}_{day_offset-1}_cog.tif"
        
        # Vérifier si les fichiers existent
        if os.path.exists(path1) and os.path.exists(path2):
            return path1, path2
        else:
            return None, None
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image : {str(e)}")
        return None, None

# Fonction principale Streamlit
def main():
    st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Exploration Dynamique de Cartes : Comparaison Évolutive d'un événement entre Deux Jours.</h1>", unsafe_allow_html=True)

    # Introduction
    st.write(
    "Bienvenue dans notre application d'exploration dynamique de cartes. "
    "Comparez de manière évolutive les données des événements telles que l'humidité, la température et les précipitations "
    "à travers le temps."
    )


    # Sélection de la date
    selected_date = st.selectbox("Sélectionner la date", ["2023-07-01", "2023-08-01", "2023-09-01"])

    # Sélection du phénomène
    selected_phenomenon = st.selectbox("Sélectionner le phénomène", ["humidity", "precipitation", "temperature"])

     # Explication du slider
    st.write(
        "Utilisez le slider ci-dessous pour naviguer entre les cartes. L'image de gauche représente "
        "le jour sélectionné, tandis que l'image de droite est celle du jour précédent."
    )

    # Slider pour la navigation entre les cartes
    day_offset = st.slider("Sélectionner le jour (aujourd'hui = 0, hier = -1, etc.)", -5, 0, 0)

    # Calcul de la date basée sur le décalage
    selected_date_index = selected_date  # Ajustez si nécessaire

    # Charger et afficher les images pour le jour sélectionné et le jour précédent
    carte_image1, carte_image2 = load_map(selected_date_index, selected_phenomenon, day_offset)

    # Ajouter les images à la carte
    if carte_image1 is not None and carte_image2 is not None:
        layer_name1 = "Image 1"
        layer_name2 = "Image 2"
        m.add_raster(carte_image1, colormap="terrain", layer_name=layer_name1)
        m.add_raster(carte_image2, colormap="terrain", layer_name=layer_name2)

    m.split_map(carte_image1, carte_image2)

    # Ajout d'une couche de carte satellite (Mapbox Satellite)
    folium.TileLayer(
            tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiemFpbmFibyIsImEiOiJjbHBhMHpkMGcwMndxMmpsc3lmdjZrZjA5In0.mV-R22EqLzc4ww5IrGoXBA',
            attr='Mapbox',
            name='Satellite',
            ).add_to(m)
    
    # Ajout de la position de la souris
    mouse_position = plugins.MousePosition(position='bottomright')
    m.add_child(mouse_position)

    # Ajout du contrôle de commutation de couche
    folium.LayerControl().add_to(m)

    folium_static(m)

    

if __name__ == "__main__":
    main()
