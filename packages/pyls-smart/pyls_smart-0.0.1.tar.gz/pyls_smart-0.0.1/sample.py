import sys

sample=['one', 'two', 'three']
# print(*sample)

if sys.stdout.isatty():
    print(*sample)
elif not sys.stdout.isatty():
    for i in sample:
        print(i)