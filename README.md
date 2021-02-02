Titech Lecture Recommendation System
===

# Requirements
Python 3.9

# Installation
### Python Modules
```console
$ pip -r install requirements.txt
```

### MeCab
```console
$ brew install mecab
$ brew install mecab-ipadic
$ git clone https://github.com/neologd/mecab-ipadic-neologd.git
$ mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n
$ rm -r mecab-ipadic-neologd
```

### WordNet
```console
$ make download
```
