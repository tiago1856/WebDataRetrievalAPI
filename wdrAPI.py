from flask import Flask
from flask import jsonify
from flask import request
import json	
from werkzeug.exceptions import HTTPException

import WebDataRetrieval as dr


app = Flask(__name__)

'''
@app.errorhandler(Exception)
def server_error(err):
	app.logger.info((err)
	return "exception", 500
'''

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

#########################################
#	TEST
#########################################

@app.route('/')
def hello_world():
    return 'Hi from WebDataRetrievalAPI!'



#########################################
#	API
#########################################



# http://localhost:5000/api/getservices
@app.route('/api/getservices')
def getServices():
	s = dr.WebDataRetrieval()	
	return jsonify(s.getServices())
    


# http://localhost:5000/api/getbaseurls
@app.route('/api/getbaseurls')
def getBaseUrls():
	s = dr.WebDataRetrieval()	
	return jsonify(s.getBaseUrls())



# http://localhost:5000/api/getbaseurl?service=racius
@app.route('/api/getbaseurl')
def getBaseUrl():
	service  = request.args.get('service', None)
	if service:
		s = dr.WebDataRetrieval()	
		response = s.getBaseUrl(service)
		if response:
			return jsonify({"service": response})
		else:
			return jsonify({"error": "No service named " + service + "!"})
	else:
		return jsonify({"error": "You must specify a service!"})


# http://localhost:5000/api/getsus
@app.route('/api/getsus')
def getSUs():
	s = dr.WebDataRetrieval()	
	return jsonify(s.getSUs())

# http://localhost:5000/api/getdata?service=racius&name=HEMOVIDA+Lda&nif=506036944
@app.route('/api/getdata')
def getData():
	s = dr.WebDataRetrieval()
	service  = request.args.get('service', None)
	if service:		
		name  = request.args.get('name', None)
		nif  = request.args.get('nif', None)
		key_nif  = request.args.get('key_nif', None)
		key_google  = request.args.get('key_google', None)
		address  = request.args.get('address', None)
		city  = request.args.get('city', None)		
		country  = request.args.get('country', None)
		if name or nif:			
			response = s.getData(service=service, name=name, nif=nif, key_nif=key_nif, key_google=key_google, address=address,city=city,country=country)
			return jsonify(response)
		else:
			return jsonify({"error": "You must specify a name and/or its nif number!"})
	else:
		return jsonify({"error": "You must specify a service!"})


#http://localhost:5000/api/getalldata?name=HEMOVIDA+Lda&nif=506036944&key_google=YOUR_KEY&key_nif=YOUR_KEY
@app.route('/api/getalldata')
def getAllData():
	s = dr.WebDataRetrieval()
	name  = request.args.get('name', None)
	nif  = request.args.get('nif', None)
	key_nif  = request.args.get('key_nif', None)
	key_google  = request.args.get('key_google', None)
	address  = request.args.get('address', None)
	city  = request.args.get('city', None)		
	country  = request.args.get('country', None)	
	if name or nif:		
		response = s.getAll(name=name, nif=nif, key_nif=key_nif, key_google=key_google, address=address,city=city,country=country)
		return jsonify(response)
	else:
		return jsonify({"error": "You must specify, at least, a name and/or its nif number!"})



#########################################
#	MAIN
#########################################

# MAIN
if __name__ == "__main__":
	print ("\nAttempting to start server ...")
	#app.run(threaded = True)
	app.run(host='0.0.0.0')


