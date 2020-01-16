.PRECIOUS: %.data
objects = prot01.txt prot02.txt prot03.txt

all: $(objects)

%.txt: my_command.sh %.data
	bash $^ > $@

%.data:
	echo "My data" > $@
	
clean:
	@echo "Cleaning up"
	-rm *.txt
	-rm *.data
 
