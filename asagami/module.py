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
  def get_name(self) -> str:
    pass

  def get_block_types(self) -> List['BlockType']:
    return []

  def get_inline_types(self) -> List['InlineType']:
    return []

  def get_block_renderer(self) -> List['BlockRenderer']:
    return []

  def get_inline_renderer(self) -> List['InlineRenderer']:
    return []


class BlockType(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self) -> str:
    pass

  @abc.abstractmethod
  def get_patterns(self) -> List[Pattern]:
    pass

  def get_tokenizer(self) -> BlockTokenizer:
    return self.tokenizer

  @abc.abstractstaticmethod
  def tokenizer(match: Match) -> BlockToken:
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

  def get_tokenizer(self) -> InlineTokenizer:
    return self.tokenizer

  @abc.abstractstaticmethod
  def tokenizer(match: Match) -> InlineToken:
    pass

  def get_transformer(self) -> Optional[InlineTransformer]:
    return None


class BlockRenderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  def render_html(self, token: BlockToken, env: DocumentEnvironment) -> Any:
    pass


class InlineRenderer(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def get_name(self):
    pass

  def render_html(self, token: InlineToken, env: DocumentEnvironment) -> Any:
    pass
