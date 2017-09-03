from typing import (
  List,
  Dict,
  Pattern,
  Match,
  Optional,
  Set,
)

import abc
from collections import OrderedDict
import re

from .module import BlockModule, InlineModule
from .token import (
  BlockTokenizer,
  InlineTokenizer,
  BlockToken,
  TokenAttributes,
  InlineToken)

BlockGrammarRules = Dict[Pattern, BlockTokenizer]
InlineGrammarRules = Dict[Pattern, InlineTokenizer]


class Grammar:
  def gen_block_pattern(self, name: str) -> Pattern:
    pattern: Pattern = re.compile(
      r'^\.\. *' + f'{name}' + r' *'
      + r'(?P<attributes>(\n {4}\.\. +[a-zA-Z0-9_]+ *: *.+ *)*)'
      + r'(?P<body>(\n {4}.*)*)\n?',
    )
    return pattern

  def gen_inline_pattern(self, name):
    pattern: Pattern = re.compile(
      r'^:'
      + f'{name}'
      + r'(?P<attributes>(\{[^\}]*\})?):'
      + '\{(?P<value>[^\}]*)\}'
    )
    return pattern

  block_attribute_pattern = re.compile(
    r'^ {4}\.\. *(?P<name>[a-zA-Z0-9_]+) *: *(?P<value>.+?) *$',
    re.MULTILINE,
  )

  inline_attribute_pattern = re.compile(
    r'^(?P<name>[a-zA-Z0-9_]+)\s*=\s*(?P<value>[^,]+),?'
  )

  def parse_block_attributes(self, attribute_text: str) -> TokenAttributes:
    attributes = OrderedDict()
    attribute_text = attribute_text.strip('\n')
    while attribute_text:
      result = self.block_attribute_pattern.match(attribute_text)
      if result is None:
        raise RuntimeError('invalid attributes text: {}'.format(repr(attribute_text)))
      name = result['name']
      value = result['value']
      attributes[name] = value
      attribute_text = attribute_text[result.end():]
      attribute_text = attribute_text.strip('\n')
    return attributes

  def parse_inline_attributes(self, attribute_text: str) -> TokenAttributes:
    attributes = OrderedDict()
    if not attribute_text: # empty string
      return attributes
    assert attribute_text.startswith('{')
    assert attribute_text.endswith('}')
    attribute_text = attribute_text[1:-1]
    while attribute_text:
      result = self.inline_attribute_pattern.match(attribute_text)
      if result is None:
        raise RuntimeError('invalid attributes text: {}'.format(repr(attribute_text)))
      name = result['name']
      value = result['value']
      attributes[name] = value
      attribute_text = attribute_text[result.end():]
    return attributes


class Parser(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def parse(self, text: str):
    raise NotImplementedError()


class BlockParser(Parser):
  tokens: List[BlockToken]
  modules: List[BlockModule]
  rules: BlockGrammarRules

  def __init__(
      self,
      modules: List[BlockModule],
      grammar: Grammar = Grammar(),
  ):
    self.modules = modules
    self.rules = self._gen_rules(grammar, modules)

  @classmethod
  def _gen_rules(cls, grammer: Grammar, modules: List[BlockModule]) -> BlockGrammarRules:
    rules = OrderedDict()
    for m in modules:
      tokenizer = m.get_tokenizer()
      for pattern in m.get_patterns():
        rules[pattern] = tokenizer

    names: Set[str] = set([
      m.get_name()
      for m in modules
    ])
    for name in names:
      pattern = grammer.gen_block_pattern(name)
      rules[pattern] = cls._gen_tokenizer(grammer, name)
    return rules

  @staticmethod
  def _gen_tokenizer(grammer, name):
    def tokenizer(match: Match):
      attributes = match['attributes']
      body = match['body']
      return BlockToken(
        name=name,
        body=body,
        attributes=grammer.parse_block_attributes(attributes),
      )

    return tokenizer

  def parse(self, text: str) -> List[BlockToken]:
    tokens = []
    text = text.rstrip('\n')

    while text:
      for pat, tokenizer in self.rules.items():
        result: Optional[Match] = pat.match(text)
        if result is None:
          continue
        else:
          token = tokenizer(result)  # TODO: catch tokenizer failure
          tokens.append(token)
          text = text[result.end():]
          break
      else:
        raise RuntimeError('Infinite loop at: %s' % text)
    return tokens


class InlineParser(Parser):
  tokens: List[InlineToken]
  modules: List[InlineModule]
  rules: InlineGrammarRules

  def __init__(
      self,
      modules: List[InlineModule],
      grammar: Grammar = Grammar(),
  ):
    self.tokens = []
    self.modules = modules
    self.rules = self._gen_rules(grammar, modules)

  @classmethod
  def _gen_rules(cls, grammer: Grammar, modules: List[InlineModule]) -> InlineGrammarRules:
    rules = OrderedDict()
    for m in modules:
      tokenizer = m.get_tokenizer()
      for pattern in m.get_patterns():
        rules[pattern] = tokenizer

    names: Set[str] = set([
      m.get_name()
      for m in modules
    ])
    for name in names:
      pattern = grammer.gen_inline_pattern(name)
      rules[pattern] = cls._gen_tokenizer(grammer, name)
    return rules

  @staticmethod
  def _gen_tokenizer(grammer, name):
    def tokenizer(match: Match):
      attributes = match['attributes']
      value = match['value']
      return InlineToken(
        name=name,
        value=value,
        attributes=grammer.parse_inline_attributes(attributes),
      )

    return tokenizer

  def parse(self, text: str) -> List[InlineToken]:
    tokens = []
    text = text.rstrip('\n')

    while text:
      for pat, tokenizer in self.rules.items():
        result: Optional[Match] = pat.match(text)
        if result is None:
          continue
        else:
          token = tokenizer(result)  # TODO: catch tokenizer failure
          tokens.append(token)
          text = text[result.end():]
          break
      else:
        raise RuntimeError('Infinite loop at: %s' % text)
    return tokens
