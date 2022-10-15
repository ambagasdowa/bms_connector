# NOTES Operations

#    POST: to create data.
#    GET: to read data.
#    PUT: to update data.
#    DELETE: to delete data.

#import os
#import subprocess
# import logging  # for paramiko debug
from typing import Optional
from typing import Union
from fastapi import FastAPI
from fabric import Connection


bms = FastAPI(
    title='Development UES API Documentation', docs_url="/api", openapi_url="/api/v1"
)


@bms.get('/')
async def read_root():
    return {"Hello": "Python"}


@bms.get('/guests/{guest}/commands/{command}')
async def read_guest_command(guest: str, command: str, q: Optional[str] = None):
    # NOTE can query a database in hir
    # For Example
    # request = await some_sql_query()

    newQuery = "Response String is -> " + q

# NOTE connect_kwargs (dict) –
#
# Keyword arguments handed verbatim to SSHClient.connect (when open is called).
#
# from => class paramiko.client.SSHClient
# connect_kwargs.password
#connect(hostname, port=22, username=None, password=None, pkey=None, key_filename=None, timeout=None, allow_agent=True, look_for_keys=True, compress=False, sock=None, gss_auth=False, gss_kex=False, gss_deleg_creds=True, gss_host=None, banner_timeout=None, auth_timeout=None, gss_trust_dns=True, passphrase=None, disabled_algorithms=None)

    link = Connection(
        host=guest,
        user='node_two',
        connect_kwargs={
            "password": "pekas",
        },
    )

    #    sudopass = Responder(
    #        pattern=r'\[sudo\] password:',
    #        response='mypassword\n',
    #    )

    #    link.run('sudo whoami', pty=True, watchers=[sudopass])
    result = link.run(command)

    # return{"item_id": item_id, "q": newQuery + " Remote command execute is => " + result.command + " => " + result.stdout}
    return{"client": guest, "q": newQuery + " Remote command execute is => " + result.command + " => " + result.stdout}
