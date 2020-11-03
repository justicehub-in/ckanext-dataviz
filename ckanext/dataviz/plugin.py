# encoding: utf-8

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

default = toolkit.get_validator(u'default')
boolean_validator = toolkit.get_validator(u'boolean_validator')
not_empty = toolkit.get_validator('not_empty')


class DataVizBaseView(p.SingletonPlugin):
    """
    DataViz view plugin
    """
    if not p.toolkit.check_ckan_version('2.3'):
        raise p.toolkit.CkanVersionException(
            'This extension requires CKAN >= 2.3. If you are using a ' +
            'previous CKAN version the PDF viewer is included in the main ' +
            'CKAN repository.')
    
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        """
        Set up the resource library, public directory and
        template directory for the view
        """
        p.toolkit.add_public_directory(config, 'public')
        p.toolkit.add_template_directory(config, 'templates')
        p.toolkit.add_resource('public', 'dataviz')

    def can_view(self, data_dict):
        resource = data_dict['resource']
        return resource.get(u'datastore_active')

    def view_template(self, context, data_dict):
        return u'base_view.html'

    def form_template(self, context, data_dict):
        return u'base_form.html'
    
    def get_helpers(self):
        from ckanext.dataviz import helpers as dataviz_helpers
        return {
                'dataviz_theme': dataviz_helpers.dataviz_theme
                }
    
    def setup_template_variables(self, context, data_dict):
        resource = data_dict['resource']
        resource_view = data_dict['resource_view']
        resource_view['show_legends'] = bool(resource_view.get('show_legends'))

        fields = _get_fields_without_id(resource)

        # TODO: Another possibility
        # q = Query.new(resource_id=resource_view[u'resource_id'], fields=resource_view[u'x_axis'])
        # result = q.execute()

        return {'resource': resource,
                'resource_view': resource_view,
                'fields': fields,
                'group_by_is_required': False,
                'chart_type': 'base'}

    def info(self):
        return {
            u'name': u'dataviz_view',
            u'title': u'Bar Chart',
            u'filterable': True,
            u'icon': u'bar-chart',
            u'requires_datastore': True,
            u'default_title': p.toolkit._(u'Graph'),
            u'schema': {
                u'responsive': [default(False), boolean_validator],
                u'x_axis': [not_empty],
                u'chart_title': [default('')],
                u'x_axis_title': [default('')],
                u'y_axis_title': [default('')]
            }
        }

    def before_map(self, m):
        m.connect(
            u'/dataviz_view/ajax/{resource_view_id}',
            controller=u'ckanext.dataviz.controller'
                       u':DataVizController',
            action=u'ajax')
        return m


def _get_fields_without_id(resource):
    fields = _get_fields(resource)
    return [{'value': v['id']} for v in fields if v['id'] != '_id']


def _get_fields(resource):
    data = {
        'resource_id': resource['id'],
        'limit': 0
    }
    result = p.toolkit.get_action('datastore_search')({}, data)
    return result['fields']
