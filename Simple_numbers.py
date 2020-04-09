num = int(input())
for j in range(2, num+1):
    print(j)
    check = 0
    for i in range(2,num+1):
        print("num:", num, "j:", j, "i:", i)
        if num % i == 0 and check < 2:
            check += 1
            ##print("num:", num, "i:", i, "check:", check)
        elif num % i == 0:
            check += 1
            break
        else:
            continue
    if check <= 2:
        print("Это простое число:", j)