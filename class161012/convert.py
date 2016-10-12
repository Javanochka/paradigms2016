def convert(n, base=2):
    if not n:
        return [0]
    ans = []
    while n:
        ans.append((n % base))
        n //= base
    return list(reversed(ans))


def to_dec(lis, base=2):
    ans = 0
    for t in lis:
        ans *= base
        ans += t
    return ans
