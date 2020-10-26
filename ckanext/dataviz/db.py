from abc import abstractmethod
from ckan.plugins import toolkit


class Query(object):
    def __init__(self, resource_id, fields):
        """
        Query object as Interface
        :param resource_id : Resource id which needs to be fetched for processing
        :param fields      : List of fields for visualization
        """
        self.resource_id = resource_id
        self.fields = fields

    @abstractmethod
    def execute(self):
        """
        Fetch results in a given format from backend
        : result: Dict
        """
        pass

    @classmethod
    def new(cls, *args, **kwargs):
        backend_type = toolkit.config.get(u'ckanext.backend.type')
        queries = {
            'datastore': DataStoreQuery
        }

        query_class = queries.get(backend_type, DataStoreQuery)
        return query_class(*args, **kwargs)


class DataStoreQuery(Query):
    def __init__(self, *args, **kwargs):
        super(DataStoreQuery, self).__init__(*args, **kwargs)

    def execute(self):
        datastore_search = toolkit.get_action(u'datastore_search')
        response = datastore_search(None, {
            u"resource_id": self.resource_id,
            u"fields": self.fields
        })

        return response['records']
