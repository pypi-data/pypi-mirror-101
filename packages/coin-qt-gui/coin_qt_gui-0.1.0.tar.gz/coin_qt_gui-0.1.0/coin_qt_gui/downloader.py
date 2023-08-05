import urllib.request
import json

"""
	https://pt.stackoverflow.com/questions/245695/dicas-de-apis-para-a-verifica%C3%A7ao-de-cota%C3%A7%C3%B5es-em-bitcoin
	https://www.mercadobitcoin.net/api/ETH/ticker/
	https://www.mercadobitcoin.net/api/BTC/ticker/
 """

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
]

user_agent = user_agents[1]

def ping(url) -> bool:
    """Verifica se uma página web está conectada ou offline"""

    print("Verificando conexão com a internet", end=" ")
    try:
        urllib.request.urlretrieve(url)
    except Exception as err:
        print(err)
        return False
    else:
        print("OK")
        return True

def request_api_page(url_api) -> float:
    """
	Retorna o valor de buy no json
	"""

    try:
        req = urllib.request.Request(url_api, data=None, headers={'User-Agent': user_agent})
        page = urllib.request.urlopen(req)
    except Exception as err:
        return err
    else:
        content = page.read().decode('utf-8')
        data = json.loads(content)
        value_BRL = float(data['ticker']['buy'])
        return value_BRL

def get_html_page(url: str) -> list:
    """
	Faz o request de uma página e retorna o conteúdo.
	"""
    try:
        req = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})
        html = urllib.request.urlopen(req)
    except Exception as err:
       print(err)
    else:
        return html.read().decode('utf-8')
