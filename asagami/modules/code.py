from typing import Match

import re

from asagami.document import DocumentEnvironment
from asagami.module import (
  BlockRenderer,
  BlockType,
  InlineRenderer,
  InlineType,
  Module,
)
from asagami.token import (
  BlockToken,
  InlineToken,
)

name = 'code'


class CodeModule(Module):
  def get_name(self):
    return name

  def get_block_types(self):
    return [
      CodeBlockType(),
    ]

  def get_inline_types(self):
    return [
      CodeInlineType(),
    ]

  def get_block_renderer(self):
    return [CodeBlockRenderer()]

  def get_inline_renderer(self):
    return [CodeInlineRenderer()]


class CodeBlockType(BlockType):
  def get_name(self):
    return name

  def get_patterns(self):
    return [re.compile(r"```(?P<lang>[^\n]*)(?=\n)(?P<code>(\n.*(?!```))*)\n```")]

  def get_tokenizer(self):
    return self._tokenizer

  @staticmethod
  def _tokenizer(match: Match) -> BlockToken:
    attributes = {'lang': match['lang']}
    code = match['code']
    return BlockToken(
      name=name,
      attributes=attributes,
      body=code,
    )


class CodeInlineType(InlineType):
  def get_name(self):
    return name

  def get_patterns(self):
    return [re.compile(r"`(?P<code>([^`]*))`")]

  def get_tokenizer(self):
    return self._tokenizer

  @staticmethod
  def _tokenizer(match: Match) -> InlineToken:
    attributes = {'lang': match['lang']}
    code = match['code']
    return InlineToken(
      name=name,
      attributes=attributes,
      value=code,
    )


class CodeBlockRenderer(BlockRenderer):
  def render_html(self, token: BlockToken, env: DocumentEnvironment):
    return f'<code>{token.body}</code>'


class CodeInlineRenderer(InlineRenderer):
  def render_html(self, token: InlineToken, env: DocumentEnvironment):
    return f'<code>{token.value}</code>'
