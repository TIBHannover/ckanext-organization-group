"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest

from ckan.plugins import toolkit
from ckanext.organization_group.controllers import GroupOwnershipController
from ckanext.organization_group.lib import Helper

@pytest.mark.ckan_config("ckan.plugins", "organization_group")
@pytest.mark.ckan_config("SECRET_KEY", "test_secret")
@pytest.mark.usefixtures("with_plugins")
def test_add_ownership_view_rejects_anonymous_users(app):
    response = app.get(
        toolkit.url_for(
            "organization_group.add_ownership_view", id="example"
        ),
        status=403,
    )

    assert response.status_code == 403


def test_plugin_detection_matches_complete_plugin_names(monkeypatch):
    monkeypatch.setitem(
        toolkit.config,
        "ckan.plugins",
        "organization_group machine_link_extra",
    )

    assert Helper.check_plugin_enabled("organization_group") is True
    assert Helper.check_plugin_enabled("machine_link") is False


def test_groups_list_uses_python_boolean_for_ckan_action(monkeypatch):
    captured = {}

    def group_list(_context, data_dict):
        captured.update(data_dict)
        return [{"id": "group-id", "name": "group-name"}]

    monkeypatch.setattr(
        toolkit,
        "get_action",
        lambda action: group_list if action == "group_list" else None,
    )
    monkeypatch.setattr(Helper, "check_access_edit_group", lambda _id: True)

    assert Helper.get_groups_list()[-1] == {
        "value": "group-id",
        "text": "group-name",
    }
    assert captured["all_fields"] is True


@pytest.mark.usefixtures("with_request_context")
def test_user_helpers_handle_anonymous_requests():
    assert GroupOwnershipController.get_user_org() == "0"
    assert GroupOwnershipController.get_user_group() == "0"
