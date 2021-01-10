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

Or just:

```bash
pip install -r requirements.txt
```


## Retrieved Fields

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



## Endpoints

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
```
Result:

```json
{"service":"https://www.racius.com/"}
```



```python
http://localhost:5000/api/getdata?service=racius&name=HEMOVIDA+Lda&nif=506036944&key_nif=YOUR_KEY
```
Result:

```json
{
  "actividade": null,
  "cae": "86906",
  "codigo_freguesia": "110639",
  "codigo_postal": "1600-871",
  "concelho": "Lisboa",
  "data": {},
  "data_inicio": "01/01/2002",
  "distrito": "Lisboa",
  "email": "hemovida.lda@gmail.com",
  "estado": "active",
  "fax": "211956029",
  "forma_juridica": "LDA",
  "freguesia": "São Domingos de Benfica",
  "horario": null,
  "latitude": null,
  "localidade": "Lisboa",
  "longitude": null,
  "morada": "Rua São Tomás de Aquino, Nº 16 - A",
  "nif": "506036944",
  "nome": "Hemovida Lda",
  "nome_legal": "Hemovida Lda - Sociedade por Quotas",
  "site": "www.hemovida.com",
  "status": {
    "codigopostal.ciberforma": "OK",
    "einforma": "OK",
    "nif": "OK",
    "portugalio": "NOT_FOUNDED",
    "racius": "OK"
  },
  "telefone": "917646119",
  "telemovel": null,
  "type": "Corporation",
  "urls": {
    "codigopostal.ciberforma": "https://codigopostal.ciberforma.pt/dir/506036944/hemovida-lda/",
    "einforma": "https://www.einforma.pt/servlet/app/portal/ENTP/prod/ETIQUETA_EMPRESA/nif/506036944/",
    "nif": "https://www.nif.pt/",
    "portugalio": "https://www.portugalio.com/hemovida/",
    "racius": "https://www.racius.com/hemovida-lda/"
  }
}

```

```python
http://localhost:5000/api/getalldata?name=HEMOVIDA+Lda&nif=506036944&key_google=YOUR_KEY&key_nif=YOUR_KEY
```
Result:

```json
{
  "actividade": null,
  "cae": "86906",
  "codigo_freguesia": "110639",
  "codigo_postal": "1600-871",
  "concelho": "Lisboa",
  "data": {},
  "data_inicio": "01/01/2002",
  "distrito": "Lisboa",
  "email": "hemovida.lda@gmail.com",
  "estado": "active",
  "fax": "211956029",
  "forma_juridica": "LDA",
  "freguesia": "São Domingos de Benfica",
  "horario": null,
  "latitude": null,
  "localidade": "Lisboa",
  "longitude": null,
  "morada": "Rua São Tomás de Aquino, Nº 16 - A",
  "nif": "506036944",
  "nome": "Hemovida Lda",
  "nome_legal": "Hemovida Lda - Sociedade por Quotas",
  "site": "www.hemovida.com",
  "status": {
    "codigopostal.ciberforma": "OK",
    "einforma": "OK",
    "google": "ACCESS_ERROR",
    "nif": "OK",
    "portugalio": "NOT_FOUNDED",
    "racius": "OK"
  },
  "telefone": "917646119",
  "telemovel": null,
  "type": "Corporation",
  "urls": {
    "codigopostal.ciberforma": "https://codigopostal.ciberforma.pt/dir/506036944/hemovida-lda/",
    "einforma": "https://www.einforma.pt/servlet/app/portal/ENTP/prod/ETIQUETA_EMPRESA/nif/506036944/",
    "google": "GEOPY package: https://pypi.org/project/geopy/",
    "nif": "https://www.nif.pt/",
    "portugalio": "https://www.portugalio.com/hemovida/",
    "racius": "https://www.racius.com/hemovida-lda/"
  }
}
```



## Limitations

* *Nif service*: 1000/month | 100/day | 10/hour | 1/minute


## Todo
* multithreading for all data
* in GetAll, the google api will be used iff the other services didn't provided the coordinated.
* more sites

## License
[MIT](https://choosealicense.com/licenses/mit/)
