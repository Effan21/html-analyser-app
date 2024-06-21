import aiohttp
import asyncio
import streamlit as st
from bs4 import BeautifulSoup, Doctype
from urllib.parse import urlparse, urljoin

# Fonction asynchrone pour effectuer une requête HEAD à une URL donnée
async def fetch(session, url):
    try:
        # Effectue une requête HEAD pour obtenir les en-têtes de la réponse
        async with session.head(url, allow_redirects=True, timeout=5) as response:
            # Retourne le statut et la raison de la réponse
            return response.status, response.reason
    except Exception as e:
        # En cas d'exception, retourne None et le message d'erreur
        return None, str(e)

# Fonction asynchrone pour valider un lien
async def validate_link(session, base_url, link, link_type):
    # Construit l'URL complète en joignant l'URL de base et le lien
    full_url = urljoin(base_url, link)
    # Vérifie la disponibilité du lien en utilisant la fonction fetch
    status, reason = await fetch(session, full_url)
    # Retourne le lien, son type, un booléen indiquant s'il est accessible, et la raison de l'échec (le cas échéant)
    return (link, link_type, status == 200 if status is not None else False, reason)

# Fonction asynchrone pour analyser le HTML d'une page à une URL donnée
async def analyze_html(url):
    async with aiohttp.ClientSession() as session:
        # Effectue une requête GET pour obtenir le contenu de la page
        async with session.get(url) as response:
            # Lève une exception si le statut de la réponse indique une erreur HTTP
            response.raise_for_status()
            # Lit le contenu de la réponse
            content = await response.text()
            # Parse le contenu HTML avec BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')

            # Détection de la version HTML (approximation)
            doctype = next((d for d in soup.contents if isinstance(d, Doctype)), None)
            html_version = doctype if doctype else "Unknown"

            # Récupération du titre de la page
            title = soup.title.string.strip() if soup.title else "No title found"

            # Comptage du nombre de titres par niveau
            headings = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}

            # Initialisation des listes pour les liens internes et externes
            internal_links = []
            external_links = []
            # Récupération du domaine de base
            domain = urlparse(url).netloc

            # Parcours de tous les éléments <a> avec un attribut href
            for link in soup.find_all('a', href=True):
                link_url = link['href']
                # Classification des liens en internes et externes
                if urlparse(link_url).netloc == domain or not urlparse(link_url).netloc:
                    internal_links.append(link_url)
                else:
                    external_links.append(link_url)

            # Détection des formulaires de connexion
            login_forms = any(form for form in soup.find_all('form') if 'password' in str(form))

            # Préparation des tâches de validation des liens
            links_to_validate = [(link, "Interne") for link in internal_links] + [(link, "Externe") for link in external_links]
            tasks = [validate_link(session, url, link, link_type) for link, link_type in links_to_validate]
            # Exécution des tâches de validation des liens en parallèle
            validation_results = await asyncio.gather(*tasks)

            # Retour des résultats de l'analyse
            return {
                'html_version': html_version,
                'title': title,
                'headings': headings,
                'internal_links': len(internal_links),
                'external_links': len(external_links),
                'login_form': login_forms,
                'link_validation': validation_results
            }
