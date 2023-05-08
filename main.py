import requests
from bs4 import BeautifulSoup
import json


def extract_conversation(url, conversation_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
    conversations = []

    # Find all <span> elements with class "field--name-title"
    for span in soup.find_all('span', class_='field--name-title'):
        # Get the text content of the span element
        span_content = span.get_text(strip=True)
        # Add the span content to the conversations list as a "soru" message
        conversations.append({
            "from": "soru",
            "value": span_content
        })

    # Find all <div> elements with class "article-detail-content"
    for div in soup.find_all('div', class_='article-detail-content'):
        # Get the text content of the div element (excluding any subtags)
        div_content = ''.join(div.find_all(string=True)).strip()
        # Add the div content to the conversations list as a "cevap" message
        conversations.append({
            "from": "cevap",
            "value": div_content
        })

    # Create a conversation JSON object with the given ID and the extracted messages
    conversation = {
        "id": conversation_id,
        "conversations": conversations
    }

    return conversation


num_of_pages = input("Kaç sayfalık soru-cevap çekmek istersiniz: ")
url = f'https://bilimgenc.tubitak.gov.tr/koselerimiz/soru-cevap?page={num_of_pages})'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')

# Find all <div> elements with class "article"
divs = soup.find_all('div', class_='article')
outputs = []

# Loop through the <div> elements and call the extract_conversation method with the desired URL
for div in divs:
    # Find the first <a> tag with href that starts with "/makale/"
    a_tag = div.find('a', href=lambda href: href and href.startswith("/makale/"))
    if a_tag:
        url = "https://bilimgenc.tubitak.gov.tr" + a_tag['href']
        print(url)
        conversation_id = url.split('/')[-1]
        conversation = extract_conversation(url, conversation_id)
        outputs.append(conversation)


# Write the output conversations to a JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(outputs, f, ensure_ascii=False, indent=4)
