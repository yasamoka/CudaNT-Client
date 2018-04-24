import asyncio
import struct

CMD_EXIT = "exit"

class ConnectivityManager:
  def set_connection_handler(self, connection_handler):
    self.connection_handler = connection_handler
    print("Connected to server successfully.")
    self.user_input()

  def connection_lost(self, exc):
    if exc is None:
      print("Connection lost")
    else:
      print("Connection lost - reason: {}".format(exc))
    self.shutdown()

  def shutdown(self):
    for task in asyncio.Task.all_tasks():
      task.cancel()
    self.connection_handler.close()

  def message_received(self, message):
    status_code, stdout_length, stderr_length, data = struct.unpack("III{}s".format(len(message) - 12), message)
    stdout_bytes, stderr_bytes = struct.unpack("{}s{}s".format(stdout_length, stderr_length), data)
    stdout = stdout_bytes.decode('utf-8')
    stderr = stderr_bytes.decode('utf-8')
    print("---STDOUT---:\n{}\n---STDERR---:\n{}\nSTATUS CODE: {}".format(stdout, stderr, status_code))
    self.user_input()

  def user_input(self):
    while True:
      cmd = input("> ")
      if cmd == "":
        continue
      if cmd.lower() == CMD_EXIT:
        self.shutdown()
        return
      message = cmd.encode('utf-8')
      self.connection_handler.send_message(message)
      break