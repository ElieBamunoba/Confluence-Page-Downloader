# Confluence Page Downloader

This Python script allows you to download the content of a Confluence page and its sub-pages, saving them as HTML files. The files are named using the page ID and title for easy identification.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library

You can install the required libraries using pip:

```bash
pip install requests python-dotenv
```

## Setup

### Clone the repository:
```
git clone https://github.com/your-username/confluence-page-downloader.git
cd confluence-page-downloader
```

Create a .env file in the project directory:
```bash
 touch .env 
 ```

Add your Confluence configuration to the .env file:
```bash
BASE_URL=https://your-confluence-instance.atlassian.net/wiki
EMAIL=your-email@example.com
API_TOKEN=your_api_token_here
```
Replace https://your-confluence-instance.atlassian.net/wiki, your-email@example.com, and your_api_token_here with your Confluence base URL, email, and API token, respectively.

## Usage
```bash
python download_confluence_pages.py
```
By default, the script will download the page with ID 33167 and its sub-pages. You can modify the PAGE_ID variable in the script to download a different page.

## Check the output:

The downloaded pages will be saved in a directory named page_<PAGE_ID>_content, where <PAGE_ID> is the ID of the main page you specified. Each file will be named using the format <page_id>_<page_title>.html.

## Script Overview
- get_current_user(): Fetches the current user's information.
- get_page_content(page_id): Fetches the content of a specified page.
- get_sub_pages(page_id): Fetches the list of child pages for a specified page.
- sanitize_filename(filename): Sanitizes a string to be used as a filename by replacing invalid characters.
- download_page_content(page_id, page_title, output_filename): Downloads the content of a page and saves it as an HTML file.
- download_page_and_subpages(page_id, output_dir): Downloads a page and its sub-pages, saving them in a specified directory.
## Notes
Make sure to handle your API token securely and do not expose it publicly.
Adjust the script as needed to fit your specific requirements.
## Contributing
Feel free to submit issues or pull requests if you have any suggestions or improvements.

## License
This project is licensed under the MIT License.
