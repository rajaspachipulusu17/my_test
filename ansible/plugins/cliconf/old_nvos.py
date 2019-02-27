#
# (c) 2017 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import collections
import re
import time
import json

from itertools import chain

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.module_utils.six import iteritems
from ansible.module_utils.network.common.config import NetworkConfig, dumps
from ansible.module_utils.network.common.utils import to_list
from ansible.plugins.cliconf import CliconfBase, enable_mode


class Cliconf(CliconfBase):

    def get(self, command, prompt=None, answer=None, sendonly=False, check_all=False):
        return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, check_all=check_all)

    def get_device_info(self):
        device_info = {}

        device_info['network_os'] = 'nvos'
        reply = self.get(command='software-show')
        data = to_text(reply, errors='surrogate_or_strict').strip()
        device_info['network_os_hostname'] = 'uans-9kspine1'

        return device_info


    def get_capabilities(self):
        result = dict()
        #result['rpc'] = self.get_base_rpc() + ['edit_banner', 'get_diff', 'run_commands', 'get_defaults_flag']
        result['rpc'] = self.get_base_rpc() 
        result['network_api'] = 'cliconf'
        result['device_info'] = self.get_device_info()
        return json.dumps(result)
