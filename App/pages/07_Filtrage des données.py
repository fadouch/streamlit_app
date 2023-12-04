import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd
from folium import plugins

# Charger le GeoDataFrame depuis le fichier GeoParquet
gdf = gpd.read_parquet('DATA.parquet')
st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Découvrez les données géographiques à l'aide de filtres interactifs et observez les marqueurs sur la carte.</h1>", unsafe_allow_html=True)
st.write("Utilisez les contrôles ci-dessous pour ajuster les coordonnées spatiales et explorer les événements géographiques.")

# Créer deux colonnes pour les latitudes et les longitudes
col_lat_min, col_lat_max = st.columns(2)
col_lon_min, col_lon_max = st.columns(2)

# Exclure les lignes avec des valeurs NaN dans les colonnes de géométrie
filtered_gdf = gdf.dropna(subset=['Geometry'])
# Vérifier si le GeoDataFrame filtré n'est pas vide
if not filtered_gdf.empty:
    # Sélection des bornes spatiales pour les latitudes
    min_lat = col_lat_min.number_input("Latitude minimale", float(filtered_gdf['Geometry'].bounds.miny.min()), float(filtered_gdf['Geometry'].bounds.maxy.max()))
    max_lat = col_lat_max.number_input("Latitude maximale", float(filtered_gdf['Geometry'].bounds.miny.min()), float(filtered_gdf['Geometry'].bounds.maxy.max()))

    # Sélection des bornes spatiales pour les longitudes
    min_lon = col_lon_min.number_input("Longitude minimale", float(filtered_gdf['Geometry'].bounds.minx.min()), float(filtered_gdf['Geometry'].bounds.maxx.max()))
    max_lon = col_lon_max.number_input("Longitude maximale", float(filtered_gdf['Geometry'].bounds.minx.min()), float(filtered_gdf['Geometry'].bounds.maxx.max()))

    # Filtrer les données en fonction des bornes spatiales
    filtered_gdf = filtered_gdf.cx[min_lon:max_lon, min_lat:max_lat]

    # Vérifier si le GeoDataFrame filtré n'est pas vide après la nouvelle requête spatiale
    if not filtered_gdf.empty:
        # Créer une carte centrée sur la zone sélectionnée
        m = folium.Map(location=[filtered_gdf['Geometry'].y.mean(), filtered_gdf['Geometry'].x.mean()], zoom_start=6)

        # Utiliser MarkerCluster pour regrouper les marqueurs
        marker_cluster = folium.plugins.MarkerCluster(name="Points").add_to(m)

        # Ajouter les marqueurs filtrés à la carte avec des informations de popup
        for index, row in filtered_gdf.iterrows():
            # Créer le contenu du popup
            popup_content = f"""
                <b>Point:</b> {index}<br>
                <b>Date(0):</b> {row['Date(jour0)']}<br>
                <b>Type d'Événement:</b> {row["Type d'Événement"]}<br>
                <b>Gravité de l'événement:</b> {row["Gravité de l'événement"]}<br>
                <b>Variation Temporelle:</b> {row['Variation Temporelle']}<br>
            """

            # Ajouter le marqueur au cluster avec le popup
            folium.Marker(
                location=[row['Geometry'].y, row['Geometry'].x],
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(marker_cluster)

        # Ajout d'une mini-carte
        minimap = folium.plugins.MiniMap()
        m.add_child(minimap)
        # Ajout d'une couche de carte satellite (Mapbox Satellite)
        folium.TileLayer(
            tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiemFpbmFibyIsImEiOiJjbHBhMHpkMGcwMndxMmpsc3lmdjZrZjA5In0.mV-R22EqLzc4ww5IrGoXBA',
            attr='Mapbox',
            name='Satellite',
        ).add_to(m)

              
        # Ajout de la position de la souris
        mouse_position = plugins.MousePosition(position='bottomleft')
        m.add_child(mouse_position)

        # Ajout du contrôle de plein écran
        fullscreen = plugins.Fullscreen()
        m.add_child(fullscreen)

        # Ajout du contrôle de commutation de couche
        folium.LayerControl().add_to(m)

        # Ajout du contrôle de mesure
        measure_control = plugins.MeasureControl(primary_length_unit='kilometers', primary_area_unit='hectares')
        m.add_child(measure_control)

        # Afficher la carte dans Streamlit
        st.write("Carte filtrée avec informations sur chaque point :")
        folium_static(m)
    else:
        st.warning("Aucune donnée disponible pour les critères de filtre sélectionnés.")
else:
    st.warning("Aucune donnée disponible après avoir exclu les lignes avec des valeurs manquantes dans les colonnes de géométrie.")
