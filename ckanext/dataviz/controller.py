import json
from ckan.plugins.toolkit import BaseController, get_action
from ckanext.dataviz.db import Query
from ckanext.dataviz.lib.utils import get_bar_chart
from ckanext.dataviz.lib.utils import get_big_number


class DataVizController(BaseController):
    def ajax(self, resource_view_id):
        resource_view = get_action(u'resource_view_show')(
            None, {u'id': resource_view_id})

        # TODO: Handle fields either as comma seperated or list
	if resource_view[u'chart_type'] == "bar":
		q = Query.new(resource_id=resource_view[u'resource_id'], fields=resource_view[u'x_axis'])
		result = q.execute()

		return json.dumps({
		    'value': get_bar_chart(result, resource_view[u'x_axis']),
		})

	if resource_view[u'chart_type'] == "bignumber":
		q = Query.new(resource_id=resource_view[u'resource_id'], fields=resource_view[u'column'])
		result = q.execute()

		return json.dumps({
		    'value': get_big_number(result, resource_view[u'column'], resource_view[u'aggregate']),
		})
