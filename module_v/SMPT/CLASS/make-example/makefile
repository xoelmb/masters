all: resut
results.txt: isles.data abyss.data
	python testzipf.py $^ > results.txt
isles.data: books/isles.txt
	python countwords.py $^ isles.data
abyss.data: books/abyss.txt
	python countwords.py $^ abyss.data

