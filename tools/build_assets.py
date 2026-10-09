#!/usr/bin/env python3
"""おかえりロードの画像素材（SVG）を生成するスクリプト。

    python3 tools/build_assets.py          # assets/*.svg を生成
    python3 tools/render_png.py            # SVG → PNG 書き出し（Playwright + Chromium）

色・寸法・文言はこのファイル、イラストは tools/art.py で管理する。
絵文字フォントには依存しない（すべてオリジナルの SVG イラスト）。
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

import art
from art import INK, place

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

FONT = "'Noto Sans CJK JP','Hiragino Sans','Yu Gothic','Meiryo',sans-serif"
# フレーバーテキスト用の色（フォントは本文と同じ丸みのあるゴシックのまま。
# ポップな見た目のまま不穏な文が書かれているほうが不気味さが出るため）
FLAVOR = "#5B5468"

# ---- パレット（てんし＝青、あくま＝ローズ で全素材を統一） ----
INK_SOFT = "#77708C"
PAPER = "#FBF4E6"
ANGEL = "#2F7FC8"
ANGEL_TINT = "#E2EFFB"
DEVIL = "#D0436A"
DEVIL_TINT = "#FBE3EA"
VIOLET = "#7A5CC6"
GOLD = "#FFC531"

TYPES = {
    #            ヘッダー色  ヘッダー文字色  ラベル
    "start": ("#3FA66B", "#FFFFFF", "スタート"),
    "goal": ("#E9744A", "#FFFFFF", "ゴール"),
    "health": (ANGEL, "#FFFFFF", "健康"),
    "temptation": (DEVIL, "#FFFFFF", "誘惑"),
    "either": (VIOLET, "#FFFFFF", "カード勝負"),
    "fork": (INK, "#FFFFFF", "わかれ道"),
    "happening": ("#F2B825", INK, "ハプニング"),
    "plain": ("#A9A5B8", "#FFFFFF", "素通り"),
}


def t(x, y, s, size, fill=INK, weight="normal", anchor="middle", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def ft(x, y, s, size, fill=FLAVOR, anchor="middle", weight="500"):
    """フレーバーテキスト（本文と同じフォント）"""
    return t(x, y, s, size, fill, weight, anchor, 'letter-spacing="1"')


def outlined(x, y, s, size, fill, stroke=INK, sw=8, anchor="middle", weight="900"):
    """ゲームロゴ風の縁取り文字"""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" '
            f'paint-order="stroke">{escape(s)}</text>')


def mix(c1, c2, k):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * k):02X}" for x, y in zip(a, b))


DEFS = f"""<defs>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
  <feDropShadow dx="0" dy="5" stdDeviation="3" flood-color="#5A4A2A" flood-opacity="0.22"/>
</filter>
<filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#5A4A2A" flood-opacity="0.12"/>
</filter>
<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
  <circle cx="4" cy="4" r="1.5" fill="#EADFC8"/>
