#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2013-2014, Epic Games, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: zabbix_task
short_description: Create Zabbix tasks
description:
   - Create Zabbix tasks: https://www.zabbix.com/documentation/current/en/manual/api/reference/task
   - This can be used to force data collection on an item.
author:
    - Gaudenz Steinlin (@gaudenz)
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
options:
    items:
        description:
            - Items to force data collection
        required: true
        type: list
        elements: int

extends_documentation_fragment:
- community.zabbix.zabbix
'''

EXAMPLES = r'''
- name: Force data collection
  local_action:
    module: community.zabbix.zabbix_task
    server_url: http://monitor.example.com
    login_user: username
    login_password: password
    items:
      - 1234
'''


from ansible.module_utils.basic import AnsibleModule, missing_required_lib

from ansible_collections.community.zabbix.plugins.module_utils.base import ZabbixBase
import ansible_collections.community.zabbix.plugins.module_utils.helpers as zabbix_utils


class Task(ZabbixBase):
    def create_task(self, items):
        return self._zapi.task.create([
            {'type': 6, # check now
             'request': {
                 'itemid': i,
                 },
             } for i in items
        ])


def main():
    argument_spec = zabbix_utils.zabbix_common_argument_spec()
    argument_spec.update(dict(
        items=dict(type='list', required=True),
    ))
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    items = module.params['items']

    task = Task(module)

    # create task
    tasks = task.create_task(items)
    if len(tasks) > 0:
        module.exit_json(
            changed=True,
            result="Successfully created task(s): %s" % tasks,
        )
    else:
        module.exit_json(changed=False)


if __name__ == '__main__':
    main()
