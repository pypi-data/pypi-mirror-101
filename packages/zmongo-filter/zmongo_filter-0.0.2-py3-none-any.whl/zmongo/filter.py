
class MongoFilter:
    """
    Permite filtrar multiples objetos de primer nivel de tipo Embebido
    y 1 de tipo RefenceField, apartir de un dict agregando como
    primera palabra el nombre del modelo seguido del campo
    de busqueda, modeloA_campo_busqueda.

    Parametros:
    - principal_models: Modelo que contiene las referencias y embebidos
    - refence_models: Modelo RefenceField
    - params: dict con keys de filtros

    Ejemplo:
    -   model_a:
        {
            "id":1,
            "name":"abc",
            "nid":"12323",
            "addres":EmbeddedDocumentField(model_b),
            "nid_type":ReferenceField(model_c, dbref=True)
        }
    - model_b:
        [
            {
                "id":1,
                "name":"cll qwer",
                "description":"
            },
            {
                "id":2,
                "name":"cll abc",
                "description":"
            }
        ]
    - model_c:
        {
            {
                "id":1,
                "name":"C.C",
                "description":"
            },
            {
                "id":2,
                "name":"C.E",
                "description":"
            }
        }
    - Params:{
            "id":1,
            "model_b_name":"cll abc",
            "model_c_name":"C.C"
        }
    - MongoFilter().queryset(model_a,model_c,Params)

    - repuesta:
        {
            "id":1,
            "name":"",
            "addres":[addres[0]],
            "nid_type":(object)
        }
    """

    def __init__(self):
        self.fields_utils = []
        self.list_refences = []
        self.dict_embedded = {}
        self.params = dict
        self.principal_models = object
        self.refence_models = object
        self.refence_instance = object
        self.refence_field = "ReferenceField"
        self.embedded_field = "ListField"

    def main(self,
             principal_models: dict,
             refence_models: dict = None,
             params: dict = dict):
        """
        """

        self.principal_models = principal_models
        self.refence_models = refence_models
        self.params = params

        self.list_field_models()
        self.list_references_field()
        self.dict_embedded_document_field()
        self.instances_refences()

        # query principal con las referencias
        queryset = principal_models.objects.filter(**self.params)

        if len(queryset) > 1:
            # si la query retorna mas 1 objeto no se realizan
            # acciones y se retorna el mismo object
            return self.multiples_objects(queryset)
        # agrega los embebidos al objeto principal
        queryset = self.instances_embedded(queryset)

        return queryset

    def list_field_models(self):
        """
        Itera sobre self.params, valida los campos que pertenecen
        al modelo y los agrega a la lista self.fields_utils
        """

        for fields in self.params:
            try:
                getattr(self.principal_models, fields)
                self.fields_utils.append(fields)
            except AttributeError:
                try:
                    _fields = fields.split("_")
                    getattr(self.principal_models, _fields[0])
                    self.fields_utils.append(fields)
                except AttributeError:
                    pass

    def list_references_field(self):
        """
        Selecciona los objetos de tipo ReferenceField, los agrega a
        la lista self.list_refences
        """

        for fields in self.fields_utils:
            try:
                type_field = getattr(self.principal_models, fields)
                if self.refence_field in str(type(type_field)):
                    self.list_refences.append(fields)
            except AttributeError:
                self.second_search_refence(
                    fields, self.refence_field, self.list_refences)

    def dict_embedded_document_field(self):
        """
        Selecciona los objetos de tipo List, los agrega a
        la lista self.dict_embedded
        """
        for fields in self.fields_utils:
            try:
                type_field = getattr(self.principal_models, fields)
                if self.embedded_field in str(type(type_field)):
                    self.dict_embedded[fields] = self.params[fields]
                    self.params.pop(fields)
            except AttributeError:
                self.second_search_embedded(
                    fields, self.embedded_field,
                    self.dict_embedded
                )

    def instances_refences(self):
        """
        Itera sobre list_refences, que contiene las keys de modelos
        ReferenceField, separa la data en 2 variables una contiene el nombre
        del campo a filtrar y la otra el valor, realizando una busqueda de tipo
        iexact, este no diferencia entre mayuscusulas-minisculas, si la
        consulta es True, se actualiza el valor de la llave de referencia
        por la instancia del objeto en self.params,
        para relizar la consulta global:

        return::
            params={
                "field_refence":instance_refence_field
            }

        - variables de referencia
            - params : almacena el valor de busqueda
            - items : almacena el key de busqueda
            - reference_name : contiene el campo de ReferenceField
        """
        data_filter = dict

        for refence in self.list_refences:
            # separa los campos y valida que existan en el modelo
            params = self.params[refence]
            field_refence = refence.split('_')
            items = "{}__{}".format(field_refence[-1], "iexact")
            reference_name = field_refence[0]

            # data_filter ej:{uuid:"52a5629c-3fb4-4267-bc39-9bc3cbb7ef50"}
            data_filter = {items: params}
            # eliminar campos de referencia
            self.params.pop(refence)

            try:
                instance = {
                    reference_name: self.refence_models.objects.get(
                        **data_filter)
                }
                # agregar dict con instancia del campo referencia
                self.params = dict(self.params, **instance)

            except Exception:
                pass

    def instances_embedded(self, query):
        """
        Itera sobre la lista de keys embedded, y separa
        en 2 variables el nombre del campo y el valor para
        buscar en el Embebido del objeto de consulta principal
        """
        if not query:
            return []

        result = query
        for embedded in self.dict_embedded:
            # separa los campos y valida que existan en el modelo
            params = self.dict_embedded[embedded]
            _refence = embedded.split('_')
            embedded = _refence[0]

            field_search = "_".join(_refence[1:])

            result = self.process_embedded(
                query, field_search, embedded, params)

        return result

    def process_embedded(self, query, items, embedded, params):
        """
        Filtra los embedded y los agrega al objeto de busqueda
        principal
        """

        query = query[0]
        dict_embedded = []

        filter_query = getattr(query, embedded)

        dict_embedded = [_find_data for _find_data in filter_query if str(
            _find_data[items]) == str(params)]

        query[embedded] = dict_embedded

        return [query]

    def multiples_objects(self, query):
        """
        """
        return query

    def second_search_refence(self, _iter, value, list_data):
        try:
            _fields = _iter.split("_")
            type_field = getattr(self.principal_models, _fields[0])
            if value in str(type(type_field)):
                list_data.append(_iter)
        except AttributeError:
            pass

    def second_search_embedded(self, _iter, value, list_data):
        try:
            _fields = _iter.split("_")
            type_field = getattr(self.principal_models, _fields[0])
            if value in str(type(type_field)):
                list_data[_iter] = self.params[_iter]
                self.params.pop(_iter)
        except AttributeError:
            pass


