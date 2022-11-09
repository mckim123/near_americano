Near Americano
================

~~현재 http://218.236.76.30:5000/ 에서 확인하실 수 있습니다.~~ <br>
카카오맵 크롤링 허용에 대한 문의 결과 비허용 답변을 받아 중단합니다.

## About the Project

Near Americano는 위치 기반 근처 카페 아메리카노 가격 검색 서비스이다.

국내 커피 시장에서 가장 선호층이 두터운 메뉴는 아메리카노이다. 지도 애플리케이션을 활용하면 주위 카페들의 위치나 이름, 전화번호 등은 쉽게 파악할 수 있으나 메뉴의 가격을 확인하기 위해서는 위치를 클릭하여 하나하나 확인해야 하는 번거로움이 있다. 아메리카노 가격을 쉽게 확인하고 비교할 수 있는 서비스를 제작하였다.

<br/>

## Getting Started

### Environment

#### OS :  Windows 10

#### Python -- 3.9.13

* Python Library
  ```sh
  Flask==2.2.2
  beautifulsoup4==4.11.1
  requests==2.28.1
  mysql==0.0.3
  selenium=4.5.0
  ```

#### MySQL -- 8.0.31

<br/>

### Get API key from KAKAO Developers
카카오 지도 API를 활용하기 위해서는 카카오 개발자 사이트의 키를 발급받아야 하며, 사이트 도메인을 등록해야 한다.
1. https://developers.kakao.com/ 에 가입하여 새 애플리케이션을 추가한다.
2. 앱 키의 JavaScript 키를 복사하여 coffee_3.py에 붙여넣는다.
3. 플랫폼에 배포할 사이트 도메인을 등록한다.

<br/>

### MySQL setting
1. "cafedata" schema를 생성한다.
```
CREATE DATABASE cafedata;
```

2. 다음 쿼리로 아래의 테이블을 생성한다.
```
CREATE TABLE cafedata.cafe (
    id VARCHAR(16) NOT NULL,
    place_name VARCHAR(45) NOT NULL,
    phone VARCHAR(16) NULL,
    road_address_name VARCHAR(45) NOT NULL,
    x VARCHAR(32) NOT NULL,
    y VARCHAR(32) NOT NULL,
    americano SMALLINT UNSIGNED NULL,
    PRIMARY KEY(id),
    UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE);
```
3. my_settings_sample.py의 Password를 수정한다.

<br/>

### Flask 서버 실행

powershell 실행, 프로젝트 폴더로 이동 후 아래 코드를 입력하여 서버를 실행할 수 있다.
```bash
flask run --host=0.0.0.0
```

<br/>

 
## Usage


1. 초기 화면은 다음과 같다.

<img width = 80% src = "https://user-images.githubusercontent.com/43123236/198879241-af0656b4-46ad-44b0-8c56-57fd5c8fcb10.PNG">

<br/><br/>

2. 지도의 원하는 위치를 클릭하고 마커를 마우스로 클릭한다.  
- 이때 클릭한 위치로 지도 중심이 이동한다.
- 검색하는 중간에는 마커를 좌클릭할 수 없으며, 로드 후 다시 검색 가능해진다.
- 아메리카노 가격 정보가 없는 카페는 최초에 인포윈도우가 닫힌 마커로 등장한다. 클릭하면 인포윈도우가 열린다.
- 최초로 검색하는 구역인 경우 시간이 걸릴 수 있다.

<img width = 80% src = "https://user-images.githubusercontent.com/43123236/198881176-ddb8c31f-155e-41d0-83c8-4d8f4e46ec58.gif">

<br/><br/>

3. 좌측 하단의 버튼을 이용하여 원치 않는 마커를 제거할 수 있다. 
- 마우스를 마커 위에 올리면 해당 마커와 오버레이를 앞으로 끌어온다.
- 모든 마커는 클릭하면 오버레이가 생성되며 재클릭시 사라진다.

<img width = 80% src = "https://user-images.githubusercontent.com/43123236/198881183-cc4068e4-a1ae-4cab-abb5-87f5f207ea33.gif">

<br/><br/>

4. 좌측 하단의 버튼을 활용하면 GPS 기능을 사용하여 화면을 이동할 수 있다.
- localhost 또는 https 통신에서만 가능하여 아직은 배포시 사용이 불가능하다.

<img width = 80% src = "https://user-images.githubusercontent.com/43123236/198881187-883423c5-4dd4-43ee-b4a2-619168637501.gif">



5. 좌측 하단의 input에 가격을 입력하고 버튼을 누르면 해당 값 이하의 가격을 갖는 카페만 나오게 된다.
- 가격은 500에서 10000까지를 100 단위로 입력할 수 있다.  

