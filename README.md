# Web Data Retrieval API

## Version

1.0.1


## Description

* xxxx
* 



## Requirements

* Python 3.7.x

### Installation

Use the package manager pip to install the necessary packages.

```bash
pip install flask
pip install lxml
pip install requests
```



## Fields

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


## Sites
* [https://www.nif.pt/](https://www.nif.pt/)
* [https://www.racius.com/](https://www.racius.com/)
* [https://codigopostal.ciberforma.pt/](https://codigopostal.ciberforma.pt/)
* [https://www.portugalio.com/](https://www.portugalio.com/)
* [https://www.einforma.pt/](https://www.einforma.pt/)
* [https://maps.googleapis.com/maps/api/geocode/](https://maps.googleapis.com/maps/api/geocode/)
* ~~[https://www.gescontact.pt/](https://www.gescontact.pt/)~~
* ~~[https://guiaempresas.universia.pt/](https://guiaempresas.universia.pt/)~~

*Notes: the google api will be used iff the other services didn't provided the coordinated.*

## Calls


```bash
/getdata?params
```
Returns a json with the data retrieved using a specific service


```bash
/getalldata?params
```

Returns a json with the data retrieved using all available services


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


params (all optional):
* *service*: service
* *name*: name of the entity
* *nif*: nif of the entity
* *key_nif*: key for the nif API rest service

Attention: all parameters are optional. 
If a service requires a non given parameter, then will either return an error or will simply move on to the next service.




## Examples

```python
sdsda
```


## TODO
* multithreading for all data
* in GetAll, the google api will be used iff the other services didn't provided the coordinated.
* more sites

## License
[MIT](https://choosealicense.com/licenses/mit/)
