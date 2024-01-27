import os
import requests
import json 

def getTokens()-> (str,str):
    mail = os.environ.get('J_QUANTS_MAIL_ADDRESS')
    passwd = os.environ.get('J_QUANTS_PASSWD')

    data={"mailaddress":mail, "password":passwd}
    refreshToken_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
    refreshToken_json = refreshToken_post.json()
    refreshToken = refreshToken_json['refreshToken']
    print(refreshToken)
    idToken_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refreshToken}")
    idToken_json = idToken_post.json()
    idToken = idToken_json['idToken']
    print(idToken)

    return refreshToken,idToken