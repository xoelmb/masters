import sys
def is_prime(num):
	if num <= 1:
		return False
	else:
		for i in range(2,num):
			if (num % i) == 0: return False
		return True
begin=int(sys.argv[1])
end=int(sys.argv[2])
for n in range(begin,end):
	if is_prime(n): print(n)

