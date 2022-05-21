#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) gaudenz.steinlin@cloudscale.ch
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


RETURN = r'''
---
hosts:
  description: List of Zabbix items. See https://www.zabbix.com/documentation/current/en/manual/api/reference/item/object for list of item values.
  returned: success
  type: list
  elements: dict
  sample: [{"itemid": "25550", "type": "18", "snmp_oid": "", "hostid": "10116", "name": "Days", ... }]
'''

DOCUMENTATION = r'''
---
module: zabbix_item_info
short_description: Gather information about Zabbix items
description:
   - This module allows you to search for Zabbix item entries.
author:
    - "Gaudenz Steinlin (@gaudenz)"
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
options:
    host:
        description:
            - Return only items that belong to a host with the given name.
        required: false
        type: str
    monitored:
        description:
            - If set to true return only enabled items that belong to monitored
              hosts.
        required: false
        default: None
        type: bool
    with_triggers:
        description:
            - If set to true return only items that are used in triggers.
        required: false
        default: None
        type: bool
    item_inventory:
        description:
            - List of item inventory keys to display in the result.
            - All keys are retrieved if no key is specified.
        type: list
        elements: str
        required: false
extends_documentation_fragment:
- community.zabbix.zabbix

'''

EXAMPLES = r'''
- name: Get host info
  local_action:
    module: community.zabbix.zabbix_item_info
    server_url: http://monitor.example.com
    login_user: username
    login_password: password
    name: ExampleHost
    timeout: 10

- name: Reduce host inventory information to provided keys
  local_action:
    module: community.zabbix.zabbix_item_info
    server_url: http://monitor.example.com
    login_user: username
    login_password: password
    name: ExampleHost
    item_inventory:
      - itemid
      - type
    timeout: 10
'''


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.zabbix.plugins.module_utils.base import ZabbixBase
import ansible_collections.community.zabbix.plugins.module_utils.helpers as zabbix_utils


class Item(ZabbixBase):
    def get_items(self, host, monitored, with_triggers, item_inventory):
        """ Get items """
        return self._zapi.item.get({
            'host': host,
            'monitored': monitored,
            'with_triggers': with_triggers,
            'output': item_inventory,
        })


def main():
    argument_spec = zabbix_utils.zabbix_common_argument_spec()
    argument_spec.update(dict(
        host=dict(type='str', default='', required=False),
        monitored=dict(type='bool', required=False, default=None),
        with_triggers=dict(type='bool', required=False, default=None),
        item_inventory=dict(type='list', default=[], required=False)
    ))
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    host = module.params['host']
    monitored = module.params['monitored']
    with_triggers = module.params['with_triggers']
    item_inventory = module.params['item_inventory']

    if not item_inventory:
        item_inventory = 'extend'

    item = Item(module)

    items = item.get_items(host, monitored, with_triggers, item_inventory)
    module.exit_json(ok=True, items=items)


if __name__ == '__main__':
    main()
