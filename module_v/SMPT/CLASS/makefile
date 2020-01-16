.PHONY: all clean
all: step_2.txt
	@echo "Workflow completed"
step_1.txt:
	echo “STEP ONE” > step_1.txt
step_2.txt: step_1.txt
	echo "STEP TWO" >> step_2.txt
clean:
	-rm step_*.txt
