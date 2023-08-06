# Mongo Filter

  

Permite filtrar múltiples objetos de primer nivel de tipo Embebido y 1 de tipo RefenceField, aparir de un dict agregando como primera palabra el nombre del modelo seguido del campo de búsqueda, modeloA_campo_busqueda.

  

Los campos de búsqueda pueden ser de tipo serializables y es capaz de reconocer valores **bool** enviados como **str**. Si envía el siguiente campo **"active":"true"** la query se ejecutara como **"active":True**

  

### Parametros:  
| principal_models | refence_models |params|
|--|--|--|
| Modelo que contiene las referencias y embebidos |Modelo RefenceField  | dict con keys para filtrar|


### Ejemplo:  

model_a:

    {    
	    "id": 1,	    
	    "name": "abc",	    
	    "nid": "12323",	    
	    "addres": EmbeddedDocumentField(model_b),	    
	    "nid_type": ReferenceField(model_c, dbref=True)    
    }

  

model_b:

    [    
        {	    
	        "id": 1,	    
	        "name": "cll qwer",	    
	        "description": ""	    
        },    
        {	    
	        "id": 2,    
	        "name": "cll abc",    
	        "description": ""    
        }    
    ]

model_c:

    {
    	{
    		"id": 1,
    		"name": "C.C",
    		"description": "
    	},
    	{
    		"id": 2,
    		"name": "C.E",
    		"description": "
    	}
    }

Parámetros de búsqueda:  

    {    
		"id": 1,    
		"model_b_name": "cll abc",    
		"model_c_name": "C.C"    
    }
QuerySet :    

> zmongo.queryset(model_a, model_c, Params)

 repuesta:  

    {   
	    "id": 1,	    
	    "name": "",	    
	    "addres": [addres[0]],	    
	    "nid_type": (object)    
    }

  

### Installation

If you're running python3 on most systems, you can install the package with the following command:

  
> pip3 install zmongo-filter

    

###  Usage

> zmongo.queryset(model_a, model_c, Params)
