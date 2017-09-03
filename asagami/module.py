from typing import (
  List,
  Pattern,
)

import abc

from .token import (
  BlockTokenizer,
  InlineTokenizer,
)


class Module(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_block_reg_exp(self) -> List[Pattern]:
    pass


class BlockModule(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self) -> str:
    pass

  @abc.abstractmethod
  def get_patterns(self) -> List[Pattern]:
    pass

  @abc.abstractmethod
  def get_tokenizer(self) -> BlockTokenizer:
    pass


class InlineModule(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def get_patterns(self) -> List[Pattern]:
    pass

  @abc.abstractmethod
  def get_tokenizer(self) -> InlineTokenizer:
    pass
