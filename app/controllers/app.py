import settings
import os
import datetime

from flask import Flask, render_template
from flask import request, jsonify, flash, session, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_login import current_user

from app.models.log import Logs, Log
from app.models.user import User
from app.models.user import LoginUser
from app.controllers.utils import GetHashValue, GetLogsJsonformat, timetostr


app = Flask(__name__, template_folder='../views', static_folder='../static')
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
   return LoginUser().get_user_one_or_none(user_id)

@app.teardown_appcontext
def remove_session(ex=None):
    from app.models.base import Session
    Session.remove()

@app.route('/', methods=['GET', 'POST'])
def login():
   if request.method == 'GET':
      return render_template('login.html')
   username = request.form['username']
   password = GetHashValue(request.form['password'])
   try:
      user = LoginUser().get_user_one_by_name(username)
      if user == None:
         return render_template('login.html', error='該当するユーザーが存在しない')
      if user.value['password'] != password:
         return render_template('login.html', error='パスワードが異なる')
      else:
         login_user(user, remember=True)
   except Exception as e:
      return redirect(url_for('login'))
   
   return render_template('message.html', current_user=current_user.user_name)
 
@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

@app.route('/message', methods=['POST'])
@login_required
def PostLogData():
   message = request.json['message']
   log = Log(time=datetime.datetime.utcnow(), name=current_user.user_name, message=message, show=0)
   log.save()
   return jsonify(ResultSet="")

@app.route('/message', methods=['GET'])
@login_required
def GetLogData():
   jslog = GetLogsJsonformat()
   if jslog is None:
      return jsonify(ResultSet="")
   return jsonify(ResultSet=jslog)

@app.route('/Delete_message', methods=['POST'])
@login_required
def DeleteLog():
   Log().DeleteAllRecord()
   return jsonify(ResultSet="")
