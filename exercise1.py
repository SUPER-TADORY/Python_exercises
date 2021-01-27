from numpy import sqrt
l=list()
while 1:
    try:
       l.append(input())
    except EOFError :
        break
l=list(map(int,l))
sum_=sum(l)
mean=sum_/len(l)
l_=[(x-mean)**2 for x in l]
sd=sqrt(sum(l_)/(len(l_)-1))
print(f'sum\t[{sum_}]')      
print(f'mean\t[{mean:.03f}]')
print(f'sd\t[{sd:.03f}]')
