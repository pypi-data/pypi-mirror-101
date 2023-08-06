# python-loggz

A helper to implement simple but standard and jsonified strategies for logging.

## Table of Contents

* [Synopsis](#synopsis)
* [Usage](#usage)
* [Installation](#installation)
* [Build](#build)
* [Tests](#tests)
* [Compatibility](#compatibility)
* [Issues](#issues)
* [Contributing](#contributing)
* [Credits](#credits)
* [Resources](#resources)
* [History](#history)
* [License](#license)

## <a name="synopsis">Synopsis</a>

A helper to implement simple but standard and jsonified strategies for logging.

## <a name="usage">Usage</a>

```python

import loggz

loggz.setup() # Initialize logging using default settings

LOG = loggz.factory('root') # Get the logger named `root`

# Add an info log including extra values...
LOG.info('Values', extra={'values': [1, 2, 3, 5, 8, 13, 2]})

```

## <a name="installation">Installation</a>

```bash
pip3 install loggz
```

## <a name="build">Build</a>

```bash
python3 setup.py build
```

## <a name="tests">Tests</a>

```bash
python3 setup.py test
```


## <a name="compatibility">Compatibility</a>

Tested using [Python 3.7](https://docs.python.org/3/whatsnew/3.7.html).

## <a name="issues"> Issues</a>

Feel free to [submit issues](https://github.com/deepnox-io/python-deepnox-log/issues) and enhancement requests.

## <a name="contributing">Contributing</a>

Please refer to project's style guidelines and guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

**NOTE**: Be sure to merge the latest from "upstream" before making a pull request!

## <a name="credits">Credits</a>

Thank you very much to this used or integrated open source developments:

* [Israel FL](https://github.com/israel-fl/python3-logstash/tree/master/logstash) for the [JSON Formatter](https://github.com/israel-fl/python3-logstash/blob/master/logstash/formatter.py).
    * MIT License (MIT), Copyright (c) 2018, Israel Flores.

## <a name="resources">Resources</a>

* [Making a Python package](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)

## <a name="history">History</a>

Please refer to [the changelog file](CHANGELOG.md).

## <a name="license">License</a>

>
> [The MIT License](https://opensource.org/licenses/MIT)
>
> Copyright (c) 2021 [Deepnox SAS](https://deepnox.io/), Paris, France.
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
>AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.
>
