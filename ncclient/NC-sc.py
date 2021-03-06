#!/usr/bin/env python
import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
if __name__ == '__main__':
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('--config', type=str, required=True,
                        help="XML file to use for configuration")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify this if you want a non-default port")
    args = parser.parse_args()
    m = manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"csr"})

    f = open(args.config)
    stuff = f.read()
    print(stuff)

    try:
        rpc_reply = m.edit_config(target='running', config=stuff)
    except Exception as e:
        print("Encountered the following RPC error:")
        print(e) 
        sys.exit()

    if rpc_reply.ok is not True:
        print("Encountered a problem configuring device")
        sys.exit()
