"""おかえりロード テストプレイ用シミュレータ

    python3 tools/simulate.py            # v4 と v5 の比較（各 4000 ゲーム）
    python3 tools/simulate.py 10000      # ゲーム数を指定

ルールをほぼ実装したモンテカルロ・シミュレータ（上級ルールなし）。ペア・J・Q・K、
お気に入りスート、大勝負、がんばれゾーン、切り札（簡略化）、歩幅カード、補給、
手札上限、呼び込み、おかえり勝負を扱う。両陣営に方針（Policy）を持たせて対戦させ、
ゲームの長さ・逆転のしやすさ・陣営差・「いつも同じ手が最善」になっていないか
（支配戦略）を調べる。AI は単純なので、数値は傾向を見るための目安として使う。
結果の読み方は DESIGN_NOTES.md を参照。
"""
import random
from collections import Counter

A, D = "A", "D"  # てんし, あくま
OPP = {A: D, D: A}
SIGN = {A: 1, D: -1}

# ---- 盤面 ----------------------------------------------------------
# lane: [lane1, lane2] each 'A'(健康) / 'B'(誘惑) / None
def square(pos, lane):
    base = {1: ("S",), 2: ("V", 1), 3: ("-",), 4: ("F",), 8: ("V", 2), 9: ("-",), 10: ("F",),
            14: ("V", 2), 15: ("O", D, "H"), 16: ("O", A, "H"), 17: ("!",), 18: ("G",)}
    if pos in base:
        return base[pos]
    if 5 <= pos <= 7:
        if lane[0] == "A":
            return {5: ("O", A, "C"), 6: ("!",), 7: ("O", A, "S")}[pos]
        return {5: ("O", D, "D"), 6: ("!",), 7: ("O", D, "S")}[pos]
    if 11 <= pos <= 13:
        if lane[1] == "A":
            return {11: ("O", A, "D"), 12: ("V", 1), 13: ("!",)}[pos]
        return {11: ("O", D, "C"), 12: ("V", 1), 13: ("!",)}[pos]


def new_deck():
    d = [(r, s) for r in range(1, 14) for s in "SHDC"]
    random.shuffle(d)
    return d


TRUMPS = ["plus3", "minus3", "guard", "double", "lane", "draw2"]