</pattern>
<pattern id="stripeA" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="6" height="12" fill="#FFFFFF" opacity="0.35"/>
</pattern>
<pattern id="cardback" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="14" height="14" fill="#EFE7F8"/><rect width="7" height="7" fill="#E3D8F2"/>
</pattern>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FDF7EC"/><stop offset="1" stop-color="#F7EEDC"/>
</linearGradient>
</defs>"""


# =====================================================================
# ボード（1920×1080、CCFOLIA の前景 80×45 マス用）
# =====================================================================
W, H = 1920, 1080
TILE = 124
COLP = 142          # 列ピッチ
ROWP = 134          # 行ピッチ
X0 = 48 + TILE / 2  # 列0の中心
Y0 = 90 + TILE / 2  # 行0の中心


def cx(c):
    return X0 + c * COLP


def cy(r):
    return Y0 + r * ROWP


# 行：0=わかれ道①健康レーン 1=序盤・中盤の本道 2=わかれ道①誘惑レーン
#     3=わかれ道②健康レーン 4=終盤の本道 5=わかれ道②誘惑レーン
SQUARES = [
    # id, type, 列, 行, ラベル上書き, 場所, アイコン, お気に入りスート, 大勝負
    ("1", "start", 0, 1, None, "おでかけ", "sneaker", None, False),
    ("2", "either", 1, 1, None, "コンビニ", "store", None, False),
    ("3", "plain", 2, 1, None, "じゅうたくがい", "houses", None, False),
    ("4", "fork", 3, 1, "わかれ道①", "赤→健康 黒→誘惑", "signpost", None, False),
    ("5A", "health", 4, 0, None, "こうえん", "tree", "♣", False),
    ("6A", "happening", 5, 0, None, "？？？", "burst", None, False),
    ("7A", "health", 6, 0, None, "ジム", "dumbbell", "♠", False),
    ("5B", "temptation", 4, 2, None, "だがしや", "candy", "♦", False),
    ("6B", "happening", 5, 2, None, "？？？", "burst", None, False),
    ("7B", "temptation", 6, 2, None, "ラーメン屋", "ramen", "♠", False),
    ("8", "either", 7, 1, "大勝負", "じはんき（合流）", "vending", None, True),
    ("9", "plain", 8, 1, None, "じゅうたくがい", "houses", None, False),
    ("10", "fork", 8, 4, "わかれ道②", "赤→健康 黒→誘惑", "signpost", None, False),
    ("11A", "health", 7, 3, None, "やおや", "carrot", "♦", False),
    ("12A", "either", 6, 3, None, "こうえんのベンチ", "bench", None, False),
    ("13A", "happening", 5, 3, None, "？？？", "burst", None, False),
    ("11B", "temptation", 7, 5, None, "ファストフード", "burger", "♣", False),
    ("12B", "either", 6, 5, None, "屋台", "lantern", None, False),
    ("13B", "happening", 5, 5, None, "？？？", "burst", None, False),
    ("14", "either", 4, 4, "大勝負", "コンビニ（合流）", "store", None, True),
    ("15", "temptation", 3, 4, None, "ケーキ屋", "cake", "♥", False),
    ("16", "health", 2, 4, None, "こうえん", "tree", "♥", False),
    ("17", "happening", 1, 4, None, "？？？", "burst", None, False),
    ("18", "goal", 0, 4, None, "おうち", "home", None, False),
]
POS = {s[0]: (cx(s[2]), cy(s[3])) for s in SQUARES}

LANE_A = "#BFDCF6"
LANE_B = "#F8C9D6"
ROAD = "#EADBBE"
ROUTES = [
    (["1", "2", "3", "4"], ROAD),
    (["4", "5A", "6A", "7A", "8"], LANE_A),
    (["4", "5B", "6B", "7B", "8"], LANE_B),
    (["8", "9", "10"], ROAD),
    (["10", "11A", "12A", "13A", "14"], LANE_A),
    (["10", "11B", "12B", "13B", "14"], LANE_B),
    (["14", "15", "16", "17", "18"], ROAD),
]


def road_svg():
    out = []
    for path, color in ROUTES:
        pts = " ".join(f"{POS[p][0]:.1f},{POS[p][1]:.1f}" for p in path)
        out.append(f'<polyline points="{pts}" fill="none" stroke="#D6C29C" stroke-width="50" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="40" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<polyline points="{pts}" fill="none" stroke="#FFFFFF" stroke-width="4" '
                   f'stroke-dasharray="12 12" stroke-linecap="round" opacity="0.9"/>')
    for path, _ in ROUTES:
        for a, b in zip(path, path[1:]):
            (x1, y1), (x2, y2) = POS[a], POS[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            out.append(f'<g transform="translate({mx:.1f},{my:.1f}) rotate({ang:.1f})">'
                       f'<circle r="13" fill="#FFFFFF" stroke="#C9B38A" stroke-width="2.5"/>'
                       f'<path d="M-4,-6 L4,0 L-4,6" fill="none" stroke="#9C8A68" stroke-width="3.5" '
                       f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    return "\n".join(out)


def header_path(x0, y0, w, h, r):
    return (f"M{x0},{y0 + h} L{x0},{y0 + r} Q{x0},{y0} {x0 + r},{y0} L{x0 + w - r},{y0} "
            f"Q{x0 + w},{y0} {x0 + w},{y0 + r} L{x0 + w},{y0 + h} Z")


def tile_svg(sq):
    sid, typ, _c, _r, label, place_name, icon, suit, big = sq
    color, label_color, default_label = TYPES[typ]
    label = label or default_label
    x, y = POS[sid]
    x0, y0 = x - TILE / 2, y - TILE / 2
    hh = 32
    out = [f'<g filter="url(#shadow)">'
           f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{TILE}" height="{TILE}" rx="18" fill="#FFFDF8"/></g>',
           f'<path d="{header_path(x0, y0, TILE, hh, 18)}" fill="{color}"/>']
    if typ in ("health", "temptation"):
        tint = ANGEL_TINT if typ == "health" else DEVIL_TINT
        out.append(f'<rect x="{x0:.1f}" y="{y0 + hh:.1f}" width="{TILE}" height="{TILE - hh - 18}" fill="{tint}"/>')
        out.append(f'<path d="M{x0},{y0 + TILE - 18} L{x0 + TILE},{y0 + TILE - 18} L{x0 + TILE},{y0 + TILE - 18} '
                   f'Q{x0 + TILE},{y0 + TILE} {x0 + TILE - 18},{y0 + TILE} L{x0 + 18},{y0 + TILE} '
                   f'Q{x0},{y0 + TILE} {x0},{y0 + TILE - 18} Z" fill="{tint}"/>')
    out.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{TILE}" height="{TILE}" rx="18" fill="none" '
               f'stroke="{color}" stroke-width="4"/>')
    # 番号
    nw = 26 if len(sid) == 1 else (34 if len(sid) == 2 else 42)
    out.append(f'<rect x="{x0 + 6:.1f}" y="{y0 + 5:.1f}" width="{nw}" height="22" rx="11" fill="#FFFFFF"/>')
    out.append(t(x0 + 6 + nw / 2, y0 + 22, sid, 16, color if typ != "happening" else INK, "900"))
    # 種類ラベル
    if typ in ("health", "temptation") or big:
        out.append(t(x0 + nw + 12, y0 + 23, label, 16, label_color, "900", "start"))
    if typ in ("health", "temptation"):
        head = art.angel(wings=False) if typ == "health" else art.devil(tail=False)
        out.append(place(head, x0 + TILE - 22, y0 + 14, 40))
    elif not big:
        out.append(t(x0 + TILE - 9, y0 + 22, label, 14 if len(label) <= 4 else 13, label_color, "900", "end"))
    # イラスト
    out.append(place(art.ICONS[icon](), x, y + 4, 58))
    # 場所名
    out.append(t(x, y0 + TILE - 10, place_name, 13 if len(place_name) <= 6 else 11, INK, "bold"))
    if suit:
        out.append(art.suit_chip(suit, x0 + TILE - 6, y0 + TILE - 8, 15))
    if big:
        out.append(art.star_badge(x0 + TILE - 4, y0 + 4, "×2", 26))
    return "\n".join(out)


def pair_icon(x, y, k=1.0):
    def card(dx, rot, suit, col):
        return (f'<g transform="translate({x + dx * k:.1f},{y:.1f}) rotate({rot}) scale({k})">'
                f'<rect x="-13" y="-18" width="26" height="36" rx="4" fill="#FFFFFF" stroke="{INK}" stroke-width="2.4"/>'
                f'<text x="0" y="2" text-anchor="middle" font-size="15" font-weight="900" fill="{col}">7</text>'
                f'<text x="0" y="14" text-anchor="middle" font-size="10" fill="{col}" font-family="\'DejaVu Sans\'">{suit}</text></g>')
    return card(-7, -12, "♠", INK) + card(7, 10, "♥", "#E0344F")


def cheer_icon(x, y, k=1.0):
    return (f'<g transform="translate({x},{y}) scale({k})">'
            f'<path d="M-8,18 L-8,-18" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M-8,-18 L16,-12 L-8,-4 Z" fill="#FF8A3D" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<text x="10" y="16" text-anchor="middle" font-size="14" font-weight="900" fill="{INK}">+2</text></g>')


def panel(x, y, w, h, title=None, color=INK):
    out = [f'<g filter="url(#soft)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#FFFFFF" fill-opacity="0.92"/></g>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="none" stroke="#E6D7B8" stroke-width="2"/>']
    if title:
        out.append(f'<rect x="{x + 18}" y="{y - 14}" width="{len(title) * 20 + 30}" height="30" rx="15" fill="{color}"/>')
        out.append(t(x + 33, y + 8, title, 18, "#FFFFFF", "900", "start"))
    return "\n".join(out)


def gimmick_svg():
    # 左側の空きスペース（列0〜3・行2〜3）：ボードのしかけ
    x, y = cx(0) - TILE / 2, cy(2) - TILE / 2 + 16
    w = 4 * COLP - (COLP - TILE)
    h = 2 * ROWP - 34
    out = [panel(x, y, w, h, "ボードのしかけ", VIOLET)]
    items = [
        (lambda ix, iy: art.suit_chip("♥", ix, iy, 17), "お気に入りスート +3", "主役がお店の好きなスートで通すと+3"),
        (lambda ix, iy: art.star_badge(ix, iy, "×2", 22), "大勝負マス ×2", "合流マスは勝負×2・10枚まで補給"),
        (lambda ix, iy: pair_icon(ix, iy, 0.95), "ペア出し", "同じ数字2枚を1組で出すと合計の数字"),
        (lambda ix, iy: cheer_icon(ix, iy), "がんばれゾーン +2／+4", "相手側に4以上で数字+2、8以上で+4"),
    ]
    for i, (draw, name, desc) in enumerate(items):
        col, row = i % 2, i // 2
        ix = x + 44 + col * (w / 2 - 4)
        iy = y + 52 + row * 70
        out.append(draw(ix, iy))
        out.append(t(ix + 32, iy - 3, name, 16, INK, "900", "start"))
        out.append(t(ix + 32, iy + 18, desc, 11.5, INK_SOFT, anchor="start"))
    ly = y + h - 26
    out.append(f'<line x1="{x + 26}" y1="{ly}" x2="{x + 62}" y2="{ly}" stroke="{LANE_A}" stroke-width="16" stroke-linecap="round"/>')
    out.append(t(x + 74, ly + 5, "健康レーン（赤♥♦で勝ち）", 13.5, ANGEL, "bold", "start"))
    lx = x + w / 2 + 8
    out.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 36}" y2="{ly}" stroke="{LANE_B}" stroke-width="16" stroke-linecap="round"/>')
    out.append(t(lx + 48, ly + 5, "誘惑レーン（黒♠♣で勝ち）", 13.5, DEVIL, "bold", "start"))
    return "\n".join(out)


def flow_svg():
    # 左下の空きスペース（列0〜4・行5）：手番の流れ
    x, y = cx(0) - TILE / 2, cy(5) - TILE / 2 + 18
    w = 5 * COLP - (COLP - TILE) - 14
    h = TILE - 18
    out = [panel(x, y, w, h, "手番の流れ", "#3FA66B")]
    steps = ["① 1d3+1 か 歩幅カード(A〜4)で進む", "② 通りすぎるお店は「呼び込み」できる",
             "③ 止まったマスで裏向き→「せーの」", "④ ゴールで「おかえり勝負」→ 判定"]
    for i, s in enumerate(steps):
        col, row = i % 2, i // 2
        out.append(t(x + 26 + col * (w / 2 - 6), y + 44 + row * 32, s, 15, INK, "bold", "start"))
    return "\n".join(out)


def title_svg():
    x, y = cx(0) - TILE / 2 + 2, cy(0) - 8
    out = [outlined(x + 4, y + 5, "おかえりロード", 56, INK, INK, 7, "start"),
           outlined(x, y, "おかえりロード", 56, "#FFFFFF", INK, 6, "start")]
    # 「お」の上の光の輪・「ド」の角
    out.append(f'<ellipse cx="{x + 30}" cy="{y - 52}" rx="20" ry="6" fill="none" stroke="#F2C230" stroke-width="5"/>')
    # リボン
    ry = y + 16
    out.append(f'<path d="M{x + 4},{ry} L{x + 372},{ry} L{x + 360},{ry + 17} L{x + 372},{ry + 34} L{x + 4},{ry + 34} L{x + 16},{ry + 17} Z" '
               f'fill="{VIOLET}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    out.append(t(x + 188, ry + 24, "〜天使とあくまのさんぽ道〜", 18, "#FFFFFF", "900"))
    out.append(place(art.angel(), x + 452, y - 6, 74))
    out.append(place(art.devil(), x + 520, y + 8, 64))
    return "\n".join(out)


def gauge_svg():
    cwid, ch = 54, 60
    gx = 112
    gy = 958
    total = 21 * cwid
    out = [t(48, gy - 46, "体調ゲージ", 22, INK, "900", "start"),
           t(170, gy - 46, "スタートは 0。おかえり勝負のあとの位置で勝敗が決まる", 14, INK_SOFT, anchor="start")]
    out.append(f'<rect x="{gx - 6}" y="{gy - 6}" width="{total + 12}" height="{ch + 12}" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>')
    for i, v in enumerate(range(-10, 11)):
        x = gx + i * cwid
        if v < 0:
            fill = mix("#FFFFFF", DEVIL, 0.10 + 0.6 * (-v) / 10)
        elif v > 0:
            fill = mix("#FFFFFF", ANGEL, 0.10 + 0.6 * v / 10)
        else:
            fill = "#FFFFFF"
        rx = 9 if v in (-10, 10) else 0
        out.append(f'<rect x="{x}" y="{gy}" width="{cwid}" height="{ch}" rx="{rx}" fill="{fill}"/>')
        if abs(v) >= 4:
            out.append(f'<rect x="{x}" y="{gy}" width="{cwid}" height="{ch}" rx="{rx}" fill="url(#stripeA)"/>')
        if i:
            out.append(f'<line x1="{x}" y1="{gy + 6}" x2="{x}" y2="{gy + ch - 6}" stroke="#FFFFFF" stroke-width="2"/>')
        label = f"+{v}" if v > 0 else ("−" + str(-v) if v < 0 else "0")
        color = "#FFFFFF" if abs(v) >= 5 else INK
        out.append(t(x + cwid / 2, gy + ch / 2 + 8, label, 21 if v else 26, color, "900"))
    out.append(f'<rect x="{gx + 10 * cwid - 3}" y="{gy - 9}" width="{cwid + 6}" height="{ch + 18}" rx="10" fill="none" stroke="{INK}" stroke-width="4"/>')
    # がんばれゾーン（2段階：相手側に4以上で+2、8以上で+4）
    def zone(c0, n, label, col):
        x0 = gx + c0 * cwid
        out.append(f'<path d="M{x0 + 4},{gy - 14} L{x0 + n * cwid - 4},{gy - 14}" stroke="{col}" stroke-width="5" stroke-linecap="round"/>')
        out.append(t(x0 + n * cwid / 2, gy - 21, label, 13, col, "900"))
    zone(0, 3, "がんばれ+4", ANGEL)
    zone(3, 4, "てんしのがんばれ（+2）", ANGEL)
    zone(14, 4, "あくまのがんばれ（+2）", DEVIL)
    zone(18, 3, "がんばれ+4", DEVIL)
    # 両端のキャラクター
    out.append(place(art.devil(), gx - 42, gy + ch / 2, 64))
    out.append(place(art.angel(), gx + total + 42, gy + ch / 2, 70))
    ty = gy + ch + 34
    out.append(t(gx, ty, "−1以下：あくまの勝ち", 17, DEVIL, "900", "start"))
    out.append(t(gx + total / 2, ty, "0：気まぐれ判定（1d6 奇数てんし／偶数あくま）", 14, INK_SOFT, "bold"))
    out.append(t(gx + total, ty, "+1以上：てんしの勝ち", 17, ANGEL, "900", "end"))
    return "\n".join(out)


def slot(x, y, w, h, label, color, sub=None, back=False):
    out = []
    if back:
        out.append(f'<rect x="{x + 10}" y="{y + 10}" width="{w - 20}" height="{h - 20}" rx="8" fill="url(#cardback)" opacity="0.8"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{color}" '
               f'stroke-width="3" stroke-dasharray="10 7"/>')
    out.append(t(x + w / 2, y + h / 2 + 6, label, 19, color, "900"))
    if sub:
        # sub は文字列、または枠に収まらないときの複数行（リスト）
        for i, line in enumerate([sub] if isinstance(sub, str) else sub):
            out.append(t(x + w / 2, y + h / 2 + 28 + i * 16, line, 12, INK_SOFT, "bold"))
    return "\n".join(out)


def card_area_svg():
    px, py, pw, ph = 1356, 22, 542, 1036
    out = [f'<g filter="url(#soft)"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="28" fill="#FFFDF8"/></g>',
           f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="28" fill="none" stroke="#E6D7B8" stroke-width="2"/>',
           outlined(px + 28, py + 50, "カード置き場", 26, INK, "#FFFFFF", 0, "start"),
           t(px + pw - 26, py + 48, "※枠の大きさは目安", 12, INK_SOFT, anchor="end")]
    cw, ch = 132, 172
    gx = (pw - 3 * cw) / 4
    y1 = py + 72
    out.append(slot(px + gx, y1, cw, ch, "山札", INK, "トランプのデッキ", back=True))
    out.append(slot(px + 2 * gx + cw, y1, cw, ch, "捨て札", INK_SOFT, "表向きで置く"))
    out.append(slot(px + 3 * gx + 2 * cw, y1, cw, ch, "除外", INK_SOFT, ["ジョーカー", "使った切り札"]))
    # 勝負エリア
    y2 = y1 + ch + 28
    out.append(f'<rect x="{px + 16}" y="{y2}" width="{pw - 32}" height="290" rx="22" fill="#F3EEFB" stroke="#D9CCF2" stroke-width="2"/>')
    out.append(outlined(px + pw / 2, y2 + 40, "勝負エリア", 24, VIOLET, "#FFFFFF", 0))
    out.append(t(px + pw / 2, y2 + 64, "裏向きで置いて「準備OK」→「せーの」で公開", 13, INK_SOFT, "bold"))
    bw, bh = 152, 190
    lx, rx = px + 46, px + pw - 46 - bw
    out.append(slot(lx, y2 + 82, bw, bh, "てんし", ANGEL, "ペアなら2枚"))
    out.append(slot(rx, y2 + 82, bw, bh, "あくま", DEVIL, "ペアなら2枚"))
    out.append(place(art.vs(), px + pw / 2, y2 + 82 + bh / 2, 64))
    out.append(place(art.angel(wings=False), lx + 18, y2 + 86, 46))
    out.append(place(art.devil(tail=False), rx + bw - 18, y2 + 86, 46))
    # 手札置き場
    y3 = y2 + 290 + 24
    hh = 200
    for i, (name, color, head) in enumerate([("てんし陣営の手札", ANGEL, art.angel(wings=False)),
                                              ("あくま陣営の手札", DEVIL, art.devil(tail=False))]):
        yy = y3 + i * (hh + 16)
        out.append(slot(px + 16, yy, pw - 32, hh, name, color, "数字カードは「自分だけ見る」・陣営で合計12枚まで・切り札（選んだ3枚）は非公開"))
        out.append(place(head, px + 52, yy + 36, 48))
    return "\n".join(out)


def scenery_svg():
    """背景の小さな飾り（雲・草）"""
    out = []
    for (x, y, k) in [(940, 300, 1.0), (1080, 220, 0.7), (360, 640, 0.6)]:
        out.append(f'<g transform="translate({x},{y}) scale({k})" opacity="0.9">'
                   f'<path d="M-40,10 Q-40,-8 -22,-8 Q-16,-26 4,-22 Q20,-34 34,-16 Q52,-14 50,6 Q50,14 40,14 L-32,14 Q-40,14 -40,10 Z" '
                   f'fill="#FFFFFF" stroke="#E6D7B8" stroke-width="3"/></g>')
    for (x, y) in [(1000, 425), (870, 160), (1190, 860), (620, 905), (1300, 280)]:
        out.append(f'<path d="M{x - 10},{y} Q{x - 8},{y - 12} {x - 4},{y} M{x},{y} Q{x + 2},{y - 16} {x + 5},{y} M{x + 7},{y} Q{x + 11},{y - 10} {x + 13},{y}" '
                   f'fill="none" stroke="#9FCF8E" stroke-width="3" stroke-linecap="round"/>')
    return "\n".join(out)


def flavor_svg():
    """道のまんなかの空き地に置く、ひとことのフレーバー"""
    out = []
    # わかれ道①の内側（5A〜7A と 5B〜7B のあいだ）
    out.append(ft(cx(5) - 6, cy(1) - 8, "――あのひとは今日も、", 15))
    out.append(ft(cx(5) + 10, cy(1) + 18, "ひとりで帰ってくる。", 15))
    # わかれ道②の内側（13A〜11A と 13B〜11B のあいだ）
    out.append(ft(cx(6) - 2, cy(4) - 6, "おなかが空いたら、", 15))
    out.append(ft(cx(6) + 14, cy(4) + 20, "おうちへ帰りましょう。", 15))
    return "\n".join(out)


def board():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
             DEFS,
             f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
             f'<rect width="{W}" height="{H}" fill="url(#dots)"/>',
             scenery_svg(),
             road_svg(),
             flavor_svg()]
    for sq in SQUARES:
        parts.append(tile_svg(sq))
    parts += [title_svg(), gimmick_svg(), flow_svg(), gauge_svg(), card_area_svg(), "</svg>"]
    return "\n".join(parts)


# =====================================================================
# コマ（200×200、600×600px で書き出し）
# =====================================================================
def token(body, label, color, tint, size=118, dy=-8):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200" font-family="{FONT}">
<defs>
<radialGradient id="g" cx="0.35" cy="0.3" r="0.85">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{tint}"/>
</radialGradient>
</defs>
<circle cx="100" cy="104" r="92" fill="{INK}" opacity="0.18"/>
<circle cx="100" cy="100" r="92" fill="{color}" stroke="{INK}" stroke-width="5"/>
<circle cx="100" cy="100" r="78" fill="url(#g)" stroke="{INK}" stroke-width="3"/>
{place(body, 100, 100 + dy, size)}
<rect x="46" y="144" width="108" height="34" rx="17" fill="{color}" stroke="{INK}" stroke-width="4"/>
<text x="100" y="168" text-anchor="middle" font-size="20" font-weight="900" fill="#FFFFFF">{escape(label)}</text>
</svg>
"""


