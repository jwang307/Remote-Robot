import jwt
import datetime

token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000)}, 'ae47bac2fcdbe515d53f9e0ba8434d6a', algorithm='HS256')

try:
    jwt.decode(token, 'ae47bac2fcdbe515d53f9e0ba8434d6a', algorithms=['HS256'])
    print(str(token.decode('utf-8')))
except:
    print("bad token")