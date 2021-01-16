#clean user data funs
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import Markup

site_secret_key = 'WEBSITE_SECRET_KEY'

def gen_unik_token(email):
    s = Serializer(site_secret_key, 60 * 30)  # 60 secs by 30 mins
    token = s.dumps({'email': email}).decode('utf-8')  # encode user id
    return token

def get_token_data(token):
    s = Serializer(site_secret_key)
    email = {'email': ''}
    try:
        email = s.loads(token)['email']
    except Exception as e:
        print(e)
    return email

def clean_user_data(data):
    #check sql commands
    """
    clean_data = {}
    for k,v in data.items():
        if v is None:
            v = ''
        clean_data[k] = escape(v)
    """
    return data

#stop sql injection test
#cross site attack
#js atk
#...