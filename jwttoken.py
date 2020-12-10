import jwt
import datetime

token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10000)}, 'randonlygeneratedkeys', algorithm='HS256')

try:
    jwt.decode(token, 'randonlygeneratedkeys', algorithms=['HS256'])
    print(str(token.decode('utf-8')))
except:
    print("bad token")