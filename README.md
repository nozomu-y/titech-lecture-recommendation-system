# version
python: 3.9

# module
```bash
python3 -m pip install PyQt5
python3 -m pip install natto-py
python3 -m pip install mecab
python3 -m pip install pandas
python3 -m pip install json
python3 -m pip install sklearn
python3 -m pip install numpy
```
# setup

## install mecab-ipadic
```bash
brew install mecab
brew install mecab-ipadic
git clone https://github.com/neologd/mecab-ipadic-neologd.git
mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n
rm -r mecab-ipadic-neologd
```
## download wnjpn.db
```bash
# at TLRS(TitechLectureResearchSystem) directory
curl http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz --output "Clustering/wnjpn.db.gz"
gzip -d Clustering/wnjpn.db.gz
```

# exec application
## GUI
```bash
# at TLRS directory
make main
```
## keyword search
```bash
# at TLRS directory
make ks
```
## feature search
```bash
# at TLRS directory
make fs
```
## koginator
```bash
# at TLRS directory
make kg
```