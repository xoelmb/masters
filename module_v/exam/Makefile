target= target.txt

all : $(target)

file.txt:

	echo "ONE LINE" > file.txt

$(target): file.txt

	echo "THE END" > file_aux.txt ;  cat $<  file_aux.txt > $@

clean:

	echo "Cleaning up"

	-rm *.txt