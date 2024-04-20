import requests
import json
# type정리
### heading_#           : 제목
### paragraph           : 일반 글
### code
### numbered_list_item
### bulleted_list_item
### toggle
### callout
def set_annotation(annotations, plain_text):
    #  heading_1, annotaions, text
    temp_text = ""
    if annotations["code"] :
        temp_text = "`"+plain_text+"`"
    elif annotations["bold"] :
        temp_text = md["md_dict"]["bold"] + plain_text + md["md_dict"]["bold"]
    elif annotations["italic"]:
        temp_text = md["md_dict"]["italic"]+plain_text+md["md_dict"]["italic"]
    else:
        temp_text = plain_text

    return temp_text

def set_text_type(o_type, rt_list):
    anno_text = ""
    type_text = ""

    ## 텍스트를 뽑아내고
    for content in rt_list:
        ### Type에 따라 Text 변환
        anno_text = anno_text + set_annotation(content['annotations'],content['plain_text'])

    ## 특성 추가
    if o_type in md["md_dict"]:
        if md["md_dict_double"][o_type] == "True":
            type_text = md["md_dict"][o_type] + anno_text + md["md_dict"][o_type]
        else:
            type_text = md["md_dict"][o_type] + anno_text

    elif o_type == "toggle":
        ## 토글 아래 내용은 어디서 가져와야될지 모르겠음
        type_text = "<details><summary>" + anno_text + "</summary></details>"

    elif o_type == "paragraph":
        type_text = anno_text

    return type_text + "<br>"

def set_other(o_type,data):
    temp_text = ""
    ## 구분선
    if o_type == "divider" :
        temp_text = "_______"

    elif o_type == "image" :
        temp_text = "!["+data["id"]+"]("+data["image"]["file"]["url"]+")"

    return temp_text

def notion_to_text(data):
    result_text = []
    for block in data['results']:
        # notion - block
        if block['object'] == 'block':
            # notion - type 체크
            o_type = block['type']
            ## Text이면 추출
            if "rich_text" in block[o_type]:
                ## 빈 공백 체크
                if len(block[o_type]['rich_text']) > 0:
                    result_text.append(set_text_type(o_type, block[o_type]['rich_text']))
                    if block['has_children']:
                        for child_data in change_to_md(block['id']):
                            result_text.append("&ensp; &ensp; "+child_data)
                else:
                    result_text.append("  ")
            ## 이미지 처리
            else:
                result_text.append(set_other(o_type,block))
        else:
            print("object=", block['object'])

    return result_text

def get_title(block_id):
    url = "https://api.notion.com/v1/pages/" + block_id
    data = requests_url(url)

    return data['properties']['제목']['title'][0]['plain_text']

def get_data(block_id):
    url = "https://api.notion.com/v1/blocks/" + block_id + "/children?page_size=100"
    data = requests_url(url)

    return data

def requests_url(url):
    headers = {'Notion-Version': notion_version
        , 'Authorization': 'Bearer ' + api_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print("status code:", response.status_code)

    return data

def change_to_md(block_id):
    data = get_data(block_id)
    result = notion_to_text(data)
    return result

## if __name__ == '__main__':
############################################
with open('config.json','r') as f:
    config = json.load(f)

with open('md_config.json','r') as f:
    md = json.load(f)

block_id=config['block_id']
api_token = config['api_token']
database_id = config['database_id']
notion_version = config['notion_version']

result = change_to_md(block_id)
result = "\n".join(str(item) for item in result)

title=get_title(block_id)

with open(title+".md","w",encoding='utf-8') as file:
    file.write(result)

print(title," 파일 생성 완료")
