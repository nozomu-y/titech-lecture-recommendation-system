main:
	python3 GUI/main.py

kg:
	python3 Koginator/koginator.py

fs:
	python3 FeatureSearch/feature_search.py

ks:
	python3 Clustering/main.py

download:
	curl http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz --output "Clustering/wnjpn.db.gz"
	gzip -d Clustering/wnjpn.db.gz