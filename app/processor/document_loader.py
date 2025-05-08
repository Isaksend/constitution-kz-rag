import requests
from bs4 import BeautifulSoup
from langchain.schema import Document
import re
import tempfile
import os
from langchain.document_loaders import PyPDFLoader, TextLoader


def fetch_constitution():
    """Fetch the Constitution from the official website"""
    url = "https://www.akorda.kz/en/constitution-of-the-republic-of-kazakhstan-50912"

    try:
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the main content (adjust selectors based on actual website structure)
        content = soup.find('div', class_='content')
        if not content:
            # Fallback to body if specific content div not found
            content = soup.find('body')

        if not content:
            raise ValueError("Could not extract content from website")

        return content.get_text()
    except Exception as e:
        print(f"Error fetching constitution: {e}")
        return None


def split_by_articles(text):
    """Split text into documents by articles"""
    if not text:
        return []

    # Pattern to match article headers
    article_pattern = re.compile(r'Article (\d+)[.\s]')

    # Find all article positions
    article_matches = list(article_pattern.finditer(text))

    documents = []

    # If no articles found, create a single document
    if not article_matches:
        doc = Document(
            page_content=text,
            metadata={
                "source": "Constitution of Kazakhstan",
                "article": "General Text"
            }
        )
        documents.append(doc)
        return documents

    # Process each article
    for i in range(len(article_matches)):
        start_pos = article_matches[i].start()

        # Determine end position (either next article or end of text)
        if i < len(article_matches) - 1:
            end_pos = article_matches[i + 1].start()
        else:
            end_pos = len(text)

        # Extract article text
        article_text = text[start_pos:end_pos].strip()

        # Extract article number
        article_num = article_matches[i].group(1)

        # Create document with metadata
        doc = Document(
            page_content=article_text,
            metadata={
                "source": "Constitution of Kazakhstan",
                "article": f"Article {article_num}"
            }
        )

        documents.append(doc)

    return documents


def process_constitution():
    """Process the Constitution into documents"""
    constitution_text = fetch_constitution()
    if constitution_text:
        return split_by_articles(constitution_text)
    return []


def process_uploaded_file(file):
    """Process an uploaded file"""
    # Get file extension
    file_extension = file.name.split('.')[-1].lower()

    if file_extension == 'txt':
        # Process text file
        content = file.read().decode("utf-8")
        return split_by_articles(content)

    elif file_extension == 'pdf':
        # Process PDF file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(file.getbuffer())
            temp_path = temp.name

        # Use PyPDFLoader to load PDF
        loader = PyPDFLoader(temp_path)
        documents = loader.load()

        # Clean up temporary file
        os.unlink(temp_path)

        return documents

    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def process_multiple_files(files):
    """Process multiple uploaded files"""
    all_documents = []

    for file in files:
        try:
            documents = process_uploaded_file(file)
            all_documents.extend(documents)
        except Exception as e:
            print(f"Error processing file {file.name}: {e}")

    return all_documents