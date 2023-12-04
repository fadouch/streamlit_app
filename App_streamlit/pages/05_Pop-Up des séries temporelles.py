import streamlit as st
import folium
from folium import plugins
import geopandas as gpd
from streamlit_folium import folium_static
import altair as alt
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd

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

    st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Explorez la Variation des Températures, des Précipitations et de l'Humidité à Travers le Temps :</h1>", unsafe_allow_html=True)

    # Charger le GeoDataFrame depuis le fichier GeoParquet
    gdf = gpd.read_parquet('DATA.parquet')

    # Sélection de la date (jour0) avec un selectbox
    selected_date = st.selectbox("Choisissez la date (jour0)", gdf['Date(jour0)'].unique())
    st.write("Cliquez sur un point de la carte pour afficher sa série temporelle des températures, des précipitations et de l'humidité.")

    # Filtrer les données en fonction de la date sélectionnée
    filtered_gdf = gdf[gdf['Date(jour0)'] == selected_date]

    # Créer une carte centrée sur le Maroc
    m = folium.Map(location=[gdf['Geometry'].y.mean(), gdf['Geometry'].x.mean()], zoom_start=6)

    # Utiliser MarkerCluster pour regrouper les marqueurs
    marker_cluster = plugins.MarkerCluster().add_to(m)

    # Fonction pour traiter une partition
    def process_partition(partition):
        markers = []
        for index, row in partition.iterrows():
            marker = folium.Marker(location=[row['Geometry'].y, row['Geometry'].x])
            
            # Création du graphique Altair
            data = {
                'Jour': list(range(-6, 1)),
                'Temperature(°C)': [row[f'temperatureJour{i}(°C)'] for i in range(-6, 1)],
                'Precipitations(cm/m²)': [row[f'precipitationJour{i}(cm/m²)'] for i in range(-6, 1)],
                'Humidité(%)': [row[f'humidityJour{i}(%)'] for i in range(-6, 1)]
            }
            
            df_chart = pd.DataFrame(data).melt('Jour')
            chart = alt.Chart(df_chart).mark_line().encode(
                x='Jour',
                y='value:Q',
                color='variable:N'
            ).properties(width=300, height=150)
            
            # Ajout du graphique dans le popup
            popup = folium.Popup(max_width=650).add_child(folium.VegaLite(chart, width=450, height=150))
            marker.add_child(popup)
            
            markers.append(marker)

        return markers

    # Diviser le GeoDataFrame en partitions (nombre de partitions à ajuster)
    num_partitions = 4
    gdf_partitions = np.array_split(filtered_gdf, num_partitions)

    # Traitement parallèle des partitions
    with ThreadPoolExecutor() as executor:
        all_markers = list(executor.map(process_partition, gdf_partitions))

    # Ajouter les marqueurs au cluster
    for markers in all_markers:
        for marker in markers:
            marker_cluster.add_child(marker)
            
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


    # Ajout du contrôle de plein écran
    fullscreen = plugins.Fullscreen()
    m.add_child(fullscreen)



    # Afficher la carte dans Streamlit
    folium_static(m)
    st.write('')
    st.subheader(" Ci-dessous, vous pouvez explorer les graphiques interactifs des séries temporelles des températures, des précipitations et de l'humidité, pour un point choisi.")

    # Sélection du point sur la carte
    selected_point = st.selectbox('Sélectionner un emplacement', gdf['Geometry'])

    # Récupération des données pour le point sélectionné
    selected_data = gdf[gdf['Geometry'] == selected_point].iloc[0]

    # Reformater les données pour le graphique
    formatted_data = pd.DataFrame({
        'Date': ['jour0', 'jour-1', 'jour-2', 'jour-3', 'jour-4', 'jour-5', 'jour-6'],
        'Température (°C)': [
            selected_data['temperatureJour0(°C)'],
            selected_data['temperatureJour-1(°C)'],
            selected_data['temperatureJour-2(°C)'],
            selected_data['temperatureJour-3(°C)'],
            selected_data['temperatureJour-4(°C)'],
            selected_data['temperatureJour-5(°C)'],
            selected_data['temperatureJour-6(°C)'],
        ],
        'Précipitations (cm/m²)': [
            selected_data['precipitationJour0(cm/m²)'],
            selected_data['precipitationJour-1(cm/m²)'],
            selected_data['precipitationJour-2(cm/m²)'],
            selected_data['precipitationJour-3(cm/m²)'],
            selected_data['precipitationJour-4(cm/m²)'],
            selected_data['precipitationJour-5(cm/m²)'],
            selected_data['precipitationJour-6(cm/m²)'],
        ],
        'Humidité (%)': [
            selected_data['humidityJour0(%)'],
            selected_data['humidityJour-1(%)'],
            selected_data['humidityJour-2(%)'],
            selected_data['humidityJour-3(%)'],
            selected_data['humidityJour-4(%)'],
            selected_data['humidityJour-5(%)'],
            selected_data['humidityJour-6(%)'],
        ],
    })

    # Création du script Highcharts
    highcharts_script = f"""
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/modules/data.js"></script>
        <div id="highchart-container" style="width:600px; height:400px;"></div>
        <script>
            var data = {formatted_data.to_json(orient='records')};
            Highcharts.chart('highchart-container', {{
                chart: {{
                    type: 'line'
                }},
                title: {{
                    text: 'Série temporelle'
                }},
                xAxis: {{
                    categories: data.map(entry => entry['Date'])
                }},
                yAxis: {{
                    title: {{
                        text: 'Valeurs'
                    }}
                }},
                series: [
                    {{
                        name: 'Température (°C)',
                        data: data.map(entry => entry['Température (°C)'])
                    }},
                    {{
                        name: 'Précipitations (cm/m²)',
                        data: data.map(entry => entry['Précipitations (cm/m²)'])
                    }},
                    {{
                        name: 'Humidité (%)',
                        data: data.map(entry => entry['Humidité (%)'])
                    }}
                ]
            }});
        </script>
    """

    # Affichage du graphique Highcharts
    st.components.v1.html(highcharts_script, height=500)


    st.write("Cliquez sur le marqueur de la carte pour afficher des informations détaillées sur l'emplacement choisi.")
    # Création de la carte avec Folium
    m = folium.Map(location=[selected_point.y, selected_point.x], zoom_start=8 )

    # Ajout d'une couche de carte satellite (Mapbox Satellite)
    folium.TileLayer(
        tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1IjoiemFpbmFibyIsImEiOiJjbHBhMHpkMGcwMndxMmpsc3lmdjZrZjA5In0.mV-R22EqLzc4ww5IrGoXBA',
        attr='Mapbox',
        name='Satellite',
    ).add_to(m)

    # Ajout d'un marqueur pour le point sélectionné avec une popup personnalisée
    popup_content = f"""
        <b>Point:</b> {selected_point}<br>
        <b>Date(0):</b> {selected_data['Date(jour0)']}<br>
        <b>Type d'Événement:</b> {selected_data["Type d'Événement"]}<br>
        <b>Gravité de l'événement:</b> {selected_data["Gravité de l'événement"]}<br>
        <b>Variation Temporelle:</b> {selected_data['Variation Temporelle']}<br>
        
    """

    folium.Marker([selected_point.y, selected_point.x], popup=folium.Popup(popup_content, max_width=300),).add_to(m)



    # Ajout d'une mini-carte
    minimap = folium.plugins.MiniMap()
    m.add_child(minimap)

    # Ajout de la position de la souris
    mouse_position = plugins.MousePosition(position='bottomleft')
    m.add_child(mouse_position)


            # Ajouter tous les points comme des cercles simples sans marqueurs
    marker_cluster = plugins.MarkerCluster(name="Points").add_to(m)
    for index, row in gdf.iterrows():
        folium.CircleMarker([row['Geometry'].y, row['Geometry'].x],radius=1.5, color='red', fill=True, fill_color='red').add_to(marker_cluster)


    # Ajout du contrôle de plein écran
    fullscreen = plugins.Fullscreen()
    m.add_child(fullscreen)

    # Ajout du contrôle de commutation de couche
    folium.LayerControl().add_to(m)

    # Affichage de la carte
    folium_static(m)