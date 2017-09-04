from typing import List

from asagami.token import BlockToken


class Document:
  def __init__(self, metadata: 'DocumentMetaData', blocks: List[BlockToken]):
    pass


class DocumentMetaData:
  def register(self, name: str, value: str):
    pass


class DocumentEnvironment:
  pass
