def invest(amount,rate,time):
    rate = rate / 100
    print(f'principal amount:{amount}')
    for n in range(1,time+1):
        value = round(amount*(1+rate)**n , 2)
        #value2 = round(value, 2)
        print(f'year {n}: ${value}')
fuli = invest(100 , 5 , 8)

