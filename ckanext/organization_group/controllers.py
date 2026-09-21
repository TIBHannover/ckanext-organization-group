# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from flask import render_template, request, redirect
import ckan.lib.helpers as h
from ckanext.organization_group.lib import Helper


class GroupOwnershipController():

    @staticmethod
    def _context():
        return {'user': getattr(toolkit.g, 'user', None)}

    @staticmethod
    def _require_authenticated():
        if not getattr(toolkit.g, 'user', None):
            toolkit.abort(
                403, "You need to authenticate before accessing this function"
            )

    @staticmethod
    def add_ownership_view(id):
        GroupOwnershipController._require_authenticated()
        context = GroupOwnershipController._context()
        try:
            package = toolkit.get_action('package_show')(
                context, {'id': id}
            )
            toolkit.check_access(
                'package_update', context, {'id': package['id']}
            )
        except toolkit.ObjectNotFound:
            toolkit.abort(404, "Package not found")
        except toolkit.NotAuthorized:
            toolkit.abort(403, "Not authorized to update this package")
        group_list = Helper.get_groups_list()
        organizations = Helper.get_organizations_list()
        stages = True
        return render_template('add_owner.html', pkg_dict=package, custom_stage=stages, group_list=group_list, org_list=organizations)
    

    @staticmethod
    def save_ownership():
        GroupOwnershipController._require_authenticated()
        context = GroupOwnershipController._context()

        package_name = request.form.get('package')        
        if package_name is None:
            return toolkit.abort(400, "Package not specified")
        
        try:
            package = toolkit.get_action('package_show')(
                context, {'id': package_name}
            )
            toolkit.check_access(
                'package_update', context, {'id': package['id']}
            )
        except toolkit.ObjectNotFound:
            return toolkit.abort(404, "Package not found")
        except toolkit.NotAuthorized:
            return toolkit.abort(403, "Not authorized to update this package")
               
        action = request.form.get('save_btn')
        if action == 'finish_ownership':
            org = request.form.get('owner_org')
            groups = request.form.getlist('selected_groups')
            if org != '0' and org:
                package['owner_org'] = org
                toolkit.get_action('package_update')(context, package)
                for group_id in groups:
                    member = {
                        'id' : group_id,
                        'object': package['id'],
                        'object_type': 'package',
                        'capacity' : 'public'
                    }                                            
                    toolkit.get_action('member_create')(context, member)
                
                sfb = toolkit.config.get('ckanext.crc.project.id')
                if sfb == "1153" and Helper.check_plugin_enabled('crc1153_specific_metadata'):
                    return redirect(h.url_for('crc1153_specific_metadata.add_metadata', package_id=str(package_name) ,  _external=True))
                elif  Helper.check_plugin_enabled('machine_link'):
                    return redirect(h.url_for('machine_link.machines_view', id=str(package_name) ,  _external=True))
                elif  sfb == "1153" and Helper.check_plugin_enabled('sample_link'):
                    return redirect(h.url_for('sample_link.add_samples_view', id=str(package_name) ,  _external=True))

                return redirect(h.url_for('dataset.read', id=str(package_name) ,  _external=True))    

            return toolkit.abort(403, "bad request")    

        return toolkit.abort(403, "bad request")
    
    
    def cancel_dataset_plugin_is_enabled():
        if Helper.check_plugin_enabled('cancel_dataset_creation'):
            return True
        return False
    

    def mediawiki_plugin_is_enabled():
        if Helper.check_plugin_enabled('machine_link'):
            return True
        return False


    def get_user_org():
        user_obj = getattr(toolkit.g, 'userobj', None)
        if not user_obj:
            return '0'
        orgs = toolkit.get_action('organization_list')({}, {'all_fields':True, 'include_users': True})
        for org in orgs:
            for user in org['users']:
                if user_obj.id == user['id']:
                    return org['id']
        return '0'
    

    def get_user_group():
        user_obj = getattr(toolkit.g, 'userobj', None)
        if not user_obj:
            return '0'
        groups = toolkit.get_action('group_list')({}, {'all_fields':True, 'include_users': True})
        for g in groups:
            for user in g['users']:
                if user_obj.id == user['id']:
                    return g['id']
        return '0'
