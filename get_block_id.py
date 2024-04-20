import requests
import json


def get_block_id(batabse_id):
    url = "https://api.notion.com/v1/databases/" + batabse_id + "/query"
    data = requests_url(url)

    return data

def requests_url(url):
    headers = {'Notion-Version': notion_version
        , 'Authorization': 'Bearer ' + api_token}

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("status code:", response.status_code)

    return data


## if __name__ == '__main__':
############################################
with open('config.json','r') as f:
    config = json.load(f)

api_token = config['api_token']
database_id = config['database_id']
notion_version = config['notion_version']

data = get_block_id(database_id)
block_id = []
for i in data['results']:
    if i['properties']['업로드']['checkbox']:
        block_id.append({"title":i['properties']['제목']['title'][0]['plain_text'],
                    "id" : i['id']})

with open('block_id.json','w',encoding='utf-8') as f:
    json.dump(block_id,f,ensure_ascii=False)