import sys
import multiprocessing

def is_prime(num):
	if num <= 1:
		return False
	else:
		for i in range(2,num):
			if (num % i) == 0: return False
		return True

begin = int(sys.argv[1])
end = int(sys.argv[2])
pool = multiprocessing.Pool(processes=4)
results = [pool.apply_async(is_prime, args=(x,)) for x in range(begin,end+1)]
output = [p.get() for p in results]
print(output)