class Game:
    def __init__(self, pa, pd, cfg):
        self.cfg = cfg
        self.pol = {A: pa, D: pd}
        self.deck = new_deck()
        self.discard = []
        h0 = cfg.get("hand0", 10)
        self.hand = {A: [self.draw1() for _ in range(h0)], D: [self.draw1() for _ in range(h0)]}
        k = cfg.get("trump_n", 6) if cfg.get("trumps", True) else 0
        self.trumps = {A: set(random.sample(TRUMPS, k)), D: set(random.sample(TRUMPS, k))}
        self.g = 0
        self.pos = 1
        self.lane = [None, None]
        self.jam = {A: False, D: False}  # 妨害を受けている
        self.turn_team = cfg.get("first", A)
        self.turns = 0
        self.events = 0
        self.hist = [0]
        self.log = Counter()
        self.over = False

    # -- カード ------------------------------------------------------
    def draw1(self):
        if not self.deck:
            self.deck = self.discard
            self.discard = []
            random.shuffle(self.deck)
            self.log["reshuffle"] += 1
        return self.deck.pop()

    def give(self, t, n):
        for _ in range(n):
            self.hand[t].append(self.draw1())
        cap = self.cfg.get("cap", 12)
        while len(self.hand[t]) > cap:
            c = min(self.hand[t])
            self.hand[t].remove(c)
            self.discard.append(c)
            self.log["cap_discard"] += 1

    def supply(self):
        mode = self.cfg.get("supply", "to10")
        for t in (A, D):
            if mode == "to10":
                need = max(0, 10 - len(self.hand[t]))
            elif mode == "plus":
                need = self.cfg.get("supply_n", 4)
            elif mode == "instant":
                need = 0
            self.log[f"supply_{t}"] += need
            self.log[f"handAtSupply_{t}"] += len(self.hand[t])
            self.give(t, need)
        self.log["supplies"] += 1

    def spend(self, t, cards):
        for c in cards:
            self.hand[t].remove(c)
            self.discard.append(c)
        if self.cfg.get("supply") == "instant":
            self.give(t, len(cards))

    def bonus(self, t):
        if not self.cfg.get("cheer", True):
            return 0
        behind = -self.g * SIGN[t]
        lv = self.cfg.get("cheer_lv", ((4, 2), (8, 4)))
        b = 0
        for th, v in lv:
            if behind >= th:
                b = v
        return b

    def mv(self, x):
        self.g = max(-10, min(10, self.g + x))
        if abs(self.g) == 10:
            self.log["pinned"] += 1

    # -- 値 ----------------------------------------------------------
    def value(self, t, cards, trump_self, trump_opp):
        if not cards:
            return 0
        v = sum(c[0] for c in cards)
        if self.jam[t]:
            v = 0
        v += self.bonus(t)
        if trump_self == "plus3":
            v += 3
        if trump_opp == "minus3":
            v = max(0, v - 3)
        return v

    # -- イベント ----------------------------------------------------
    def battle(self, mult, fork=False):
        self.events += 1
        self.log["battle"] += 1
        ctx = dict(kind="fork" if fork else "battle", mult=mult)
        plays = {}
        for t in (A, D):
            cards, tr = self.pol[t].battle(self, t, ctx)
            if not cards and self.hand[t]:
                cards = [min(self.hand[t])]  # 必ず出す
            plays[t] = (cards, tr)
        res = self.resolve(plays, mult, ctx)
        return res

    def resolve(self, plays, mult, ctx):
        vals = {}
        for t in (A, D):
            cards, tr = plays[t]
            vals[t] = self.value(t, cards, tr, plays[OPP[t]][1])
        # 消費
        jam_next = {A: False, D: False}
        for t in (A, D):
            cards, tr = plays[t]
            if cards:
                self.jam[t] = False  # 公開で解除
            if tr:
                self.trumps[t].discard(tr)
                self.log[f"trump_{tr}"] += 1
            self.spend(t, cards)
        lane = None
        if vals[A] == vals[D]:
            self.log["tie"] += 1
            if ctx["kind"] == "fork":
                lane = random.choice("AB")
            win = None
        else:
            win = A if vals[A] > vals[D] else D
            wc = plays[win][0]
            diff = self.score_amount(abs(vals[A] - vals[D]), "battle")
            ranks = [c[0] for c in wc]
            if 13 in ranks:
                diff += self.cfg.get("k_n", 3)
            mul = mult
            if plays[win][1] == "double":
                mul = 2
            diff *= mul
            if plays[OPP[win]][1] == "guard":
                diff = 0
            self.mv(SIGN[win] * diff)
            if ctx["kind"] == "fork":
                if wc:
                    reds = [c for c in wc if c[1] in "HD"]
                    pref = "A" if win == A else "B"
                    if pref == "A" and reds:
                        lane = "A"
                    elif pref == "B" and len(reds) < len(wc):
                        lane = "B"
                    else:
                        lane = "A" if reds else "B"
                else:
                    lane = random.choice("AB")
            else:
                if 11 in ranks:
                    self.jam[OPP[win]] = True
                    self.log["J"] += 1
                if 12 in ranks:
                    self.extra_moves += 1
                    self.log["Q"] += 1
        if ctx["kind"] == "fork":
            la = plays[A][1] == "lane"
            ld = plays[D][1] == "lane"
            if la and not ld:
                lane = "A"
            elif ld and not la:
                lane = "B"
        return lane

    def own(self, t, suit):
        self.events += 1
        self.log["own"] += 1
        o = OPP[t]
        ctx = dict(kind="own", suit=suit, main=t)
        mc, mtr = self.pol[t].main(self, t, ctx)
        yc, ytr = self.pol[o].yoko(self, o, ctx)
        if not mc:
            self.log["main_pass"] += 1
        if not yc:
            self.log["yoko_pass"] += 1
        mv = self.value(t, mc, mtr, ytr)
        yv = self.value(o, yc, ytr, mtr)
        for x, cards, tr in ((t, mc, mtr), (o, yc, ytr)):
            if cards:
                self.jam[x] = False
            if tr:
                self.trumps[x].discard(tr)
                self.log[f"trump_{tr}"] += 1
            self.spend(x, cards)
        if mc and mv > yv:
            x = self.score_amount(mv - yv, "own")
            ranks = [c[0] for c in mc]
            if 13 in ranks:
                x += self.cfg.get("k_n", 3)
            if self.cfg.get("fav", True) and any(c[1] == suit for c in mc):
                x += self.cfg.get("fav_n", 3)
            if mtr == "double":
                x *= 2
            if ytr == "guard":
                x = 0
            self.mv(SIGN[t] * x)
            if 11 in ranks:
                self.jam[o] = True
                self.log["J"] += 1
            if 12 in ranks:
                self.extra_moves += 1
                self.log["Q"] += 1
            return True
        return False

    def score_amount(self, diff, kind):
        mode = self.cfg.get("score", "diff")
        if mode == "diff":
            return diff
        if mode == "cap":
            return min(diff, self.cfg.get("cap_n", 5))
        if mode == "fixed":
            return self.cfg.get("stake", 3)
        if mode == "fixedplus":  # 固定＋大差ボーナス
            return self.cfg.get("stake", 3) + (2 if diff >= self.cfg.get("big", 5) else 0)

    def happening(self):
        h = random.randint(1, 6)
        if h == 2:
            self.mv(2)
        elif h == 3:
            self.mv(-2)
        elif h == 4:
            self.extra_moves += 1
        elif h == 5:
            self.pos = max(1, self.pos - 1)  # 処理なし
        elif h == 6:
            t = self.turn_team
            if self.hand[t]:
                c = min(self.hand[t])
                self.hand[t].remove(c)
                self.discard.append(c)
                self.hand[t].append(self.draw1())

    # -- 移動 --------------------------------------------------------
    def step(self, n, final_process=True):
        for i in range(n):
            self.pos += 1
            if self.pos in (8, 14) and self.cfg.get("supply") != "instant":
                self.supply()
            if self.pos >= 18:
                self.pos = 18
                self.finish()
                return
            if self.pos in (4, 10) and i < n - 1:
                self.lane[0 if self.pos == 4 else 1] = self.battle(1, fork=True)
            elif i < n - 1 and self.cfg.get("lure"):
                sq = square(self.pos, self.lane)
                if sq[0] == "O" and self.pos <= self.cfg.get("lure_max", 18) and self.pol[sq[1]].lure(self, sq[1], sq[2]):
                    self.log["lure"] += 1
                    if self.own(sq[1], sq[2]):
                        self.log["lure_ok"] += 1
                        while self.extra_moves and not self.over:
                            self.extra_moves -= 1
                            self.step(1)
                        return
        if final_process:
            self.process()

    def process(self):
        s = square(self.pos, self.lane)
        if s[0] == "F":
            self.lane[0 if self.pos == 4 else 1] = self.battle(1, fork=True)
        elif s[0] == "V":
            self.battle(s[1])
        elif s[0] == "O":
            self.own(s[1], s[2])
        elif s[0] == "!":
            self.happening()
        while self.extra_moves and not self.over:
            self.extra_moves -= 1
            self.step(1)

    def finish(self):
        if self.cfg.get("final_battle"):
            self.battle(self.cfg.get("final_mult", 1))
        self.over = True

    def play(self):
        while not self.over:
            self.turns += 1
            self.extra_moves = 0
            t = self.turn_team
            # 「はやおき」
            if "draw2" in self.trumps[t] and len(self.hand[t]) <= self.pol[t].draw2_at:
                self.trumps[t].discard("draw2")
                self.give(t, 2)
                self.log["trump_draw2"] += 1
            n = None
            if self.cfg.get("stride", True):
                c = self.pol[t].stride(self, t)
                if c:
                    self.spend(t, [c])
                    n = c[0]
                    self.log["stride"] += 1
            if n is None:
                lo, hi = self.cfg.get("move", (2, 4))
                n = random.randint(lo, hi)
            self.step(n)
            self.hist.append(self.g)
            self.turn_team = OPP[t]
        g = self.g
        if g == 0:
            self.log["zero"] += 1
            g = 1 if random.random() < 0.5 else -1
        return A if g > 0 else D


