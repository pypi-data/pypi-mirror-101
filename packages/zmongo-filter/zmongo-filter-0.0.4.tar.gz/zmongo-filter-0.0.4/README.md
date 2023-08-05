# Project description


# Mongo Filter

Permite filtrar multiples objetos de primer nivel de tipo Embebido y 1 de tipo RefenceField, apartir de un dict agregando como primera palabra el nombre del modelo seguido del campo de busqueda, modeloA_campo_busqueda.

Parametros:

    principal_models: Modelo que contiene las referencias y embebidos
    refence_models: Modelo RefenceField
    params: dict con keys de filtros

Ejemplo:

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
                "description": "
            },
            {
                "id": 2,
                "name": "cll abc",
                "description": "
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
Params:

    {
        "id": 1,
        "model_b_name": "cll abc",
        "model_c_name": "C.C"
    }
zmongo.queryset(model_a, model_c, Params)

repuesta:

    {
        "id": 1,
        "name": "",
        "addres": [addres[0]],
        "nid_type": (object)
    }

# Installation
If you're running python3 on most systems, you can install the package with the following command:

    pip3 install zmongo-filter


# Usage
    zmongo.queryset(model_a, model_c, Params)
