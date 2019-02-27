# Copyright: (c) 2018, Pluribus Networks
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import shlex
#from ansible.module_utils.connection import Connection, ConnectionError
from ansible.module_utils.connection import exec_command


def pn_cli(module, switch=None, username=None, password=None, switch_local=None):
    """
    Method to generate the cli portion to launch the Netvisor cli.
    :param module: The Ansible module to fetch username and password.
    :return: The cli string for further processing.
    """

    cli = ''

    if username and password:
        cli += '--user "%s":"%s" ' % (username, password)
    if switch:
        cli += ' switch ' + switch
    if switch_local:
        cli += ' switch-local '

    return cli


def booleanArgs(arg, trueString, falseString):
    if arg is True:
        return " %s " % trueString
    elif arg is False:
        return " %s " % falseString
    else:
        return ""


def run_cli(module, cli, state_map):
    """
    This method executes the cli command on the target node(s) and returns the
    output. The module then exits based on the output.
    :param cli: the complete cli string to be executed on the target node(s).
    :param state_map: Provides state of the command.
    :param module: The Ansible module to fetch command
    """
    state = module.params['state']
    command = state_map[state]

    cmd = shlex.split(cli)
    rc, out, err = exec_command(module, cli)
    f = open("/tmp/testout.txt", "w")
    f.write("RC: " + str(rc) + "\n")
    f.write("OUT: " + out + "\n")
    f.write("ERR: " + err + "\n")
    f.close()
    """
    try:
        connection = Connection(module._socket_path)
	f = open("/tmp/testout.txt", "w")
	f.write(module._socket_path)
	f.write(cli)
	f.close()
        response = connection.get(cli)
    except ConnectionError as exc:
        module.fail_json(msg="FAILED")
    """

    #result, out, err = module.run_command(cmd)
    results = {'changed': False}
    results.update({'stdout': out})
    module.exit_json(**results)
