import streamlit as st
from utils import is_valid_url, display_results
from analyzer import analyze_html
import asyncio

def main():
    # Configuration de la page Streamlit
    st.set_page_config(
        page_title="HTML PAGE ANALYSER 🤖",  # Titre de la page
        page_icon=":robot:",                # Icône de la page
        layout="wide",                      # Disposition large de la page
        initial_sidebar_state="expanded"    # Barre latérale élargie par défaut
    )

    # Titre principal de l'application
    st.title("HTML PAGE ANALYSER 🤖")
    st.markdown("---")  # Ligne de séparation
    st.markdown("**Bienvenue !** Entrez l'URL de la page que vous souhaitez analyser")  # Message de bienvenue

    # Champ de texte pour l'entrée de l'URL par l'utilisateur
    user_input = st.text_input("URL:", key="user_input")

    # Bouton pour envoyer l'URL
    if st.button("Envoyer", key="send_button"):
        # Vérifie si l'URL entrée est valide
        if is_valid_url(user_input):
            # Si l'URL est valide, analyse la page HTML
            results = asyncio.run(analyze_html(user_input))
            if results:
                # Si des résultats sont obtenus, les affiche
                display_results(results)
        else:
            # Affiche une erreur si l'URL n'est pas valide
            st.error("Veuillez entrer une URL valide.")

# Exécution de la fonction main() lorsque le script est exécuté
if __name__ == '__main__':
    main()
