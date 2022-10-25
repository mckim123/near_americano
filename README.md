Near Americano
================

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

<img width = 50% src = "https://user-images.githubusercontent.com/43123236/197792693-3386d541-8a2f-4b18-862e-a10459616c61.PNG">

<br/><br/>

2. 지도의 원하는 위치를 클릭하고 마커를 마우스로 클릭한다.  
- 이때 클릭한 위치로 지도 중심이 이동한다.
- 검색하는 중간에는 마커를 좌클릭할 수 없으며, 로드 후 다시 검색 가능해진다.
- 아메리카노 가격 정보가 없는 카페는 최초에 인포윈도우가 닫힌 마커로 등장한다. 클릭하면 인포윈도우가 열린다.
- 최초로 검색하는 구역인 경우 시간이 걸릴 수 있다.

<img width = 50% src = "https://user-images.githubusercontent.com/43123236/197795901-0eec566a-914c-4e69-8d28-fab0cd655290.gif">

<br/><br/>

3. 좌측 하단의 버튼을 이용하여 원치 않는 마커를 제거할 수 있다. 
- 마우스를 마커 위에 올리면 해당 마커와 오버레이를 앞으로 끌어온다.
- 모든 마커는 클릭하면 오버레이가 생성되며 재클릭시 사라진다.

<img width = 50% src = "https://user-images.githubusercontent.com/43123236/197795911-b9a8b094-9701-492d-a24d-b5ad2faa7fbb.gif">

<br/><br/>

4. 좌측 하단의 input에 가격을 입력하고 버튼을 누르면 해당 값 이하의 가격을 갖는 카페만 나오게 됩니다.
- 가격은 500에서 10000까지를 100 단위로 입력할 수 있습니다.  

<img width = 50% src = "https://user-images.githubusercontent.com/43123236/197795914-bdb1eeee-f555-4b5e-aef8-d0b1ea1141dc.gif">

<br/><br/>


5. 인포윈도우를 클릭하면 카카오맵 링크로 이동다.

<img width = 50% src = "https://user-images.githubusercontent.com/43123236/197795916-bd74ac34-9184-48cd-bcef-8c73e5e67fca.gif">

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