# =====================================================================
# 早見表（1080×2446、スクリーンパネル用）
# =====================================================================
def quick_reference():
    QW, QH = 1080, 2446
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{QW}" height="{QH}" viewBox="0 0 {QW} {QH}" font-family="{FONT}">',
         DEFS,
         f'<rect width="{QW}" height="{QH}" fill="url(#sky)"/>',
         f'<rect width="{QW}" height="{QH}" fill="url(#dots)"/>',
         outlined(62, 94, "おかえりロード 早見表", 48, INK, INK, 6, "start"),
         outlined(60, 90, "おかえりロード 早見表", 48, "#FFFFFF", INK, 5, "start"),
         place(art.angel(), QW - 170, 66, 80),
         place(art.devil(), QW - 90, 72, 70),
         ft(QW - 222, 58, "肩の上で、てんしとあくまが言い争う。", 14, anchor="end"),
         ft(QW - 222, 86, "あのひとの好物を、だれも知らない。", 14, anchor="end")]

    def box(y, h, title, color):
        p.append(f'<g filter="url(#soft)"><rect x="40" y="{y}" width="{QW - 80}" height="{h}" rx="24" fill="#FFFFFF"/></g>')
        p.append(f'<rect x="40" y="{y}" width="{QW - 80}" height="{h}" rx="24" fill="none" stroke="{color}" stroke-width="3"/>')
        p.append(f'<rect x="64" y="{y - 18}" width="{len(title) * 25 + 36}" height="38" rx="19" fill="{color}" stroke="{INK}" stroke-width="3"/>')
        p.append(t(82, y + 10, title, 22, "#FFFFFF", "900", "start"))

    # 1. 勝敗
    y = 140
    box(y, 120, "勝ち負け", INK)
    p.append(t(76, y + 60, "ゴール（マス18）で「おかえり勝負」（カード勝負1回）をした後のゲージで決まる。", 20, INK, "bold", "start"))
    p.append(t(76, y + 94, "+1以上 → てんしの勝ち　／　−1以下 → あくまの勝ち　／　0 → 1d6（奇数てんし）", 18, INK_SOFT, anchor="start"))

    # 2. 手番と手札
    y = 300
    box(y, 206, "手番と手札", "#3FA66B")
    turn = ["移動：1d3+1（2〜4マス）。振る前なら、手札の A〜4 を1枚出してその数だけ進んでもよい（歩幅カード）",
            "使ったカードは補充しない。合流マス（8・14）を通るか止まると、両陣営とも手札を合計10枚まで補給",
            "陣営の手札は合計12枚まで（超えたらすぐ選んで捨てる）。手札0枚ならカード勝負は数字0",
            "レーンのお店を通りすぎるとき、お店の陣営は「呼び込み」できる（通ればそこで止まる）"]
    for i, s_ in enumerate(turn):
        p.append(t(76, y + 60 + i * 36, s_, 17, INK, anchor="start"))

    # 3. カードの出し方
    y = 546
    box(y, 200, "カードの出し方（いつも同じ）", VIOLET)
    steps = ["① 出すカードを陣営で決めて勝負エリアに【裏向き】で置き、「準備OK」と言う（パスでも同じ）",
             "② そろったら手番プレイヤーの「せーの」で【全体に公開する】。置いていない陣営は「パス」",
             "③ ゲージを動かし、勝った／通ったカードの J・Q・K 効果としかけを処理",
             "④ 使ったカードは捨て札へ（補充はしない）"]
    for i, s in enumerate(steps):
        p.append(t(76, y + 60 + i * 36, s, 18.5, INK, anchor="start"))

    # 4. マスごとのゲージ
    y = 786
    box(y, 320, "マスごとのゲージの動き", "#E0A100")
    rows = [
        (art.angel(wings=False), "健康マス", ANGEL, "てんしが主役・あくまは横やり（どちらもパス可）", "主役 − 横やり だけ ＋ へ（マイナスなら0）"),
        (art.devil(tail=False), "誘惑マス", DEVIL, "あくまが主役・てんしは横やり（どちらもパス可）", "主役 − 横やり だけ − へ（マイナスなら0）"),
        (art.vs(), "カード勝負", VIOLET, "どちらでもマス：両陣営とも必ず1枚（またはペア）を出す。手札0なら数字0", "大きい方の陣営へ、差の分だけ動く"),
        (art.signpost(), "わかれ道", INK, "止まっても【通過しても】、どちらでもマスと同じカード勝負", "勝ったカードが 赤♥♦→健康レーン／黒♠♣→誘惑レーン"),
    ]
    for i, (icon, name, col, who, move) in enumerate(rows):
        ry = y + 62 + i * 60
        p.append(place(icon, 92, ry + 4, 46))
        p.append(t(126, ry + 11, name, 20, col, "900", "start"))
        p.append(t(280, ry - 2, who, 16.5, INK, anchor="start"))
        p.append(t(280, ry + 23, move, 16.5, INK_SOFT, anchor="start"))
    p.append(t(76, y + 302, "同数は引き分け（ゲージ動かず・効果なし。わかれ道は 1d2：奇数=健康）", 15.5, INK_SOFT, anchor="start"))

    # 5. ボードのしかけ
    y = 1146
    box(y, 250, "ボードのしかけ", "#3FA66B")
    gim = [
        (lambda ix, iy: art.suit_chip("♥", ix, iy, 18), "お気に入りスート +3", "健康／誘惑マスのお店の好きなスートで、主役が通すと +3"),
        (lambda ix, iy: art.star_badge(ix, iy, "×2", 24), "大勝負マス ×2", "合流マス（8・14）のカード勝負は、ゲージの動きが2倍（先に補給）"),
        (lambda ix, iy: pair_icon(ix, iy, 1.0), "ペア出し", "同じ数字2枚を1組で出すと、数字は2枚の合計"),
        (lambda ix, iy: cheer_icon(ix, iy, 1.1), "がんばれ +2／+4", "ゲージが相手側に4以上傾いている陣営は数字 +2、8以上なら +4"),
    ]
    for i, (draw, name, desc) in enumerate(gim):
        ry = y + 58 + i * 48
        p.append(draw(96, ry))
        p.append(t(136, ry + 7, name, 19, INK, "900", "start"))
        p.append(t(370, ry + 7, desc, 16, INK_SOFT, anchor="start"))

    # 6. 計算の順番
    y = 1436
    box(y, 250, "計算の順番（迷ったら上から）", VIOLET)
    calc = ["1 数字：カード（ペアは合計）→ 妨害なら0／♣半減 → がんばれ +2・+4 → 切り札 +3／−3",
            "2 差：健康／誘惑マスは 主役 − 横やり（0未満は0）、カード勝負は 大きい方 − 小さい方",
            "3 ボーナス（勝った／通ったカードだけ）：K の大逆転 +3、お気に入りスート +3",
            "4 2倍：大勝負マス、または おうえん団／ごほうびデー（重なっても2倍まで）",
            "5 おまもり／ごろ寝：その陣営に不利な向きの動きを0に",
            "6 ゲージを動かす（−10〜+10 で止まる）"]
    for i, s_ in enumerate(calc):
        p.append(t(76, y + 56 + i * 32, s_, 16.5, INK, anchor="start"))

    # 7. カード
    y = 1726
    box(y, 190, "カードの数字と効果（勝った／通ったときだけ）", ANGEL)
    cards = [("A〜10", "1〜10", "効果なし"),
             ("J", "11", "妨害：相手陣営が次に公開するカードを 数字0・効果なし に"),
             ("Q", "12", "先導：NPC をさらに1マス進める（先のマスも処理）"),
             ("K", "13", "大逆転：ゲージをさらに +3（自陣営側へ）")]
    for i, (c, n, e) in enumerate(cards):
        ry = y + 58 + i * 36
        p.append(t(76, ry, c, 21, INK, "900", "start"))
        p.append(t(190, ry, n, 19, INK_SOFT, "bold", "start"))
        p.append(t(270, ry, e, 17.5, INK, anchor="start"))

    # 8. 切り札
    y = 1956
    box(y, 270, "切り札カード（6枚から3枚選ぶ・1回だけ）", "#7B3FA0")
    p.append(t(76, y + 52, "てんし", 17, ANGEL, "900", "start"))
    p.append(t(230, y + 52, "あくま", 17, DEVIL, "900", "start"))
    p.append(t(400, y + 52, "効果（そえる＝数字カードと一緒に裏向きで置く）", 15, INK_SOFT, "bold", "start"))
    for i, (a, d) in enumerate(zip(TRUMPS["angel"], TRUMPS["devil"])):
        ry = y + 86 + i * 30
        eff = {"radio": "そえる：自陣営の数字 +3", "water": "そえる：相手陣営の数字 −3",
               "omamori": "そえる：ゲージが相手側へ動くなら0に", "map": "そえる：わかれ道のレーンを自陣営の側に",
               "cheer": "そえる：ゲージが自陣営側へ動くなら2倍", "early": "いつでも（自陣営の手番中）：2枚引く"}[a[0]]
        p.append(t(76, ry, a[1], 17, INK, "bold", "start"))
        p.append(t(230, ry, d[1], 17, INK, "bold", "start"))
        p.append(t(400, ry, eff, 17, INK, anchor="start"))

    y = 2266
    box(y, 150, "ハプニング表（1d6）", DEVIL)
    hap = ["1 忘れ物ニュース：何も起こらない", "2 てんし急接近：ゲージ +2", "3 あくまのささやき：ゲージ −2",
           "4 近道発見：1マス進む（先のマスも処理）", "5 寄り道：1マス戻る（処理しない）", "6 気分屋：手札1枚を捨てて1枚引く"]
    for i, s in enumerate(hap):
        col, row = divmod(i, 3)
        p.append(t(76 + col * 490, y + 52 + row * 34, s, 17.5, INK, anchor="start"))
    p.append("</svg>")
    return "\n".join(p)


