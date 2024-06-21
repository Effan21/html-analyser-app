import pandas as pd  
import streamlit as st  
from urllib.parse import urlparse, urljoin  


def is_valid_url(url):
    """
    Vérifie si une URL est valide.

    Parameters:
    - url (str): L'URL à vérifier.

    Returns:
    - bool: True si l'URL est valide, False sinon.
    """
    try:
        result = urlparse(url)
        return result.scheme in ['http', 'https'] and all([result.scheme, result.netloc])
    except ValueError:
        return False


def display_results(results):
    """
    Affiche les résultats de l'analyse d'une page web.

    Parameters:
    - results (dict): Dictionnaire contenant les résultats de l'analyse.

    """
    # Préparation des données pour afficher les informations principales sur la page
    data = [
        ("Version HTML", results['html_version']),
        ("Titre", results['title']),
        *[(level, count) for level, count in results['headings'].items()],
        ("Liens internes", results['internal_links']),
        ("Liens externes", results['external_links']),
        ("Contient un formulaire de connexion", 'Oui' if results['login_form'] else 'Non')
    ]

    # Création d'un DataFrame à partir des données
    df = pd.DataFrame(data)
    
    # Conversion du DataFrame en HTML sans index ni en-tête
    html_table = df.to_html(index=False, header=False)

    # Ajout de styles CSS pour le tableau principal
    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
            width: 50%;
        }
        
        td:nth-child(1) {
            color: white;  /* Couleur du texte pour la première colonne */
        }
        td:nth-child(2) {
            color: #33F6AF;  /* Couleur du texte pour la deuxième colonne */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Affichage du tableau principal
    st.write(html_table, unsafe_allow_html=True)

    # Ajout d'une ligne de séparation
    st.markdown("---")

    # Affichage des résultats de la validation des liens
    st.markdown("### Validation des liens")

    # Conversion des résultats de validation des liens en DataFrame
    link_validation_df = pd.DataFrame(results['link_validation'], columns=["Lien", "Type", "Disponible", "Raison"])
    link_validation_html = link_validation_df.to_html(index=True, header=True)

    # Ajout de styles CSS pour le tableau de validation des liens
    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #333;
            color: white;
        }
        td:nth-child(1) {
            color: white;  
        }
        td:nth-child(2) {
            color: #33F6AF;  
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Affichage du tableau de validation des liens
    st.write(link_validation_html, unsafe_allow_html=True)
