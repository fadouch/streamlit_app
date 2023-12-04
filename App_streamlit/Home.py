import streamlit as st
st.set_page_config(
    page_title="Dashboard",
)


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

    # CSS pour améliorer l'affichage
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .centered {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    # Titre de la page
    st.markdown("<h1 style='text-align: center; color: #1AB29D;'>Bienvenue sur notre Dashboard géoanalytique !</h1>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<h2 style='text-align: left; color: #9B9B9B;'>Projet GeoAnalytique Dashboard</h2>", unsafe_allow_html=True)

    # Description du projet
    st.write("""
    Notre projet GeoAnalytique Dashboard utilise Streamlit pour visualiser des données spatio-temporelles. 
    Nous avons créé un ensemble de données fictives avec des propriétés géospatiales et temporelles que nous affichons de manière interactive.
    Naviguez entre nos différentes pages, explorez les cartes, utilisez le slider pour naviguer entre les jours et profitez des fonctionnalités avancées du dashboard.
    """)

    # Section d'information personnelle
    st.markdown("<h2 style='text-align: left; color: #9B9B9B;'>À propos de nous</h2>", unsafe_allow_html=True)


    # Ajouter vos noms et photos avec le texte en dessous
    col1, col2 = st.columns(2)

    # Image et nom du premier membre
    with col1:
        st.image("za.jpg", width=150, caption="Abboubi Zaineb - 3CI TOPO", use_column_width=True)

    # Image et nom du deuxième membre
    with col2:
        st.image("fa1.jpg", width=150, caption="El Fettahi Fadwa - 3CI TOPO", use_column_width=True)

    # Section Aperçu Général
    st.markdown("<h2 style='text-align: left; color: #9B9B9B;'>Aperçu Général</h2>", unsafe_allow_html=True)

    # Ajouter une brève description de votre projet
    st.info("""
    **Notre projet GeoAnalytique Dashboard** utilise Streamlit pour visualiser des données spatio-temporelles. 
    Nous avons créé un ensemble de données fictives avec des propriétés géospatiales et temporelles que nous affichons de manière interactive.
    Naviguez entre nos différentes pages, explorez les cartes, utilisez le slider pour naviguer entre les jours et profitez des fonctionnalités avancées du dashboard.
    """)

    # Section Commentaires des Visiteurs
    st.markdown("<h2 style='text-align: left; color: #9B9B9B;'>Commentaires des Visiteurs</h2>", unsafe_allow_html=True)

    # Ajouter un formulaire de commentaire
    comment = st.text_area("Laissez un commentaire")

    # Bouton pour soumettre le commentaire
    if st.button("Soumettre le commentaire"):
        # Vous pouvez stocker le commentaire dans une base de données ou fichier
        st.success("Commentaire soumis avec succès!")