# ---- 方針 ------------------------------------------------------------
class Policy:
    def __init__(self, yoko=True, stride=True, save=0.5, trump=True, draw2_at=4, greedy=False, mainpass=True, thrift=None, concede=0.0, lure_min=3):
        self.thrift = thrift
        self.concede = concede
        self.lure_min = lure_min
        self.use_yoko = yoko
        self.use_stride = stride
        self.save = save          # 0=出し惜しみなし 1=強く温存
        self.use_trump = trump
        self.draw2_at = draw2_at
        self.greedy = greedy
        self.mainpass = mainpass

    def pick_strength(self, g, t, importance):
        """importance 0..1 に応じて手札の何番目を出すか"""
        h = sorted(g.hand[t], key=lambda c: c[0])
        if not h:
            return []
        if self.thrift is not None:
            target = self.thrift + (3 if importance >= 0.8 else 0) - g.bonus(t)
            if random.random() < self.concede:
                return [h[0]]
            ok = [c for c in h if c[0] >= target]
            return [ok[0]] if ok else [h[0]]
        if self.greedy:
            idx = len(h) - 1
        else:
            q = min(1.0, importance * (1.0 - 0.5 * self.save) + 0.35)
            idx = min(len(h) - 1, int(q * len(h)))
        best = [h[idx]]
        # ペア：同じ数字があり、重要なら
        if importance >= 0.8:
            cnt = Counter(c[0] for c in h)
            pairs = [r for r, n in cnt.items() if n >= 2 and r >= 5]
            if pairs:
                r = max(pairs)
                pc = [c for c in h if c[0] == r][:2]
                if 2 * r > best[0][0]:
                    best = pc
        return best

    def choose_trump(self, g, t, ctx, offense):
        if not self.use_trump or not g.trumps[t]:
            return None
        tr = g.trumps[t]
        imp = ctx.get("mult", 1) == 2 or abs(g.g) >= 6 or g.pos >= 14
        if ctx["kind"] == "fork" and "lane" in tr and random.random() < 0.5:
            return "lane"
        if not imp:
            return None
        for cand in (["plus3", "double", "minus3"] if offense else ["guard", "minus3", "plus3"]):
            if cand in tr and not (cand == "double" and ctx.get("mult", 1) == 2):
                return cand
        return None

    def battle(self, g, t, ctx):
        imp = 0.9 if ctx.get("mult", 1) == 2 else (0.6 if ctx["kind"] == "fork" else 0.45)
        if ctx["kind"] == "fork":
            # 自陣営レーンの色を優先
            want = "HD" if t == A else "SC"
            h = sorted([c for c in g.hand[t] if c[1] in want], key=lambda c: c[0])
            if h and h[-1][0] >= 7:
                k = min(len(h) - 1, int((0.5 + 0.4 * (1 - self.save)) * len(h)))
                return [h[k]], self.choose_trump(g, t, ctx, True)
        return self.pick_strength(g, t, imp), self.choose_trump(g, t, ctx, True)

    def main(self, g, t, ctx):
        h = g.hand[t]
        if not h:
            return [], None
        fav = [c for c in h if c[1] == ctx["suit"] and c[0] >= 6]
        if fav:
            c = max(fav)
            return [c], self.choose_trump(g, t, ctx, True)
        cards = self.pick_strength(g, t, 0.6)
        if self.mainpass and cards and cards[0][0] <= 4:
            return [], None
        return cards, self.choose_trump(g, t, ctx, True)

    def yoko(self, g, t, ctx):
        if not self.use_yoko or not g.hand[t]:
            return [], None
        # 手札が少ないときは控える
        if len(g.hand[t]) <= 2 + 3 * self.save:
            return [], None
        return self.pick_strength(g, t, 0.5), self.choose_trump(g, t, ctx, False)

    def lure(self, g, t, suit):
        h = g.hand[t]
        if len(h) < self.lure_min:
            return False
        return any(c[0] >= 9 or (c[1] == suit and c[0] >= 6) for c in h)

    def stride(self, g, t):
        if not self.use_stride:
            return None
        lows = sorted([c for c in g.hand[t] if c[0] <= 4], key=lambda c: c[0])
        best = None
        for c in lows:
            p = g.pos + c[0]
            if p > 18:
                continue
            # 通過するわかれ道・補給は気にしない簡易版
            lane = list(g.lane)
            if g.pos < 4 <= p - 1 or g.pos < 10 <= p - 1:
                continue  # 通過時の勝負が入る移動は避ける
            s = square(min(p, 18), lane) if (p < 5 or p > 7 or lane[0]) and (p < 11 or p > 13 or lane[1]) else None
            if s is None:
                continue
            score = 0
            if s[0] == "O":
                score = 3 if s[1] == t else -3
            elif s[0] == "G":
                score = 5 if g.g * SIGN[t] > 0 else -5
            if score > 0 and (best is None or score > best[0]):
                best = (score, c)
        return best[1] if best else None