def queryset(self,
             principal_models: dict,
             refence_models: dict = None,
             params: dict = dict):
    """
    Permite filtrar multiples objetos de primer nivel de tipo Embebido
    y 1 de tipo RefenceField, apartir de un dict agregando como
    primera palabra el nombre del modelo seguido del campo
    de busqueda, modeloA_campo_busqueda.

    Parametros:
    :: principal_models: Modelo que contiene las referencias y embebidos
    :: refence_models: Modelo RefenceField
    :: params: dict con keys de filtros

    Ejemplo:
    -   model_a:
        {
            "id":1,
            "name":"abc",
            "nid":"12323",
            "addres":EmbeddedDocumentField(model_b),
            "nid_type":ReferenceField(model_c, dbref=True)
        }
    - model_b:
        [
            {
                "id":1,
                "name":"cll qwer",
                "description":"
            },
            {
                "id":2,
                "name":"cll abc",
                "description":"
            }
        ]
    - model_c:
        {
            {
                "id":1,
                "name":"C.C",
                "description":"
            },
            {
                "id":2,
                "name":"C.E",
                "description":"
            }
        }
    - Params:{
            "id":1,
            "model_b_name":"cll abc",
            "model_c_name":"C.C"
        }
    :: MongoFilter().queryset(model_a,model_c,Params)

    - repuesta:
        {
            "id":1,
            "name":"",
            "addres":[addres[0]],
            "nid_type":(object)
        }
    """
    result = MongoFilter().main(
        principal_models,
        refence_models,
        params
    )
    return result
