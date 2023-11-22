import pandas as pd
import requests
import geohash2

def oneroom(addr):
    # 1. 망원동의 위도, 경도 구하기
    url = f'https://apis.zigbang.com/v2/search?leaseYn=N&q={addr}&serviceType=원룸'
    response = requests.get(url)
    lat = response.json()['items'][0]['lat']
    lng = response.json()['items'][0]['lng']
    
    # 2. geohash 값 구하기
    geohash = geohash2.encode(lat, lng, precision=5)
    
    # 3. geohash 위치의 매물아이디 찾아오기
    url = f'https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸'
    response = requests.get(url)
    
    #4. response 값에서 아이디값만 가져오기
    items = response.json()['items']
    ids = []
    for item in items:
        ids.append(item['item_id'])
        
    #5. 해당 아이디의 매물 정보 가져와서 필요한 데이터 뽑아내기
    url = 'https://apis.zigbang.com/v2/items/list'
    params = {'domain': 'zigbang', 'item_ids': ids}
    response = requests.post(url, params)
    
    items = response.json()['items']
    df = pd.DataFrame(items)
    
    columns = ['item_id', 'title', 'deposit', 'rent', 'address1', 'size_m2', 'manage_cost']
    df = df[columns]
    df = df.loc[df['address1'].str.contains(addr)]
    return df.reset_index(drop=True)