def run(n, pa=None, pd=None, cfg=None, seed=None):
    if seed is not None:
        random.seed(seed)
    cfg = cfg or {}
    wins = Counter()
    agg = Counter()
    turns = []
    events = []
    lead3 = [0, 0]
    leadlast = [0, 0]
    finals = Counter()
    for _ in range(n):
        g = Game(pa or Policy(), pd or Policy(), cfg)
        w = g.play()
        wins[w] += 1
        agg.update(g.log)
        turns.append(g.turns)
        events.append(g.events)
        finals[g.g] += 1
        h = g.hist
        if len(h) > 3 and h[3] != 0:
            lead3[0] += 1
            lead3[1] += (h[3] > 0) == (w == A)
        # ゴール直前2手番前のリード
        if len(h) > 3 and h[-3] != 0:
            leadlast[0] += 1
            leadlast[1] += (h[-3] > 0) == (w == A)
    r = dict(angel=wins[A] / n, turns=sum(turns) / n, events=sum(events) / n,
             lead3=lead3[1] / max(1, lead3[0]), lead_2before=leadlast[1] / max(1, leadlast[0]),
             pinned_end=(finals[10] + finals[-10]) / n, zero=agg["zero"] / n)
    return r, agg, finals


PRESETS = {
    "v4": {},
    "v5": {"lure": True, "lure_max": 13, "final_battle": True, "trump_n": 3},
}


