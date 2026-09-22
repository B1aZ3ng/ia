#made by jakbin on https://github.com/jakbin
#edited by me to integrate into my game server application
import os
import shutil
import tempfile
from functools import wraps
from pathlib import Path
from zipfile import ZipFile
from shutil import rmtree

from flask import Flask, render_template, request, send_from_directory, json, Response, session, Blueprint
from werkzeug.utils import secure_filename

from filebrowser.funcs import get_size, diff, folderCompare
from filebrowser import auth

import globals
#since I won't be using his auth system, I can't be bothered to edit out every auth, so ill just make it false
auth_enabled = False 

# ---------- Helpers ----------
def custom_response(res, status_code):
    return Response(mimetype="application/json", response=json.dumps(res), status=status_code)



fb = Blueprint("filebrowser", __name__)


# Ensure a password exists if auth is enabled
if auth_enabled and not auth.is_password_set():
    import secrets as _secrets
    pwd = ''.join(_secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
    auth.set_password(pwd)
    print("Authentication enabled. Username: admin")
    print(f"Generated password: {pwd}")

def login_required(fn):
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        if auth_enabled and not session.get('logged_in', False):
            return custom_response({'error': 'Unauthorized'}, 401)
        return fn(*args, **kwargs)
    return _wrapper

def build_path(*parts):
    return os.path.join(*parts)

def list_dir_data(curr_path: str):
    folders, folders_date, files, files_size, files_date = [], [], [], [], []
    dir_list = os.listdir(curr_path)
    for item in dir_list:
        full = os.path.join(curr_path, item)
        if os.path.isdir(full):
            folders.append(item)
            folders_date.append(diff(full))
    for item in dir_list:
        full = os.path.join(curr_path, item)
        if os.path.isfile(full):
            files.append(item)
            files_size.append(get_size(full))
            files_date.append(diff(full))
    print(files)
    return list(zip(folders, folders_date)), list(zip(files, files_size, files_date))

# ---------- Auth Routes ----------
@fb.route('/auth/status')
def auth_status():
    return custom_response({
        'authEnabled': bool(auth_enabled),
        'loggedIn': bool(session.get('logged_in', False)),
        'user': 'admin' if session.get('logged_in') else None
    }, 200)

@fb.route('/auth/login', methods=['POST'])
def auth_login():
    if not auth_enabled:
        return custom_response({'ok': True, 'authEnabled': False}, 200)
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')
    if username != 'admin' or not auth.verify_password(password):
        return custom_response({'ok': False, 'error': 'Invalid credentials'}, 401)
    session['logged_in'] = True
    session['user'] = 'admin'
    return custom_response({'ok': True}, 200)

@fb.route('/auth/logout', methods=['POST'])
def auth_logout():
    session.clear()
    return custom_response({'ok': True}, 200)

# ---------- UI Route ----------
@fb.route("/<int:serverId>/filebrowser/")
def home(serverId):
    #print (globals.GAME_SERVERS[session.get("userId")][serverId].get_path())
    return render_template('/fb_index.html',serverId=serverId)

# ---------- File/Folder Routes ----------
@fb.route("/<int:serverId>/filebrowser/load-data", methods=['POST'])

def loaddata(serverId):
    data = request.get_json()
    name = data['name']
    folder = data['folder']
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    curr_path = build_path(home_path,folder, name)
    print (home_path, curr_path)
    if folderCompare(home_path, curr_path):
        folders_data, files_data = list_dir_data(curr_path)
        return render_template('fb_data.html', folders_data=folders_data, files_data=files_data)
    else:
        return '0', 201

@fb.route('/<int:serverId>/filebrowser/info')
def info(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    print (home_path)
    foldername = os.path.basename(home_path)
    lastmd = diff(home_path)
    dir_list = os.listdir(home_path)
    file = sum(1 for item in dir_list if os.path.isfile(item))
    folder = sum(1 for item in dir_list if os.path.isdir(item))
    data = {'foldername': foldername, 'lastmd': lastmd, 'file': file, 'folder': folder}
    return custom_response(data, 200)

@fb.route('/<int:serverId>/filebrowser/folderlist', methods=['POST'])
def folderlist(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    foldername = data['foldername']
    folder = data['folder']
    curr_path = build_path(home_path,folder, foldername)
    if folderCompare(home_path, curr_path) and str(curr_path) != (str(os.path.join(home_path,'..'))):
        dir_list = os.listdir(curr_path)
        folders = []
        for item in dir_list:
            if os.path.isdir(os.path.join(curr_path,item)):
                folders.append({"path":item })
        return {"item":folders}
    else:
        return {"item":"no more folder", "status":False}

@fb.route('/<int:serverId>/filebrowser/copyItem', methods=['POST'])
def copyItem(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    source = data['source']
    itemName = data['itemName']
    destination = data['destination']
    fodestination = data['fodestination']
    fullSource = build_path(home_path,source, itemName)
    fullDestination = build_path(home_path,source, fodestination, destination)
    try:
        shutil.copy2(fullSource, fullDestination)
        return '1'
    except NotADirectoryError:
        shutil.copytree(fullSource, fullDestination)
        return '1'
    else:
        return '0'

@fb.route('/<int:serverId>/filebrowser/moveItem', methods=['POST'])
def moveItem(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    source = data['source']
    destination = data['destination']
    itemName = data['itemName']
    fodestination = data['fodestination']
    fullSource = build_path(home_path,source, itemName)
    fullDestination = build_path(home_path,source, fodestination, destination)
    try:
        shutil.move(fullSource, fullDestination)
        return '1'
    except NotADirectoryError:
        shutil.copytree(fullSource, fullDestination)
        return '1'
    else:
        return '0'

@fb.route("/<int:serverId>/filebrowser/new-folder", methods = ['POST'])
def newfolder(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    name = data['name']
    folder = data['folder']
    try:
        os.mkdir(build_path(home_path,folder, name))
        return "1"
    except IOError as e:
        return str(e)

@fb.route("/<int:serverId>/filebrowser/new-file", methods = ['POST'])
def newfile(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    name = data['name']
    folder = data['folder']
    file_path = build_path(home_path,folder, name)
    try:
        with open(file_path, 'w') as fp:
            pass
        return "1"
    except IOError as e:
        return str(e)

@fb.route("/<int:serverId>/filebrowser/upload", methods = ['POST'])
def upload(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    folder = request.form.get('folder')
    target = build_path(home_path,folder)
    f = request.files['file1']
    if f.filename == "":
        return 'No file selected'
    elif f:
        f.save(os.path.join(target, secure_filename(f.filename)))
        return "1"

@fb.route("/<int:serverId>/filebrowser/delete", methods = ['POST'])
def delete(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    name = data['name']
    folder = data['folder']
    target = build_path(home_path,folder, name)
    if os.path.isdir(target):
        folders = os.listdir(target)
        if folders == []:
            try:
                os.rmdir(target)
                return "1"
            except IOError as e:
                return str(e)
        else:
            try:
                rmtree(target)
                return "1"
            except IOError as e:
                return str(e)
    else:
        os.path.isfile(target)
        try:
            os.remove(target)
            return "1"
        except IOError as e:
            return str(e)

@fb.route("/<int:serverId>/filebrowser/rename", methods = ['POST'])
def rename(serverId):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    data = request.get_json()
    name = data['name']
    folder = data['folder']
    dst = data['dst']
    target = build_path(home_path,folder, name)
    fullDestination = build_path(home_path,folder, dst)
    try:
        os.rename(target, fullDestination)
        return "1"
    except IOError as e:
        return str(e)

@fb.route("/<int:serverId>/filebrowser/download/<path:name>")
def download(serverId,name):
    home_path = globals.GAME_SERVERS[session.get("userId")][serverId].get_path()
    target = build_path(home_path,name)

    def get_all_dir(directory):
        file_paths = list()
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths

    if os.path.isdir(target):
        os.chdir(os.path.dirname(target))
        foldername = os.path.basename(target)
        file_paths = get_all_dir(foldername)
        # temp_dir = tempfile.gettempdir()  # kept for future use
        try:
            with ZipFile(f"{foldername}.zip", "w") as zipf:
                for file in file_paths:
                    zipf.write(file)
            return send_from_directory(directory=os.path.dirname(target), path=f"{foldername}.zip", as_attachment=True)
        finally:
            if os.path.exists(f"{foldername}.zip"):
                os.remove(f"{foldername}.zip")
    else:
        try:
            return send_from_directory(directory=os.path.dirname(target), path=os.path.basename(target), as_attachment=True)
        except IOError:
            return "can't download"





