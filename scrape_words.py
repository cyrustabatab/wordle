from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase




url = "https://scrabble.merriam.com/words/start-with/{letter}"

def get_page(url):

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(e)
    else:
        return response


for letter in ascii_lowercase:
    letter_url = url.format(letter)

    response = get_page(letter_url)


    soup = BeautiulSoup(response.text,'lxml')






