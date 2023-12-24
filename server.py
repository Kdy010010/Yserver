import os
from flask import Flask, render_template, request, send_from_directory, session
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    room = session.get('room')
    socketio.emit('message', msg, room=room)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

@socketio.on('file')
def handle_file(data):
    room = session.get('room')
    socketio.emit('file', {'filename': data['filename'], 'url': f'/uploads/{data['filename']}'}, room=room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    session['room'] = room
    socketio.emit('message', f'{username} 님이 채팅방에 참여하셨습니다.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    session.pop('room', None)
    socketio.emit('message', f'{username} 님이 채팅방에서 나가셨습니다.', room=room)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    socketio.run(app, debug=True)
