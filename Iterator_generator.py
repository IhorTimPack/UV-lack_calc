class multifilter:
    def judge_half(pos, neg):  # допускает элемент, если его допускает хотя бы половина фукнций (pos >= neg)
        if pos >= neg: return True
    def judge_any(pos, neg):  # допускает элемент, если его допускает хотя бы одна функция (pos >= 1)
        if pos >= 1: return  True
    def judge_all(pos, neg):  # допускает элемент, если его допускают все функции (neg == 0)
        if neg == 0: return True
    def __init__(self, iterable, *funcs, judge=judge_any):
        self.iterable = iterable
        pos, neg = 0, 0
        for i in self.iterable:
            for j in funcs:
                print(i, end=" ",)
                print(j[i])
                if j[i] is True:
                    self.pos += 1
                    print("pos", self.pos)
                else:
                    self.neg += 1
                    print("neg", self.neg)

        # iterable - исходная последовательность
        # funcs - допускающие функции
        # judge - решающая функция
    def __iter__(self):
        return self
        # возвращает итератор по результирующей последовательности
def mul2(x):
        return x % 2 == 0
def mul3(x):
        return x % 3 == 0
def mul5(x):
        return x % 5 == 0
a = [i for i in range(31)]  # [0, 1, 2, ... , 30]
print(a)
print(list(multifilter(a, mul2, mul3, mul5)))  # [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
print("111")
print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half)))  # [0, 6, 10, 12, 15, 18, 20, 24, 30]
print("222")
print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all)))  # [0, 30]
print("333")