# =====================================================================
# 切り札カード（400×600、800×1200px で書き出し）
# =====================================================================
TRUMPS = {
    "angel": [
        # id, 名前, アイコン, タイミング, 効果（行ごと）, ひとこと
        ("radio", "ラジオたいそう", "dumbbell", "そえる", ["自陣営のカードの数字", "+3"], "体はいつも、動けるようにしておくこと。"),
        ("water", "おみずをどうぞ", "bottle", "そえる", ["相手陣営のカードの数字", "−3"], "渇きは、空腹よりも先にやってくる。"),
        ("omamori", "おまもり", "omamori", "そえる", ["この公開でゲージが", "あくま側へ動くなら", "その動きを0にする"], "守られているのは、どちらのほうだろう。"),
        ("map", "ちずアプリ", "phone_map", "そえる", ["わかれ道で、勝ち負けに", "関係なくレーンを", "健康レーンにする"], "明るい道を選びなさい。人目のある道を。"),
        ("cheer", "おうえん団", "megaphone", "そえる", ["この公開でゲージが", "てんし側へ動くなら", "その動きを2倍にする"], "声援がやむと、町はおそろしく静かだ。"),
        ("early", "はやおき", "alarm", "いつでも", ["自陣営の手番中に使う", "山札から2枚引いて", "陣営の手札に加える"], "朝の道は、ひとりきりの人が多い。"),
    ],
    "devil": [
        ("oomori", "大盛りサービス", "burger", "そえる", ["自陣営のカードの数字", "+3"], "満腹のあいだは、だれも困らない。"),
        ("sleepy", "ねむけさそい", "zzz", "そえる", ["相手陣営のカードの数字", "−3"], "眠っているあいだは、町が静かでいい。"),
        ("gorone", "ごろ寝", "pillow", "そえる", ["この公開でゲージが", "てんし側へ動くなら", "その動きを0にする"], "動かないことも、ひとつのやさしさだ。"),
        ("smell", "いいにおい", "steam_smell", "そえる", ["わかれ道で、勝ち負けに", "関係なくレーンを", "誘惑レーンにする"], "においの元は、いつも厨房の奥にある。"),
        ("reward", "ごほうびデー", "cake", "そえる", ["この公開でゲージが", "あくま側へ動くなら", "その動きを2倍にする"], "今日の分は、もう食べたことにしよう。"),
        ("late", "よふかし", "moon", "いつでも", ["自陣営の手番中に使う", "山札から2枚引いて", "陣営の手札に加える"], "夜は長い。おなかは、また空く。"),
    ],
}


