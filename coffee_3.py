import requests
import json
import crawler
import mysql.connector

url = "https://dapi.kakao.com"
API_KEY = "9ce2252d987df592085cb9f475f235f6"
headers = {"Authorization" : f"KakaoAK {API_KEY}"}

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=MYPASSWORD,
    database='cafedata'
)
cur = mydb.cursor()

def americano(local_y, local_x):

    path = f"/v2/local/search/keyword.json"

    data = {"query":"카페", "category_group_code":"CE7", "x":local_x, "y":local_y, "radius":1000, "sort":"distance"}

    near_cafes = requests.get(url+path, headers = headers, params = data).json()['documents']

    filtered_cafes = list()
    id_list = list()
    crawl_id = list()
    crawl_needed_cafes = list()

    info_contents = ("id", "place_name", "phone", "road_address_name", "x", "y")

    for i in range(len(near_cafes)):
        if ("북카페" in near_cafes[i]['category_name'].split() or "보드카페" in near_cafes[i]['category_name'].split()):
            continue
        else:
            id_list.append(near_cafes[i]['id'])
            filtered_cafes.append(near_cafes[i])

    cur.execute(f"SELECT * FROM cafe WHERE id IN {tuple(id_list)};")
    db_result = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    found_id = [row['id'] for row in db_result]

    crawled_result = []
    result_to_db = []

    for i in range(len(filtered_cafes)):
        if filtered_cafes[i]['id'] not in found_id:
            crawl_id.append(filtered_cafes[i]['id'])
            cafe_info = {}
            for content in info_contents:
                if filtered_cafes[i][content]:
                    cafe_info[content] = filtered_cafes[i][content]
                else:
                    cafe_info[content] = ''
            crawl_needed_cafes.append(cafe_info)

    if crawl_id:
        menu = crawler.extract_menu(crawl_id)
        for i, id in enumerate(crawl_id):
            has_americano = False
            for menu_name in menu[id].keys():
                if '아메리카노' in menu_name:
                    menu[id] = menu[id][menu_name]
                    has_americano = True
                    break
                elif 'americano' in menu_name:
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


'''
local_x = 126.953706
local_y = 37.478822
result = americano(local_y, local_x)
'''