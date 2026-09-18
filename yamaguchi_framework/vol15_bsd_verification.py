# Yamaguchi Framework 第十五巻 付録C 再現コード
# BSD: 中心零点の位数と先頭係数の数値検証 (Python 3 + mpmath)
#
# 出力:
#   定理2 — 4 曲線の ε・L(1)・L'(1)・L''(1)・L'''(1) と位数の読み出し
#   定理3 — 実周期 Ω・正準高さ・レギュレータによる BSD 先頭係数の検証
#
# 注意 (誠実性):
#   - Lderiv_k(k) は下位の導値が全て消えることを仮定した式である (本文 §2)。
#   - 正準高さは naive height の 2^n 倍点極限 (n = 8) であり、誤差 O(4^-n)。
#   - 数値の零 (|L| < 10^-30 等) は零の証明ではない (本文 定理4)。

import itertools
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 30

# (Cremona ラベル, [a1,a2,a3,a4,a6], 導手 N, 既知の Mordell–Weil 階数, 生成点)
CURVES = [
    ("11a1",   (0, -1, 1, -10, -20),   11, 0, []),
    ("37a1",   (0,  0, 1,  -1,   0),   37, 1, [(0, 0)]),
    ("389a1",  (0,  1, 1,  -2,   0),  389, 2, [(0, 0), (-1, 1)]),
    ("5077a1", (0,  0, 1,  -7,   6), 5077, 3, [(-2, 3), (-1, 3), (0, 2)]),
]

# ---- a_p: F_p 上の点の勘定 --------------------------------------------------
def sieve_primes(n):
    s = bytearray([1]) * (n + 1); s[0:2] = b"\x00\x00"
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = b"\x00" * len(s[i * i::i])
    return [i for i in range(n + 1) if s[i]]

