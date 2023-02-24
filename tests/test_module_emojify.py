''' test emojify '''

import unittest
import sys

sys.path.insert(0, 'src')

from src.bobbit.modules import emojify

# Test Cases

class EmojifyTestCase(unittest.IsolatedAsyncioTestCase):
    dummy_table = {
        'dog': {
            '🐕': 5,
            '🐶': 5,
            '🌭': 1
        },
        'cat': {
            '🐈': 3,
            '🐱': 1
        },
        'tree': {
            '🌴': 2,
            '🎄': 1
        },
        'ball': {
            '🏀': 1
        }
    }
    
    async def test_00_get_emoji_match(self):
        cases = {
            'dog': ['🐕','🐶','🌭'], # basic functionality
            'CAT': ['🐈','🐱'],       # test ignore-case
            'tree': ['🌴','🎄'],      # test ignoring punctuation
            'bigtree': None,           # not in table
            'is': None,                # common words are excluded
        }

        for word, expected in cases.items():
            res = emojify.get_emoji_match(self.dummy_table, word)

            if expected is None:
                self.assertIsNone(res)
            else:
                self.assertIn(res, expected)

    async def test_01_add_emojis(self):
        cases = {
            'ball so hard': ['ball 🏀 so hard'],
            'nothing to see here': ['nothing to see here'],
            'raining cat and dog': (f'raining cat {c} and dog {d}'
                                        for c in self.dummy_table['cat']
                                        for d in self.dummy_table['dog'])
        } 

        for text, expected in cases.items():
            self.assertIn(emojify.add_emojis(text, self.dummy_table), expected)

if __name__ == '__main__':
    unittest.main()