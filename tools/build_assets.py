#!/usr/bin/env python3
"""おかえりロードの画像素材（SVG）を生成するスクリプト。

    python3 tools/build_assets.py          # assets/*.svg を生成
    python3 tools/render_png.py            # SVG → PNG 書き出し（Playwright + Chromium）

色・寸法はこのファイル冒頭の定数でまとめて管理する。
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

FONT = "'Noto Sans CJK JP','Hiragino Sans','Yu Gothic','Meiryo',sans-serif"

# ---- パレット（てんし＝青、あくま＝ローズ で全素材を統一） ----
INK = "#3A3550"
INK_SOFT = "#7A7490"
PAPER = "#FBF6EC"
ROAD = "#E8DCC4"
ANGEL = "#2F7FC8"
ANGEL_TINT = "#E2EFFB"
DEVIL = "#D0436A"
DEVIL_TINT = "#FBE3EA"

TYPES = {
    #        枠色       塗り       絵文字  ラベル
    "start": ("#3FA66B", "#E3F4E9", "🚶", "スタート"),
    "goal": ("#E07B1F", "#FDEBD6", "🏠", "ゴール"),
    "health": (ANGEL, ANGEL_TINT, "😇", "健康"),
    "temptation": (DEVIL, DEVIL_TINT, "😈", "誘惑"),
    "either": ("#7A5CC6", "#EEE8FA", "❓", "どちらでも"),
    "fork": (INK, "#ECEAF2", "🔀", "わかれ道"),
    "happening": ("#D99A00", "#FFF3D2", "❗", "ハプニング"),
    "plain": ("#A3A1AE", "#F2F1F4", "➖", "素通り"),
}


def t(x, y, s, size, fill=INK, weight="normal", anchor="middle", extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


# =====================================================================
# ボード（1920×1080、CCFOLIA の前景 80×45 マス用）
# =====================================================================
W, H = 1920, 1080
TILE = 122
COLP = 142          # 列ピッチ
ROWP = 134          # 行ピッチ
X0 = 50 + TILE / 2  # 列0の中心
Y0 = 92 + TILE / 2  # 行0の中心


def cx(c):
    return X0 + c * COLP


def cy(r):
    return Y0 + r * ROWP


# 行：0=わかれ道①健康レーン 1=序盤・中盤の本道 2=わかれ道①誘惑レーン
#     3=わかれ道②健康レーン 4=終盤の本道 5=わかれ道②誘惑レーン
SQUARES = [
    # id, type, 列, 行, 名前（ラベル上書き）, 場所
    ("1", "start", 0, 1, None, "おでかけ"),
    ("2", "either", 1, 1, None, "コンビニ"),
    ("3", "plain", 2, 1, None, "じゅうたくがい"),
    ("4", "fork", 3, 1, "わかれ道①", "赤→健康／黒→誘惑"),
    ("5A", "health", 4, 0, None, "こうえん"),
    ("6A", "happening", 5, 0, None, "？？？"),
    ("7A", "health", 6, 0, None, "ジム"),
    ("5B", "temptation", 4, 2, None, "だがしや"),
    ("6B", "happening", 5, 2, None, "？？？"),
    ("7B", "temptation", 6, 2, None, "ラーメン屋"),
    ("8", "either", 7, 1, "どちらでも", "じはんき（合流）"),
    ("9", "plain", 8, 1, None, "じゅうたくがい"),
    ("10", "fork", 8, 4, "わかれ道②", "赤→健康／黒→誘惑"),
    ("11A", "health", 7, 3, None, "やおや"),
    ("12A", "either", 6, 3, None, "こうえんのベンチ"),
    ("13A", "happening", 5, 3, None, "？？？"),
    ("11B", "temptation", 7, 5, None, "ファストフード"),
    ("12B", "either", 6, 5, None, "屋台"),
    ("13B", "happening", 5, 5, None, "？？？"),
    ("14", "either", 4, 4, "どちらでも", "コンビニ（合流）"),
    ("15", "temptation", 3, 4, None, "ケーキ屋"),
    ("16", "health", 2, 4, None, "こうえん"),
    ("17", "happening", 1, 4, None, "？？？"),
    ("18", "goal", 0, 4, None, "おうち"),
]
POS = {s[0]: (cx(s[2]), cy(s[3])) for s in SQUARES}

ROUTES = [
    # (経路, 道の色)
    (["1", "2", "3", "4"], ROAD),
    (["4", "5A", "6A", "7A", "8"], "#C9DFF4"),
    (["4", "5B", "6B", "7B", "8"], "#F5CDD8"),
    (["8", "9", "10"], ROAD),
    (["10", "11A", "12A", "13A", "14"], "#C9DFF4"),
    (["10", "11B", "12B", "13B", "14"], "#F5CDD8"),
    (["14", "15", "16", "17", "18"], ROAD),
]


def road_svg():
    out = []
    for path, color in ROUTES:
        pts = " ".join(f"{POS[p][0]:.1f},{POS[p][1]:.1f}" for p in path)
        out.append(f'<polyline points="{pts}" fill="none" stroke="#D8C9AC" stroke-width="44" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="36" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<polyline points="{pts}" fill="none" stroke="#FFFFFF" stroke-width="3" '
                   f'stroke-dasharray="10 12" stroke-linecap="round" opacity="0.9"/>')
    # 進行方向の矢印（各区間の中点）
    import math
    for path, _ in ROUTES:
        for a, b in zip(path, path[1:]):
            (x1, y1), (x2, y2) = POS[a], POS[b]
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            out.append(f'<path d="M-7,-9 L6,0 L-7,9" transform="translate({mx:.1f},{my:.1f}) rotate({ang:.1f})" '
                       f'fill="none" stroke="#9C8A68" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    return "\n".join(out)


def tile_svg(sid, typ, label, place):
    stroke, fill, emoji, default_label = TYPES[typ]
    label = label or default_label
    x, y = POS[sid]
    x0, y0 = x - TILE / 2, y - TILE / 2
    out = []
    if typ == "fork":
        fill_attr = "url(#forkFill)"
    else:
        fill_attr = fill
    out.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{TILE}" height="{TILE}" rx="20" '
               f'fill="{fill_attr}" stroke="{stroke}" stroke-width="4" filter="url(#shadow)"/>')
    # 番号バッジ
    bw = 30 if len(sid) == 1 else (38 if len(sid) == 2 else 46)
    out.append(f'<rect x="{x0 + 8:.1f}" y="{y0 + 8:.1f}" width="{bw}" height="26" rx="13" fill="{stroke}"/>')
    out.append(t(x0 + 8 + bw / 2, y0 + 27, sid, 17, "#FFFFFF", "bold"))
    out.append(t(x + 10, y + 6, emoji, 40, extra="font-family=\"'Noto Color Emoji',sans-serif\""))
    out.append(t(x, y + 34, label, 18 if len(label) <= 5 else 16, INK, "bold"))
    out.append(t(x, y + 52, place, 12 if len(place) <= 8 else 11, INK_SOFT))
    return "\n".join(out)


def slot(x, y, w, h, label, color, sub=None, dashed=True):
    dash = 'stroke-dasharray="9 7"' if dashed else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" fill-opacity="0.6" '
           f'stroke="{color}" stroke-width="3" {dash}/>',
           t(x + w / 2, y + h / 2 + 6, label, 18, color, "bold")]
    if sub:
        out.append(t(x + w / 2, y + h / 2 + 28, sub, 12, INK_SOFT))
    return "\n".join(out)


def card_area_svg():
    px, py, pw, ph = 1352, 24, 544, 1032
    out = [f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="28" fill="#FFFFFF" fill-opacity="0.7" '
           f'stroke="#E2D6BE" stroke-width="2"/>']
    # 山札・捨て札・除外
    out.append(t(px + 28, py + 46, "カード置き場", 22, INK, "bold", "start"))
    out.append(t(px + pw - 28, py + 46, "※枠の大きさは目安", 13, INK_SOFT, anchor="end"))
    cw, ch = 132, 176
    gx = (pw - 3 * cw) / 4
    y1 = py + 70
    out.append(slot(px + gx, y1, cw, ch, "山札", INK, "トランプのデッキ", dashed=False))
    out.append(slot(px + 2 * gx + cw, y1, cw, ch, "捨て札", INK_SOFT, "表向きで置く"))
    out.append(slot(px + 3 * gx + 2 * cw, y1, cw, ch, "除外", INK_SOFT, "ジョーカー"))
    # 勝負エリア
    y2 = y1 + ch + 30
    out.append(f'<rect x="{px + 16}" y="{y2}" width="{pw - 32}" height="276" rx="20" fill="#F6F2FB"/>')
    out.append(t(px + pw / 2, y2 + 36, "勝負エリア", 22, "#7A5CC6", "bold"))
    out.append(t(px + pw / 2, y2 + 60, "裏向きで置いて「せーの」で公開", 14, INK_SOFT))
    bw, bh = 150, 186
    out.append(slot(px + 56, y2 + 76, bw, bh, "てんし", ANGEL, "😇 健康マスでは主役"))
    out.append(slot(px + pw - 56 - bw, y2 + 76, bw, bh, "あくま", DEVIL, "😈 誘惑マスでは主役"))
    out.append(t(px + pw / 2, y2 + 76 + bh / 2 + 10, "VS", 30, "#7A5CC6", "bold"))
    # 手札置き場
    y3 = y2 + 276 + 26
    hh = 214
    out.append(slot(px + 16, y3, pw - 32, hh, "てんし陣営の手札", ANGEL, "裏向きで置き「自分だけ見る」"))
    out.append(slot(px + 16, y3 + hh + 18, pw - 32, hh, "あくま陣営の手札", DEVIL, "裏向きで置き「自分だけ見る」"))
    return "\n".join(out)


def gauge_svg():
    gx, gy, cwid, ch = 50, 950, 60, 66
    out = [t(gx, gy - 16, "体調ゲージ", 22, INK, "bold", "start"),
           t(gx + 130, gy - 16, "ゲームの開始時は 0。ゴールした瞬間の位置で勝敗が決まる", 14, INK_SOFT, anchor="start")]
    for i, v in enumerate(range(-10, 11)):
        x = gx + i * cwid
        if v < 0:
            k = (-v) / 10
            fill = mix("#FFFFFF", DEVIL, 0.12 + 0.55 * k)
        elif v > 0:
            k = v / 10
            fill = mix("#FFFFFF", ANGEL, 0.12 + 0.55 * k)
        else:
            fill = "#FFFFFF"
        out.append(f'<rect x="{x}" y="{gy}" width="{cwid}" height="{ch}" fill="{fill}" stroke="#FFFFFF" stroke-width="3"/>')
        label = f"+{v}" if v > 0 else str(v)
        color = "#FFFFFF" if abs(v) >= 6 else INK
        out.append(t(x + cwid / 2, gy + ch / 2 + 8, label, 22 if v else 26, color, "bold"))
    out.append(f'<rect x="{gx}" y="{gy}" width="{21 * cwid}" height="{ch}" rx="6" fill="none" stroke="#D8C9AC" stroke-width="3"/>')
    out.append(f'<rect x="{gx + 10 * cwid}" y="{gy - 4}" width="{cwid}" height="{ch + 8}" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>')
    out.append(t(gx, gy + ch + 26, "😈 −1以下：あくま陣営の勝ち", 17, DEVIL, "bold", "start"))
    out.append(t(gx + 21 * cwid / 2, gy + ch + 26, "0：気まぐれ判定（1d6 奇数てんし／偶数あくま）", 15, INK_SOFT))
    out.append(t(gx + 21 * cwid, gy + ch + 26, "てんし陣営の勝ち：+1以上 😇", 17, ANGEL, "bold", "end"))
    return "\n".join(out)


def legend_svg():
    # 左側の空きスペース（列0〜3・行2〜3）に凡例
    x, y = cx(0) - TILE / 2, cy(2) - TILE / 2 + 6
    w = 4 * COLP - (COLP - TILE)
    h = 2 * ROWP - 24
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#FFFFFF" fill-opacity="0.75" stroke="#E2D6BE" stroke-width="2"/>',
           t(x + 22, y + 36, "マスの種類", 19, INK, "bold", "start")]
    items = [
        ("health", "健康", "てんしが出す／あくまは横やり"),
        ("temptation", "誘惑", "あくまが出す／てんしは横やり"),
        ("either", "どちらでも", "両陣営でカード勝負"),
        ("fork", "わかれ道", "カード勝負＋色でレーン決定"),
        ("happening", "ハプニング", "1d6 でハプニング表"),
        ("plain", "素通り", "何も起こらない"),
    ]
    for i, (typ, name, desc) in enumerate(items):
        col, row = divmod(i, 3)
        ix = x + 22 + col * (w / 2 - 6)
        iy = y + 54 + row * 52
        stroke, fill, emoji, _ = TYPES[typ]
        f = "url(#forkFill)" if typ == "fork" else fill
        out.append(f'<rect x="{ix}" y="{iy}" width="40" height="40" rx="10" fill="{f}" stroke="{stroke}" stroke-width="3"/>')
        out.append(t(ix + 20, iy + 29, emoji, 22, extra="font-family=\"'Noto Color Emoji',sans-serif\""))
        out.append(t(ix + 52, iy + 17, name, 15, INK, "bold", "start"))
        out.append(t(ix + 52, iy + 36, desc, 12, INK_SOFT, anchor="start"))
    # レーン凡例
    ly = y + h - 22
    out.append(f'<line x1="{x + 22}" y1="{ly}" x2="{x + 62}" y2="{ly}" stroke="#C9DFF4" stroke-width="14" stroke-linecap="round"/>')
    out.append(t(x + 74, ly + 6, "健康レーン（赤 ♥♦ で勝つと）", 14, ANGEL, "bold", "start"))
    lx = x + w / 2 + 16
    out.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 40}" y2="{ly}" stroke="#F5CDD8" stroke-width="14" stroke-linecap="round"/>')
    out.append(t(lx + 52, ly + 6, "誘惑レーン（黒 ♠♣ で勝つと）", 14, DEVIL, "bold", "start"))
    return "\n".join(out)


def flow_svg():
    # 左下の空きスペース（列0〜4・行5）に手番の流れ
    x, y = cx(0) - TILE / 2, cy(5) - TILE / 2 + 4
    w = 5 * COLP - (COLP - TILE) - 12
    h = TILE - 8
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="#FFFFFF" fill-opacity="0.75" stroke="#E2D6BE" stroke-width="2"/>',
           t(x + 22, y + 34, "手番の流れ", 19, INK, "bold", "start")]
    steps = ["① 1d6 で NPC を進める", "② 止まったマスを処理する", "③ 使ったカードを捨てて補充", "④ 相手陣営に手番を渡す"]
    for i, s in enumerate(steps):
        col, row = divmod(i, 2)
        out.append(t(x + 22 + col * (w / 2), y + 66 + row * 30, s, 15, INK, anchor="start"))
    return "\n".join(out)


def mix(c1, c2, k):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * k):02X}" for x, y in zip(a, b))


DEFS = f"""<defs>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#5A4A2A" flood-opacity="0.18"/>
</filter>
<linearGradient id="forkFill" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{ANGEL_TINT}"/><stop offset="0.49" stop-color="{ANGEL_TINT}"/>
  <stop offset="0.51" stop-color="{DEVIL_TINT}"/><stop offset="1" stop-color="{DEVIL_TINT}"/>
</linearGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse">
  <circle cx="4" cy="4" r="1.6" fill="#E9DFCB"/>
</pattern>
</defs>"""


def board():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">',
             DEFS,
             f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
             f'<rect width="{W}" height="{H}" fill="url(#dots)"/>']
    # タイトル（列0〜3・行0 の空きスペース）
    tx, ty = cx(0) - TILE / 2, cy(0) - 18
    parts.append(t(tx, ty, "おかえりロード", 46, INK, "900", "start"))
    parts.append(t(tx + 4, ty + 38, "〜天使とあくまのさんぽ道〜", 22, INK_SOFT, "bold", "start"))
    parts.append(t(tx + 4, ty + 66, "1d6 で進み、止まったマスでカードを出し合おう", 15, INK_SOFT, anchor="start"))
    parts.append(road_svg())
    for sid, typ, _c, _r, label, place in SQUARES:
        parts.append(tile_svg(sid, typ, label, place))
    parts.append(legend_svg())
    parts.append(flow_svg())
    parts.append(gauge_svg())
    parts.append(card_area_svg())
    parts.append("</svg>")
    return "\n".join(parts)


# =====================================================================
# コマ（200×200、600×600px で書き出し）
# =====================================================================
def token(emoji, label, color, tint):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200" font-family="{FONT}">
<defs>
<radialGradient id="g" cx="0.35" cy="0.3" r="0.8">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{tint}"/>
</radialGradient>
</defs>
<circle cx="100" cy="100" r="92" fill="{color}"/>
<circle cx="100" cy="100" r="80" fill="url(#g)"/>
<text x="100" y="114" text-anchor="middle" font-size="76" font-family="'Noto Color Emoji',sans-serif">{emoji}</text>
<rect x="44" y="140" width="112" height="34" rx="17" fill="{color}"/>
<text x="100" y="164" text-anchor="middle" font-size="20" font-weight="bold" fill="#FFFFFF">{escape(label)}</text>
</svg>
"""