<img width = 80% src = "https://user-images.githubusercontent.com/43123236/198879708-4dce60ac-2029-4ef9-b5d9-a442561cbc2a.gif">

<br/><br/>


6. 인포윈도우를 클릭하면 카카오맵 링크로 이동한다.

<a href="https://user-images.githubusercontent.com/43123236/198879824-1d0423b7-e62f-4c51-abfb-4d8b23bed487.gif"><img width = 80% src = "https://user-images.githubusercontent.com/43123236/198879824-1d0423b7-e62f-4c51-abfb-4d8b23bed487.gif" alt = '링크 이동'></a>

<br/><br/>
<br/><br/>


## Workflows

1. Kakao 지도 API의 지도, 마커 생성
    - 카카오 지도 API에서 제공하는 지도를 화면에 표시한다. 이후 파란색 마커를 생성한다.(사용자의 위치를 지정하는 역할)
    - 사용자가 마커를 클릭하면 마커의 자리는 고정되며, fetch() 함수를 활용하여 API 요청(POST)을 비동기적으로 보낸다.(async, await)

2. Flask server에서 API 호출 수신
    - POST 요청을 통해 전달받은 위도, 경도 정보를 활용하여 결과를 반환하도록 coffee_3.py를 실행하며, 위도, 경도 정보를 인자로 전달한다.

3. coffee_3.py의 실행
    - 전달받은 위도, 경도 정보를 바탕으로 근처 카페 정보에 대한 카카오 API 요청을 보낸다.(거리순으로 인근 30개를 수신한다.)
    - 받은 카페 정보 중 만화카페, 보드게임카페, 고양이카페, 라이브카페 등 커피가 주 목적이 아닌 카테고리를 제외하고 최대 20개의 카페 정보만 남긴다.
    - 저장된 프랜차이즈 카페들은 가격 정보를 바로 적용한다.
    - 다른 카페들에 대해서는 database에서 검색하여 이미 크롤링한 기록이 있다면 해당 정보를 불러오고, 정보가 없는 카페들에 대해서는 id list를 생성 후 crawler.py를 실행하여 아메리카노 가격 정보가 있는지 정보를 생성한다.
    - 반환된 결과를 database에 반영한 후 Flask server에 return한다.

4. Flask server Response
    - coffee_3.py의 함수에서 return받은 결과를 응답한다.

5. index.html에서 정보 수신
    - 비동기적으로 수신한 json파일을 이용하여 마커를 생성한다.
    - 이미 생성한 마커는 넘어가고 그렇지 않은 경우 커피 모양 마커, 그 위 가게명, 가격 정보, 링크를 담은 오버레이를 생성한다.
    - 각각의 마커에 대해 이벤트리스너가 정상적으로 작동할 수 있도록 클로져를 사용한다.


<br/><br/>
<br/><br/>


## Additional Planned Features

- 주소 검색 및 지정 기능
    - geolocation을 활용한 최초 주소 검색 기능이 localhost에서는 구현되었으나, 기타 상황에서는 등장하지 않는 오류가 있다. 일반적으로도 사용할 수 있도록 보완할 계획이다.
    - searchbox를 만들어 주소를 검색하고, 해당 위치로 지도를 이동시킬 수 있도록 하는 기능을 구현할 것이다.

- 체크박스를 활용한 가격대, 메뉴 선택
    - 현재 가격을 입력하면 해당 가격 이하의 카페만 등장하도록 해두었다. 아메리카노 외의 메뉴도 추가하여 필터를 만들 계획이다.

- 오래된 가격, 없는 가격, 없는 가게 등을 타 경로로 검색 및 추가/갱신
    - 카카오맵 사이트에 가격을 올리지 않았거나 사진으로만 메뉴를 올린 경우 가격 정보를 얻지 못한다는 단점이 있다. 이를 해결할 다른 경로를 찾아 보완할 계획이다.
    - 카페 카테고리로 검색하기 때문에 햄버거 프랜차이즈 등의 저가 커피를 파는 가게가 제외된다. 이들을 포함하고 속도는 잡을 수 있는 방법을 보완할 계획이다.

- 정보 전달력
    - 현재 비슷한 주소에 여러 개의 마커가 있는 경우 겹침으로 인해 불편이 있다. 클러스터링 등의 방법을 활용하여 겹치더라도 정보를 쉽게 확인할 수 있도록 구현할 계획이다.
    - 현재의 오버레이 방식보다 바로 아메리카노의 가격 정보를 전달할 방법을 찾아 초기의 목적을 달성할 계획이다.

- 배포
    - 현재 로컬 PC를 Flask 서버로 활용하여 test까지 완료된 상황이다. 이를 기타 클라우드 사이트를 통해 배포하여 로컬 서버를 가동하지 않고도 사용할 수 있도록 구현할 계획이다.
