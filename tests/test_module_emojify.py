''' test bobbit.bot '''

import unittest
import sys

sys.path.insert(0, 'src')

from   src.bobbit.modules.emojify import get_emoji_match

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
            '🌳': 2,
            '🌲': 2,
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
            'bigtree': None,           # not in table
            'is': None,                # common words are excluded
        }

        for word, expected in cases.items():
            res = await get_emoji_match(self.dummy_table, word)

            if expected is None:
                self.assertIsNone(res)
            else:
                self.assertIn(res, expected)    

if __name__ == '__main__':
    unittest.main()