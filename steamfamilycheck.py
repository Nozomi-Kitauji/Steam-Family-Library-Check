import requests

def get_owned_games(steam_id):
    url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': API_KEY,
        'steamid': steam_id,
        'format': 'json',
        'include_appinfo': True
    }
    response = requests.get(url, params=params, verify=True)
    data = response.json()
    games = data.get('response', {}).get('games', [])
    return {game['appid']: game['name'] for game in games}

def get_currency(countrycode):
    url = 'https://store.steampowered.com/api/appdetails/'
    params = {
        'appids': 400,
        'filters': 'price_overview',
        'cc': countrycode, 
    }
    response = requests.get(url, params=params, verify=True)
    data = response.json()
    if data["400"]['success']:
        price_info = data["400"]['data'].get('price_overview', {})
        return price_info.get('currency')

def get_batch_game_prices(appids, countrycode):
    url = 'https://store.steampowered.com/api/appdetails/'
    appids_str = ','.join(map(str, appids))  # 将多个appids拼接为字符串，批量获取价格
    params = {
        'appids': appids_str,
        'filters': 'price_overview',
        'cc': countrycode,  # 国家代码，根据需要修改
        #'l': 'cn'    # 语言，根据需要修改
    }
    
    try:
        response = requests.get(url, params=params, verify=True)
        
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}, 请求URL: {response.url}")
            return {appid: 0 for appid in appids}
        
        data = response.json()
        
        # 检查数据是否有效
        if data is None or not isinstance(data, dict):
            print(f"无效的响应数据: {data}")
            return {appid: 0 for appid in appids}
        
        prices = {}
        
        for appid in appids:
            appid_str = str(appid)
            
            if appid_str in data and data[appid_str].get('success', False):
                app_data = data[appid_str]['data']
                
                # 检查 app_data 是否为字典
                if isinstance(app_data, dict):
                    price_info = app_data.get('price_overview', {})
                    if price_info:
                        prices[appid] = price_info.get('initial', 0) / 100
                    else:
                        print(f"未找到 {appid} 的价格信息，价格设为0。")
                        prices[appid] = 0
                # 免费游戏        
                else:
                    prices[appid] = 0
                    
            else:
                print(f"未能获取 appid {appid} 在{COUNTRY_CODE}地区的价格信息，跳过该游戏。")
                prices[appid] = 0
                
        return prices
    
    except Exception as e:
        print(f"请求失败或处理异常: {e}")
        return {appid: 0 for appid in appids}

print("家庭共享库存及新增用户库存变化查询工具（以现时原价计价）")
print("1.本工具查询库存需要与账号绑定的STEAM API KEY，请到 https://steamcommunity.com/dev/apikey 登录获取并妥善保管。")
API_KEY = input("请输入STEAM API KEY：")

print("2.本工具查询库存价格需要地区代码，若库存游戏未在该区上架则无法计入（价格计为0）。")
print("常用地区代码：国区-CN，港区-HK，日本-JP，美国-US，俄罗斯-RU，巴西-BR，阿根廷-AR，土耳其-TR")
print("其余请自行查询ISO-3166两位字母代码，若输入不存在代码则默认为美区。")
COUNTRY_CODE = input("请输入地区代码：")
CURRENCY = get_currency(COUNTRY_CODE)

print("3.本工具查询用户库存需要用户的游戏详情已设置为公开，并需要用户的64位Steam ID。")
print("若不清楚用户64位Steam ID，可到 https://steamid.io 并输入用户主页URL以查询steamID64。")
FAMILY_USERIDSTR = input("请输入共享家庭中所有用户的64位Steam ID，以空格分隔：")

USER_IDS = FAMILY_USERIDSTR.split(' ', -1)
library_appids = set()
print("查询中...")

for USER_ID in USER_IDS:
    user_games = get_owned_games(USER_ID)
    library_appids = library_appids.union(set(user_games.keys()))
    
library_appids_list = list(library_appids)
batch_size = 100
total_price = 0

for i in range(0, len(library_appids_list), batch_size):
    batch_appids = library_appids_list[i:i + batch_size]
    batch_prices = get_batch_game_prices(batch_appids, COUNTRY_CODE)
    for appid in batch_appids:
        price = batch_prices[appid]
        total_price += price
print(f'家庭共享库中共有 {len(library_appids)}个游戏，这些游戏的总价格为: {total_price:.2f} {CURRENCY}\n')

USER0_ID = input("4.请输入新增用户的64位Steam ID：")
print("查询中...")
user0_games = get_owned_games(USER0_ID)
if not user0_games:
    print("无法获取用户的游戏列表。请确保用户的游戏详情已设置为公开。")
user0_appids = set(user0_games.keys())

# 找出用户0独有的游戏
unique_appids = user0_appids - library_appids

unique_appids_list = list(unique_appids)
batch_size = 100
total_price = 0

print(f'该用户拥有 {len(unique_appids)} 个共享库中没有的游戏。')
print('这些游戏及其价格如下：\n')

for i in range(0, len(unique_appids_list), batch_size):
    batch_appids = unique_appids_list[i:i + batch_size]
    batch_prices = get_batch_game_prices(batch_appids, COUNTRY_CODE)
    
    for appid in batch_appids:
        game_name = user0_games[appid]
        price = batch_prices[appid]
        total_price += price
        print(f'游戏名称: {game_name}, 价格: {price:.2f} {CURRENCY}')

print(f'该用户拥有 {len(unique_appids)} 个共享库中没有的游戏，这些游戏的总价格为: {total_price:.2f} {CURRENCY}')
input("\n按下回车键退出程序...")