from typing import (
  List,
  Pattern,
)

import abc

from asagami.document import DocumentEnvironment
from .token import (
  BlockTokenizer,
  InlineTokenizer,
  BlockToken,
  InlineToken,
)


class Module(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_block_reg_exp(self) -> List[Pattern]:
    pass


class BlockType(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self) -> str:
    pass

  @abc.abstractmethod
  def get_patterns(self) -> List[Pattern]:
    pass

  @abc.abstractmethod
  def get_tokenizer(self) -> BlockTokenizer:
    pass


class InlineType(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def get_patterns(self) -> List[Pattern]:
    pass

  @abc.abstractmethod
  def get_tokenizer(self) -> InlineTokenizer:
    pass


class BlockTransformer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def transform(self, env: DocumentEnvironment, token: BlockToken):
    pass


class InlineTransformer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def transform(self, env: DocumentEnvironment, token: InlineToken):
    pass


class BlockRenderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def render(self, token: BlockToken) -> str:
    pass


class InlineRenderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def render(self, token: BlockToken) -> str:
    pass
