from hashlib import sha256
from datetime import datetime

class Block:
  def __init__(self, timestamp, lastHash, hash, data, validator = None, signature = None):
    self.timestamp = timestamp
    self.lastHash = lastHash
    self.hash = hash
    self.data = data
    self.validator = validator
    self.signature = signature

  def __str__(self):
    return """Block - 
        Timestamp : {}
        Last Hash : {}
        Hash      : {}
        Data      : {}
        Validator : {}
        Signature : {}
    """.format(self.timestamp, self.lastHash, self.hash, self.data, self.validator, self.signature)

  def genesis():
    return Block("genesis time", "----", "genesis-hash", "")

  def hash(timestamp, lastHash, data):
    return sha256(str(timestamp + lastHash + data).encode('utf-8')).hexdigest()

  def createBlock(lastBlock, data):
    timestamp = str(datetime.now())
    lastHash = lastBlock.hash
    hash = Block.hash(timestamp, lastHash, data)

    return Block(timestamp, lastHash, hash, data)
