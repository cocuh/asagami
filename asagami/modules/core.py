from typing import Match

import re

from asagami.document import DocumentEnvironment
from asagami.module import InlineRenderer, InlineType, Module
from asagami.token import (
  InlineToken,
)


class BoldModule(Module):
  def get_name(self):
    return 'bold'

  def get_inline_types(self):
    return [BoldInlineType()]

  def get_inline_renderer(self):
    return [BoldInlineRenderer()]


class BoldInlineType(InlineType):
  def get_name(self):
    return 'bold'

  def get_patterns(self):
    return [re.compile('\*(?P<value>[^\*]+)\*')]

  def get_tokenizer(self):
    return self.tokenizer

  @staticmethod
  def tokenizer(match: Match) -> InlineToken:
    return InlineToken(
      name='bold',
      value=match['value'],
      attributes={},
    )


class BoldInlineRenderer(InlineRenderer):
  def get_name(self):
    return 'bold'

  def render_html(self, token: InlineToken, env: DocumentEnvironment):
    return f'<b>{token.value}</b>'


class ItalicModule(Module):
  def get_name(self):
    return 'italic'

  def get_inline_types(self):
    return [ItalicInlineType()]

  def get_inline_renderer(self):
    return [ItalicInlineRenderer()]


class ItalicInlineType(InlineType):
  def get_name(self):
    return 'italic'

  def get_patterns(self):
    return [re.compile('/(?P<value>[^/]+)/')]

  def get_tokenizer(self):
    return self.tokenizer

  @staticmethod
  def tokenizer(match: Match) -> InlineToken:
    return InlineToken(
      name='italic',
      value=match['value'],
      attributes={},
    )


class ItalicInlineRenderer(InlineRenderer):
  def get_name(self):
    return 'italic'

  def render_html(self, token: InlineToken, env: DocumentEnvironment):
    return f'<i>{token.value}</i>'


class UnderlineModule(Module):
  def get_name(self):
    return 'underline'

  def get_inline_types(self):
    return [UnderlineInlineType()]

  def get_inline_renderer(self):
    return [UnderlineInlineRenderer()]


class UnderlineInlineType(InlineType):
  def get_name(self):
    return 'underline'

  def get_patterns(self):
    return [re.compile('_(?P<value>[^_]+)_')]

  def get_tokenizer(self):
    return self.tokenizer

  @staticmethod
  def tokenizer(match: Match) -> InlineToken:
    return InlineToken(
      name='underline',
      value=match['value'],
      attributes={},
    )


class UnderlineInlineRenderer(InlineRenderer):
  def get_name(self):
    return 'underline'

  def render_html(self, token: InlineToken, env: DocumentEnvironment):
    return f'<u>{token.value}</u>'


class LinkModule(Module):
  def get_name(self):
    return 'link'

  def get_inline_types(self):
    return [UrlLinkInlineType()]

  def get_inline_renderer(self):
    return [UrlLinkInlineRenderer()]


class UrlLinkInlineType(InlineType):
  def get_name(self):
    return 'link'

  def get_patterns(self):
    return [re.compile('\[(?P<value>[\]])+\]\((?P<url>https?://[\)]+)\)')]

  def get_tokenizer(self):
    return self.tokenizer

  @staticmethod
  def tokenizer(match: Match) -> InlineToken:
    return InlineToken(
      name='link',
      value=match['value'],
      attributes={
        'href': match['url']
      },
    )


class UrlLinkInlineRenderer(InlineRenderer):
  def get_name(self):
    return 'link'

  def render_html(self, token: InlineToken, env: DocumentEnvironment):
    href = token.attributes["href"]
    return f'<a href="{href}">{token.value}</a>'
