from typing import Any, Callable, List, Match, Optional, Pattern

import abc

from .document import DocumentEnvironment
from .token import (
  BlockToken,
  InlineToken,
)

BlockTokenizer = Callable[
  [
    Match,
  ],
  BlockToken,
]
InlineTokenizer = Callable[
  [
    Match,
  ],
  InlineToken,
]

BlockTransformer = Callable[
  [
    DocumentEnvironment,
    BlockToken,
  ],
  None,
]

InlineTransformer = Callable[
  [
    DocumentEnvironment,
    InlineToken,
  ],
  None,
]


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

  def get_transformer(self) -> Optional[BlockTransformer]:
    return None


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

  def get_transformer(self) -> Optional[InlineTransformer]:
    return None


class BlockRenderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def render(self, token: BlockToken) -> Any:
    pass


class InlineRenderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  @abc.abstractmethod
  def render(self, token: InlineToken) -> Any:
    pass
