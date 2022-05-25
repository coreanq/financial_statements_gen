import OpenDartReader
import sys, json

__vserion__  = "0.1.0"


if __name__ == "__main__":

    user_setting_json = []
    with open(r"financial_statements_gen\user_setting.json", "r") as json_file:
        user_setting_json = json.load(json_file)

    # ==== 0. 객체 생성 ====kkkkkkkj
    # 객체 생성 (API KEY 지정) 
    api_key = user_setting_json['api_key']

    dart = OpenDartReader(api_key) 


    # == 1. 공시정보 검색 ==
    # 삼성전자 2019-07-01 하루 동안 공시 목록 (날짜에 다양한 포맷이 가능합니다)
    df = dart.list('005930', end='2019-7-1')

    print(df)

