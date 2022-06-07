# financial_statements 
 - OPENDART 사용하여 [퀀트투자할수있다] 책의 관련 지표 데이터화 
 - <img src="http://image.yes24.com/goods/45504859/XL)" width="40%" height="30%" title="px(픽셀) 크기 설정" alt="퀀트투자할수있다"></img>

## Development Environment
 - Windows 10 64bit
 - python 3.9.13 이상 
 - poetry 

## Features

## Prerequisite after clone 
 - [OPENDART](https://opendart.fss.or.kr/) 에 인증키 신청
 - financial_statements_gen 폴더에 user_setting.json 파일 만들기
 - user_setting.json 파일내 "api_key": "opendart key value" 인증키 넣기
 - poetry update
 - 아래는 옵션 사항
    - [한국거래소](http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101) "전종목기본정보", "PER/PBR/배당수익률(개별종목)" 엑셀 다운로드
    - [재무정보일괄다운로드](https://opendart.fss.or.kr/disclosureinfo/fnltt/dwld/main.do) 에서 "연결재무상태표", "연결포괄손익계산서" 다운로드

## HowTo 
 - python financial_statements_gen.py

