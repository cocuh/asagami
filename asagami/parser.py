from typing import Dict, List, Match, Optional, Pattern, Set, Tuple

import re
from collections import OrderedDict

from .document import Document, DocumentMetaData
from .module import BlockTokenizer, BlockType, InlineTokenizer, InlineType
from .token import BlockToken, InlineToken, TokenAttributes

BlockGrammarRules = Dict[Pattern, BlockTokenizer]
InlineGrammarRules = Dict[Pattern, InlineTokenizer]


class Grammar:
  block_attribute_pattern = re.compile(
    r'^ {4}\.\. *(?P<name>[a-zA-Z0-9_]+) *: *(?P<value>.+?) *$',
    re.MULTILINE,
  )

  inline_attribute_pattern = re.compile(
    r'^(?P<name>[a-zA-Z0-9_]+) *= *(?P<value>[^,]+),?',
  )

  metadata_pattern = re.compile(
    r'r^::(?P<name>[a-zA-Z0-9_]+) *: *(?P<value>.*)$',
    re.MULTILINE,
  )

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
    if not attribute_text:  # empty string
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


class MetaDataParser:
  def __init__(self, grammar: Grammar = Grammar()):
    self.grammar = grammar

  def parse(self, metadata: DocumentMetaData, text: str) -> Tuple[DocumentMetaData, str]:
    text = text.lstrip('\n ')
    while text:
      match = self.grammar.metadata_pattern.match(text)
      if match is None:
        break
      name = match['name']
      value = match['value']
      metadata.register(name, value)
      text = text[match.end():].lstrip('\n ')
    return metadata, text


class BlockParser:
  types: List[BlockType]
  rules: BlockGrammarRules
  inline_parser: 'InlineParser'

  def __init__(
      self,
      block_types: List[BlockType],
      inline_parser: 'InlineParser',
      grammar: Grammar = Grammar(),
  ):
    self.types = block_types
    self.rules = self._gen_rules(grammar, block_types)
    self.inline_parser = inline_parser

  @classmethod
  def _gen_rules(cls, grammer: Grammar, types: List[BlockType]) -> BlockGrammarRules:
    rules = OrderedDict()
    for t in types:
      tokenizer = t.get_tokenizer()
      for pattern in t.get_patterns():
        rules[pattern] = tokenizer

    names: Set[str] = set([
      t.get_name()
      for t in types
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


class InlineParser:
  types: List[InlineType]
  rules: InlineGrammarRules

  def __init__(
      self,
      types: List[InlineType],
      grammar: Grammar = Grammar(),
  ):
    self.types = types
    self.rules = self._gen_rules(grammar, types)

  @classmethod
  def _gen_rules(cls, grammer: Grammar, types: List[InlineType]) -> InlineGrammarRules:
    rules = OrderedDict()
    for t in types:
      tokenizer = t.get_tokenizer()
      for pattern in t.get_patterns():
        rules[pattern] = tokenizer

    names: Set[str] = set([
      t.get_name()
      for t in types
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


class Parser:
  def __init__(self, custom_modules, grammar=Grammar()):
    self.custom_modules = custom_modules
    self.grammar = grammar

  def parse(self, text: str):
    metadata_parser = MetaDataParser()
    metadata = DocumentMetaData()
    metadata, body = metadata_parser.parse(metadata, text)

    block_types, inline_types = load_modules(metadata)  # TODO

    inline_parser = InlineParser(
      types=inline_types,
      grammar=self.grammar,
    )
    block_parser = BlockParser(
      block_types=block_types,
      inline_parser=inline_parser,
      grammar=self.grammar,
    )

    block_tokens = block_parser.parse(body)
    document = Document(
      metadata=metadata,
      blocks=block_tokens,
    )
    return document
