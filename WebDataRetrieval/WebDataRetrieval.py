# pip install lxml
# pip insall requests
#
#	KNOWN ISSUES:
#		RACIUS:
#			EX: 
# 				Gomes & Ferreira, Lda
#				https://www.racius.com/gomes-ferreira-lda-7/
#
#		CODIGOPOSTAL.CIBERFORMA
#			if LDA => it may or may not have it in the url
#

from lxml import html
import requests
import json
#mport logging
import unicodedata
import re
from geopy.geocoders import GoogleV3
from geopy.exc import (
    GeocoderQueryError,
    GeocoderQuotaExceeded,
    ConfigurationError,
    GeocoderParseError,
    GeocoderAuthenticationFailure,
    GeocoderInsufficientPrivileges,
    GeocoderTimedOut,
    GeocoderServiceError,
    GeocoderUnavailable,
    GeocoderNotFound
)

#logger = logging.getLogger("root")
#logger.setLevel(logging.DEBUG)
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)




def replacePTChars(s):
	return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def replaceAllNonAlfaNum(s,by_what=" "):
	return re.sub('[^A-Za-z0-9]+', by_what, s)
	
# including trailing spaces
def removeAllExtraSpaces(s):
	#return re.sub(' +', ' ',s)
	return " ".join(s.split())


class WebDataRetrieval():
	
	# when merging, the highest in the list the highest the priority
	# so, put the best and more reliable services on top
	SERVICES_BASE_URLS = {
		'nif': 'https://www.nif.pt/',
		"racius" : 'https://www.racius.com/',
		"codigopostal.ciberforma" : 'https://codigopostal.ciberforma.pt/dir/',
		"portugalio" : 'https://www.portugalio.com/',
		"einforma" : 'https://www.einforma.pt/servlet/app/portal/ENTP/prod/ETIQUETA_EMPRESA/nif/',
		"google": "GEOPY package: https://pypi.org/project/geopy/"
	}
	



	# all the relevant data to be extracted
	def newResult(self):
		result = {
			'type': None,
			'nome': None,
			'nome_legal': None,
			'nif': None,
			'data_inicio': None,		# data inicio de actividade | constituição
			'morada': None,
			'localidade': None,
			'distrito': None,
			'concelho': None,
			'freguesia': None,
			'codigo_freguesia': None,
			'codigo_postal': None,
			'forma_juridica': None,		# LDA | Cooperativa | Sociedade por Quotas | Sociedade Unipessoal
			'telefone': None,
			'fax': None,
			'cae': None,
			'actividade': None,			# descricao da actividade
			'site': None,
			'latitude': None,
			'longitude': None,
			'horario': None,
			'email': None,
			'telemovel': None,
			'estado': None,		# EM ACTIVIDADE | EM INSOLVENCIA | EM REVITALIZAÇÃO | ENCERRADA (Dissolução e Liquidação)
			'status': None,		# OK => some data was fetched	| NOT_FOUNDED => 404 or nothing
			'url': None,		# used url
			'service': None,	# servico usado
			'data': {},		# miscelaneous data. Ex: google place_id 
		}
		return result


	def __init__(self):
		pass

	def getServices(self):
		return list(self.SERVICES_BASE_URLS.keys())
	
	def getBaseUrls(self):
		return list(self.SERVICES_BASE_URLS.values())

	def getBaseUrl(self, service):
		if service in self.SERVICES_BASE_URLS:
			return self.SERVICES_BASE_URLS[service]
		return None

	def getSUs(self):
		return self.SERVICES_BASE_URLS

	def sanitize(self, name_or_address):
		temp = name_or_address.lower()	
		temp = replacePTChars(temp)
		temp = replaceAllNonAlfaNum(temp)
		temp = removeAllExtraSpaces(temp)
		return temp



