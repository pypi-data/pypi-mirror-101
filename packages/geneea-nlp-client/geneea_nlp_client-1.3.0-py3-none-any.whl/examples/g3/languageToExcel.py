# Copyright 2019 Geneea Analytics s.r.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Analyzes a plain text file (one document per line) and saves the language of the document to an excel file using pandas.

call as

```
python languageToExcel.py -i input.txt -o output.xlsx

```

or

```
python languageToExcel.py -o output.xlsx < input.txt
```
"""
import argparse
import sys

from typing import Tuple, Iterable, TextIO

from geneeanlpclient import g3

import pandas as pd

USER_KEY = None    # fill your API key here (or define it as env variable, and remove as a parameter in create)


def getLanguage(file: TextIO) -> Iterable[Tuple[str, str]]:
    requestBuilder = g3.Request.Builder(
        analyses=[g3.AnalysisType.LANGUAGE],
    )

    with g3.Client.create(userKey=USER_KEY) as analyzer:
        for idx, text in enumerate(file):
            result = analyzer.analyze(requestBuilder.build(id=str(idx), text=text))
            l = result.language
            yield result.docId, l.detected


def main(args):
    print('USER_KEY', USER_KEY, file=sys.stderr)

    with open(args.input, encoding='utf8') if args.input else sys.stdin as file:
        records = getLanguage(file)

        df = pd.DataFrame(records, columns=['docId', 'language'])
        writer = pd.ExcelWriter(args.output, engine='xlsxwriter')
        df.to_excel(writer, index=False, header=True)
        writer.save()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--input", help="Input file, one text per line in utf8")
    argparser.add_argument("-o", "--output", required=True, help="The resulting excel file; columns: docId, language")
    main(argparser.parse_args())
