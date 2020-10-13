## Gamepad
read out input from Gamepad, send to phone through socket connection

###Start Python Env
`python3 -m venv .env`
`source .env/bin/activate`

### Intall packages
`pip3 install flask`
`pip3 install sockets`
`pip3 install flask-socketio`

or 

`pip3 install -r requirements.txt`

### Generate self signed certificate
`openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`

### Run
`python3 app.py`