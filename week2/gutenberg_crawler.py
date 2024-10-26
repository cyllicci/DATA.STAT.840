import requests
import bs4
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

Gutenberg_home_page_url = 'https://www.gutenberg.org'
Gutenberg_top_page_url = Gutenberg_home_page_url + '/browse/scores/top'

if not os.path.exists("downloaded_books"):
    os.makedirs("downloaded_books")

lemmatizer = WordNetLemmatizer()

def getpagetext(parsedpage):
    scriptelements=parsedpage.find_all('script')
    for scriptelement in scriptelements:
        scriptelement.extract()
    pagetext=parsedpage.get_text()
    return pagetext

def parse_webpage(url):
    try:
        response=requests.get(url, timeout=10)
        response.raise_for_status()
        parsed_html=bs4.BeautifulSoup(response.content,'html.parser')
        return parsed_html
    except requests.exceptions.RequestException as e:
        print(f"Error fetcing {url}: {e}" )
        return None

def extract_actual_book_content(read_online_url, book_title):
    parsed_html = parse_webpage(read_online_url)
    if parsed_html is None:
        return ""
    full_text = getpagetext(parsed_html)
    HEADER_TEXT_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK " + book_title.upper() + " ***"
    FOOTER_TEXT_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK " + book_title.upper() + " ***"
    start_index = full_text.find(HEADER_TEXT_MARKER) + len(HEADER_TEXT_MARKER)
    end_index = full_text.find(FOOTER_TEXT_MARKER)
    return full_text[start_index:end_index].strip()

def crawl_ebook(relative_link, author, title):
    e_book_url = Gutenberg_home_page_url + relative_link
    parsed_html = parse_webpage(e_book_url)

    read_online_link = parsed_html.find('a', title='Read online')['href']
    actual_content = extract_actual_book_content(Gutenberg_home_page_url + read_online_link, title)
    save_text_to_file(author, title, actual_content)

def save_text_to_file(author, title, content):
    clean_title = ''.join(c for c in title if c.isalnum() or c.isspace()).replace(' ', '_')
    file_path = os.path.join("downloaded_books", f"{clean_title}")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"saved {title} by {author} to {file_path}")
    except OSError as e:
        print(f"Error saving {title} by {author} to {file_path}: {e}")

def get_author_and_title(relative_link):
    e_book_url = Gutenberg_home_page_url + relative_link
    parsed_html = parse_webpage(e_book_url)

    if parsed_html is None:
        return "Unknown Author", "Unknown Title"

    try:
        book_author = parsed_html.find('a', itemprop="creator").text.strip()
        book_title = parsed_html.find('td', itemprop="headline").text.strip()
    except AttributeError:
        print(f"Error parsing author or title for {relative_link}")
        return "Unknown Author", "Unknown Title"
    
    return book_author, book_title

def get_author_and_title_list(relative_links):
    author_title_pairs = []
    for link in relative_links:
        author, title = get_author_and_title(link)
        author_title_pairs.append((author, title))
    return author_title_pairs

def print_book_list(books):
    for idx, (author, title) in enumerate(books, 1):
        print(f"{idx}. Author: {author}, Title: {title}")

def gutenberg_top_k_ebook_crawler(top_page_url, k):
    parsed_html = parse_webpage(top_page_url)

    books_last_30_header = parsed_html.find('h2', id='books-last30')
    book_list = books_last_30_header.find_next('ol')
    book_items = book_list.find_all('li')
    e_book_links = []
    for book_item in book_items[0:k]:
        a_element = book_item.find_next('a')
        e_book_links.append(a_element['href'])
    print("Books that will be downloaded:")
    books = get_author_and_title_list(e_book_links)
    print_book_list(books)

    print()

    for i, (link, (author, title)) in enumerate(zip(e_book_links, books)):
        print(f"Downloading book {i+1}/{k}: {title} by {author}")
        crawl_ebook(link, author, title)

def tokenize_and_lemmatize(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def process_books(directory="downloaded_books"):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encodings='utf-8') as file:
            text = file.read()
            lemmatized_tokens = tokenize_and_lemmatize(text)
            print(f"\nTokenized and lemmatized text for {filename}:\n", lemmatized_tokens[:50])  # Show first 50 tokens

def main():
    gutenberg_top_k_ebook_crawler(Gutenberg_top_page_url, 20)
    process_books()

main()