def duel(n, px, py, cfg):
    """px と py を両陣営で入れ替えて対戦させ、px の勝率を返す"""
    r1, _, _ = run(n, px, py, cfg, seed=2)
    r2, _, _ = run(n, py, px, cfg, seed=3)
    return (r1["angel"] + (1 - r2["angel"])) / 2


def report(n):
    rows = [
        ("てんし陣営の勝率", lambda r, c: r["angel"]),
        ("手番数（平均）", lambda r, c: r["turns"]),
        ("カードを出す場面（平均）", lambda r, c: r["events"]),
        ("3手番後のリード側が勝つ率", lambda r, c: r["lead3"]),
        ("ゴール2手番前のリード側が勝つ率", lambda r, c: r["lead_2before"]),
        ("ゲージ端（±10）で終わる率", lambda r, c: r["pinned_end"]),
        ("横やりする方針の勝率（vs しない）", lambda r, c: duel(n, Policy(), Policy(yoko=False), c)),
        ("いつも最大のカードを出す方針の勝率（vs 標準）", lambda r, c: duel(n, Policy(greedy=True), Policy(), c)),
        ("歩幅カードを使う方針の勝率（vs 使わない）", lambda r, c: duel(n, Policy(), Policy(stride=False), c)),
    ]
    res = {k: run(n, cfg=c, seed=1)[0] for k, c in PRESETS.items()}
    print(f"{'指標':<34}" + "".join(f"{k:>8}" for k in PRESETS))
    for name, f in rows:
        print(f"{name:<30}" + "".join(f"{f(res[k], PRESETS[k]):>8.2f}" for k in PRESETS))


if __name__ == "__main__":
    import sys
    report(int(sys.argv[1]) if len(sys.argv) > 1 else 4000)
