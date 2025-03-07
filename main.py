from pprint import pprint  # Verileri daha okunaklı yazmak için kullanılır
from uuid import uuid4  # Evrensel benzersiz UUID'ler oluşturmak için kullanılır

from requests import get  # HTTP GET istekleri yapmak için kullanılır

# API'den veri çekme
API_KEY = 'ca3dac370b6a487d921e8c5ed5f9e181'  # API anahtarınızı buraya gireriz
endpoint = f'https://newsapi.org/v2/everything?q=tesla&from=2025-02-07&sortBy=publishedAt&apiKey={API_KEY}'
response = get(url=endpoint)
data = response.json()  # API'den dönen JSON verisini Python sözlüğüne çevirir

if 'articles' in data:
    pprint(data['articles'][:3])  # İlk 3 makaleyi yazdıran komut
else:
    print("Hata: API'den beklenen veri alınamadı.")

# İlk makaleyi yazdırma
if 'articles' in data and len(data['articles']) > 0:
    first_article = data['articles'][0]
    print(f"Author: {first_article.get('author', 'Bilinmiyor')}")
    print(f"Title: {first_article.get('title', 'Bilinmiyor')}")
    print(f"Content: {first_article.get('content', 'Bilinmiyor')}")
    print(f"Description: {first_article.get('description', 'Bilinmiyor')}")
    print(f"PublishedAt: {first_article.get('publishedAt', 'Bilinmiyor')}")
    print(f"Source: {first_article.get('source', {}).get('name', 'Bilinmiyor')}")

# Veri işlemleri için fonksiyonlar
local_data = {}  # UUID ile saklanacak yerel veri deposunu belirttik


def create_data(author: str, content: str, description: str, publishedAt: str) -> dict:
    article_id = str(uuid4())
    local_data[article_id] = {
        'author': author,
        'content': content,
        'description': description,
        'publishedAt': publishedAt,
    }
    return local_data


def update_data(article_id: str, content: str, description: str) -> dict:
    if article_id in local_data:
        local_data[article_id].update({
            'content': content,
            'description': description
        })
    else:
        print("Hata: Güncellenecek veri bulunamadı!")
    return local_data


def delete_data(article_id: str) -> dict:
    if article_id in local_data:
        del local_data[article_id]
    else:
        print("Hata: Silinecek veri bulunamadı!")
    return local_data


def list_data():
    pprint(local_data)


# Kullanıcı işlemleri
while True:
    process = input('\nİşlem giriniz (create, list, update, delete, exit): ').strip().lower()

    if process == 'create':
        author = input('Author: ')
        content = input('Content: ')
        description = input('Description: ')
        publishedAt = input('PublishedAt: ')
        pprint(create_data(author, content, description, publishedAt))

    elif process == 'list':
        list_data()

    elif process == 'update':
        article_id = input('Güncellenecek ID: ')
        content = input('Yeni Content: ')
        description = input('Yeni Description: ')
        pprint(update_data(article_id, content, description))

    elif process == 'delete':
        article_id = input('Silinecek ID: ')
        pprint(delete_data(article_id))

    elif process == 'exit':
        break

    else:
        print('Geçersiz işlem, tekrar deneyin.')
