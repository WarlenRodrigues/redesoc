import credentials
import requests
import json

from base64 import b64encode


URL = 'https://api.rawg.io/api/'

API_KEY = credentials.get_api_key()

def writeCreator(creator):
  oldFile = {}
  with open('creators.json', 'r') as file:
    oldFile = json.load(file)


  if str(creator["id"]) in oldFile:
      print(f'Creator {creator["id"]} already register')
  else:
    with open('creators.json', 'w') as file:

        # print(f'Add: {creator["id"]}')
        oldFile[creator["id"]] = creator
        file.write(json.dumps(oldFile))



def getCreatorPage(nextPage):
    if not nextPage:
      return
    else:
      print(f'GET: {nextPage}')
      response = requests.get(nextPage)
      print(f'Status code: {response.status_code}')
    # # Se o request deu errado, isso pode ser verificado pelo status code.
    # if response.status_code != 200:
    #     print(response)
    #     raise 'Errou'
    data = response.json()

    creators = data['results']

    # print(f'creators: {creators}\n')
    for creator in creators:
      writeCreator(creator)


if __name__ == '__main__':
    route = 'creators'
    nextPage = URL + route + f'?key={API_KEY}'
    for page in range(900,2444):
      nextPage = f'https://api.rawg.io/api/creators?key={API_KEY}&page={page}'
      getCreatorPage(nextPage)
