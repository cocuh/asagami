from typing import Dict, List, Union

from collections import namedtuple

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
