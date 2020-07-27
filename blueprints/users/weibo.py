# 引导用户授权地址
authorize_url = 'https://api.weibo.com/oauth2/authorize'

# 应用 App Key:
client_id = '3960285513'
# 应用 App Secret
client_secret = '6a17b9caf57cf885a2d7c283f6eee4db'
# App Key  App Secret可在应用的详情信息中找到

# 回调地址,线上地址
redirect_uri = 'http://127.0.0.1:5000/login/bindemail/'
# 获取用户access_token地址
access_token_url = 'https://api.weibo.com/oauth2/access_token'
# 获取用户信息的 url
info_url = 'https://api.weibo.com/2/users/show.json'
