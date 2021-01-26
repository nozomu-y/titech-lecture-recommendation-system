# version
python: 3.9

# package
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

## mecab-ipadicのインストール
```bash
brew install mecab
brew install mecab-ipadic
git clone https://github.com/neologd/mecab-ipadic-neologd.git
mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n
rm -r mecab-ipadic-neologd
```
## wnjpn.dbのダウンロード
```bash
curl http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz --output "Clustering/wnjpn.db.gz"
gzip -d Clustering/wnjpn.db.gz
```

# アプリケーションの実行
## GUI
```bash
make main
```
## キーワード検索
```bash
make ks
```
## 特徴量検索
```bash
make fs
```
## コギネーター
```bash
make kg
```