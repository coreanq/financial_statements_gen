from distutils.log import error
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
  '''
  재무 상태표
  '''
  df = pd.read_csv( '{}_BS.txt'.format(header_string), sep='\t', encoding='utf-8' )
  # 불필요 열 삭제 
  df.drop(['재무제표종류', '시장구분', '업종', '업종명', '통화'], axis='columns', inplace=True)
  # print(df.head(60))

  # 필요데이터만 추출 
  # 자산총계 - 부채 총계 ->  순자산 
  # 자산총계/부채총계/자본금 
  # regx 로 원하는 내용과 일치하는 데이터만 추출 
  filter = df['항목코드'].str.match('^ifrs-full_Assets$|^ifrs-full_Liabilities$|^ifrs-full_IssuedCapital$')
  df = df[filter]
  df = df.reset_index(drop=True)
  print(df.shape, df.index, df.columns)
  # print(df.head(60))
  return df


  pass

def getPL(header_string : str) -> pd.DataFrame:
  '''
  연결포괄손익계산서
  포괄이 아니면 데이터가 누락되어 있음
  기본주당이익(손실) 항목은 누락인 경우 있으므로 사용금지
  매출액/매출원가/매출총이익만 봄

  '''
  df = pd.read_csv( '{}_PL.txt'.format(header_string), sep='\t', encoding='utf-8', encoding_errors='replace' )
  # 불필요 열 삭제 
  df.drop(['재무제표종류', '시장구분', '업종', '업종명', '통화'], axis='columns', inplace=True)
  # print(df.head(50))

  # regx 로 원하는 내용과 일치하는 데이터만 추출 
  filter = df['항목코드'].str.match('^ifrs-full_Revenue$|^ifrs-full_CostOfSales$|^ifrs-full_GrossProfit$')
  df = df[filter]
  df = df.reset_index(drop=True)
  print(df.shape, df.index, df.columns)
  print(df.head(50))
  return df
  pass


def getStockBasicInfo(header_string : str) -> pd.DataFrame:
  df = pd.read_excel( '{}_stock_basic.xlsx'.format(header_string) )
  # 불필요 열 삭제 
  df.drop(['소속부', '대비', '등락률', '시가', '고가', '저가', '거래대금' ], axis='columns', inplace=True)

  # 필요데이터만 추출 
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

  df = df[['종목코드', '거래량', '시가총액', '상장주식수']]
  print(df.shape, df.index, df.columns)
  print(df.head(60))

  # 시가 총액 기준으로 정렬
  # df = df.sort_values(by=['시가총액'])
  # df = df.reset_index(drop=True)
  return df

def getStockDetailInfo(header_string : str) -> pd.DataFrame:
  df = pd.read_excel( '{}_stock_detail.xlsx'.format(header_string) )
  # 불필요 열 삭제 
  df.drop(['대비', '등락률', '선행 EPS', '선행 PER', '주당배당금', '배당수익률'], axis='columns', inplace=True)

  # 필요데이터만 추출 
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

  print(df.shape, df.index, df.columns)

  df = df[df['EPS'] != '-']

  df = df[df['PER'] != '-']

  df = df[df['BPS'] != '-']

  df = df[df['PBR'] != '-']

  df = df.reset_index(drop=True)
  print(df.shape, df.index, df.columns)
  print(df.head(60))
  return df


def calculatePBR():
  pass

def calculatePER(stock_data : pd.DataFrame, pl_data : pd.DataFrame) -> pd.Series:
  '''
  주가 / 주당순이익(EPS)
  # 종목 코드 리스트만 별도로 가져옴
  # 종목 코드 리스트를 통한 주가 및 주당 순이익 데이터 가져옴
  # 위 데이터를 열로 만든 후 pd.DataSeries 로 추가 
  '''

  stock_code_list = stock_data['종목코드']

  result_list = []
  print( len( stock_data['종목코드']))

  for index, value in stock_data['종목코드'].items():
    # print(value)
    filter = pl_data['종목코드'].str.contains(value)
    if( pl_data[filter].empty == False):
      print(pl_data[filter])
      # print(pl_data[filter])
  
  stock_data['PER'] = result_list


  pass

