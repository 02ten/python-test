def pr8():
    lst = [ 0, 8, 5, 20, 14, 20, 317, 20 ]
    print(lst)
    lst[lst.index(20)] = 200
    print(lst)

    lst = [ "", "str", "1234", "", "", "qwerty" ]
    print(lst)
    lst = list(filter(None, lst))
    print(lst)

    lst = [ 5, 14, -8, 234, 1 ]
    print(lst)
    lst = [ x ** 2 for x in lst ]
    print(lst)

    lst = [ 0, 8, 5, 20, 14, 20, 317, 20 ]
    print(lst)
    lst = [ x for x in lst if (x != 20) ]
    print(lst)

if __name__ == '__main__':
    pr8()