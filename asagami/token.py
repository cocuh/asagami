from typing import Dict, List, Union

TokenAttributes = Dict[str, Union[str, List[str]]]


class BlockToken:
  def __init__(self, name: str, body: str, attributes: TokenAttributes):
    self.name = name
    self.body = body
    self.attributes = attributes


class InlineToken:
  def __init__(self, name: str, value: str, attributes: TokenAttributes):
    self.name = name
    self.value = value
    self.attributes = attributes
