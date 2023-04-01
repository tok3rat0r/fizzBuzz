import multiprocessing
import string
from math import pi, sin

from timer import timer


@timer
def fizzbuzz_original(n: int) -> list[str]:
    result = []
    for i in range(1, n+1):
        if i % 15 == 0:
            result.append('FizzBuzz')
        elif i % 5 == 0:
            result.append('Buzz')
        elif i % 3 == 0:
            result.append('Fizz')
        else:
            result.append(str(i))
    return result


def fb_single(i: int) -> str:
    if i % 15 == 0:
        return 'FizzBuzz'
    elif i % 5 == 0:
        return 'Buzz'
    elif i % 3 == 0:
        return 'Fizz'
    else:
        return str(i)


@timer
def fizzbuzz_map(n: int) -> list[str]:
    return list(map(fb_single, range(1, n+1)))


@timer
def fizzbuzz_parallel(n: int, p: int) -> list[str]:
    with multiprocessing.Pool(p) as pool:
        result = pool.map(fb_single, range(1, n+1))
    return result


@timer
def fizzbuzz_chunks(n: int) -> list[str]:
    result = []
    i = 1
    while len(result) < n:
        chunk = [
            str(i), str(i+1), "Fizz", str(i+3), "Buzz",
            "Fizz", str(i+6), str(i+7), "Fizz", "Buzz",
            str(i+10), "Fizz", str(i+12), str(i+13), "FizzBuzz"
        ]
        result += chunk
        i += 15
    return result[:n]


@timer
def fizzbuzz_counter(n: int) -> list[str]:
    result = []
    i, j, k = 1, 1, 1
    while i <= n:
        if j == 3 and k == 5:
            result.append("FizzBuzz")
            j, k = 0, 0
        elif k == 5:
            result.append("Buzz")
            k = 0
        elif j == 3:
            result.append("Fizz")
            j = 0
        else:
            result.append(str(i))
        i += 1
        j += 1
        k += 1
    return result


@timer
def fizzbuzz_sets(n: int) -> list[str]:
    result = []
    set3 = {3*i for i in range(1, n//3+1)}
    set5 = {5*i for i in range(1, n//5+1)}
    set15 = set3.intersection(set5)
    for i in range(1, n+1):
        if i in set15:
            result.append("FizzBuzz")
        elif i in set5:
            result.append("Buzz")
        elif i in set3:
            result.append("Fizz")
        else:
            result.append(str(i))
    return result


@timer
def fizzbuzz_dict(n: int) -> list[str]:
    d = {
        "Fizz": {3*i for i in range(1, n//3+1)},
        "Buzz": {5*i for i in range(1, n//5+1)}
    }
    return [
        sorted(
            [str(i), ''.join(sorted([k for k, v in d.items() if i in v], reverse=True))],
            reverse=True
        )[0]
        for i in range(1, n+1)
    ]


@timer
def fizzbuzz_bases(n: int) -> list[str]:
    def dec2base(x: int, base: int) -> str:  # Valid for x >= 0, base <= 36
        chars = string.digits + string.ascii_letters
        if x == 0:
            return chars[0]
        digits = []
        while x:
            digits.append(chars[x % base])
            x = x // base
        digits.reverse()
        return ''.join(digits)

    result = []
    for i in range(1, n+1):
        if dec2base(i, 15)[-1] == "0":
            result.append("FizzBuzz")
        elif dec2base(i, 5)[-1] == "0":
            result.append("Buzz")
        elif dec2base(i, 3)[-1] == "0":
            result.append("Fizz")
        else:
            result.append(str(i))
    return result


@timer
def fizzbuzz_digits(n: int) -> list[str]:
    def recursive_digit_sum(k: int) -> int:
        str_k = str(k)
        if len(str_k) == 1:
            return k
        else:
            sum_digits = sum([int(d) for d in str_k])
            return recursive_digit_sum(sum_digits)

    result = []
    for i in range(1, n+1):
        i_str = str(i)
        dig_add = recursive_digit_sum(i)
        if dig_add in {3, 6, 9} and i_str[-1] in {'0', '5'}:
            result.append('FizzBuzz')
        elif i_str[-1] in {'0', '5'}:
            result.append('Buzz')
        elif dig_add in {3, 6, 9}:
            result.append('Fizz')
        else:
            result.append(i_str)
    return result


@timer
def fizzbuzz_sine(n: int) -> list[str]:
    result = []
    domain = range(1, n+1)
    absine3 = [abs(sin(k*pi/3)) for k in domain]
    absine5 = [abs(sin(k*pi/5)) for k in domain]
    for i in domain:
        if absine3[i-1] < 0.5 and absine5[i-1] < 0.5:
            result.append("FizzBuzz")
        elif absine5[i-1] < 0.5:
            result.append("Buzz")
        elif absine3[i-1] < 0.5:
            result.append("Fizz")
        else:
            result.append(str(i))
    return result


if __name__ == '__main__':
    z = 99999
    fb_ori = fizzbuzz_original(z)
    fb_map = fizzbuzz_map(z)
    assert fb_map == fb_ori
    fb_par = fizzbuzz_parallel(z, 8)
    assert fb_par == fb_ori
    fb_chu = fizzbuzz_chunks(z)
    assert fb_chu == fb_ori
    fb_cou = fizzbuzz_counter(z)
    assert fb_cou == fb_ori
    fb_set = fizzbuzz_sets(z)
    assert fb_set == fb_ori
    fb_dic = fizzbuzz_dict(z)
    assert fb_dic == fb_ori
    fb_bas = fizzbuzz_bases(z)
    assert fb_bas == fb_ori
    fb_dig = fizzbuzz_digits(z)
    assert fb_dig == fb_ori
    fb_sin = fizzbuzz_sine(z)
    assert fb_sin == fb_ori
