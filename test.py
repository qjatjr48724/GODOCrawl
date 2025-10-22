# 1. 라이브러리 불러오기
import os
import time
import hmac, hashlib
import urllib.parse
import urllib.request
import requests
import ssl
import openpyxl
import json
from datetime import date
from datetime import timedelta

# 엑셀에 저장할 오늘 날짜 포맷
today_date = date.today().strftime('%Y%m%d')

### 쿠팡 api 연동 Start

os.environ['TZ'] = 'GMT+0'
datetime=time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
method = "GET"

cp_venderId = "A01093941"
cp_secretkey = "a4e91ae56e91a47b696712dd29008a405e8d4c25"
cp_accesskey = "7b6058d9-7745-4cf8-9881-cf4a469c0512"
cp_domain = "https://api-gateway.coupang.com"
# 일단위 페이지 url
cp_url = "/v2/providers/openapi/apis/api/v5/vendors/"+cp_venderId+"/ordersheets"
cp_path = cp_domain+cp_url
# 검색 시작일시
cp_createdAtFrom = str(date.today()-timedelta(days=7))
# 검색 종료일시 (오늘날짜)
cp_createdAtTo = str(date.today())

message = datetime+method+cp_url

#********************************************************#
#authorize, demonstrate how to generate hmac signature here
signature=hmac.new(cp_secretkey.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()
authorization  = "CEA algorithm=HmacSHA256, access-key="+cp_accesskey+", signed-date="+datetime+", signature="+signature
#print out the hmac key
# print(authorization)
#********************************************************#

# ************* SEND THE REQUEST *************
# Example Endpoint
# https://api-gateway.coupang.com/v2/providers/openapi/apis/api/v5/vendors/A00012345/ordersheets?createdAtFrom=2025-07-15%2B09:00&createdAtTo=2025-07-25%2B09:00&maxPerPage=50&status=INSTRUCT
cp_api_path = "https://api-gateway.coupang.com"+cp_url+"?createdAtFrom="+cp_createdAtFrom+"%2B09:00&createdAtTo="+cp_createdAtTo+"%2B09:00&maxPerPage=100&status=INSTRUCT"


# print(cp_createdAtFrom)
# print(cp_createdAtTo)
# print(message)
print(datetime)

# ************* SEND THE REQUEST *************

req = urllib.request.Request(cp_api_path)

req.add_header("Content-type","application/json;charset=UTF-8")
req.add_header("Authorization",authorization)

req.get_method = lambda: method

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    resp = urllib.request.urlopen(req,context=ctx)
except urllib.request.HTTPError as e:
    print(e.code)
    print(e.reason)
    print(e.fp.read())
except urllib.request.URLError as e:
    print(e.errno)
    print(e.reason)
    print(e.fp.read())
else:
    # 200
    body = resp.read().decode(resp.headers.get_content_charset())
    print(body)








### 쿠팡 api 연동 End



# 2. Workbook 만들기
wb = openpyxl.Workbook()







# 자동으로 만들어지는 시트 이름 정하기
sheet = wb.active
sheet.title = "판매 주문수집"




# 대한통운 파일접수 Format 항목 정리
first_col = ['예약구분', '집하예정일', '받는분성명', '받는분전화번호', '받는분기타연락처', '받는분우편번호', '받는분주소(전체, 분할)', '운송장번호', '고객주문번호', '품목명', '	박스수량', '박스타입', '기본운임', '배송메세지1', '배송메세지2', '품목명', '운임구분']
# 첫번째 행 적용
sheet.append(first_col)





# 수하인 정보 받아오기
# 전화번호는 거의 대부분 010-0000-0000 형식으로 들어옴(후처리 필요X)
consignee_name = "아서렌탈"
consignee_phone = "010-6626-2668"
consignee_address = "인천 부평구 부평대로 337, 847호"



row = ["일반", today_date, consignee_name, consignee_phone, "", "", consignee_address, "", "", "", 1, "", "", "", "", "", ""]

sheet.append(row)


# 3. 파일 저장 위치 지정
new_filename = "C:/Users/UserK/Desktop/[작업물]/[판매] 주문수집 프로그램/test.xlsx"

# 4. 파일 저장하기
wb.save(new_filename)