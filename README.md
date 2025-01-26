# Steam-Family-Library-Check
Steam家庭共享库存及新增用户库存变化查询工具
## 功能

1.可以查询steam家庭共享库的游戏数量和总价格

2.可以查询一个steam用户能给家庭新增的游戏、价格、总价格


## 注意事项

1.本工具查询库存需要与账号绑定的STEAM API KEY，请到 https://steamcommunity.com/dev/apikey 登录获取并妥善保管。

2.本工具查询库存价格需要地区代码，若库存游戏未在该区上架则无法计入（价格计为0）。常用地区代码：国区-CN，港区-HK，日本-JP，美国-US，俄罗斯-RU，巴西-BR，阿根廷-AR，土耳其-TR，其余请自行查询ISO-3166两位字母代码，若输入不存在的代码则默认为美区。

3.本工具查询用户库存需要用户的游戏详情已设置为公开，并需要用户的64位Steam ID。若不清楚用户64位Steam ID，可到 https://steamid.io 并输入用户主页URL以查询steamID64。
