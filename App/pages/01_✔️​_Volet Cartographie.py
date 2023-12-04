import streamlit as st
import geopandas as gpd
import plotly.express as px


# Charger les données GeoParquet
gdf = gpd.read_parquet('DATA.parquet')

# Afficher le titre de l'application
st.markdown("<h1 style='text-align: left; color: #1AB29D;'>Bienvenue dans le Dashboard GeoAnalytique!</h1>", unsafe_allow_html=True)

st.write(
    """
    Explorez les données géographiques en sélectionnant une date
    et une colonne à cartographier. Utilisez les options ci-dessous pour personnaliser votre expérience.
    """
)

# Sélection de la date
selected_date = st.selectbox("Choisissez la date (jour0)", gdf['Date(jour0)'].unique())

# Sélection de la colonne à cartographier
selected_column = st.selectbox(
    "Choisissez la colonne à cartographier",
    ["Type d'Événement", 'Gravité de l\'événement', 'Variation Temporelle', 'humidityJour0(%)', 'precipitationJour0(cm/m²)', 'temperatureJour0(°C)']
)

# Filtrer le DataFrame en fonction de la date sélectionnée
filtered_gdf = gdf[gdf['Date(jour0)'] == selected_date]

# Vérifier si le DataFrame filtré n'est pas vide
if not filtered_gdf.empty:
    # Création de la carte avec Plotly Express
    fig = px.scatter_mapbox(
        filtered_gdf,
        lat=filtered_gdf.geometry.y,
        lon=filtered_gdf.geometry.x,
        color=selected_column,  # Utiliser la colonne sélectionnée pour la couleur
        hover_name="Type d'Événement",
        title=f"Carte - {selected_column} ({selected_date})",
        height=600
    )
    fig.update_layout(mapbox_style="carto-positron")


    # Ajout de la ligne pour ajuster le niveau de zoom avec Mapbox
    fig.update_mapboxes(center=dict(lat=filtered_gdf.geometry.y.mean(), lon=filtered_gdf.geometry.x.mean()), zoom=4)

     # Ajout de la phrase sous le titre
    fig.add_annotation(
        text="Pour la carte du type d'événement, double cliquez sur la légende pour isoler une trace.",
        showarrow=False,
        xref="paper", yref="paper",
        x=0, y=-0.1
    )

    # Affichage de la carte avec Streamlit
    st.plotly_chart(fig)
else:
    st.warning("Aucune donnée disponible pour la date sélectionnée.")
