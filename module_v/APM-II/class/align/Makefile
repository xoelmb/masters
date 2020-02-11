CC=gcc # icpc
C_FILES=dp_table.c
 
OBJ_FILES=$(C_FILES:.c=.o)
LD_FLAGS=-lm -lrt
CC_FLAGS=-Wall -g -Ofast

all: alignC generate_datasets

alignC: $(OBJ_FILES) alignC.c
	$(CC) $(CC_FLAGS) alignC.c $(OBJ_FILES) -o alignC $(LD_FLAGS)
	
generate_datasets: $(OBJ_FILES) generate_datasets.c
	$(CC) $(CC_FLAGS) generate_datasets.c -o generate_datasets $(LD_FLAGS)
	
%.o: %.c
	$(CC) $(CC_FLAGS) -c -o $@ $< 

clean:
	rm -rf alignC generate_datasets *.o