# =====================================================================
# 早見表（1080×1440、スクリーンパネル用）
# =====================================================================
def quick_reference():
    QW, QH = 1080, 1440
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{QW}" height="{QH}" viewBox="0 0 {QW} {QH}" font-family="{FONT}">',
         DEFS,
         f'<rect width="{QW}" height="{QH}" fill="{PAPER}"/>',
         f'<rect width="{QW}" height="{QH}" fill="url(#dots)"/>',
         t(60, 86, "おかえりロード 早見表", 44, INK, "900", "start"),
         t(QW - 60, 86, "ルールブック v3", 18, INK_SOFT, anchor="end")]

    def box(y, h, title, color):
        p.append(f'<rect x="40" y="{y}" width="{QW - 80}" height="{h}" rx="24" fill="#FFFFFF" stroke="{color}" stroke-width="3"/>')
        p.append(f'<rect x="40" y="{y}" width="12" height="{h}" rx="6" fill="{color}"/>')
        p.append(t(76, y + 44, title, 26, color, "bold", "start"))

    # 1. 勝敗
    y = 120
    box(y, 150, "勝ち負け", INK)
    p.append(t(76, y + 86, "NPC がゴール（マス18）に着いた瞬間の体調ゲージで決まる。", 20, INK, anchor="start"))
    p.append(t(76, y + 122, "+1以上 → てんし陣営の勝ち　／　−1以下 → あくま陣営の勝ち　／　0 → 1d6（奇数てんし）", 18, INK_SOFT, anchor="start"))

    # 2. カードの出し方
    y = 290
    box(y, 220, "カードの出し方（いつも同じ）", "#7A5CC6")
    steps = ["① 出すカードを陣営で決めて勝負エリアに【裏向き】で置き、「準備OK」と言う（パスでも同じ）",
             "② そろったら手番プレイヤーの「せーの」で【全体に公開する】。置いていない陣営は「パス」",
             "③ ゲージを動かし、勝った／通ったカードの J・Q・K 効果を処理",
             "④ 使ったカードは捨て札へ。出した人はすぐ1枚補充する"]
    for i, s in enumerate(steps):
        p.append(t(76, y + 88 + i * 36, s, 19, INK, anchor="start"))

    # 3. 場面ごとのゲージ
    y = 530
    box(y, 330, "マスごとのゲージの動き", "#D99A00")
    rows = [
        ("😇 健康マス", ANGEL, "てんしが主役・あくまは横やり（どちらもパス可）", "主役 − 横やり だけ ＋ へ（マイナスなら0）"),
        ("😈 誘惑マス", DEVIL, "あくまが主役・てんしは横やり（どちらもパス可）", "主役 − 横やり だけ − へ（マイナスなら0）"),
        ("❓ どちらでも", "#7A5CC6", "両陣営とも必ず1枚（手札0なら数字0）", "大きい方の陣営へ、差の分だけ動く"),
        ("🔀 わかれ道", INK, "どちらでもマスと同じカード勝負", "勝ったカードが 赤♥♦→健康レーン／黒♠♣→誘惑レーン"),
    ]
    for i, (name, col, who, move) in enumerate(rows):
        ry = y + 80 + i * 62
        p.append(t(76, ry + 8, name, 21, col, "bold", "start"))
        p.append(t(270, ry - 4, who, 17, INK, anchor="start"))
        p.append(t(270, ry + 22, move, 17, INK_SOFT, anchor="start"))
    p.append(t(76, y + 316, "同数は引き分け（ゲージ動かず・効果なし。わかれ道は 1d2：奇数=健康）", 16, INK_SOFT, anchor="start"))

    # 4. カード
    y = 880
    box(y, 250, "カードの数字と効果（勝った／通ったときだけ）", ANGEL)
    cards = [("A〜10", "1〜10", "効果なし"),
             ("J", "11", "妨害：相手陣営が次に公開するカードを 数字0・効果なし に"),
             ("Q", "12", "先導：NPC をさらに1マス進める（先のマスも処理）"),
             ("K", "13", "大逆転：ゲージをさらに +3（自陣営側へ）")]
    for i, (c, n, e) in enumerate(cards):
        ry = y + 92 + i * 40
        p.append(t(76, ry, c, 22, INK, "bold", "start"))
        p.append(t(190, ry, n, 20, INK_SOFT, anchor="start"))
        p.append(t(270, ry, e, 18, INK, anchor="start"))

    # 5. ハプニング
    y = 1150
    box(y, 250, "ハプニング表（1d6）", DEVIL)
    hap = ["1 忘れ物ニュース：何も起こらない", "2 てんし急接近：ゲージ +2", "3 あくまのささやき：ゲージ −2",
           "4 近道発見：1マス進む（先のマスも処理）", "5 寄り道：1マス戻る（処理しない）", "6 気分屋：手札1枚を捨てて1枚引く"]
    for i, s in enumerate(hap):
        col, row = divmod(i, 3)
        p.append(t(76 + col * 490, y + 92 + row * 46, s, 19, INK, anchor="start"))
    p.append("</svg>")
    return "\n".join(p)


def main():
    (ASSETS / "board_route_gauge.svg").write_text(board(), encoding="utf-8")
    (ASSETS / "token_npc.svg").write_text(token("🚶", "NPC", "#E07B1F", "#FDEBD6"), encoding="utf-8")
    (ASSETS / "token_angel.svg").write_text(token("😇", "てんし", ANGEL, ANGEL_TINT), encoding="utf-8")
    (ASSETS / "token_devil.svg").write_text(token("😈", "あくま", DEVIL, DEVIL_TINT), encoding="utf-8")
    (ASSETS / "token_gauge.svg").write_text(token("💗", "体調", INK, "#ECEAF2"), encoding="utf-8")
    (ASSETS / "quick_reference.svg").write_text(quick_reference(), encoding="utf-8")


if __name__ == "__main__":
    main()