if __name__ == "__main__":

    user_setting_json = []
    with open(r"financial_statements_gen\user_setting.json", "r") as json_file:
        user_setting_json = json.load(json_file)

    api_key = user_setting_json['api_key']
    dart = OpenDartReader(api_key) 

    info_header = 'sample/2022_1Q'

    continue_bs_df = getBS(info_header + "_C")
    continue_pl_df = getPL(info_header + "_C")

    separate_bs_df = getBS(info_header)
    separate_pl_df = getPL(info_header)

    stock_basic_df = getStockBasicInfo(info_header)
    stock_detail_df = getStockDetailInfo(info_header)


    # merge 주식 정보 

    #######################################################################################3
    # 시가 총액 컬럼 추가 
    # 시가 총액의 경우 공시 정보가 아니기 때문에 누락이 없음 
    additional_stock_info_list = []
    column_name = '시가총액'

    src_df = stock_basic_df
    for index, value in stock_detail_df['종목코드'].iteritems():

        temp_df = src_df[ src_df['종목코드'].str.contains(value) ]
        if( len(temp_df) != 0 ):
            additional_stock_info_list.append( temp_df.iloc[0]['시가총액'] )
        else:
            print("시가총액 누락 종목 {}".format( value ))
            # 기본정보에 없는 코드 삭제 
            additional_stock_info_list.append( np.nan )

    stock_detail_df[column_name] = additional_stock_info_list

    # print( len(stock_detail_df), stock_detail_df.head(20) )


    #######################################################################################3
    # 매출액 컬럼 추가 
    additional_stock_info_list = []
    column_name = '매출액'

    src_df = continue_pl_df
    alternate_df = separate_pl_df

    for index, value in stock_detail_df['종목코드'].iteritems():
        temp_df = src_df[ (src_df['종목코드'].str.contains(value)) & (src_df['항목코드'].str.contains('ifrs-full_Revenue') )  ]
        # print(temp_df.head(10))

        if( len(temp_df) != 0 ):
                # 컬럼 이름이 포함된 index 를 찾아 cell 값을 찾는다 
                cell_contents =  temp_df.iloc[0][ temp_df.columns.tolist().index('당기 1분기 3개월') ]
                cell_contents = cell_contents.replace(',', '')
                cell_contents = int(cell_contents)
                additional_stock_info_list.append( cell_contents)
        else:
            temp_df = alternate_df[ (alternate_df['종목코드'].str.contains(value)) & (alternate_df['항목코드'].str.contains('ifrs-full_Revenue') )  ]
            # 기본정보에 없는 경우 이전 자료 searching 

            if( len(temp_df) != 0 ):
                # 컬럼 이름이 포함된 index 를 찾아 cell 값을 찾는다 
                cell_contents =  temp_df.iloc[0][ temp_df.columns.tolist().index('당기 1분기 3개월') ]
                cell_contents = cell_contents.replace(',', '')
                cell_contents = int(cell_contents)
                additional_stock_info_list.append( cell_contents)

            else:
                # print("매출액 누락 종목 {}".format( value ))
                additional_stock_info_list.append( np.nan )

    stock_detail_df[column_name] = additional_stock_info_list

    # print( len(stock_detail_df), stock_detail_df.head(10) )

    #######################################################################################3
    # 매출총이익 컬럼 추가 
    additional_stock_info_list = []
    column_name = '매출총이익'

    src_df = continue_pl_df
    alternate_df = separate_pl_df

    for index, value in stock_detail_df['종목코드'].iteritems():
        temp_df = src_df[ (src_df['종목코드'].str.contains(value)) & (src_df['항목코드'].str.contains('ifrs-full_GrossProfit') )  ]
        # print(temp_df.head(10))

        if( len(temp_df) != 0 ):
                # 컬럼 이름이 포함된 index 를 찾아 cell 값을 찾는다 
                cell_contents =  temp_df.iloc[0][ temp_df.columns.tolist().index('당기 1분기 3개월') ]
                cell_contents = cell_contents.replace(',', '')
                cell_contents = int(cell_contents)
                additional_stock_info_list.append( cell_contents)
        else:
            temp_df = alternate_df[ (alternate_df['종목코드'].str.contains(value)) & (alternate_df['항목코드'].str.contains('ifrs-full_grossProfit') )  ]
            # 기본정보에 없는 경우 이전 자료 searching 

            if( len(temp_df) != 0 ):
                # 컬럼 이름이 포함된 index 를 찾아 cell 값을 찾는다 
                cell_contents =  temp_df.iloc[0][ temp_df.columns.tolist().index('당기 1분기 3개월') ]
                cell_contents = cell_contents.replace(',', '')
                cell_contents = int(cell_contents)
                additional_stock_info_list.append( cell_contents)
            else:
                # print("매출총이익 누락 종목 {}".format( value ))
                additional_stock_info_list.append( np.nan )

    stock_detail_df[column_name] = additional_stock_info_list

    #######################################################################################3
    # 자산 컬럼 추가 
    additional_stock_info_list = []
    column_name = '자산'

    src_df = continue_bs_df
    alternate_df = separate_bs_df

    for index, value in stock_detail_df['종목코드'].iteritems():
        temp_df = src_df[ (src_df['종목코드'].str.contains(value)) & (src_df['항목코드'].str.contains('ifrs-full_EquityAndLiabilities|ifrs-full_Assets') )  ]
        # print(temp_df.head(10))

        if( len(temp_df) != 0 ):
                # 컬럼 이름이 포함된 index 를 찾아 cell 값을 찾는다 
                cell_contents =  temp_df.iloc[0][ temp_df.columns.tolist().index('당기 1분기말') ]
                cell_contents = cell_contents.replace(',', '')
                cell_contents = int(cell_contents)
                additional_stock_info_list.append( cell_contents)
        else:
            temp_df = alternate_df[ (alternate_df['종목코드'].str.contains(value)) & (alternate_df['항목코드'].str.contains('ifrs-full_grossProfit') )  ]
            # 기본정보에 없는 경우 이전 자료 searching 

            if( len(temp_df) != 0 ):
                # 컬럼 이름이 포함된 index 를 찾아 cell 값을 찾는다 
                cell_contents =  temp_df.iloc[0][ temp_df.columns.tolist().index('당기 1분기말') ]
                cell_contents = cell_contents.replace(',', '')
                cell_contents = int(cell_contents)
                additional_stock_info_list.append( cell_contents)
            else:
                # print("매출총이익 누락 종목 {}".format( value ))
                additional_stock_info_list.append( np.nan )

    stock_detail_df[column_name] = additional_stock_info_list


    ####################################################################################

    print( len(stock_detail_df), stock_detail_df.head(10) )
    stock_detail_df.to_excel("result_before_drop.xlsx")

    stock_detail_df.dropna(inplace=True)
    stock_detail_df.reset_index(inplace=True)

    stock_detail_df.to_excel("result.xlsx")

    print("done")




