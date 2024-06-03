import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'tester123'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
 mqtt.subscribe('Home/BedRoom/1/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
 data = dict(
 topic=message.topic,
 payload=message.payload.decode()
 )
 print(data['payload'])
 socketio.emit('mqtt_message', data=data)

@app.route('/')
def index():
 return render_template('index.html')

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
 print(level, buf)

if __name__ == '__main__':
 socketio.run(app, host='0.0.0.0', port=5001, use_reloader=False, debug=True)
