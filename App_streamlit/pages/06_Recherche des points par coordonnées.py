import streamlit as st
import geopandas as gpd
from streamlit_folium import folium_static
import folium
from folium import plugins
from shapely.geometry import Point

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

    # Titre du code
    st.title("")
    st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Exploration Géographique : Recherche et Visualisation cartographique de Points Géographiques </h1>", unsafe_allow_html=True)

    # Charger le fichier GeoParquet
    gdf = gpd.read_parquet("DATA.parquet")

    # Widget pour saisir les coordonnées
    coord_input = st.text_input("Entrez les coordonnées (latitude, longitude) :", "")
    st.write("Exemple : 30.405, -8.098")

    # Rayon de proximité (ajustez selon vos besoins)
    proximity_radius = 0.01  # par exemple, 0.01 degré pour environ 1 km

    # Diviser les coordonnées saisies
    if coord_input:
        lat, lon = map(float, coord_input.split(','))
        st.write("Coordonnées saisies :", lat, lon)  # Affichage pour déboguer
        
        # Calculer la distance euclidienne entre les coordonnées saisies et chaque point
        gdf['distance'] = gdf['Geometry'].apply(lambda geom: Point(geom).distance(Point(lon, lat)))
        
        # Filtrer les points dans le rayon spécifié
        nearby_points = gdf[gdf['distance'] <= proximity_radius]
        
        # Afficher les résultats
        if not nearby_points.empty:
            st.write("Points trouvés ")

            # Créer une carte centrée sur les coordonnées saisies avec une précision limitée
            m = folium.Map(location=[round(lat, 3), round(lon, 3)], zoom_start=10)

            # Ajouter tous les points comme des cercles simples sans marqueurs
            marker_cluster = plugins.MarkerCluster(name="Points").add_to(m)

            for index, row in gdf.iterrows():
                folium.CircleMarker([row['Geometry'].y, row['Geometry'].x], radius=3, fill=True, color='blue').add_to(marker_cluster)

            # Ajout du point recherché comme un marqueur avec popup
            selected_point = nearby_points.iloc[0]['Geometry']
            selected_data = nearby_points.iloc[0]

            popup_content = f"""
                <b>Point:</b> {selected_point.x}, {selected_point.y}<br>
                <b>Date(0):</b> {selected_data['Date(jour0)']}<br>
                <b>Type d'Événement:</b> {selected_data["Type d'Événement"]}<br>
                <b>Gravité de l'événement:</b> {selected_data["Gravité de l'événement"]}<br>
                <b>Variation Temporelle:</b> {selected_data['Variation Temporelle']}<br>
            """

            folium.Marker([selected_point.y, selected_point.x], popup=folium.Popup(popup_content, max_width=300)).add_to(m)

            # Ajout d'une couche de carte satellite (Mapbox Satellite)
            folium.TileLayer(
                tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiemFpbmFibyIsImEiOiJjbHBhMHpkMGcwMndxMmpsc3lmdjZrZjA5In0.mV-R22EqLzc4ww5IrGoXBA',
                attr='Mapbox',
                name='Satellite',
                ).add_to(m)
        
            # Ajout d'une mini-carte
            minimap = folium.plugins.MiniMap()
            m.add_child(minimap)

            # Ajout de la position de la souris
            mouse_position = plugins.MousePosition(position='bottomleft')
            m.add_child(mouse_position)

            # Ajout du contrôle de commutation de couche
            folium.LayerControl().add_to(m)
            
            # Ajout du contrôle de plein écran
            fullscreen = plugins.Fullscreen()
            m.add_child(fullscreen)

            # Affichage de la carte
            folium_static(m)
            
        else:
            st.write("Aucun point trouvé dans le rayon spécifié.")
