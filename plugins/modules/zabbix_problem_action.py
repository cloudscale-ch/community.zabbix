#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) gaudenz.steinlin@cloudscale.ch
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


RETURN = r'''
---
hosts:
  description: Acknowledge or close Zabbix problems. See
  https://www.zabbix.com/documentation/current/en/manual/api/reference/event.
  returned: success
  type: list
  elements: dict
  sample: []
'''

DOCUMENTATION = r'''
---
module: zabbix_problem_action
short_description: Modify Zabbix problems
description:
   - Acknowledge or close Zabbix problems.
   - Add a message to Zabbix problems.
   - Change a problems severity.
author:
    - "Gaudenz Steinlin (@gaudenz)"
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
options:
    eventid:
        description:
            - ID of the problem event.
        required: true
        type: int
    action:
        description:
             - Action to perform
        required: true
        choices: [close, acknowledge, message, severity, unacknowledge]
        type: str
    message:
        description:
            - Message to add to the problem.
            - Required if action is "message".
        required: false
        type: str
    severity:
        descripton:
            - New severity of the problem.
            - Required if action is "severity"
        required: false
        choices: [0, 1, 2, 3, 4, 5]
        type: int
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

ACTION_MAP = {
    'close': 1,
    'acknowledge': 2,
    'message': 4,
    'severity': 8,
    'unacknowledge': 16,
}

class ProblemAction(ZabbixBase):
    def acknowledge(self, eventid, action, message=None, severity=None):
        """ Acknowledge problems"""

        parameters = {
            'eventids': eventid,
            'action': ACTION_MAP[action],
        }

        if action == 'message':
            parameters['message'] = message
        elif action == 'severity':
            parameters['severity'] = severity

        return self._zapi.event.acknowledge(parameters)


def main():
    argument_spec = zabbix_utils.zabbix_common_argument_spec()
    argument_spec.update(dict(
        eventid=dict(type='int', required=True),
        action=dict(type='str', choices=['close', 'acknowledge', 'message', 'severity', 'unacknowledge'], required=True),
        message=dict(type='str', required=False),
        severity=dict(type='int', choices=[0,1,2,3,4,5], required=False),
    ))
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_if=[
            ['action', 'message', ['message']],
            ['action', 'severity', ['severity']],
        ],
    )

    problem = ProblemAction(module)

    module.exit_json(ok=True,
                     changed=True,
                     problems=problem.acknowledge(
                         module.params['eventid'],
                         module.params['action'],
                         module.params['message'],
                         module.params['severity'],
                     ))


if __name__ == '__main__':
    main()
