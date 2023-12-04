import streamlit as st
import base64
import leafmap

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
        gif_filename = f'carte_{selected_date}_humidity.gif'
    elif selected_attribute == "precipitation":
        images = f'cartes intepolees/{selected_date}_precipitation*.tif'
        gif_filename = f'carte_{selected_date}_precipitation.gif'
    elif selected_attribute == "temperature":
        images = f'cartes intepolees/{selected_date}_temperature*.tif'
        gif_filename = f'carte_{selected_date}_temperature.gif'
    else:
        st.write("Sélection non prise en charge.")

    # Génération du timelapse avec leafmap
    leafmap.create_timelapse(
        images,
        out_gif=gif_filename,
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
    st.write(f"**Le timelapse correspondant** :")

    # Affichage du timelapse généré
    width = 600
    st.markdown(f'<img src="data:image/gif;base64,{base64.b64encode(open(gif_filename, "rb").read()).decode()}" alt="timelapse" width="{width}">', unsafe_allow_html=True)
