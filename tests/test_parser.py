from unittest import TestCase, mock

from nose.tools import eq_

import asagami.parser


class TestParseBlockAttributes(TestCase):
  def setUp(self):
    self.grammer = asagami.parser.Grammar()

  def test_it(self):
    result = asagami.parser.parse_block_attributes(
      self.grammer,
      '\n'
      '    .. hoge: ninja   \n'
      '    ..piyo: youjo\n'
      '    ..    bad_ninja: good_ninja\n'
    )
    eq_(len(result), 3)
    eq_(result['hoge'], 'ninja')
    eq_(result['piyo'], 'youjo')
    eq_(result['bad_ninja'], 'good_ninja')


class TestBlockParser(TestCase):
  def test_it(self):
    from asagami.module import BlockModule

    class YoujoModule(BlockModule):
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
    from asagami.module import BlockModule

    class YoujoModule(BlockModule):
      def get_name(self):
        return 'youjo'

      def get_patterns(self):
        return []

      def get_tokenizer(self):
        return None

    class NinjaModule(BlockModule):
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
    from asagami.module import BlockModule
    import re
    tokenizer = mock.MagicMock()

    class YoujoModule(BlockModule):
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
