import os
from config import config
from datetime import datetime

class LogManager:
  def __init__(self):
    self.filepath = config.FILEPATH

  def append(self, data):
    with open(self.filepath, 'a', encoding='utf-8') as f:
      f.write(f"{datetime.now().isoformat()} | {data}\n")

  def exists(self):
    return os.path.isfile(self.filepath)
  
  def flush(self):
    with open(self.filepath, 'a', encoding='utf-8') as f:
      f.flush()

  def delete(self):
    if self.exists():
      os.remove(self.filepath)
