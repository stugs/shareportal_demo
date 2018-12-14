#!/usr/local/bin/python3

import json
from boxsdk import JWTAuth
from boxsdk import Client
from boxsdk.object.collaboration import CollaborationRole
from flask import Flask
from flask import request

app = Flask(__name__)

sdk = JWTAuth.from_settings_file('./38487735_v17qtrdu_config.json')
Box = Client(sdk)
BoxUser = Box.user(user_id='3259416447')

directory_tree = {}

def dir_index (folder_id,myname,mytype):
	tree = {'text': myname}
	tree['id'] = mytype+"_"+str(folder_id)
	if mytype == "root":
		tree['type'] = "root"
		mytype = "folder"
	else:
		tree['type'] = "folder"
	if mytype == 'folder':
		tree['children'] = [dir_index(x["id"],x["name"],x["type"]) for x in Box.as_user(BoxUser).folder(folder_id=folder_id).get_items(limit=100, offset=0)]
	else:
		tree['type'] = "file"
	return tree

@app.route('/')

def main():

	if request.args.get('endshare'):
		if request.args.get('endshare').startswith("folder"):
			collaboration = Box.as_user(BoxUser).folder(request.args.get('endshare')[7:]).get_collaborations()
			for collab in collaboration:
			    Box.as_user(BoxUser).collaboration(collab.id).delete()
		elif request.args.get('endshare').startswith("file"):
			collaboration = Box.as_user(BoxUser).file(request.args.get('endshare')[5:]).get_collaborations()
			for collab in collaboration:
			    Box.as_user(BoxUser).collaboration(collab.id).delete()
		return()
	elif request.args.get('startshare'):
		if request.args.get('startshare').startswith("folder"):
			collaboration = Box.as_user(BoxUser).folder(folder_id=request.args.get('startshare')[7:]).collaborate_with_login(request.args.get('email'), CollaborationRole.EDITOR,can_view_path='false')
		elif request.args.get('startshare').startswith("file"):
			collaboration = Box.as_user(BoxUser).file(request.args.get('startshare')[5:]).collaborate_with_login(request.args.get('email'), CollaborationRole.EDITOR)
		return(request.args.get('email'))
	else:
		with open("template.html", 'r') as txt_file:
			template_text = txt_file.read()
		return (template_text.replace('STUFF', json.dumps(dir_index(60798796555,"Box","root"),indent=2)))
