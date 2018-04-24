import struct
import asyncio
import ssl
import argparse

from connection_handler import ConnectionHandler
from connectivity_manager import ConnectivityManager

SERVER_COMMON_NAME = "CudaNT Server"

parser = argparse.ArgumentParser()
parser.add_argument("-ca", help="CA filepath", required=True)
parser.add_argument("-key", help="Key filepath", required=True)
parser.add_argument("-cert", help="Certificate filepath", required=True)
parser.add_argument("-host", help="Server host", required=True)
parser.add_argument("-port", help="Server port", required=True)
args = parser.parse_args()

ca_filepath = args.ca
key_filepath = args.key
cert_filepath = args.cert
server_host = args.host
server_port = args.port

loop = asyncio.get_event_loop()
connectivity_manager = ConnectivityManager()
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca_filepath)
ssl_context.check_hostname = False
ssl_context.load_cert_chain(cert_filepath, key_filepath)
client_coro = loop.create_connection(lambda: ConnectionHandler(connectivity_manager), server_host, server_port, ssl=ssl_context)
try:
  while True:
    loop.run_until_complete(client_coro)
except asyncio.CancelledError:
  loop.close()