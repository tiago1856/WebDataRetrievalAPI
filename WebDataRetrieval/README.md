# Web Data Retrieval Module

## Version

1.0.1


## Description

Given an entity's name and/or nif, tries to retrieve information about that entity from several sites. It returns a json with all the available information.
In case nothing is found (maybe the entity doesn't exist), *'status': 'NOT FOUNDED'* or *None*, else 'status': 'OK'*.
Both scraping and REST APIs services are used.
Some REST services require keys in order to function.



## Requirements

* Python 3.7.x

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary packages.

```bash
pip install lxml
pip install requests
```


## Fields
These are the fields the service tries to retrieve from the web:


* **type**
* **nome**
* **nome_legal**
* **nif**
* **data_de_inicio**    (data inicio de actividade | constituição)
* **morada**
* **localidade**
* **distrito**
* **concelho**
* **freguesia**
* **codigo_freguesia**
* **codigo_postal**
* **forma_juridica**    (LDA | Cooperativa | Sociedade por Quotas | Sociedade Unipessoal)
* **telefone**
* **fax**
* **cae**
* **actividade**       (descricao da actividade)
* **site**
* **latitude**
* **longitude**
* **horario**
* **email**
* **telemovel**
* **estado**        (EM ACTIVIDADE | EM INSOLVENCIA | EM REVITALIZAÇÃO | ENCERRADA (Dissolução e Liquidação))
* **status**        (OK, NOT_FOUNDED, [ACCESS_ERROR, QUOTA_EXCEEDED, TIME_OUT, SERVICE_ERROR, UNKNOWN_ERROR])
* **url / urls**	(url if single service)
* **service**	    (servico usado)
* **data**		    (miscelaneous data. Ex: google place_id)


## Sites / APIs
* [https://www.nif.pt/](https://www.nif.pt/)
* [https://www.racius.com/](https://www.racius.com/)
* [https://codigopostal.ciberforma.pt/](https://codigopostal.ciberforma.pt/)
* [https://www.portugalio.com/](https://www.portugalio.com/)
* [https://www.einforma.pt/](https://www.einforma.pt/)
* [https://maps.googleapis.com/maps/api/geocode/](https://maps.googleapis.com/maps/api/geocode/)
* ~~[https://www.gescontact.pt/](https://www.gescontact.pt/)~~
* ~~[https://guiaempresas.universia.pt/](https://guiaempresas.universia.pt/)~~



## Main Functions

```python
def getServices()
```
Returns a list of all available services/websites.


```python
def getBaseUrl(service)
```

Returns the base url of a specific service/website.


```python
def getBaseUrls()
```

Returns a list of all services and corresponding base urls.


```python
def GetSUs()
```

Returns a dictionary with the all available services and their respective base urls


```python
def sanitize(name_or_address)
```

Given string, returns it: lowercase, no portuguese special characters, no extra spaces, no non-alfanumeric chars


```python
def getData(self, service=None, name=None, address=None, city=None, country=None, nif=None, key_nif=None, google_key=None)
```

Returns a dictionary with the data obtained from the selected service.


```python
def getAll(self, name=None,address=None, city=None, country=None, nif=None, key_nif=None, google_key=None)
```

Returns a dictionary with the data obtained from all the available services.





## Example

```python
import WebDataRetrieval as dr

try:
	print (s.getData("racius", "HEMOVIDA Lda"))
	print (s.getData("codigopostal.ciberforma", "HEMOVIDA Lda", nif=506036944))
	print (s.getData("portugalio", "HEMOVIDA Lda"))
	print (s.getData("einforma", "HEMOVIDA Lda", nif=506036944))
	print (s.getData("nif", "HEMOVIDA Lda", nif=506036944))
	print (s.getAll(name="HEMOVIDA Lda", nif=506036944, key_google=YOUR_KEY))
	print (s.getServices())
	print (s.getBaseUrls())	
	print (s.getData("google", name="HEMOVIDA Lda", country="portugal", key_google=YOUR_KEY))
	print (s.getData("nif", name="HEMOVIDA Lda", nif=506036944, key_nif=YOUR_KEY))
except Exception as e:
	print (e)
```


## Limitations

* *Nif service*: 1000/month | 100/day | 10/hour | 1/minute

## Update Notes:
* gescontact: removed
* guiaempresas: removed

## Todo
* multithreading
* more sites
* in *GetAll*, the google api will be used iff the other services didn't provided the coordinated.

## License
[MIT](https://choosealicense.com/licenses/mit/)
