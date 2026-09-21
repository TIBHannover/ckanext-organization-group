# encoding: utf-8

import ckan.plugins.toolkit as toolkit


class Helper():

    def get_groups_list():
        groups = toolkit.get_action('group_list')({}, {'all_fields': True})
        group_list = []
        temp = {}
        group_list.append(temp)
        for group in groups:
            if not Helper.check_access_edit_group(group['id']):
                continue
            temp = {}
            temp['value'] = group['id']
            temp['text'] = group['name']
            group_list.append(temp)
        
        return group_list
    
    def get_organizations_list():
        orgs = toolkit.get_action('organization_list')({}, {'all_fields': True})
        org_list = []
        temp = {}
        temp['value'] = '0'
        temp['text'] = 'No organization'
        org_list.append(temp)
        for org in orgs:
            if not Helper.check_access_add_dataset_to_org(org['id']):
                continue
            temp = {}
            temp['value'] = org['id']
            temp['text'] = org['name']
            org_list.append(temp)
        
        return org_list
    

    def check_plugin_enabled(plugin_name):
        enabled_plugins = toolkit.config.get("ckan.plugins", "").split()
        return plugin_name in enabled_plugins
    

    def check_access_edit_group(group_id):
        user_obj = getattr(toolkit.g, 'userobj', None)
        if not user_obj:
            return False
        groups = toolkit.get_action('group_list')({}, {'all_fields':True, 'include_users': True})
        for g in groups:
            if g['id'] == group_id:
                for user in g['users']:
                    if user_obj.id == user['id']:
                        return True
        return False


    def check_access_add_dataset_to_org(org_id):
        user_obj = getattr(toolkit.g, 'userobj', None)
        if not user_obj:
            return False
        orgs = toolkit.get_action('organization_list')({}, {'all_fields':True, 'include_users': True})
        for org in orgs:
            if org['id'] == org_id:
                for user in org['users']:
                    if user_obj.id == user['id']:
                        return True
        return False