def trump_card(side, card):
    _id, name, icon, timing, lines, flavor = card
    color = ANGEL if side == "angel" else DEVIL
    tint = ANGEL_TINT if side == "angel" else DEVIL_TINT
    dark = mix(color, INK, 0.35)
    head = art.angel(wings=False) if side == "angel" else art.devil(tail=False)
    team = "てんしの切り札" if side == "angel" else "あくまの切り札"
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600" font-family="{FONT}">',
         DEFS,
         f'<rect x="4" y="4" width="392" height="592" rx="30" fill="{color}" stroke="{INK}" stroke-width="6"/>',
         f'<rect x="20" y="20" width="360" height="560" rx="20" fill="#FFFDF8" stroke="{INK}" stroke-width="3"/>',
         # タイミング
         f'<rect x="34" y="34" width="{len(timing) * 22 + 28}" height="36" rx="18" fill="{GOLD if timing == "いつでも" else color}" stroke="{INK}" stroke-width="3"/>',
         t(48, 59, timing, 19, INK if timing == "いつでも" else "#FFFFFF", "900", "start"),
         place(head, 340, 54, 58),
         # 名前
         t(200, 118, name, 40 if len(name) <= 6 else 34, dark, "900"),
         # イラスト
         f'<circle cx="200" cy="262" r="112" fill="{tint}" stroke="{INK}" stroke-width="3"/>',
         f'<circle cx="200" cy="262" r="112" fill="url(#stripeA)" opacity="0.5"/>',
         place(art.ICONS[icon](), 200, 262, 168),
         # 効果
         f'<rect x="40" y="396" width="320" height="126" rx="16" fill="{tint}" stroke="{color}" stroke-width="3"/>']
    n = len(lines)
    y0 = 459 - (n - 1) * 17
    for i, line in enumerate(lines):
        big = line in ("+3", "−3")
        p.append(t(200, y0 + i * 34 + (8 if big else 0), line, 40 if big else 22, INK, "900" if big else "bold"))
    p.append(ft(200, 548, flavor, 15 if len(flavor) <= 18 else 14))
    p.append(f'<path d="M110 566 L290 566" stroke="{color}" stroke-width="2" opacity="0.5"/>')
    p.append(t(200, 590, f"{team}・1回だけ", 13, "#FFFFFF", "900"))
    p.append("</svg>")
    return "\n".join(p)


