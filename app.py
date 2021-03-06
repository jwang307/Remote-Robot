from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, session
from socket import socket, AF_INET, SOCK_DGRAM
from flask_socketio import SocketIO, emit
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ae47bac2fcdbe515d53f9e0ba8434d6a'
socketio = SocketIO(app)
mySocket = socket(AF_INET, SOCK_DGRAM , 0)
lst_clients=[]

def check_jwt_valid(token):
    valid = True
    try:
        data =  jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except Exception as e:
        session.clear
        print('token exception '+ str(e))
        valid = False
    return valid

def sendmessage(keyname):
    try:
        # RC phone ip address and port number
        print('sent to rc phone ' + keyname)
        mySocket.sendto(keyname.encode('utf-8'),('192.168.49.1',11039))
        return keyname
    except Exception as inst:
        print(inst)


@app.route("/",  methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if len(lst_clients) >=1:
            error = "Can only allow one user at a time."
        else:
            token = request.form['token']
            if check_jwt_valid(token):
                session['Authorization']=token
                resp = make_response(redirect(url_for('gamepad',data='test') ,code=307))
               # resp.set_cookie('Authorization', token, samesite=None, secure=True);
                resp.headers.add('Set-Cookie','Authorization='+token +'; SameSite=None; Secure')
                return resp
            else:
                error = "Token is not valid"
    return render_template('login.html', error=error)

@app.route("/gamepad", methods=['POST'])
def gamepad():
    token = session.get('Authorization')
    if not token:
        token = request.cookies.get('Authorization')
    if (len(lst_clients) == 0 or (request.sid and request.sid in lst_clients)) and check_jwt_valid(token):
        return render_template('gamepad.html')
    else:
        error = "Token is not valid"
        return render_template('login.html', error=error)

@socketio.on('my_event', namespace='/test')
def test_message(message):
    print("in test_message"+ message['data'])
    token = session.get('Authorization')
    if not token:
        token = request.cookies.get('Authorization')
    if check_jwt_valid(token):
        sendmessage(message['data'])
        emit('my_response',
            {'data':  "receieved" + message['data']})
    else:
        emit('redirect', '/')

@socketio.on('connect', namespace='/test')
def connect():
    lst_clients.append(request.sid)
    print("client connected " + str(request.sid))


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    lst_clients.remove(request.sid)
    print("Client disconnected " + str(request.sid))
    emit('redirect', '/')


if __name__ == "__main__":
    #this is the rasberrypi internal ip(find on router network), should match in index.html
    app.run(debug = True, host="0.0.0.0", port = 2005, threaded = True, ssl_context=('cert.pem', 'key.pem'))
   