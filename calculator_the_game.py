import sys
import re


puzzles = [
    # level, start, goal, keys
    (70, 7, 81, ['-9', 'x3', '+4', '+/-', 'R']),
    (71, 0, -43, ['-5', '+7', '-9', 'R']),
    (72, 0, 28, ['+6', '-3', 'R', '<<']),
    (73, 0, 136, ['1', '+2', 'x3', 'R']),
    (74, 0, -1, ['+5', 'R', '+/-']),
    (75, 0, -25, ['+4', 'x3', 'R', '+/-']),
    (76, 0, -5, ['+7', 'x3', 'R', '+/-']),
    (77, 88, 41, ['/4', '-4', 'R']),
    (78, 100, 101, ['0', 'x2', '2=>10', 'R', '0=>1']),
    (79, 0, 424, ['/2', '5', '5=>4', 'R']),
    (80, 99, 100, ['9', '/9', 'R', '1=>0']),
    (81, 8, 30, ['2', '-4', '2=>3', 'R']),
    (82, 101, 222, ['-1', 'R', '0=>2']),
    (83, 36, 500, ['x4', '/3', '1=>5', 'R']),
    (84, 0, 196, ['1', '+12', 'x13', 'R', '<<']),
    (85, 50, 101, ['1=>10', '+50', 'R', '5=>1']),
    (86, 1, 2048, ['2', 'x4', 'x10', 'R']),
    (87, 12, 123, ['12', '+1', '12=>2', 'R']),
    (88, 86, 55, ['+2', '+14', 'R', '0=>5']),
    (89, 0, 3, ['1', 'S']),
    (90, 1231, 4, ['S', '3=>1', '2=>3']),
    (91, 0, 45, ['x9', '4', 'x3', '3=>5', 'S']),
    (92, 424, 28, ['x4', '4=>6', 'S']),
    (93, 3, 8, ['3', '+33', 'S', '3=>1']),
    (94, 24, 44, ['/2', '4', '1=>2', 'S']),
    (95, 142, 143, ['x9', '+9', '44=>43', 'S']),
    (96, 24, 1, ['/3', 'x4', '5=>10', 'S']),
    (97, 4, 100, ['3', 'x3', '+1', 'S']),
    (98, 93, 8, ['+4', 'x3', 'S']),
    (99, 5, 16, ['x5', '/2', 'S', '5=>2']),
    (100, 128, 64, ['x4', '/4', 'S', '5=>16']),
]


def I(v):
    v = str(v)
    if '.' in v:
        v = v.rstrip('0').rstrip('.')
    return int(v)


# these lambda's are a crime against humanity and should be broken out into actual functions
key_funcs = [
    (r'^[0-9]+$', lambda x, v: int(str(I(v)) + x)),
    (r'^[+-][1-9][0-9]*$', lambda x, v: v + int(x)),
    (r'^\+/-$', lambda x, v: -v),
    (r'^x[1-9][0-9]*$', lambda x, v: v * int(x[1:])),
    (r'^/[1-9][0-9]*$', lambda x, v: v / int(x[1:])),
    (r'^R$', lambda x, v: int(str(abs(I(v)))[::-1]) * (1 if v > 0 else -1)),
    (r'^<<$', lambda x, v: int(str(I(v))[:-1]) if abs(v) > 9 else 0),
    (r'[0-9]+=>[0-9]+', lambda x, v: int(str(I(v)).replace(*x.split('=>')))),
    (r'^S$', lambda x, v: sum(int(i) for i in str(I(v)))),
]


def get_key(key):
    for r, f in key_funcs:
        if re.match(r, key):
            def bob(v):
                try:
                    return f(key, v)
                except Exception:
                    return 'err'
            return bob
    assert False


def solve(start, goal, keys):
    keys = [(key, get_key(key)) for key in keys]
    state = [(start, [])]

    while True:
        value, moves = state.pop(0)
        assert len(moves) < 7
        for key, func in keys:
            new_value = func(value)
            new_moves = moves + [key]
            if new_value == goal:
                return new_moves
            # print(new_moves, value, new_value)
            state.append((new_value, new_moves))


def main(argv):
    for level, start, goal, keys in puzzles:
        print(level, solve(start, goal, keys))


if __name__ == "__main__":
    main(sys.argv)
