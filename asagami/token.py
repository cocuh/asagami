from typing import Dict, List, Union

TokenAttributes = Dict[str, Union[str, List[str]]]


class BlockToken:
  def __init__(self, name: str, body: str, attributes: TokenAttributes):
    self.name = name
    self.attributes = attributes
    self.body = body


class InlineToken:
  def __init__(self, name: str, value: str, attributes: TokenAttributes):
    self.name = name
    self.attributes = attributes
    self.value = value


class ParagraphToken:
  def __init__(self, name: str, children: List[InlineToken], attributes: TokenAttributes):
    self.name = name
    self.attributes = attributes
    self.children = children
