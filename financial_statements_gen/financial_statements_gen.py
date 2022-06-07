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


def getBS(header_string : str) -> pd.DataFrame:
  df = pd.read_csv( '{}_BS.txt'.format(header_string), sep='\t', encoding='euc-kr' )
  # 불필요 열 삭제 
  df.drop(['재무제표종류', '시장구분', '업종', '업종명', '통화'], axis='columns', inplace=True)
  # print(df.head(60))

  # 필요데이터만 추출 
  # 자산총계 - 부채 총계 ->  순자산 
  # 자산총계/부채총계/자본금 
  # regx 로 원하는 내용과 일치하는 데이터만 추출 
  filter = df['항목코드'].str.match('^ifrs-full_Assets$|^ifrs-full_Liabilities$|^ifrs-full_IssuedCapital$')
  df = df[filter]
  print(df.shape, df.index, df.columns)
  print(df.head(60))
  return df


  pass

def getPL(header_string : str) -> pd.DataFrame:
  df = pd.read_csv( '{}_PL.txt'.format(header_string), sep='\t', encoding='euc-kr' )
  # 불필요 열 삭제 
  df.drop(['재무제표종류', '시장구분', '업종', '업종명', '통화'], axis='columns', inplace=True)
  print(df.head(50))

  # regx 로 원하는 내용과 일치하는 데이터만 추출 
  filter = df['항목코드'].str.match('^ifrs-full_Revenue$|^ifrs-full_CostOfSales$|^ifrs-full_GrossProfit$|^ifrs-full_BasicEarningsLossPerShare$|^ifrs-full_BasicEarningsLossPerShareFromContinuingOperations$')
  df = df[filter]
  print(df.shape, df.index, df.columns)
  print(df.head(50))
  return df
  pass

def getStockInfo(header_string : str) -> pd.DataFrame:
  df = pd.read_excel( '{}_stock.xlsx'.format(header_string) )
  # 불필요 열 삭제 
  df.drop(['소속부', '대비', '등락률', '시가', '고가', '저가', '거래대금' ], axis='columns', inplace=True)

  # 필요데이터만 추출 
  # 자산총계 - 부채 총계 ->  순자산 
  # 자산총계/부채총계/자본금 
  # regx 로 원하는 내용과 일치하는 데이터만 추출 
  filter = df['시장구분'].str.match('^KOSPI$|^KOSDAQ$')
  df = df[filter]

  # 스팩 제거 
  filter = df['종목명'].str.contains('스팩')
  df = df[~filter]

  # 우선주 제거 
  # ▷ 마지막 1자리는 보통주/우선주 구분
  # 마지막 1자리는 종목구분코드입니다. 보통주는 0이 배정되고, 그 외 우선주 등 종류주식은 발생순서에 따라 K부터 순차적으로 부여합니다. Z 이후부터는 미부여된 알파벳을 다시 순차적으로 부여하는데, 이때 I, O, U는 제외합니다.
  # 우선주의 종목구분코드 구분은 2013년을 기준으로 약간 달라졌습니다. 2013년 이전까지 우선주는 5부터 순차적으로 홀수를 배정받았습니다. 현재 볼 수 있는 대부분의 우선주 코드 끝자리가 5인 이유입니다.
  # 2번째 우선주는 7, 3번째 우선주는 9가 각각 배정됩니다. 사이사이 짝수는 기존에 상장한 우선주의 신주발행 시 부여됩니다.
  filter = df['종목코드'].str.endswith('0')
  df = df[filter]

  # 시가 총액 기준으로 정렬
  df = df.sort_values(by=['시가총액']).head(500)
  df = df.reset_index(drop=True)
  print(df.shape, df.index, df.columns)

  print(df.head(60))
  return df


def calculatePBR():
  pass

def calculatePER():
  '''
  주가 / 주당순이익(EPS) 
  '''
  pass



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

#     PARAMS = {
#     'crtfc_key': api_key, # API 인증키
#     'corp_code': '00126380', # 삼성전자 고유번호
#     'bsns_year': '2022', # 사업연도(4자리)
#     'reprt_code': '11013', # 사업보고서
#     }

#     resp = requests.get(url = DART_URL_LIST['financial_statements'], params = PARAMS)

#     # http 정상응답시 처리
# if resp.status_code == 200:
#   data_json = resp.json()

#   # OUTPUT
#   # data_str = json.dumps(data_json, indent=4, ensure_ascii=False)
#   # print(data_str)

#   if data_json['status'] == "000":
#     detail = data_json['list']
    
#     # Json 코드 DataFrame으로 변환
#     df = pd.json_normalize(detail)

#     for column_name in df.columns:
#         print(column_name)
#         # print(df[[column_name]])
#         pass

#     # print(df)
#     #
#     df = df[['fs_div', 'fs_nm', 'sj_div', 'sj_nm', 'account_nm', 'thstrm_nm', 'thstrm_amount','thstrm_add_amount', 'frmtrm_nm', 'frmtrm_amount', 'frmtrm_add_amount']]

#     result = df.loc[(df.fs_div == 'OFS') & (df.sj_div == 'IS'),:]


#     is_df = { 'ofs' : df.loc[ (df.fs_div == 'OFS') & (df.sj_div == 'IS') ] ,
#               'cfs' : df.loc[ (df.fs_div == 'CFS') & (df.sj_div == 'IS') ] 
#     }

#     bs_df = { 'ofs' : df.loc[ (df.fs_div == 'OFS') & (df.sj_div == 'BS') ] ,
#               'cfs' : df.loc[ (df.fs_div == 'CFS') & (df.sj_div == 'BS') ] 
#     }

#     # is_df['cfs'].to_excel("is.xlsx")
#     # bs_df['cfs'].to_excel("bs.xlsx")

#     # print(bs_df['cfs'])

#     # print(bs_df['cfs'].loc[ bs_df['cfs'].account_nm == '자산총계' , ['thstrm_amount', 'frmtrm_amount'] ] )

#     print(sys.maxsize)

#     ths_jasan = int(bs_df['cfs'].loc[ bs_df['cfs'].account_nm == '자산총계' , 'thstrm_amount' ].iloc[0].replace(',', ''))
#     frm_jasan = int(bs_df['cfs'].loc[ bs_df['cfs'].account_nm == '자산총계' , 'frmtrm_amount' ].iloc[0].replace(',', ''))
#     ths_iik = int(is_df['cfs'].loc[ is_df['cfs'].account_nm == '당기순이익', 'thstrm_amount' ].iloc[0].replace(',', ''))



#     result_df = (ths_iik * 4)/ ((ths_jasan + frm_jasan) /2 ) * 100



#     print(result_df)

#     #calculate ROA
#     '''
#     ROA = 당기순이익(연율화) / 총자산총계(평균 )

#     당기순이익(연율화)에서 당기순이익을 어떻게 연율화하였는지 구체적인 식을 알고 싶습니다
#       연율화는 해당 분기의 데이터를 1년 기간으로 맞춰주는 작업입니다.
#       당기순이익 * 연율화계수 (1Q:4, 2Q:2, 3Q:4/3, 4Q:1)
#       (예: 누적 1분기*4, 2분기*2, 3분기4/3, 4분기*1)
#     '''
#     df = pd.read_csv('20220527.txt', sep='\t', encoding='euc-kr' )


#     print(df.shape)

#     df.to_excel("result.xlsx")
#   else :
#     print(data_json['message'])


    header_str = 'sample/2022_1Q'
    bs_df = getBS(header_str)
    pl_df = getPL(header_str)
    stock_df = getStockInfo(header_str)
    print("done")




