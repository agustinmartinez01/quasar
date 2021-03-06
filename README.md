# Operaciòn Fuego de Quasar

## Arquitectura de Software

A continuaciòn se exponen una vista de la arquitectura Api Rest Django 
![image](https://drive.google.com/uc?export=view&id=1VSUsNQA1D8Ew2BgnGhOQYACbKyFZKDCT)

Aqui se muestra el diagrama de clases utilizada (Patron de diseño Mediator)

![image](https://drive.google.com/uc?export=view&id=1qtDHeoWrgNzTRNARu872AO_NQTxELyaH)


Deploy AWS EC2 Djando Rest Api
[Deploy AWS Django] (https://medium.com/saarthi-ai/ec2apachedjango-838e3f6014ab)

## EndPoints para su utilización


 * Method GET -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/satelite/ 
 	* Listado de satelites disponible en la base de datos
 * Method GET -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/satelite/id 
 	* satelite disponible en la base de datos
 * Method Post -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/satelite/ 
 -> Guarda un satelite en la base de datos
 	Body :
 	```json
 	{
 		"name":String,
 		"latitude":Float,
		"longitude":Float
		}
	```
* Method Put -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/satelite/id
 -> Guarda un satelite en la base de datos
 	Body :
 	```json
 	{
 		"name":String,
 		"latitude":Float,
		"longitude":Float
		"message":[String]
		"distance":Float
		}
	```

* Method Post -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/topsecret/ 
	* Devuelve el mensaje decifrado en caso de poder con la posición
	Body: 
	```json
	{
		'satelites':[
			{
			 "name":<String>,
			 "message":[String],
			 "distance": Float
			},
			{
			"name":<String>,
			"message"::[String],
			"distance": Float
			},
			{
			"name":<String>,
			"message"::[String],
			"distance":Float

			}
	    	]
	}
	```
* Method Get -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/topsecret_split/<String> 
	* Devuelve el mensaje desifrado en caso de poder con la distancia a ese satelite
* Method Post -> http://ec2-18-191-118-253.us-east-2.compute.amazonaws.com/api/topsecret_split 
	* Guarda en el satelite pasado en el body por name los atributos message y distance nuevos
	Body:
	```json
	{
		 "name":<String>,
		 "message":[String],
		 "distance": Float
		}
	```
## Comando para correr Test
	python3 manage.py test Space.tests
