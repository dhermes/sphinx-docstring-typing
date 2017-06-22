# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import mock
import pytest

import sphinx_docstring_typing


def process_sphinx_input(input_):
    app = mock.Mock(spec=['warn', 'verbose'])
    app.warn.side_effect = print
    app.verbose.side_effect = print

    lines = input_[::]
    sphinx_docstring_typing.autodoc_process_docstring(
        app, None, None, None, None, lines)

    return lines


@pytest.mark.parametrize('input_,expected', [
    (['Any'],
     [':py:obj:`~typing.Any`']),
    (['Sequence[int]'],
     [':py:obj:`~typing.Sequence` [ :py:obj:`int` ] ']),
    (['Tuple[int, int]'],
     [':py:obj:`~typing.Tuple` [ :py:obj:`int`, :py:obj:`int` ] ']),
    (['Sequence[int, List[str]]'],
     [':py:obj:`~typing.Sequence` [ :py:obj:`int`, :py:obj:`~typing.List` '
      '[ :py:obj:`str` ]  ] ']),
    (['Tuple[int,...]'],
     [':py:obj:`~typing.Tuple` [ :py:obj:`int`, ... ] ']),
    (['blah blah Sequence[int] blah blah'],
     ['blah blah :py:obj:`~typing.Sequence` [ :py:obj:`int` ]  blah blah']),
    (['Mapping[str, Any]'],
     [':py:obj:`~typing.Mapping` [ :py:obj:`str`, :py:obj:`~typing.Any` ] ']),
    (['Optional[datetime]'],
     [':py:obj:`~typing.Optional` [ :py:obj:`datetime` ] ']),
    (['*Optional[datetime]*'],
     [':py:obj:`~typing.Optional` [ :py:obj:`datetime` ] ']),
])
def test_autodoc_process_docstring(input_, expected):
    lines = process_sphinx_input(input_)
    assert lines != input_
    assert lines == expected


def test_autodoc_process_target():
    input_ = [
        '        In addition ``include_syntax`` adds a feature that analyzes',
        '        the document for semantic and syntactic information.',
        '',
        '        .. note::',
        '',
        '            This is intended for users who are familiar with machine',
        '            learning and need in-depth text features to build upon.',
        '',
        '        .. _annotateText: https://link.com',
        '',
        '        See `annotateText`_.',
    ]
    transformed = process_sphinx_input(input_)
    # There should be nothing to modify here.
    assert transformed == input_


def test_autodoc_process_class_refs():
    input_ = [
        'TextAnnotation contains a structured representation of OCR extracted',
        ('  text. The hierarchy of an OCR extracted text '
         'structure is like this:'),
        ('  TextAnnotation -> Page -> Block -> Paragraph -> Word '
         '-> Symbol Each'),
        ('  structural component, starting from Page, may further '
         'have their own'),
        ('  properties. Properties describe detected languages, '
         'breaks etc.. Please'),
        '  refer to the',
        ('  [google.cloud.vision.v1.TextAnnotation.TextProperty]'
         '[google.cloud.vision.v1.TextAnnotation.TextProperty]'),
        '  message definition below for more detail.',
    ]
    transformed = process_sphinx_input(input_)
    # There should be nothing to modify here.
    assert transformed == input_
