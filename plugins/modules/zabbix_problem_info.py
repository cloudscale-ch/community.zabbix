#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) gaudenz.steinlin@cloudscale.ch
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


RETURN = r'''
---
problems:
  description: List of Zabbix problems. See
  https://www.zabbix.com/documentation/current/en/manual/api/reference/problem.
  returned: success
  type: list
  elements: dict
  sample: []
'''

DOCUMENTATION = r'''
---
module: zabbix_problem_info
short_description: Gather information about Zabbix problems
description:
   - This module allows you to search for Zabbix problems.
author:
    - "Gaudenz Steinlin (@gaudenz)"
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
options:
    host:
        description:
            - Return problems for the host with this name.
        required: true
        type: str
   severities:
        description:
            - Return only problems with the given severities
        required: false
        type: list
        elements: int
        default: [1,2,3,4,5]
   acknowledged:
        description:
            - If true return only acknowledged problems
        required: false
        type: bool
        default: None
   suppressed:
        description:
            - If true return only problems in maintenance.
        required: false
        type: bool
        default: None
extends_documentation_fragment:
- community.zabbix.zabbix

'''

EXAMPLES = r'''
- name: Get host info
  local_action:
    module: community.zabbix.zabbix_problem_info
    server_url: http://monitor.example.com
    login_user: username
    login_password: password
    name: ExampleHost
    timeout: 10
'''


from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.zabbix.plugins.module_utils.base import ZabbixBase
import ansible_collections.community.zabbix.plugins.module_utils.helpers as zabbix_utils


class Problem(ZabbixBase):
    def get_problems(self, host, severities, acknowledged, suppressed):
        """ Get problems"""
        hostids = self._zapi.host.get({
            'filter': {
                'host': [host, ],
            },
            'output': ['hostid'],
        })
        return self._zapi.problem.get({
            'hostids': [h['hostid'] for h in hostids],
            'severities': severities,
            'acknowledged': acknowledged,
            'suppressed': suppressed,
        })


def main():
    argument_spec = zabbix_utils.zabbix_common_argument_spec()
    argument_spec.update(dict(
        host=dict(type='str', required=True),
        severities=dict(type='list', elements='int', default=[1,2,3,4,5], required=False),
        acknowledged=dict(type='bool', default=None, required=False),
        suppressed=dict(type='bool', default=None, required=False),
    ))
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    host = module.params['host']
    severities = module.params['severities']
    acknowledged = module.params['acknowledged']
    suppressed = module.params['suppressed']

    problem = Problem(module)

    module.exit_json(ok=True, problems=problem.get_problems(host,
                                                            severities,
                                                            acknowledged,
                                                            suppressed,
                                                            ))


if __name__ == '__main__':
    main()
