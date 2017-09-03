from unittest import TestCase, mock

from nose.tools import eq_

import asagami.parser


class TestGrammerGenInlinePattern(TestCase):
  def setUp(self):
    self.grammar = asagami.parser.Grammar()

  def test_it(self):
    pattern = self.grammar.gen_inline_pattern('youjo')
    self.assertIsNotNone(pattern.match(':youjo:{}'))
    self.assertIsNotNone(pattern.match(':youjo:{hoge}'))
    self.assertIsNone(pattern.match(':youo:{hoge}'))


class TestGrammarParseBlockAttributes(TestCase):
  def setUp(self):
    self.grammar = asagami.parser.Grammar()

  def test_it(self):
    result = self.grammar.parse_block_attributes(
      '\n'
      '    .. hoge: ninja   \n'
      '    ..piyo: youjo\n'
      '    ..    bad_ninja: good_ninja\n'
    )
    eq_(len(result), 3)
    eq_(result['hoge'], 'ninja')
    eq_(result['piyo'], 'youjo')
    eq_(result['bad_ninja'], 'good_ninja')


class TestGrammarParseInlineAttributes(TestCase):
  def setUp(self):
    self.grammar = asagami.parser.Grammar()

  def test_it(self):
    result = self.grammar.parse_inline_attributes(
      '{hoge=piyo,youjo=ninja,href="http://dakko.site/"}'
    )
    eq_(len(result), 3)
    eq_(result['hoge'], 'piyo')
    eq_(result['youjo'], 'ninja')
    eq_(result['href'], '"http://dakko.site/"')


class TestBlockParser(TestCase):
  def test_it(self):
    from asagami.module import BlockType

    class YoujoModule(BlockType):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return []

      def get_tokenizer(self):
        return None

    modules = [
      YoujoModule(),
    ]
    grammer = asagami.parser.Grammar()
    parser = asagami.parser.BlockParser(modules, grammer)
    tokens = parser.parse(
      '.. youjo\n'
      '    .. youjo: ninja\n'
      '    .. huga : gegege   \n'
    )
    eq_(
      len(tokens),
      1,
    )
    token = tokens[0]
    eq_(token.name, 'youjo')
    eq_(len(token.attributes), 2)
    eq_(token.attributes['youjo'], 'ninja')
    eq_(token.attributes['huga'], 'gegege')

  def test_multiple_module(self):
    from asagami.module import BlockType

    class YoujoModule(BlockType):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return []

      def get_tokenizer(self):
        return None

    class NinjaModule(BlockType):
      def get_name(self):
        return 'ninja'

      def get_patterns(self):
        return []

      def get_tokenizer(self):
        return None

    modules = [
      YoujoModule(),
      NinjaModule(),
    ]
    grammer = asagami.parser.Grammar()
    parser = asagami.parser.BlockParser(modules, grammer)
    tokens = parser.parse(
      '.. youjo\n'
      '    .. youjo: ninja\n'
      '.. youjo\n'
      '.. ninja\n'
      '    .. huga : gegege   \n'
    )
    eq_(
      len(tokens),
      3,
    )
    eq_(tokens[0].name, 'youjo')
    eq_(len(tokens[0].attributes), 1)
    eq_(tokens[0].attributes['youjo'], 'ninja')
    eq_(tokens[1].name, 'youjo')
    eq_(len(tokens[1].attributes), 0)
    eq_(tokens[2].name, 'ninja')
    eq_(len(tokens[2].attributes), 1)
    eq_(tokens[2].attributes['huga'], 'gegege')

  def test_tokenizer(self):
    from asagami.module import BlockType
    import re
    tokenizer = mock.MagicMock()

    class YoujoModule(BlockType):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return [re.compile(r"```(?P<code>(\n.*(?!```))*)\n```")]

      def get_tokenizer(self):
        return tokenizer

    modules = [
      YoujoModule(),
    ]
    grammer = asagami.parser.Grammar()
    parser = asagami.parser.BlockParser(modules, grammer)
    parser.parse(
      '```\n'
      'youjo love code\n'
      'ninja love code\n'
      '```'
    )
    tokenizer.assert_called_once()
    match = tokenizer.call_args[0][0]
    eq_(
      match.end(),
      len(
        '```\n'
        'youjo love code\n'
        'ninja love code\n'
        '```'
      )
    )
    eq_(
      match['code'],
      '\n'
      'youjo love code\n'
      'ninja love code'
    )


class TestInlineParser(TestCase):
  def test_it(self):
    from asagami.module import InlineType

    class YoujoModule(InlineType):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return []

      def get_tokenizer(self):
        return None

    modules = [
      YoujoModule(),
    ]
    grammer = asagami.parser.Grammar()
    parser = asagami.parser.InlineParser(modules, grammer)
    tokens = parser.parse(
      ':youjo:{hoge}'
    )
    eq_(
      len(tokens),
      1,
    )
    token = tokens[0]
    eq_(token.name, 'youjo')
    eq_(token.value, 'hoge')
    eq_(token.attributes, {})

  def test_attribtues(self):
    from asagami.module import InlineType

    class YoujoModule(InlineType):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return []

      def get_tokenizer(self):
        return None

    modules = [
      YoujoModule(),
    ]
    grammer = asagami.parser.Grammar()
    parser = asagami.parser.InlineParser(modules, grammer)
    tokens = parser.parse(
      ':youjo{ninja=hoge,onaka=guruguru}:{hoge}'
    )
    eq_(
      len(tokens),
      1,
    )
    token = tokens[0]
    eq_(token.name, 'youjo')
    eq_(token.value, 'hoge')
    eq_(token.attributes, {'ninja': 'hoge', 'onaka': 'guruguru'})

  def test_tokenizer(self):
    from asagami.module import InlineType
    import re

    tokenizer = mock.MagicMock()

    class YoujoModule(InlineType):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return [
          re.compile('^\$(?P<value>[^\$]+)\$')
        ]

      def get_tokenizer(self):
        return tokenizer

    modules = [
      YoujoModule(),
    ]
    grammer = asagami.parser.Grammar()
    parser = asagami.parser.InlineParser(modules, grammer)
    tokens = parser.parse(
      ':youjo:{hoge}$\mathcal{A}(\mathcal{D})$'
    )
    eq_(
      len(tokens),
      2,
    )
    token = tokens[0]
    eq_(token.name, 'youjo')
    eq_(token.value, 'hoge')
    eq_(token.attributes, {})

    tokenizer.assert_called_once()
    eq_(tokenizer.call_args[0][0]['value'], '\mathcal{A}(\mathcal{D})')