def trump_back(side):
    color = ANGEL if side == "angel" else DEVIL
    tint = ANGEL_TINT if side == "angel" else DEVIL_TINT
    body = art.angel() if side == "angel" else art.devil()
    team = "てんしの切り札" if side == "angel" else "あくまの切り札"
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600" viewBox="0 0 400 600" font-family="{FONT}">',
        DEFS,
        f'<rect x="4" y="4" width="392" height="592" rx="30" fill="{color}" stroke="{INK}" stroke-width="6"/>',
        f'<rect x="20" y="20" width="360" height="560" rx="20" fill="{tint}" stroke="{INK}" stroke-width="3"/>',
        f'<rect x="20" y="20" width="360" height="560" rx="20" fill="url(#stripeA)"/>',
        f'<circle cx="200" cy="270" r="128" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>',
        place(body, 200, 266, 200),
        f'<rect x="70" y="440" width="260" height="56" rx="28" fill="{color}" stroke="{INK}" stroke-width="4"/>',
        t(200, 478, team, 26, "#FFFFFF", "900"),
        t(200, 540, "おかえりロード", 22, INK, "900"),
        "</svg>"])


def trump_sheet():
    """README・早見用の一覧（6×2 枚＋裏面2枚）"""
    k = 0.5
    cw, ch, gap = 400 * k, 600 * k, 24
    cols = 7
    w = cols * cw + (cols + 1) * gap
    h = 2 * ch + 3 * gap
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" font-family="{FONT}">',
         f'<rect width="{w:.0f}" height="{h:.0f}" fill="{PAPER}"/>']
    for r, side in enumerate(["angel", "devil"]):
        items = [trump_back(side)] + [trump_card(side, c) for c in TRUMPS[side]]
        for c, svg in enumerate(items):
            x = gap + c * (cw + gap)
            y = gap + r * (ch + gap)
            inner = svg.replace('<svg xmlns="http://www.w3.org/2000/svg" width="400" height="600"',
                                f'<svg x="{x:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{ch:.0f}"', 1)
            p.append(inner)
    p.append("</svg>")
    return "\n".join(p)


