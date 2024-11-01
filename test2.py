def chuangjian():
    path = "C:/Users/zhangzhenyan/Desktop/"
    for num in range(1, 11):
        filename = f'{num}.txt'
        file = open(path + filename, 'w')
        file.write(f'this is a samplefile Number {num}')
        file.close()


cj = chuangjian()
