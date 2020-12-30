
Version: 1.0.0

# Description

* Given an entity's name and/or nif, tries to retrieve information about that entity from several sites. It returns a json with all the available information.
* In case nothing is found (maybe the entity doesn't exist), *'status': 'NOT FOUNDED'* or *None*, else 'status': 'OK'*.
* Both scraping and API services are used.
* Some services (APIs) require keys in order to function.



# Requirements

* Python 3.7.x
* modules: lxml, requests


# Fields

* type
* nome
* nome_legal
* nif
* data_de_inicio    (data inicio de actividade | constituição)
* morada
* localidade
* distrito
* concelho
* freguesia
* codigo_freguesia
* codigo_postal
* forma_juridica    (LDA | Cooperativa | Sociedade por Quotas | Sociedade Unipessoal)
* telefone
* fax
* cae
* actividade         (descricao da actividade)
* site
* latitude
* longitude
* horario
* email
* telemovel
* estado        (EM ACTIVIDADE | EM INSOLVENCIA | EM REVITALIZAÇÃO | ENCERRADA (Dissolução e Liquidação))
* status        (OK => some data was fetched	| NOT_FOUNDED => 404 or nothing)
* url / urls	(url if single service)
* service	    (servico usado)
* data		    (miscelaneous data. Ex: google place_id)


# Sites
* [https://www.nif.pt/](https://www.nif.pt/)
* [https://www.racius.com/](https://www.racius.com/)
* [https://codigopostal.ciberforma.pt/](https://codigopostal.ciberforma.pt/)
* [https://www.portugalio.com/](https://www.portugalio.com/)
* [https://www.einforma.pt/](https://www.einforma.pt/)
* [https://maps.googleapis.com/maps/api/geocode/](https://maps.googleapis.com/maps/api/geocode/)
* ~~[https://www.gescontact.pt/](https://www.gescontact.pt/)~~
* ~~[https://guiaempresas.universia.pt/](https://guiaempresas.universia.pt/)~~



# Functions

* def getServices()

Returns a list of all available services/websites.

* def getBaseUrl(service)

Returns the base url of a specific service/website.

* def getBaseUrls()

Returns a list of all services and corresponding base urls.

* def GetSUs()

returns a dictionary with the all available services and their respective base urls

* def sanitize(name_or_address)

Given string, returns it: lowercase, no portuguese special characters, no extra spaces, no non-alfanumeric chars

* def getData(self, service="racius", name=None, address=None, city=None, country=None, nif=None, key_nif=None, google_key=None)

Returns a dictionary with the data obtained from the selected service.

* def getAll(self, name=None,address=None, city=None, country=None, nif=None, key_nif=None, google_key=None)

Returns a dictionary with the data obtained from all the available services.



# Updated Notes:
* gescontact: removed
* guiaempresas: removed


# Example

```python
import WebDataRetrieval as dr

try:
	s = dr.WebDataRetrieval()	
	print (s.getData("racius", "HEMOVIDA Lda"))
	print (s.getData("codigopostal.ciberforma", "HEMOVIDA Lda", 506036944))
	print (s.getData("portugalio", "HEMOVIDA Lda"))
	print (s.getData("einforma", "HEMOVIDA Lda", 506036944))
	print (s.getData("nif", "HEMOVIDA Lda", 506036944))
	print (s.getAll(name="HEMOVIDA Lda", nif=506036944))
	print (s.getServices())
	print (s.getBaseUrls())
except Exception as e:
	print (e)
```

# TODO
* multithreading
* more sites
* in GetAll, the google api will be used iff the other services didn't provided the coordinated.

