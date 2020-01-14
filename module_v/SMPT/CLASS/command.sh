sbatch --job-name=xoel --nodes=1 --partition=research.q --wrap "echo 'I have written a submit script' > text.txt; sleep 30; ls"
