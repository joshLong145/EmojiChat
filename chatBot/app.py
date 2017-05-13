from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
import exception_handling
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
#loading login page or main chat page
def index():
	if not session.get('logged_in'):
		return render_template("login.html")
	else:
		return render_template('chat.html')

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/login',methods=['POST'])
def log_in():
	#complete login if name is not an empty string or doesnt corss with any names currently used across sessions
	if request.form['username'] != None and request.form['username'] != "":
		session['logged_in'] = True
		# cross check names and see if name exists in current session
		session['username'] = request.form['username']
		return redirect(url_for('index'))

	return redirect(url_for('index'))
	
@app.route("/logout")
def log_out():
	# Clear the session
    session.clear()
    # Redirect the user to the main page
    return redirect(url_for('index'))
# /////////socket io config ///////////////
#when message is recieved from the client    
@socketio.on('message')
def handleMessage(msg):
    print("Message recieved: " + msg)
    send(session.get('username') + " " + msg,broadcast = True)
# socket-io error handling
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass

if __name__ == '__main__':
    socketio.run(app,debug=True,host='0.0.0.0', port=4000)
