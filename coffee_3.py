import requests
import json
import crawler
import mysql.connector
from my_settings import MY_DATABASES

url = "https://dapi.kakao.com"
API_KEY = "9ce2252d987df592085cb9f475f235f6"
headers = {"Authorization" : f"KakaoAK {API_KEY}"}

mydb = mysql.connector.connect(
    database = MY_DATABASES['DATABASE'],
    user = MY_DATABASES['USER'],
    password = MY_DATABASES['PASSWORD'],
    host = MY_DATABASES['HOST'],
    port = MY_DATABASES['PORT']
)

def americano(local_y, local_x):

    cur = mydb.cursor()

    path = f"/v2/local/search/keyword.json"

    data1 = {"query":"카페", "category_group_code":"CE7", "x":local_x, "y":local_y, "sort":"distance"}
    data2 = {"query":"카페", "category_group_code":"CE7", "x":local_x, "y":local_y, "page":2, "sort":"distance"}

    near_cafes = requests.get(url+path, headers = headers, params = data1).json()['documents']
    near_cafes += requests.get(url+path, headers = headers, params = data2).json()['documents']

    filtered_cafes = list()
    id_list = list()
    crawl_id = list()
    crawl_needed_cafes = list()

    remove_set = {"보드카페", "북카페", "만화카페", "라이브카페", "고양이카페"}
    
    info_contents = ("id", "place_name", "phone", "road_address_name", "x", "y")
    for i in range(len(near_cafes)):
        if (set(near_cafes[i]['category_name'].split()) & remove_set) or ("방탈출" in near_cafes[i]['place_name']):
            continue
        else:
            id_list.append(near_cafes[i]['id'])
            filtered_cafes.append(near_cafes[i])
            if len(id_list) == 20:
                break

    cur.execute(f"SELECT * FROM cafe WHERE id IN {tuple(id_list)};")
    db_result = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    found_id = [row['id'] for row in db_result]

    crawled_result = []
    result_to_db = []

    for i in range(len(filtered_cafes)):
        if filtered_cafes[i]['id'] not in found_id:
            cafe_info = {}
            for content in info_contents:
                if filtered_cafes[i][content]:
                    cafe_info[content] = filtered_cafes[i][content]
                else:
                    cafe_info[content] = ''
            crawl_id.append(filtered_cafes[i]['id'])
            crawl_needed_cafes.append(cafe_info)

    if crawl_id:
        menu = crawler.extract_menu(crawl_id)
        for i, id in enumerate(crawl_id):
            has_americano = False
            for menu_name in menu[id].keys():
                if ('아메리카노' in menu_name or 'americano' in menu_name) and \
                    ('ice' in menu_name or '아이스' in menu_name):
                    menu[id] = menu[id][menu_name]
                    has_americano = True
                    break
            if not has_americano:
                for menu_name in menu[id].keys():
                    if ('아메리카노' in menu_name or 'americano' in menu_name):
                        menu[id] = menu[id][menu_name]
                        has_americano = True
                        break

            if has_americano:
                crawl_needed_cafes[i]["americano"] = menu[id]

            else:
                crawl_needed_cafes[i]["americano"] = 0
            crawled_result.append(crawl_needed_cafes[i])
            result_to_db.append(tuple(crawl_needed_cafes[i].values()))

    if crawl_id:
        cur.execute(f"INSERT INTO cafe VALUES {str(result_to_db)[1:len(str(result_to_db))-1]};")
        mydb.commit()

    cur.close()
    return json.dumps({"Cafe":(db_result + crawled_result)}, ensure_ascii=False)