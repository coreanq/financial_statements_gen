import OpenDartReader
import requests
import pandas as pd
import json,sys
import numpy as np

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
    'bsns_year': '2022', # 사업연도(4자리)
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
        # print(df[[column_name]])
        pass

    # print(df)
    #
    df = df[['fs_div', 'fs_nm', 'sj_div', 'sj_nm', 'account_nm', 'thstrm_nm', 'thstrm_amount','thstrm_add_amount', 'frmtrm_nm', 'frmtrm_amount', 'frmtrm_add_amount']]

    result = df.loc[(df.fs_div == 'OFS') & (df.sj_div == 'IS'),:]


    is_df = { 'ofs' : df.loc[ (df.fs_div == 'OFS') & (df.sj_div == 'IS') ] ,
              'cfs' : df.loc[ (df.fs_div == 'CFS') & (df.sj_div == 'IS') ] 
    }

    bs_df = { 'ofs' : df.loc[ (df.fs_div == 'OFS') & (df.sj_div == 'BS') ] ,
              'cfs' : df.loc[ (df.fs_div == 'CFS') & (df.sj_div == 'BS') ] 
    }

    # is_df['cfs'].to_excel("is.xlsx")
    # bs_df['cfs'].to_excel("bs.xlsx")

    # print(bs_df['cfs'])

    # print(bs_df['cfs'].loc[ bs_df['cfs'].account_nm == '자산총계' , ['thstrm_amount', 'frmtrm_amount'] ] )

    print(sys.maxsize)

    ths_jasan = int(bs_df['cfs'].loc[ bs_df['cfs'].account_nm == '자산총계' , 'thstrm_amount' ].iloc[0].replace(',', ''))
    frm_jasan = int(bs_df['cfs'].loc[ bs_df['cfs'].account_nm == '자산총계' , 'frmtrm_amount' ].iloc[0].replace(',', ''))
    ths_iik = int(is_df['cfs'].loc[ is_df['cfs'].account_nm == '당기순이익', 'thstrm_amount' ].iloc[0].replace(',', ''))



    result_df = (ths_iik * 4)/ ((ths_jasan + frm_jasan) /2 ) * 100



    print(result_df)

    #calculate ROA
    '''
    ROA = 당기순이익(연율화) / 총자산총계(평균 )

    당기순이익(연율화)에서 당기순이익을 어떻게 연율화하였는지 구체적인 식을 알고 싶습니다
      연율화는 해당 분기의 데이터를 1년 기간으로 맞춰주는 작업입니다.
      당기순이익 * 연율화계수 (1Q:4, 2Q:2, 3Q:4/3, 4Q:1)
      (예: 누적 1분기*4, 2분기*2, 3분기4/3, 4분기*1)
    '''


  else :
    print(data_json['message'])



