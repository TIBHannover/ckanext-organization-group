# ckanext-organization-group

This CKAN extension includes `organization_group` plugin. The plugin ables users to link a dataset to a group while creating the dataset. It also makes the organization and group mandatory fields for users. 


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
|  2.9 | Yes    |
|  2.10 | Yes   |
|  2.11 | Yes   |
| earlier | No |           |



## Installation

To install ckanext-organization-group:

1. Activate your CKAN virtual environment, for example:

        source /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv (Suggested location: /usr/lib/ckan/default/src)
:

        git clone https://github.com/TIBHannover/Organization-Group.git
        cd ckanext-organization-group
        pip install -e .
        pip install -r requirements.txt

3. Add `organization_group` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).


4. Restart CKAN and supervisor. For example if you've deployed CKAN with nginx on Ubuntu:

        sudo service nginx reload
        sudo service supervisor reload