def main():
    (ASSETS / "board_route_gauge.svg").write_text(board(), encoding="utf-8")
    (ASSETS / "token_npc.svg").write_text(token(art.walker(), "NPC", "#E9744A", "#FDEBD6", 120, -10), encoding="utf-8")
    (ASSETS / "token_angel.svg").write_text(token(art.angel(), "てんし", ANGEL, ANGEL_TINT), encoding="utf-8")
    (ASSETS / "token_devil.svg").write_text(token(art.devil(), "あくま", DEVIL, DEVIL_TINT), encoding="utf-8")
    (ASSETS / "token_gauge.svg").write_text(token(art.heart_pulse(), "体調", INK, "#ECEAF2", 104, -12), encoding="utf-8")
    (ASSETS / "quick_reference.svg").write_text(quick_reference(), encoding="utf-8")
    cards = ASSETS / "cards"
    cards.mkdir(exist_ok=True)
    for side, items in TRUMPS.items():
        (cards / f"{side}_back.svg").write_text(trump_back(side), encoding="utf-8")
        for c in items:
            (cards / f"{side}_{c[0]}.svg").write_text(trump_card(side, c), encoding="utf-8")
    (ASSETS / "trump_cards_sheet.svg").write_text(trump_sheet(), encoding="utf-8")


if __name__ == "__main__":
    main()
