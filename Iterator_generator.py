class multifilter:
    def judge_half(pos, neg):  # допускает элемент, если его допускает хотя бы половина фукнций (pos >= neg)
        if pos >= neg: return True

    def judge_any(pos, neg):  # допускает элемент, если его допускает хотя бы одна функция (pos >= 1)
        if pos >= 1: return True

    def judge_all(pos, neg):  # допускает элемент, если его допускают все функции (neg == 0)
        if neg == 0: return True

    def __init__(self, iterable, *funcs, judge=judge_any):  # iterable - исходная последовательность, funcs - допускающие функции. judge - решающая функция
        self.iterable = iterable
        all_funcs = [i for i in funcs]
        print(all_funcs)
        posit, negat = 0, 0
        """for i in self.iterable:
            for j in funcs:
                if j(i) is True:
                    posit += 1
                else:
                    negat += 1
            print("i:", i, "; pos:", posit, "; neg:", negat)
        if self.judje(posit, negat):
            yield i"""
    def __iter__(self):  # возвращает итератор по результирующей последовательности
        for i in self.iterable:
            for j in self.all_funcs:
                if j(i) is True:
                    posit += 1
                else:
                    negat += 1
            print("i:", i, "; pos:", posit, "; neg:", negat)
        if self.judje(posit, negat):
            yield self.i

def mul2(x):
        return x % 2 == 0
def mul3(x):
        return x % 3 == 0
def mul5(x):
        return x % 5 == 0
a = [i for i in range(31)]  # [0, 1, 2, ... , 30]
print(a)
print(list(multifilter(a, mul2, mul3, mul5)))  # [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
#print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half)))  # [0, 6, 10, 12, 15, 18, 20, 24, 30]
#print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all)))  # [0, 30]
