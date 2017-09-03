from unittest import TestCase
from nose.tools import eq_

from asagami.parser import Grammar


class TestBlockPattern(TestCase):
  def test_standard(self):
    g = Grammar()
    pattern = g.gen_block_pattern('block')
    result = pattern.match('.. block')
    self.assertIsNotNone(result)
    eq_(result['attributes'], '')
    eq_(result['body'], '')

  def test_no_space(self):
    g = Grammar()
    pattern = g.gen_block_pattern('block')
    result = pattern.match('..block')
    self.assertIsNotNone(result)
    eq_(result['attributes'], '')
    eq_(result['body'], '')

  def test_body(self):
    g = Grammar()
    pattern = g.gen_block_pattern('block')
    result = pattern.match('.. block\n    hoge\n')
    self.assertIsNotNone(result)
    eq_(result['attributes'], '')
    eq_(result['body'], '\n    hoge')

  def test_body_attributes(self):
    g = Grammar()
    pattern = g.gen_block_pattern('block')
    result = pattern.match('.. block\n'
                           '    .. piyo : youjo\n'
                           '    .. ninja:huge\n'
                           '    hoge')
    self.assertIsNotNone(result)
    eq_(result['attributes'], '\n    .. piyo : youjo\n    .. ninja:huge')
    eq_(result['body'], '\n    hoge')

  def test_body_blank_line(self):
    g = Grammar()
    pattern = g.gen_block_pattern('block')
    result = pattern.match('.. block\n    hoge\n    \n    hoge')
    self.assertIsNotNone(result)
    eq_(result['attributes'], '')
    eq_(result['body'], '\n    hoge\n    \n    hoge')

  def test_body_blank_line_attributes(self):
    g = Grammar()
    pattern = g.gen_block_pattern('block')
    result = pattern.match('.. block\n'
                           '    .. piyo : youjo\n'
                           '    .. ninja:huge\n'
                           '    hoge\n'
                           '    \n'
                           '    hoge\n')
    self.assertIsNotNone(result)
    eq_(result['attributes'], '\n    .. piyo : youjo\n    .. ninja:huge')
    eq_(result['body'], '\n    hoge\n    \n    hoge')
