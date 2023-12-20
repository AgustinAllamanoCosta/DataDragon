from src.blockchain.block import Block
import base64

class Blockchain:
  def __init__(self):
    self.chain = [Block.genesis()]

  def addBlock(self, data):
    block = Block.createBlock(self.chain[len(self.chain) - 1 ], str(data))
    self.chain.append(block)

    return block
  
  def toDictionary(chain):
    chain_to_dictionary = []
    for block in chain:
      if block.data:
        chain_to_dictionary.append({ "timestamp": block.timestamp, "lastHash": block.lastHash, "hash": block.hash, "data": base64.b64decode(block.data[1:]), "validator": block.validator, "signature": block.signature })
      else:
        chain_to_dictionary.append({ "timestamp": block.timestamp, "lastHash": block.lastHash, "hash": block.hash, "data": block.data, "validator": block.validator, "signature": block.signature })
    return chain_to_dictionary

  def isValidChain(chain):
    if Blockchain.toDictionary([chain[0]]) != Blockchain.toDictionary([Block.genesis()]):
      return False

    for i in range(1, len(chain)):
      block = chain[i]
      lastBlock = chain[i - 1]
      if block.lastHash != lastBlock.hash or block.hash != Block.blockHash(block):
        return False

    return True

  def replaceChain(self, newChain):
    if len(newChain) <= len(self.chain):
        print("Received chain is not longer than the current chain")
        return
    elif not self.isValidChain(newChain):
        print("Received chain is invalid")
        return
    
    print("Replacing the current chain with new chain")
    self.chain = newChain

  def blockHash(block):
    timestamp, lastHash, data = block.timestamp, block.lastHash, block.data
    return Block.hash(timestamp, lastHash, data)
