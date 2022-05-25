import OpenDartReader
import requests
import pandas as pd
import json

__vserion__  = "0.1.0"



DART_URL_LIST = {
    "financial_statements": "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
}

api_key = ''

if __name__ == "__main__":

    user_setting_json = []
    with open(r"financial_statements_gen\user_setting.json", "r") as json_file:
        user_setting_json = json.load(json_file)

    api_key = user_setting_json['api_key']
    dart = OpenDartReader(api_key) 


    # == 1. 공시정보 검색 ==
    # df = dart.finstate_all('00126380', 2021, reprt_code='11013', fs_div="CFS")

    # for column_name in df.columns:
    #     print(column_name)
    #     print(df[[column_name]].tail(10))
    #     pass

    PARAMS = {
    'crtfc_key': api_key, # API 인증키
    'corp_code': '00126380', # 삼성전자 고유번호
    'bsns_year': '2021', # 사업연도(4자리)
    'reprt_code': '11013', # 사업보고서
    }

    resp = requests.get(url = DART_URL_LIST['financial_statements'], params = PARAMS)

    # http 정상응답시 처리
if resp.status_code == 200:
  data_json = resp.json()

  # OUTPUT
  # data_str = json.dumps(data_json, indent=4, ensure_ascii=False)
  # print(data_str)

  if data_json['status'] == "000":
    detail = data_json['list']
    
    # Json 코드 DataFrame으로 변환
    df = pd.json_normalize(detail)

    for column_name in df.columns:
        print(column_name)
        print(df[[column_name]].tail(10))
        pass

    # print(df)
    #
    print(df[['account_nm', 'thstrm_nm', 'thstrm_amount', 'frmtrm_nm', 'frmtrm_amount']])

  else :
    print(data_json['message'])