def ap_good(a, p):
    # p 奇素数, 良い還元: (2y+a1x+a3)^2 = 4f(x)+(a1x+a3)^2 =: g(x), a_p = -Σ χ(g(x))
    a1, a2, a3, a4, a6 = a
    sq = [0] * p
    for t in range((p + 1) // 2 + 1):
        sq[t * t % p] = 1
    chi = [0] + [(1 if sq[t] else -1) for t in range(1, p)]
    s = 0
    for x in range(p):
        g = (4 * (x * x * x + a2 * x * x + a4 * x + a6) + (a1 * x + a3) ** 2) % p
        s += chi[g]
    return -s

def ap_p2(a):
    a1, a2, a3, a4, a6 = a
    cnt = 1
    for x in range(2):
        for y in range(2):
            if (y * y + a1 * x * y + a3 * y - (x ** 3 + a2 * x * x + a4 * x + a6)) % 2 == 0:
                cnt += 1
    return 2 + 1 - cnt

def ap_bad(a, p):
    # 乗法的還元 (素数導手): 特異点を除いて数える。a_p = p - #E_ns(F_p)
    a1, a2, a3, a4, a6 = a
    cnt = 1
    for x in range(p):
        for y in range(p):
            F = (y * y + a1 * x * y + a3 * y - (x ** 3 + a2 * x * x + a4 * x + a6)) % p
            if F != 0:
                continue
            Fx = (a1 * y - 3 * x * x - 2 * a2 * x - a4) % p
            Fy = (2 * y + a1 * x + a3) % p
            if Fx == 0 and Fy == 0:
                continue          # 特異点 (ノード) は非特異点集合に入れない
            cnt += 1
    return p - cnt

def an_list(a, N, nmax):
    ps = sieve_primes(nmax)
    ap = {}
    for p in ps:
        if p == 2:
            ap[p] = ap_p2(a) if N % 2 else ap_bad(a, 2)
        elif N % p == 0:
            ap[p] = ap_bad(a, p)
        else:
            ap[p] = ap_good(a, p)
    an = [0] * (nmax + 1); an[1] = 1
    for p in ps:
        pk = p; prev, cur = 1, ap[p]
        powers = {p: ap[p]}
        while pk * p <= nmax:
            nxt = cur * ap[p] if N % p == 0 else cur * ap[p] - p * prev
            prev, cur = cur, nxt
            pk *= p
            powers[pk] = cur
        for pk, c in powers.items():
            for m in range(1, nmax // pk + 1):
                if m % p == 0 or an[m] == 0:
                    continue
                an[m * pk] = an[m] * c
    return an

# ---- L の中心値と導値 (Λ(s) = ∫_1^∞ (t^{s-1} + ε t^{1-s}) h(t) dt から) ------
def f_sum(an, N, A):
    # f(A) = Σ a_n/n · exp(-2πnA/√N)。 L(1) = f(A) + ε f(1/A) (任意の A > 0)
    C = mp.sqrt(N) / (2 * mp.pi)
    s = mp.mpf(0)
    for n in range(1, len(an)):
        if an[n] == 0:
            continue
        x = A * n / C
        if x > 90:
            break
        s += mp.mpf(an[n]) / n * mp.e ** (-x)
    return s

def eps_detect(an, N, A=mp.mpf('1.3')):
    f1, fA, fiA = f_sum(an, N, mp.mpf(1)), f_sum(an, N, A), f_sum(an, N, 1 / A)
    eps = (f1 - fA) / (fiA - f1)
    return (1 if eps > 0 else -1), abs(eps - (1 if eps > 0 else -1)), f1

def Lprime(an, N):
    # ε = -1 のとき L'(E,1) = 2 Σ a_n/n · E1(2πn/√N)
    C = mp.sqrt(N) / (2 * mp.pi)
    return 2 * mp.fsum(mp.mpf(an[n]) / n * mp.e1(n / C)
                       for n in range(1, len(an)) if an[n] and n / C < 90)

def Lderiv_k(an, N, k):
    # 前提: L(1) = ... = L^{(k-1)}(1) = 0 のとき L^{(k)}(1) = (2/C) Σ a_n I_k(n/C),
    # I_k(x) = ∫_1^∞ (log t)^k e^{-xt} dt
    C = mp.sqrt(N) / (2 * mp.pi)
    Ik = lambda x: mp.quad(lambda t: mp.log(t) ** k * mp.e ** (-x * t), [1, 2, 5, mp.inf])
    return 2 / C * mp.fsum(an[n] * Ik(n / C)
                           for n in range(1, len(an)) if an[n] and n / C < 60)

# ---- 有理点の算術: 加法・正準高さ・レギュレータ -----------------------------
def on_curve(a, P):
    a1, a2, a3, a4, a6 = a; x, y = P
    return y * y + a1 * x * y + a3 * y == x ** 3 + a2 * x * x + a4 * x + a6

def ec_add(a, P, Q):
    a1, a2, a3, a4, a6 = [Fraction(t) for t in a]
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P; x2, y2 = Q
    if x1 == x2 and y1 + y2 + a1 * x2 + a3 == 0:
        return None
    if P == Q:
        lam = (3 * x1 * x1 + 2 * a2 * x1 + a4 - a1 * y1) / (2 * y1 + a1 * x1 + a3)
    else:
        lam = (y2 - y1) / (x2 - x1)
    nu = y1 - lam * x1
    x3 = lam * lam + a1 * lam - a2 - x1 - x2
    return (x3, -(lam + a1) * x3 - nu - a3)

def canonical_height(a, P, n=8):
    # ĥ(P) = lim h(2^n P)/4^n, h = log max(|分子|, |分母|)。誤差 O(4^-n)
    Q = (Fraction(P[0]), Fraction(P[1]))
    for _ in range(n):
        Q = ec_add(a, Q, Q)
        if Q is None:
            return mp.mpf(0)
    x = Q[0]
    return mp.log(max(abs(x.numerator), abs(x.denominator))) / mp.mpf(4) ** n

def height_pairing(a, P, Q, n=8):
    S = ec_add(a, (Fraction(P[0]), Fraction(P[1])), (Fraction(Q[0]), Fraction(Q[1])))
    hS = canonical_height(a, S, n) if S else mp.mpf(0)
    return (hS - canonical_height(a, P, n) - canonical_height(a, Q, n)) / 2

def regulator(a, gens, n=8):
    r = len(gens)
    if r == 0:
        return mp.mpf(1)
    H = mp.matrix(r, r)
    for i in range(r):
        H[i, i] = canonical_height(a, gens[i], n)
    for i, j in itertools.combinations(range(r), 2):
        H[i, j] = H[j, i] = height_pairing(a, gens[i], gens[j], n)
    return mp.det(H).real if r > 1 else H[0, 0]

# ---- 実周期 Ω ----------------------------------------------------------------
def real_period(a):
    # Y^2 = g(x) = 4x^3 + b2 x^2 + 2 b4 x + b6。実根 1 個なら 1 成分、3 個なら 2 成分
    a1, a2, a3, a4, a6 = a
    b2 = a1 * a1 + 4 * a2; b4 = 2 * a4 + a1 * a3; b6 = a3 * a3 + 4 * a6
    g = lambda x: 4 * x ** 3 + b2 * x ** 2 + 2 * b4 * x + b6
    roots = mp.polyroots([4, b2, 2 * b4, b6])
    reals = sorted(r.real for r in roots if abs(r.imag) < 1e-20)
    e1 = mp.mpf(reals[-1])
    om = mp.quad(lambda t: 4 * t / mp.sqrt(g(e1 + t * t)), [0, 1, 5, 50, mp.inf])
    if len(reals) == 3:                      # コンパクト成分も E(R) に入る
        e3, e2 = mp.mpf(reals[0]), mp.mpf(reals[1])
        omc = mp.quad(lambda u: (e2 - e3) * mp.sin(2 * u)
                      / mp.sqrt(abs(g(e3 + (e2 - e3) * mp.sin(u) ** 2))),
                      [mp.mpf('1e-12'), mp.pi / 4, mp.pi / 2 - mp.mpf('1e-12')])
        om += 2 * omc
    return om.real if hasattr(om, 'real') else om

# ---- 実行 --------------------------------------------------------------------
if __name__ == "__main__":
    NMAX = 2000
    print("定理2  中心零点の位数の読み出し (数値)")
    data = {}
    for label, a, N, rank, gens in CURVES:
        an = an_list(a, N, NMAX)
        e, dev, f1 = eps_detect(an, N)
        L1 = (1 + e) * f1
        row = {"an": an, "eps": e, "L1": L1}
        print(f"\n  {label}: N={N}, 既知の階数 r={rank}")
        print(f"    ε = {e:+d} (実測偏差 {mp.nstr(dev, 3)}),  L(E,1) = {mp.nstr(L1, 12)}")
        if e == -1:
            Lp = Lprime(an, N); row["Lp"] = Lp
            print(f"    L'(E,1) = {mp.nstr(Lp, 12)}")
            if abs(Lp) < 1e-8:
                print(f"    L'''(E,1) = {mp.nstr(Lderiv_k(an, N, 3), 12)}")
        elif abs(L1) < 1e-8:
            print(f"    L''(E,1) = {mp.nstr(Lderiv_k(an, N, 2), 12)}")
        for P in gens:
            assert on_curve(a, P), (label, P)
        if gens:
            print(f"    生成点 {gens} は全て曲線上 (検証済)")
        data[label] = row

    print("\n定理3  先頭係数 = Ω × 高さの行列式")
    for label, a, N, rank, gens in CURVES:
        om = real_period(a)
        reg = regulator(a, gens)
        an = data[label]["an"]
        if rank == 0:
            lead = data[label]["L1"]
        elif rank == 1:
            lead = data[label]["Lp"]
        else:
            lead = Lderiv_k(an, N, rank) / mp.factorial(rank)
        print(f"  {label}: Ω = {mp.nstr(om, 12)}, Reg = {mp.nstr(reg, 10)}, "
              f"L^({rank})(1)/{rank}! = {mp.nstr(lead, 10)}, "
              f"比 L/(Ω·Reg) = {mp.nstr(lead / (om * reg), 8)}")
    print("\n  11a1 の比 1/5 は BSD の右辺 c_11·|Ш|/|T|^2 = 5·1/25 (玉河数 5, 捩れ Z/5Z)。")
    print("  他 3 曲線は c = 1, |T| = 1, |Ш| = 1 (予想) なので比の予測は 1。")
