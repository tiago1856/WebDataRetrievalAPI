# Web Data Retrieval API

## Version

1.0.1


## Description

This service is designed to obtain, from the web, the most relevant information about an entity.
For that, it scrapes a number of sites and it also uses some existing APIs to complement the retrieved data.
 



## Requirements

* Python 3.7.x

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the necessary packages.

```bash
pip install flask
pip install lxml
pip install requests
pip install geopy
```



## Retrieved Fields

These are the fields the service tries to retrieve from the web:


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


## Sites / APIs
* [https://www.nif.pt/](https://www.nif.pt/)
* [https://www.racius.com/](https://www.racius.com/)
* [https://codigopostal.ciberforma.pt/](https://codigopostal.ciberforma.pt/)
* [https://www.portugalio.com/](https://www.portugalio.com/)
* [https://www.einforma.pt/](https://www.einforma.pt/)
* [https://maps.googleapis.com/maps/api/geocode/](https://maps.googleapis.com/maps/api/geocode/)
* ~~[https://www.gescontact.pt/](https://www.gescontact.pt/)~~
* ~~[https://guiaempresas.universia.pt/](https://guiaempresas.universia.pt/)~~



## Calls

Requests to this API can take the following forms:


```bash
/getservices
```

Returns a json with all available services


```bash
/getbaseurls
```

Returns a json with the base urls of all services


```bash
/getsus
```

Returns a json with the all available services and their respective base urls


```bash
/getbaseurl?params
```

Returns a json with the base url of a specific service







```bash
/getdata?params
```
Returns a json with the data retrieved using a specific service





```bash
/getalldata?params
```

Returns a json with the data retrieved using all available services



**Available parameters:**
* *service*: service
* *name*: name of the entity
* *address*: address of the entity
* *city*: city of the entity
* *country*: country of the entity
* *nif*: nif of the entity
* *key_nif*: key for the nif API rest service
* *key_google*: key for the google geocoding API rest service

Note that all parameters are optional. If a service requires one and this is not given, then will either return an error or, in the case of *getalldata* will simply move on to the next service.




## Examples

```python

http://localhost:5000/api/getbaseurl?service=racius

http://localhost:5000/api/getdata?service=racius&name=HEMOVIDA+Lda&nif=506036944

http://localhost:5000/api/getalldata?name=HEMOVIDA+Lda&nif=506036944&key_google=YOUR_KEY&key_nif=YOUR_KEY

```


## TODO
* multithreading for all data
* in GetAll, the google api will be used iff the other services didn't provided the coordinated.
* more sites

## License
[MIT](https://choosealicense.com/licenses/mit/)
