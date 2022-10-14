import requests
import json
url = "https://dapi.kakao.com"
API_KEY = "9ce2252d987df592085cb9f475f235f6"
headers = {"Authorization" : f"KakaoAK {API_KEY}"}
FORMAT = "json"

path = f"/v2/local/search/address.{FORMAT}"
path2 = "/v2/local/geo/coord2regioncode.json?x=126.943232&y=37.486592"
path3 = f"/v2/local/search/keyword.{FORMAT}"

data = {"query":"카페", "category_group_code":"CE7", "x":126.953743, "y":37.478851, "radius":1000, "sort":"distance"}

req1 = requests.get(url+path3, headers = headers, params = data).json()
req1['documents'][0]





https://www.googleapis.com/geolocation/v1/geolocate?key=