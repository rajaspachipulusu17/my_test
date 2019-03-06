
    
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
from ansible.module_utils.common._collections_compat import Mapping
from ansible.module_utils.network.common.utils import to_list
from ansible.plugins.cliconf import CliconfBase, enable_mode


class Cliconf(CliconfBase):

    @enable_mode
    def get_config(self, source='running', flags=None, format=None):
        pass

    @enable_mode
    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        pass

    def get(self, command=None, prompt=None, answer=None, sendonly=False, output=None, check_all=False):
        if not command:
            raise ValueError('must provide value of command to execute')
        if output:
            raise ValueError("'output' value %s is not supported for get" % output)

        return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, check_all=check_all)


    def get_option_values(self):
        return {
            'format': ['text'],
            'diff_match': ['line', 'strict', 'exact', 'none'],
            'diff_replace': ['line', 'block'],
            'output': []
        }

    def get_capabilities(self):
        result = dict()
        #result['rpc'] = self.get_base_rpc() + ['run_commands']
        result['rpc'] = self.get_base_rpc()
        result['network_api'] = 'cliconf'
        result['device_info'] = self.get_device_info()
        result.update(self.get_option_values())
        return json.dumps(result)

    def get_device_info(self):
        device_info = {}

        device_info['network_os'] = 'nvos'
        device_info['network_os_version'] = '16.04'
        reply = self.get(command='software-show')
        f = open("/tmp/regex.txt", "a")
        data = to_text(reply, errors='surrogate_or_strict').strip()
        match = re.search(r'version: (\S+)\),', data)
        if match:
            device_info['network_os_version'] = match.group(1)
        f.write("\n data %s" % data)
        f.write("\n match %s" % match)
        f.write("\n device_info %s" % device_info)
        f.close()

        return device_info


#    def run_commands(self, commands=None, check_rc=True):
#        if commands is None:
#            raise ValueError("'commands' value is required")
#
#        responses = list()
#        for cmd in to_list(commands):
#            if not isinstance(cmd, Mapping):
#                cmd = {'command': cmd}
#
#            f = open("/tmp/regex.txt", "a")
#            f.write("\n cmd %s\n\n\n\n" % cmd)
#            f.close()
#            output = cmd.pop('output', None)
#            if output:
#                raise ValueError("'output' value %s is not supported for run_commands" % output)
#
#            try:
#                out = self.send_command(**cmd)
#                f = open("/tmp/regex.txt", "a")
#                f.write("\n out %s" % out)
#                f.close()
#            except AnsibleConnectionFailure as e:
#                if check_rc:
#                    raise
#                out = getattr(e, 'err', e)
#
#            if out is not None:
#                try:
#                    out = to_text(out, errors='surrogate_or_strict').strip()
#                except UnicodeError:
#                    raise ConnectionError(msg=u'Failed to decode output from %s: %s' % (cmd, to_text(out)))
#
#                try:
#                    out = json.loads(out)
#                except ValueError:
#                    pass
#
#                responses.append(out)
#
##            responses.append(out)
#
#        return responses