#	def printR(self, result = None):
#		if not result:
#			return
#		for key, value in result.items():
#			logger.info('{}: {}'.format(key, value))
		


	# dashes: dashes between words?
	# lda: lda or limitada at the end?
	# sa: SA or S.A. or S.A at the end?
	# unipessoal: unipessoal in the url?
	def parseName(self, name, dashes=True, lda = True, sa = True, unipessoal = True):
		if dashes:
			name = name.replace(" ", "-")
		if not lda:
			name = name.replace('lda',"")
			name = name.replace('limitada',"")
				
		if not unipessoal:
			name = name.replace('unipessoal',"")

		if not sa:
			if name.endswith('-sa'):
				name = name[:-2]		
			elif name.endswith('-s-a'):
				name = name[:-3]		

		# some cleanups
		#name = name.strip()
		while name.endswith('-'):			
			name = name[:-1]

		return name


	# used by einforma
	def format_date(self, date):
		mes,ano = date.split(' ',2)
		mes = self.sanitize(mes)
		if mes == "janeiro":
			mes = 1
		elif mes == "fevereiro":
			mes = 2
		elif mes == "marco":
			mes = 3
		elif mes == "abril":
			mes = 4
		elif mes == "maio":
			mes = 5
		elif mes == "junho":
			mes = 6
		elif mes == "julho":
			mes = 7
		elif mes == "agosto":
			mes = 8
		elif mes == "setembro":
			mes = 9
		elif mes == "outubro":
			mes = 10
		elif mes == "novembro":
			mes = 11
		elif mes == "dezembro":
			mes = 12
		return "01-" + str(mes) + "-" + ano


	#DASHES
	#LDA
	#LIMITADA
	#PREPOSICOES
	#LOWERCASE
	def Racius(self, empresa, NIF=None):

		if not empresa:
			raise RuntimeError("Requires a name!")

		# finalize the URL
		empresa = self.parseName(empresa, dashes=True, lda = True)
		URL = self.SERVICES_BASE_URLS['racius'] + empresa + '/'

		# fetch the page
		page = requests.get(URL)
		tree = html.fromstring(page.content)
		
		result = self.newResult()

		result['url']  = URL
		result['service']  = 'racius'
		if NIF:
			 result['nif']  = NIF
		
		###
		#tree = html.fromstring(PP)
		###	
		title = tree.xpath('//title/text()')
		if '404' in title[0]:
			result['status'] = "NOT_FOUNDED"
			return result
		
		
		data_json = tree.xpath('//script[@type="application/ld+json"]/text()')
		if len(data_json) > 0:
			data = data_json[0]
			data = json.loads(data)
			
			result['type'] = data.get("@type")
			result['nome'] = data.get("name")
			result['nome_legal'] = data.get("legalName")
			result['nif'] = data.get("taxID")
			result['data_inicio'] = data.get("foundingDate")
			if data.get("address"):
				result['morada'] = data.get("address").get("streetAddress")
				result['localidade'] = data.get("address").get("addressLocality")
				result['codigo_postal'] = data.get("address").get("postalCode")	


			result['estado'] = "EM ACTIVIDADE"
			if len(data_json) > 1:		
				for e in data_json:
					e = json.loads(e)
					content = e.get("name")
					if content.find("Dissolução e Liquidação") != -1:
						result['estado'] = "ENCERRADA"
						break
					elif content.find("Insolvência") != -1:
						result['estado'] = "EM INSOLVÊNCIA"
						break
					elif content.find("Revitalização") != -1:
						result['estado'] = "EM REVITALIZAÇÃO"
						break
				
				
			data = tree.xpath('//table[@class="table"]/tr/*/text()')		
			
			juridica_index = data.index("Forma Jurídica") if "Forma Jurídica" in data else None
			if juridica_index:		
				result['forma_juridica'] = data[juridica_index + 1]

			if result['data_inicio'] == "" or result['data_inicio'] is None:
				init_index = data.index("Data Constituição") if "Data Constituição" in data else None
				if init_index:
					result['data_inicio'] = data[init_index + 1]		
			
			result['status'] = "OK"
			
			return result
			
		return result


	# DASHES
	# LDA AND NO LDA
	# S.A. ->S-A
	# LOWCASE
	# NIF
	# PROPOSITIONS
	# UNIPESSOAL
	def CodigoPostal_Ciberforma(self, empresa, NIF = None):
		
		if not empresa:
			raise RuntimeError("Requires a name!")
		if not NIF:
			raise RuntimeError("Requires a NIF!")
		

		# finalize the URL
		empresa = self.parseName(empresa,dashes=True)
		URL = self.SERVICES_BASE_URLS['codigopostal.ciberforma'] + str(NIF) + '/' + empresa + '/'	

		# fetch the page
		page = requests.get(URL)		
		tree = html.fromstring(page.content)
		#tree = html.fromstring(PP)
		
		result = self.newResult()
		
		result['service']  = 'codigopostal.ciberforma'
		result['url']  = URL
		result['nif']  = NIF		
			
		title = tree.xpath('//title/text()')
		if '404' in title[0]:
			result['status'] = "NOT_FOUNDED"
			return result
			


		nome = tree.xpath('//span[@class="auto-title left"]/text()')
		if len(nome) > 0:
			result['nome'] = nome[0]	
			

		temp = tree.xpath('//h4//text()')
		tel = temp.index("Telefone: ") if "Telefone: " in temp else None
		if tel:
			result['telefone'] = temp[tel + 1]

		tel = temp.index("Fax: ") if "Fax: " in temp else None
		if tel:
			result['fax'] = temp[tel + 1]
		
		tel = temp.index("Site: ") if "Site: " in temp else None
		if tel:
			result['site'] = temp[tel + 1]
		
		tel = temp.index("E-Mail: ") if "E-Mail: " in temp else None
		if tel:
			result['email'] = temp[tel + 1]



		morada = tree.xpath('//h4[@class=""]/text()')
		if len(morada) > 0:
			result['morada'] = morada[0]
		if len(morada) > 1:
			result['localidade'] = morada[1]
		if len(morada) > 2:
			cp = re.sub('[^0-9-]+', "", morada[2])
			result['codigo_postal'] = cp
		
		d_c_f = tree.xpath('//h6/a/text()')
		if len(d_c_f) > 0:
			result['freguesia'] = d_c_f[0]
		if len(d_c_f) > 1:
			result['concelho'] = (d_c_f[1].split(' ', 1)[1]).split(' ', 1)[1]
		if len(d_c_f) > 2:
			result['distrito'] = (d_c_f[2].split(' ', 1)[1]).split(' ', 1)[1]

		nif = tree.xpath('//div[@class="ads-details-info col-md-10"]/p/text()')
		if len(nif) > 0:
			#nif_item = None
			data = None
			for i in nif:
				if i.find("Constituída") != -1: # in i:
					data = i
					break
			if data:
				result['data_inicio'] = data.split('em ')[1]

		cae = tree.xpath('//div[@class="ads-details-info col-md-8"]/*/text()')
		c_f = ""
		cod_cae = ""
		for i in cae:
			if i.find("Código de freguesia") != -1: # in i:
				c_f = i
			if i.find("com o CAE") != -1:# in i:
				cod_cae = i
		if c_f != '':
			result['codigo_freguesia'] = c_f.split(': ')[1]
		if cod_cae != '':
			result['cae'] = cod_cae.split('com o CAE ')[1]	

	
		
		result['status'] = "OK"
		
		return result

	# DASHES
	# PROPOSICOES
	# NO LDA
	# NO SA
	# LOWCASE
	# NO UNIPESSOAL
	def Portugalio(self, empresa, NIF = None):

		if not empresa:
			raise RuntimeError("Requires a name!")

		# finalize the url
		empresa = self.parseName(empresa,dashes=True, lda=False, sa=False, unipessoal=False)		
		URL = self.SERVICES_BASE_URLS['portugalio'] + empresa + '/'	

		# fetch the page
		page = requests.get(URL)	
		tree = html.fromstring(page.content)
		#tree = html.fromstring(PP)

		result = self.newResult()

		result['service']  = 'portugalio'
		result['url']  = URL
		if NIF:
			 result['nif']  = NIF
		
		title = tree.xpath('//title/text()')
		if 'Página não encontrada' in title[0]:
			result['status'] = "NOT_FOUNDED"
			return result


		data = tree.xpath('//script[@type="application/ld+json"]/text()')
		if len(data) > 0:

			final_pos =  data[0].find('\"]}')
			if final_pos < 0:
				final_pos =  data[0].find("}}") + 3
			else:
				final_pos += 5
			data = data[0][data[0].find('{"@') : final_pos]
			
			# description usually contains " which can fuck things up when conv to json
			# so, remove the field it before the conversion
			desc = data.find('\"description\"')
			if desc > 1:
				desc_end = data.find('\",', desc)
				a1 = data[0: desc]
				a2 = data[desc_end + 2:]
				data = a1+a2
			
			data = json.loads(data)
			
			result['type'] = data.get("@type")
			if data.get("address"):
				result['codigo_postal'] = data.get("address").get("PostalAddress")		
				result['morada'] = data.get("address").get("streetAddress")
				result['localidade'] = data.get("address").get("addressLocality")		
			result['nome'] = data.get("name")
			if data.get("geo"):
				result['latitude'] = data.get("geo").get("latitude")
				result['longitude'] = data.get("geo").get("longitude")
			result['nif'] = data.get("taxID")		
			result['telefone'] = data.get("telephone")
			if result['telefone']:
				if len(result['telefone']) > 0:
					result['telefone'] = (result['telefone'][0]).replace(" ", "")
			result['fax'] = data.get("faxNumber")
			if result['fax']:
				result['fax'] = result['fax'].replace(" ", "")
			
			if data.get("url"):
				if len(data.get("url")) > 1:
					result['site'] = data.get("url")[1]
			
			result['horario'] = data.get("openingHours")
		
		
			nif = tree.xpath('//div[@class="company-flat-inner-content"]/*/b/text()')
			cae = tree.xpath('//div[@class="company-flat-inner-content"]/*/text()')
			
			if nif:
				nif = "".join(nif)
				result['nif'] = re.sub('[^0-9]+', "", nif)
			

			if cae:
				cae = [s for s in cae if " CAE " in s]
				if len(cae) > 0:
					cae = cae[0].split("CAE ")[1]
					cae = cae.split(" ")[0]
					result['cae'] = cae
		
			result['status'] = "OK"

		return result





	def Einforma(self, empresa, NIF = None):
		
		if not NIF:
			raise RuntimeError("Requires a NIF!")

		# finalize url creation
		URL = self.SERVICES_BASE_URLS['einforma'] + str(NIF) + "/"
		
		result = self.newResult()

		result['service']  = 'einforma'
		result['url']  = URL
		result['nif']  = NIF

		# fetch page
		page = requests.get(URL)		
		tree = html.fromstring(page.content)
		#tree = html.fromstring(PP)


		status = tree.xpath('//p[@class="title01 mt0"]/text()')
		if len(status) > 0:
			if status[0].find("Empresa não encontrada") != -2: # in status[0]):
				result['status'] = "NOT_FOUNDED"
				return result
		
		
		nome = tree.xpath('//span[@itemprop="name"]/text()')
		if len(nome) > 0:
			result['nome'] = nome[0]
		
		morada = tree.xpath('//span[@itemprop="streetaddress"]/text()')
		if len(morada) > 0:
			result['morada'] = morada[0]
		
		cp = tree.xpath('//span[@itemprop="postalcode"]/text()')
		if len(cp) > 0:
			result['codigo_postal'] = cp[0]
		
		site = tree.xpath('//span[@itemprop="url"]/text()')
		if len(site) > 0:
			result['site'] = site[0]
		
		
		localidade = tree.xpath('//span[@class="locality"]/text()')
		if len(localidade) > 0:
			result['localidade'] = localidade[0]
		
		data_inicio = tree.xpath('//span[@class="type"]/text()')
		if len(data_inicio) > 0:
			result['data_inicio'] = self.format_date(data_inicio[0])	# month year

		result['status'] = "OK"

		return result



	def getNifInfo(self, nif = None, key_nif = None):
		if not nif:
			raise RuntimeError("Requires a NIF!")
		if not key_nif:
			raise RuntimeError("Requires a key! Request one at http://www.nif.pt/contactos/api/")
		
		# complete the url
		url = 'https://www.nif.pt/?json=1&q={}&key={}'.format(nif, key_nif)

		# fetch the data
		results = requests.get(url)
		results = results.json()

		result = self.newResult()

		result['service']  = 'nif'
		result['status'] = 'NOT FOUNDED'
		result['url']  = self.SERVICES_BASE_URLS['nif']

		nif = str(nif)

		if 'result' in  results and results['result'] != 'success':
			if results['result'] == 'error':
				result['status'] = 'ERROR'
				return result
			raise RuntimeError(results['message'])
		
		if 'records' in results and nif in results['records']:
			results = results['records'][nif]
			
			result['status'] = 'OK'
			
			if 'title' in results:
				result['nome'] = results['title']
			if 'address' in results:
				result['morada'] = results['address']
			cp=None
			cp_ext=None
			if 'pc4' in results:
				cp = results['pc4']
			if 'pc3' in results:
				cp_ext = results['pc3']
			result['codigo_postal'] = cp
			if cp and cp_ext:
				result['codigo_postal'] += "-" + cp_ext
			if 'city' in results:
				result['localidade'] = results['city']
			if 'start_date' in results:
				result['data_inicio'] = results['start_date']
			
			if 'activity' in results:
				result['actividade'] = results['activity']
			if 'status' in results:
				result['estado'] = results['status']
			if 'cae' in results:
				result['cae'] = results['cae']
			
			if 'contacts' in results:
				contacts = results['contacts']
				if 'email' in contacts:
					result['email'] = contacts['email']
				if 'phone' in contacts:
					result['telefone'] = contacts['phone']
				if 'website' in contacts:
					result['site'] = contacts['website']
				if 'fax' in contacts:
					result['fax'] = contacts['fax']
			
			if 'structure' in results:
				struct = results['structure']
				if 'nature' in struct:
					result['forma_juridica'] = struct['nature']

			
			
			if 'geo' in results:
				geo = results['geo']
				if 'region' in geo:
					result['distrito'] = geo['region']
				if 'county' in geo:
					result['concelho'] = geo['county']
				if 'parish' in geo:
					result['freguesia'] = geo['parish']
			
			if 'place' in results:
				place = results['place']
				if not result['morada'] and 'address' in place:
					result['morada'] = place['address']
				if not result['codigo_postal'] and 'pc4' in place:
					cp_ext = None
					cp = place['pc4']
					if 'pc3' in place:
						cp_ext = place['pc3']
					result['codigo_postal'] = cp
					if cp_ext:
						result['codigo_postal'] += "-" + cp_ext
				if not result['localidade'] and 'city' in place:
					result['localidade'] = place['city']
				
		return result


	def getGoogleInfo(self, address=None, name=None, city=None, country=None, key_google=None):

		if not key_google:
			raise RuntimeError("Requires a key! Check https://developers.google.com/maps/documentation/geocoding/get-api-key for more information.")

		if not address and not name:
			raise RuntimeError("Requires either a name or an address!")

		addr = "" if name is None else name
		addr = addr + ("" if address is None else ", " + address)
		addr = addr + ("" if city is None else ", " + city)
		addr = addr + ("" if country is None else ", " + country)


		# start service
		geolocator_google = GoogleV3(api_key=key_google)

		result = self.newResult()
		result['service']  = 'google'
		result['status'] = 'NOT FOUNDED'
		result['url']  = self.SERVICES_BASE_URLS['google']

		try:
			# fetch the data
			data = geolocator_google.geocode(addr,exactly_one=False)

			if data:			
				answer = data[0].raw

				result['status'] = "OK"		
				result["morada"] = data[0].address
				result["latitude"] = data[0].latitude
				result["longitude"] = data[0].longitude
				result["codigo_postal"] = ",".join([x['long_name'] for x in answer.get('address_components') 
										if 'postal_code' in x.get('types')])
				result["localidade"] = ",".join([x['long_name'] for x in answer.get('address_components') 
										if 'locality' in x.get('types')]).split(',')[0]

				result["data"].update({'place_id': answer.get("place_id")})

				return result

		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			result['status'] = 'ACCESS_ERROR'
		except GeocoderQuotaExceeded:
			result['status'] = 'QUOTA_EXCEEDED'
		except GeocoderTimedOut:
			result['status'] = 'TIME_OUT'
		except (GeocoderServiceError,GeocoderUnavailable,GeocoderNotFound):
			result['status'] = 'SERVICE_ERROR'
		except Exception:
			result['status'] = 'UNKNOWN_ERROR'

		
		return result




	def getData(self, service=None, name=None, address=None, city=None, country=None, nif=None, key_nif=None, key_google=None):
		if not service:
			raise RuntimeError ("No service specified!")
		if name:
			name = self.sanitize(name)
		if service == "racius":
			return self.Racius(name,nif)
		elif service == "codigopostal.ciberforma":
			return self.CodigoPostal_Ciberforma(name,nif)
		elif service == "portugalio":
			return self.Portugalio(name,nif)
		elif service == "einforma":
			return self.Einforma(name,nif)
		elif service == "nif":
			return self.getNifInfo(nif, key_nif)
		elif service == "google":
			 return self.getGoogleInfo(address=address, name=name, city=city, country=country, key_google=key_google)
		else:
			raise RuntimeError ("Service [{}] is not available!".format(service))
				



	# merge  2 results
	# NOTES: remove url and service fields from final result
	# *********************************************************
	# NOTES: THIS FUNCTION IS A MESS ... NEEDS REFACTORING
	#		 ensure merge: r1->r2 or rev
	# *********************************************************
	def merge(self, r1,r2):
		if 'urls' not in r1:
			r1.update({'urls':{r1['service']:r1['url']}})	
		r2.update({'urls':{r2['service']:r2['url']}})

		if type(r1['status']) != dict:
			r1['status'] = {r1['service']:r1['status']}

		# merge r1 and r2
		result = dict((k,v if k in r1 and r1[k] in [None, ''] else r1[k]) for k,v in r2.items())


		# date - select + use /
		if result['data_inicio']:
			valid_date_chars = set('-/')
			if r1['data_inicio'] and any((c in valid_date_chars) for c in r1['data_inicio']):
				if r2['data_inicio'] and not any((c in valid_date_chars) for c in r2['data_inicio']): 
					result['data_inicio'] = r1['data_inicio']
			elif r2['data_inicio'] and any((c in valid_date_chars) for c in r2['data_inicio']):
				if r1['data_inicio'] and not any((c in valid_date_chars) for c in r1['data_inicio']): 
					result['data_inicio'] = r2['data_inicio']
			else:
				result['data_inicio'] = None
		if result['data_inicio']:
			result['data_inicio']=result['data_inicio'].replace('-','/')

		# cp
		if r1['codigo_postal'] and r2['codigo_postal']:
			if len(r1['codigo_postal']) > len(r2['codigo_postal']):
				result['codigo_postal'] = r1['codigo_postal']
			else:
				result['codigo_postal'] = r2['codigo_postal']
		
		# urls		
		result['urls'].update({r2['service']:r2['url']})

		# status
		result['status'].update({r2['service']:r2['status']})

		# data
		result['data'].update(r2['data'])
		
		return result



	def getAll(self, name=None, address=None, city=None, country=None, nif=None, key_nif=None, key_google=None):
		result = self.newResult()
		for service in self.SERVICES_BASE_URLS:
			try:
				r = self.getData(service=service, nif=nif, key_nif=key_nif, address=address, name=name, city=city, country=country, key_google=key_google)
				result = self.merge(result, r)
			except Exception:
				pass	# do not merge

		result.pop('url', None)
		result.pop('service', None)
		
		# dealing with more consequences of the merge mess - remove the none keys
		if None in result['urls']:
			del(result['urls'][None])
		if None in result['status']:
			del(result['status'][None])
		return result
