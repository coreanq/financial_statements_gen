# financial_statements 
 - OPENDART 사용하여 [퀀트투자할수있다] 책의 관련 지표 데이터화 
 - <img src="http://image.yes24.com/goods/45504859/XL)" width="40%" height="30%" title="px(픽셀) 크기 설정" alt="퀀트투자할수있다"></img>

## Development Environment
 - Windows 10 64bit
 - python 3.9.13 이상 

## Features

## HowTo 
 - [OPENDART](https://opendart.fss.or.kr/) 에 인증키 신청
 - user_setting.json 파일 만들어서 'api-key' 값에 인증키 문자열로 저장 
 - [한국거래소](http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101) 시세 정보 엑셀 다운로드
 - [재무정보일괄다운로드](https://opendart.fss.or.kr/disclosureinfo/fnltt/dwld/main.do) 에서 "재무상태표", "손익계산서" 다운로드
 - python financial_statements_gen.py

