from collections import namedtuple
from typing import Callable, Match, Union, List, Dict

TokenAttributes = Dict[str, Union[str, List[str]]]

BlockToken = namedtuple(
  'BlockToken',
  field_names=[
    'name',
    'body',
    'attributes',
  ],
)

InlineToken = namedtuple(
  'InlineToken',
  field_names=[
    'name',
    'value',
    'attributes',
  ],
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
