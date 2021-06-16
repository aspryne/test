import os
import subprocess
import sys
import json
import logging
import time

HOST = ""
SCHEMA = "http://"
CURL_CMD = "curl -k -sL "
URL_GET_TOKEN_X = ""
URL_GET_TOKEN_H = ""
URL_GET_TENANTS = ""
URL_UPDATE_TENANTS = ""
URL_UPDATE_SETTING = ""
SETTING_VALUE = ""

env_dist = os.environ
log_path = "."

logger = logging.getLogger("update")
file_handler = logging.FileHandler(log_path + "/update.log")
file_handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def log(content):
	logger.info("======================================")
	logger.info(content)
	logger.info("======================================")

def execute(cmd):
	rs = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
	rs.wait()
	retcode = rs.returncode
	retlines = ''
	for line in rs.stdout.readlines():
			retlines = retlines + line
	return {"code":retcode, "message":retlines}

def get_cmd_gettoken():
	token = get_cmd_gethtoken()
	return token

def get_cmd_gethtoken():
	log(CURL_CMD + URL_GET_TOKEN_H)
	return CURL_CMD + URL_GET_TOKEN_H	
	
def get_cmd_setting(token, body):
	return CURL_CMD + '-X GET -H "Cookie:LWSSO_COOKIE_KEY=' + token + '" ' + URL_SETTING

	
def get_cmd_updatesetting(token, body):
	return CURL_CMD + '-X PUT -H "Cookie:LWSSO_COOKIE_KEY=' + token + '" -H "Content-Type:application/json" -d \'' + body + '\' ' + URL_UPDATE_SETTING

def update():
	# get token
	result = execute(get_cmd_gettoken())
	log(result)
	# run success
	if result["code"] == 0:
		token = result["message"]
		# get tenants list
		log(result)
		
		update_command = get_cmd_setting(token, "{" + SETTINGNAME + ": "+ SETTING_VALUE +"}")
		log("command: " + update_command)
		result = execute(update_command)
		log( "Value Before" )
		log( result )

		
		update_command = get_cmd_updatesetting(token, "{" + SETTINGNAME + ": "+ SETTING_VALUE +"}")
		log("command: " + update_command)
		result = execute(update_command)
                log( result )
                
 		update_command = get_cmd_setting(token, "{" + SETTINGNAME + ": "+ SETTING_VALUE +"}")
 		log("command: " + update_command)
 		result = execute(update_command)
 		log( "Value After" )
 		log( result )
                
		return True
	else:
		log("execut get token failed!")
		return False


if __name__ == "__main__":
	if len(sys.argv) != 7:
                print sys.argv
		print len(sys.argv)
		print "wrong args, [HOST] [TENANTID] [user] [password] [boolean|value] [SETTING_NAME]"
		sys.exit(-1)

	HOST = sys.argv[1]
	TENANTID = sys.argv[2]
	user = sys.argv[3]
	pwd = sys.argv[4]
	value = sys.argv[5]
	SETTINGNAME = sys.argv[6]

	URL_GET_TOKEN_H = '"' + SCHEMA + HOST + "/auth/authentication-endpoint/authenticate/login?login=" + user + "&password=" + pwd + "&tenantId=" + TENANTID + '"'
	SETTING_VALUE = value
	URL_UPDATE_SETTING = '"' + SCHEMA + HOST + "/rest/" + TENANTID  + "/TenantSettings/settings/" + SETTINGNAME +'"'
        URL_SETTING = '"' + SCHEMA + HOST + "/rest/" + TENANTID  + "/TenantSettings/settings/" + SETTINGNAME +'"'


	if update():
		print("Updated setting to :" + SETTING_VALUE)
		sys.exit(0)
	else:
		sys.exit(-1)

