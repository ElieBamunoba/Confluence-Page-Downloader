import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import re
import pdfkit

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
base_url = os.getenv('BASE_URL')
email = os.getenv('EMAIL')
api_token = os.getenv('API_TOKEN')

if not base_url or not email or not api_token:
    raise ValueError("BASE_URL, EMAIL, and API_TOKEN must be set in the .env file.")

auth = HTTPBasicAuth(email, api_token)
headers = {'Accept': 'application/json'}

def get_current_user():
    """Fetches the current user's information."""
    url = f'{base_url}/rest/api/user/current'
    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()
    return response.json()

def get_page_content(page_id):
    """Fetches the content of a page."""
    url = f"{base_url}/rest/api/content/{page_id}"
    response = requests.get(url, headers=headers, auth=auth, params={"expand": "body.storage"})
    response.raise_for_status()
    
    page_data = response.json()
    if 'body' not in page_data or 'storage' not in page_data['body']:
        print(f"Page {page_id} does not exist or is inaccessible.")
        return None
    return page_data

def get_sub_pages(page_id):
    """Fetches the list of child pages for a given page."""
    url = f"{base_url}/rest/api/content/{page_id}/child/page"
    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()
    return response.json().get('results', [])

def sanitize_filename(filename):
    """Sanitizes a string to be used as a filename."""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_page_content(page_id, page_title, output_filename_html, output_filename_pdf):
    """Downloads the page content and saves it as a .html and .pdf file."""
    page_data = get_page_content(page_id)
    if page_data is None:
        print(f"Failed to retrieve page {page_id}. Skipping.")
        return
    
    html_content = page_data["body"]["storage"]["value"]
    
    # Save the HTML content to a file
    with open(output_filename_html, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    # Convert HTML to PDF and save
    pdfkit.from_file(output_filename_html, output_filename_pdf)

def download_page_and_subpages(page_id, output_dir):
    """Downloads the page and its sub-pages."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the main page
    page_data = get_page_content(page_id)
    if page_data is None:
        return
    page_title = page_data['title']
    sanitized_title = sanitize_filename(page_title)
    output_filename_html = os.path.join(output_dir, f"{page_id}_{sanitized_title}.html")
    output_filename_pdf = os.path.join(output_dir, f"{page_id}_{sanitized_title}.pdf")
    download_page_content(page_id, page_title, output_filename_html, output_filename_pdf)
    
    # Fetch and download sub-pages
    sub_pages = get_sub_pages(page_id)
    for sub_page in sub_pages:
        sub_page_id = sub_page['id']
        sub_page_title = sub_page['title']
        sanitized_sub_title = sanitize_filename(sub_page_title)
        sub_output_filename_html = os.path.join(output_dir, f"{sub_page_id}_{sanitized_sub_title}.html")
        sub_output_filename_pdf = os.path.join(output_dir, f"{sub_page_id}_{sanitized_sub_title}.pdf")
        print(f"Downloading sub-page: {sub_page_title} (ID: {sub_page_id})")
        download_page_content(sub_page_id, sub_page_title, sub_output_filename_html, sub_output_filename_pdf)

if __name__ == "__main__":
    try:
        user_info = get_current_user()
        print(f"Your username is: {user_info.get('email', 'N/A')}")
        print(f"Your display name is: {user_info.get('displayName', 'N/A')}")
        
        PAGE_ID = '360449'
        OUTPUT_DIR = f"page_{PAGE_ID}_content"
        download_page_and_subpages(PAGE_ID, OUTPUT_DIR)
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
