from flask import *
import os
import json
import re
import urllib3
import random


app = Flask(__name__)
http = urllib3.PoolManager()

def return_response(object):
    return Response(json.dumps(object), mimetype='application/json')

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/getCpuUsage')
def returnCpuUsage():
    ret = os.popen("uptime | cut -d' ' -f12,13,14").read().strip()
    return return_response(ret)

@app.route('/getMemory')
def getMemory():
    ret = os.popen("free -m | grep Mem | tr -s ' ' | cut -d' ' -f2,3,4,7").read().strip()
    return return_response(ret)

@app.route('/getTop5Processes')
def getTop5Processes():
    ret = os.popen("ps aux | tr -s ' ' | sort -nrk 3,3 | head -n 5 | cut -d' ' -f1,2,3,4,11").read().strip()
    return return_response(ret)

@app.route('/getConnections')
def getConnections():
    ret = os.popen('netstat -natp | tr -s " "').read().strip()
    return return_response(ret)

@app.route('/getConnectionsCount')
def getConnectionsCount():
    ret = os.popen('netstat -natp | grep -c tcp').read().strip()
    return return_response(ret)

@app.route('/getApacheLogSpaceUsage')
def getApacheLogSpaceUsage():
    ret = os.popen("sudo du -sh /var/log/apache2").read().strip()
    return return_response(re.split(r'\t+', ret)[0])

@app.route('/getDiskSpace')
def getDiskSpace():
    ret = os.popen('sudo df -BG | grep /dev/sda1 | tr -s " "').read().strip()
    return return_response(ret)

@app.route('/killDeterlabTracing')
def killDeterlabTracing():
    os.popen('sudo kill -9 $(ps aux | grep -i "analyze.py" | tr -s " " | head -n 1 | cut -d" " -f2)')
    return return_response("ok")

@app.route('/testWebserver')
def testWebserver():
    n = random.randint(1,10)
    try:
        r = os.popen('curl 127.0.0.1/' + str(n) + '.html -m 1 -s -o /dev/null -w  "%{time_total},%{http_code}\n"').read().strip()
        r = r.split(",")
        if(len(r) == 2 and (r[1] == "200" or r[1] == 200)):
            if(float(r[0]) > 0.35):
                return return_response("bad")
            elif (float(r[0]) > 0.15):
                return return_response("meh")
            else:
                return return_response("ok")
        else:
            return return_response("fail")
    except Exception as e:
        print(e)
        return return_response("fail")


app.run(port=3030,host='0.0.0.0', debug=True)
