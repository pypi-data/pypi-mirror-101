import json
from unittest import TestCase

from pathlib import Path

from geneeanlpclient.common.dictutil import JsonType
from geneeanlpclient.g3.reader import _buildOffsetMapping
from geneeanlpclient.g3 import UDep, fromDict, toDict

from tests.geneeanlpclient.g3 import examples


class TestRW(TestCase):

    @staticmethod
    def _replaceClauseByRoot(dictG3: JsonType) -> None:
        """
        Utility class to replace all 'clause' functions in tokens by 'root'. Readers replace clause by root.
        Clause is a deprecated non-UD function, equivalent to root.
        """

        for para in dictG3.get('paragraphs', []):
            for sentence in para.get('sentences', []):
                for token in sentence.get('tokens', []):
                    if token.get('fnc') == 'clause':
                        token['fnc'] = 'root'

    def test_read_write(self):
        self.maxDiff = None

        examplesPath = Path(__file__).parent / 'examples'
        exampleFiles = list(examplesPath.glob('example*.json'))
        self.assertEqual(127, len(exampleFiles))

        for exampleFile in exampleFiles:
            with exampleFile.open(encoding='utf8') as file:
                obj = fromDict(json.load(file))

            actual = toDict(obj)

            with exampleFile.open(encoding='utf8') as file:
                expected = json.load(file)
                if expected.get('itemSentiments') == {}:
                    del expected['itemSentiments']
                TestRW._replaceClauseByRoot(expected)

            self.assertDictEqual(expected, actual)

    def test_tokens(self):
        obj = examples.example_full_obj()

        token0 = obj.paragraphs[0].sentences[0].tokens[0]  # Angela

        self.assertEqual(token0._id, 'w0')
        self.assertEqual(token0.text, 'Angela')
        self.assertEqual(token0.charSpan.start, 0)
        self.assertEqual(token0.charSpan.end, 6)
        self.assertEqual(token0.origText, 'Angela')
        self.assertEqual(token0.origCharSpan.start, 0)
        self.assertEqual(token0.origCharSpan.end, 6)
        self.assertEqual(token0.deepLemma, 'Angela')
        self.assertEqual(token0.lemma, None)  # missing
        self.assertEqual(token0.morphTag, 'NNP')
        self.assertEqual(token0.fnc, UDep.COMPOUND)
        self.assertEqual(token0.feats, {"negated": "false"})

        self.assertEqual(token0.parent.text, 'Merkel')
        self.assertEqual(token0.children, [])
        self.assertEqual(token0.previous(), None)
        self.assertEqual(token0.next().text, 'Merkel')

    def test_tecto(self):
        obj = examples.example_full_obj()

        d0 = obj.paragraphs[0].sentences[0].tectoTokens[0]  # root
        d1 = obj.paragraphs[0].sentences[0].tectoTokens[1]  # Angela Merkel
        w0 = obj.paragraphs[0].sentences[0].tokens[0]  # Angela
        w1 = obj.paragraphs[0].sentences[0].tokens[1]  # Merkel

        self.assertEqual(d1._id, 'd1')
        self.assertEqual(d1.lemma, 'Angela Merkel')
        self.assertEqual(d1.parent, d0)
        self.assertEqual(d1.fnc, 'clause')
        self.assertEqual(d1.tokens.tokens, [w0, w1])

    def test_orig_corr_text(self):
        examplesPath = Path(__file__).parent / 'examples'

        def test(toks):
            self.assertEqual(toks[3].text, 'chybí')
            self.assertEqual(toks[3].charSpan.start, 13)
            self.assertEqual(toks[3].charSpan.end, 18)
            self.assertEqual(toks[3].origText, 'chybý')
            self.assertEqual(toks[3].origCharSpan.start, 13)
            self.assertEqual(toks[3].origCharSpan.end, 18)
            self.assertEqual(toks[4].text, 'nové')
            self.assertEqual(toks[4].charSpan.start, 19)
            self.assertEqual(toks[4].charSpan.end, 23)
            self.assertEqual(toks[4].origText, 'nové')
            self.assertEqual(toks[4].origCharSpan.start, 19)
            self.assertEqual(toks[4].origCharSpan.end, 23)
            self.assertEqual(toks[5].text, 'alba')
            self.assertEqual(toks[5].charSpan.start, 24)
            self.assertEqual(toks[5].charSpan.end, 28)
            self.assertEqual(toks[5].origText, 'albumy')
            self.assertEqual(toks[5].origCharSpan.start, 24)
            self.assertEqual(toks[5].origCharSpan.end, 30)
            self.assertEqual(toks[6].text, '🤣')
            self.assertEqual(toks[6].charSpan.start, 29)
            self.assertEqual(toks[6].charSpan.end, 30)
            self.assertEqual(toks[6].origText, '🤣')
            self.assertEqual(toks[6].origCharSpan.start, 31)
            self.assertEqual(toks[6].origCharSpan.end, 32)
            self.assertEqual(toks[7].text, '.')
            self.assertEqual(toks[7].charSpan.start, 30)
            self.assertEqual(toks[7].charSpan.end, 31)
            self.assertEqual(toks[7].origText, '.')
            self.assertEqual(toks[7].origCharSpan.start, 32)
            self.assertEqual(toks[7].origCharSpan.end, 33)

        with (examplesPath / 'example_TOKENS.json').open(encoding='utf8') as file:
            withOrig = json.load(file)

        obj = fromDict(withOrig)
        test(obj.paragraphs[0].sentences[0].tokens)

        with (examplesPath / 'G3v311_example_TOKENS.json').open(encoding='utf8') as file:
            withCorr = json.load(file)

        obj = fromDict(withCorr)
        test(obj.paragraphs[0].sentences[0].tokens)

        self.assertDictEqual(withOrig, toDict(obj))

    def test_codepoint_offsets(self):
        examplesPath = Path(__file__).parent / 'examples'

        def test(toks):
            self.assertEqual(toks[1].text, '🐦🎾')
            self.assertEqual(toks[1].charSpan.start, 2)
            self.assertEqual(toks[1].charSpan.end, 4)
            self.assertEqual(toks[2].text, 'obchodě')
            self.assertEqual(toks[2].charSpan.start, 5)
            self.assertEqual(toks[2].charSpan.end, 12)
            self.assertEqual(toks[3].text, 'chybí')
            self.assertEqual(toks[3].charSpan.start, 13)
            self.assertEqual(toks[3].charSpan.end, 18)
            self.assertEqual(toks[4].text, 'nové')
            self.assertEqual(toks[4].charSpan.start, 19)
            self.assertEqual(toks[4].charSpan.end, 23)
            self.assertEqual(toks[5].text, 'alba')
            self.assertEqual(toks[5].charSpan.start, 24)
            self.assertEqual(toks[5].charSpan.end, 28)
            self.assertEqual(toks[6].text, '🤣')
            self.assertEqual(toks[6].charSpan.start, 29)
            self.assertEqual(toks[6].charSpan.end, 30)
            self.assertEqual(toks[7].text, '.')
            self.assertEqual(toks[7].charSpan.start, 30)
            self.assertEqual(toks[7].charSpan.end, 31)

        with (examplesPath / 'example_TOKENS.json').open(encoding='utf8') as file:
            withCodepoint = json.load(file)

        obj = fromDict(withCodepoint)
        test(obj.paragraphs[0].sentences[0].tokens)

        with (examplesPath / 'G3v320_example_TOKENS.json').open(encoding='utf8') as file:
            notCodepoint = json.load(file)

        obj = fromDict(notCodepoint)
        test(obj.paragraphs[0].sentences[0].tokens)

        self.assertDictEqual(withCodepoint, toDict(obj))


class TestOffsetMapping(TestCase):

    def test_buildOffsetMapping(self):
        self.assertIsNone(_buildOffsetMapping('ASCII text'))

        text = '>> 🐦 Xňž … 👩🏻🎓 <<'
        offs = _buildOffsetMapping(text)
        self.assertListEqual([
            0,1,2,3,3,4,5,6,7,8,9,10,11,11,12,12,13,13,14,15,16,17
        ], offs)
