"""おかえりロードのオリジナル・イラスト（SVG パーツ）。

どの関数も 64×64 の座標系で描いた <g> 要素の中身を返す。
place(icon, x, y, size) で任意の位置・大きさに配置する。
線は INK の太線＋丸い角でそろえ、塗りはパレットの色だけを使う。
"""

INK = "#3A3550"
SW = 3.2  # 標準の線の太さ（64座標系）

S = f'stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round"'


def place(body, x, y, size, rotate=0):
    """64×64 のアイコンを、中心 (x, y)・一辺 size で配置する。"""
    k = size / 64
    rot = f" rotate({rotate} 32 32)" if rotate else ""
    return f'<g transform="translate({x - size / 2:.1f},{y - size / 2:.1f}) scale({k:.4f}){rot}">{body}</g>'


# ---------------------------------------------------------------- 場所アイコン
def sneaker():
    return f"""
<path d="M7 44 L8 28 Q9 24 13 24 L22 24 Q24 31 31 32 L44 34 Q57 36 57 45 L57 47 L7 47 Z" fill="#F07A5A" {S}/>
<path d="M22 24 Q24 31 31 32" fill="none" {S}/>
<path d="M14 30 L20 30 M15 36 L23 36" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round"/>
<rect x="5" y="45" width="54" height="8" rx="4" fill="#FFFFFF" {S}/>
<path d="M40 40 Q46 39 52 41" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round"/>"""


def home():
    return f"""
<rect x="40" y="10" width="7" height="14" fill="#B9705A" {S}/>
<path d="M14 30 L14 55 L50 55 L50 30" fill="#FFF1DC" {S}/>
<path d="M6 32 L32 9 L58 32" fill="#E9744A" {S}/>
<rect x="26" y="38" width="12" height="17" rx="2" fill="#9A6248" {S}/>
<circle cx="35" cy="47" r="1.4" fill="#FFE07A"/>
<rect x="17" y="35" width="7" height="7" rx="1.5" fill="#FFE59A" {S}/>
<rect x="41" y="35" width="7" height="7" rx="1.5" fill="#FFE59A" {S}/>
<path d="M32 27 C29 23 24 26 28 30 L32 33 L36 30 C40 26 35 23 32 27 Z" fill="#F25C82" stroke="none"/>"""


def store():
    return f"""
<rect x="9" y="22" width="46" height="34" rx="3" fill="#FFFFFF" {S}/>
<rect x="9" y="14" width="46" height="11" rx="3" fill="#56B07C" {S}/>
<path d="M17 14 L17 25 M27 14 L27 25 M37 14 L37 25 M47 14 L47 25" stroke="#FFFFFF" stroke-width="3"/>
<rect x="9" y="14" width="46" height="11" rx="3" fill="none" {S}/>
<rect x="14" y="31" width="20" height="16" rx="2" fill="#BFE3F7" {S}/>
<rect x="39" y="31" width="11" height="25" rx="2" fill="#E8F5FC" {S}/>
<path d="M17 44 L23 35" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>"""


def houses():
    return f"""
<path d="M36 32 L36 54 L58 54 L58 32" fill="#EAF2FF" {S}/>
<path d="M32 34 L47 20 L62 34" fill="#7AA6E0" {S}/>
<rect x="44" y="41" width="7" height="13" rx="1.5" fill="#7AA6E0" {S}/>
<path d="M6 30 L6 54 L32 54 L32 30" fill="#FFF3DD" {S}/>
<path d="M2 32 L19 15 L36 32" fill="#F0A35A" {S}/>
<rect x="12" y="38" width="8" height="8" rx="1.5" fill="#FFE59A" {S}/>
<rect x="22" y="40" width="6" height="14" rx="1.5" fill="#B9705A" {S}/>"""


def tree():
    return f"""
<rect x="28" y="38" width="8" height="18" rx="2" fill="#A86E4A" {S}/>
<circle cx="22" cy="30" r="12" fill="#6CC070" {S}/>
<circle cx="42" cy="30" r="12" fill="#6CC070" {S}/>
<circle cx="32" cy="20" r="13" fill="#7BCF7E" {S}/>
<path d="M25 22 Q28 16 34 15" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" opacity="0.8"/>
<path d="M10 56 L54 56" {S}/>
<circle cx="45" cy="52" r="3" fill="#F7A6C2" stroke="none"/><circle cx="17" cy="52" r="3" fill="#FFE07A" stroke="none"/>"""


def dumbbell():
    return f"""
<rect x="16" y="29" width="32" height="6" rx="3" fill="#C9CCD6" {S}/>
<rect x="8" y="18" width="9" height="28" rx="3" fill="#4C79C8" {S}/>
<rect x="47" y="18" width="9" height="28" rx="3" fill="#4C79C8" {S}/>
<rect x="3" y="23" width="6" height="18" rx="2.5" fill="#6E95D8" {S}/>
<rect x="55" y="23" width="6" height="18" rx="2.5" fill="#6E95D8" {S}/>
<path d="M11 22 L11 30 M50 22 L50 30" stroke="#FFFFFF" stroke-width="2.4" stroke-linecap="round" opacity="0.8"/>
<path d="M24 12 L26 8 M32 11 L32 6 M40 12 L38 8" {S} fill="none"/>"""


def candy():
    return f"""
<path d="M18 32 L5 21 L8 32 L5 43 Z" fill="#7FD3E8" {S}/>
<path d="M46 32 L59 21 L56 32 L59 43 Z" fill="#7FD3E8" {S}/>
<ellipse cx="32" cy="32" rx="16" ry="13" fill="#FF8DB3" {S}/>
<path d="M22 24 Q30 32 24 41 M32 20 Q40 30 33 44 M41 22 Q47 30 43 40" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
<ellipse cx="32" cy="32" rx="16" ry="13" fill="none" {S}/>"""


def ramen():
    return f"""
<path d="M20 6 L28 30 M28 5 L33 30" stroke="#C9935E" stroke-width="3.4" stroke-linecap="round"/>
<path d="M8 30 L56 30 Q55 50 32 53 Q9 50 8 30 Z" fill="#E9504A" {S}/>
<path d="M14 38 L20 34 L26 38 L32 34 L38 38 L44 34 L50 38" fill="none" stroke="#FFFFFF" stroke-width="2.4" stroke-linejoin="round"/>
<ellipse cx="32" cy="30" rx="24" ry="5" fill="#F9D27A" {S}/>
<path d="M17 30 Q20 27 23 30 Q26 33 29 30 Q32 27 35 30 Q38 33 41 30 Q44 27 47 30" fill="none" stroke="#E0A93C" stroke-width="2"/>
<circle cx="42" cy="28" r="4" fill="#FFFFFF" {S}/><circle cx="42" cy="28" r="1.6" fill="#F7A6C2"/>
<rect x="24" y="53" width="16" height="5" rx="2" fill="#E9504A" {S}/>"""


def vending():
    return f"""
<rect x="14" y="5" width="36" height="54" rx="4" fill="#EF5E5E" {S}/>
<rect x="19" y="10" width="26" height="24" rx="2" fill="#E8F5FC" {S}/>
<rect x="22" y="14" width="5" height="9" rx="1.5" fill="#56B07C"/><rect x="29.5" y="14" width="5" height="9" rx="1.5" fill="#F0A35A"/><rect x="37" y="14" width="5" height="9" rx="1.5" fill="#4C79C8"/>
<path d="M21 26 L43 26" stroke="{INK}" stroke-width="2"/>
<circle cx="24" cy="30" r="1.5" fill="{INK}"/><circle cx="32" cy="30" r="1.5" fill="{INK}"/><circle cx="40" cy="30" r="1.5" fill="{INK}"/>
<rect x="19" y="45" width="26" height="8" rx="2" fill="#5A2E3E" {S}/>
<rect x="41" y="37" width="4" height="5" rx="1" fill="#FFE07A" stroke="none"/>"""


def carrot():
    return f"""
<path d="M30 16 Q22 6 18 10 Q24 14 27 19 M34 16 Q38 4 44 7 Q38 12 36 19 M32 16 Q31 6 32 3" fill="#6CC070" {S}/>
<path d="M22 20 Q32 14 42 20 Q40 38 32 60 Q24 38 22 20 Z" fill="#F58A2E" {S}/>
<path d="M26 28 L31 29 M28 38 L33 38 M30 47 L34 46" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M36 24 Q37 30 35 36" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" opacity="0.8"/>"""


def bench():
    return f"""
<path d="M13 40 L13 54 M51 40 L51 54" {S} fill="none"/>
<rect x="6" y="14" width="52" height="8" rx="3" fill="#C98A55" {S}/>
<rect x="6" y="24" width="52" height="8" rx="3" fill="#C98A55" {S}/>
<rect x="4" y="35" width="56" height="8" rx="3" fill="#B87745" {S}/>
<path d="M14 32 L14 35 M50 32 L50 35" {S}/>
<path d="M18 50 Q22 46 26 50" fill="none" stroke="#6CC070" stroke-width="3" stroke-linecap="round"/>
<path d="M40 52 Q43 48 46 52" fill="none" stroke="#6CC070" stroke-width="3" stroke-linecap="round"/>"""


def burger():
    return f"""
<path d="M9 28 Q10 10 32 10 Q54 10 55 28 Z" fill="#F2B35B" {S}/>
<ellipse cx="24" cy="18" rx="1.6" ry="1" fill="#FFFFFF"/><ellipse cx="33" cy="15" rx="1.6" ry="1" fill="#FFFFFF"/><ellipse cx="41" cy="20" rx="1.6" ry="1" fill="#FFFFFF"/><ellipse cx="29" cy="23" rx="1.6" ry="1" fill="#FFFFFF"/>
<path d="M7 30 L13 34 L19 30 L25 34 L31 30 L37 34 L43 30 L49 34 L57 30" fill="#7BCF7E" {S}/>
<rect x="7" y="33" width="50" height="9" rx="4.5" fill="#8A4B33" {S}/>
<path d="M9 42 L55 42 L52 47 L12 47 Z" fill="#FFD84E" {S}/>
<path d="M9 47 L55 47 Q55 55 46 55 L18 55 Q9 55 9 47 Z" fill="#F2B35B" {S}/>"""


def lantern():
    return f"""
<path d="M32 3 L32 9" {S}/>
<rect x="21" y="8" width="22" height="6" rx="2" fill="{INK}"/>
<ellipse cx="32" cy="32" rx="19" ry="20" fill="#EF5E5E" {S}/>
<path d="M14 26 Q32 30 50 26 M13 34 Q32 38 51 34 M16 42 Q32 45 48 42" fill="none" stroke="#C23F45" stroke-width="2"/>
<ellipse cx="32" cy="32" rx="19" ry="20" fill="none" {S}/>
<rect x="21" y="50" width="22" height="6" rx="2" fill="{INK}"/>
<path d="M28 56 L28 62 M32 56 L32 62 M36 56 L36 62" stroke="#FFD84E" stroke-width="2.4" stroke-linecap="round"/>
<path d="M22 22 Q24 16 30 15" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" opacity="0.7"/>"""


def cake():
    return f"""
<path d="M8 34 L44 22 L56 30 L56 50 L20 58 L8 50 Z" fill="#FFF6E8" {S}/>
<path d="M8 34 L20 42 L56 30" fill="none" {S}/>
<path d="M20 42 L20 58" {S}/>
<path d="M8 42 L20 50 M8 46 L20 54" stroke="#F7A6C2" stroke-width="3"/>
<path d="M20 50 L56 39" stroke="#F7A6C2" stroke-width="3"/>
<path d="M8 34 L44 22 L56 30 L20 42 Z" fill="#FFFFFF" {S}/>
<path d="M36 17 Q30 15 31 22 Q32 28 37 28 Q42 28 43 22 Q44 15 38 17 Z" fill="#EF4E6A" {S}/>
<path d="M36 16 L35 12 M38 16 L41 13" stroke="#56B07C" stroke-width="2.6" stroke-linecap="round"/>"""


def burst():
    import math
    pts = []
    for i in range(16):
        r = 29 if i % 2 == 0 else 20
        a = math.pi * 2 * i / 16 - math.pi / 2
        pts.append(f"{32 + r * math.cos(a):.1f},{32 + r * math.sin(a):.1f}")
    return f"""
<polygon points="{' '.join(pts)}" fill="#FFD23F" {S}/>
<rect x="28.5" y="15" width="7" height="21" rx="3.5" fill="{INK}"/>
<circle cx="32" cy="44" r="4.2" fill="{INK}"/>"""


def signpost():
    return f"""
<rect x="29" y="8" width="6" height="52" rx="2" fill="#A86E4A" {S}/>
<path d="M10 12 L46 12 L56 20 L46 28 L10 28 Z" fill="#5B9BE0" {S}/>
<path d="M54 32 L18 32 L8 40 L18 48 L54 48 Z" fill="#EE6D8E" {S}/>
<path d="M17 20 L39 20" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
<path d="M25 40 L47 40" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
<path d="M18 60 L46 60" {S}/>"""


def vs():
    return f"""
<path d="M6 10 L58 10 L58 46 L36 46 L26 58 L26 46 L6 46 Z" fill="#9B7BE0" {S}/>
<text x="32" y="38" text-anchor="middle" font-size="25" font-weight="900" fill="#FFFFFF" font-family="'Noto Sans CJK JP',sans-serif">VS</text>"""


ICONS = {
    "sneaker": sneaker, "home": home, "store": store, "houses": houses, "tree": tree,
    "dumbbell": dumbbell, "candy": candy, "ramen": ramen, "vending": vending, "carrot": carrot,
    "bench": bench, "burger": burger, "lantern": lantern, "cake": cake, "burst": burst,
    "signpost": signpost, "vs": vs,
}


# ---------------------------------------------------------------- キャラクター
def angel(wings=True):
    """てんしちゃん（64×64）"""
    w = ""
    if wings:
        w = f"""
<path d="M15 30 Q6 22 1 26 Q0 34 4 38 Q2 44 8 46 Q9 51 16 48 Z" fill="#FFFFFF" {S}/>
<path d="M5 33 Q9 35 13 34 M8 41 Q12 42 15 40" fill="none" stroke="#C9D6EA" stroke-width="2" stroke-linecap="round"/>
<path d="M49 30 Q58 22 63 26 Q64 34 60 38 Q62 44 56 46 Q55 51 48 48 Z" fill="#FFFFFF" {S}/>
<path d="M59 33 Q55 35 51 34 M56 41 Q52 42 49 40" fill="none" stroke="#C9D6EA" stroke-width="2" stroke-linecap="round"/>"""
    return f"""{w}
<ellipse cx="32" cy="9" rx="13" ry="4.2" fill="none" stroke="#F2C230" stroke-width="4"/>
<ellipse cx="32" cy="9" rx="13" ry="4.2" fill="none" stroke="#FFF2B0" stroke-width="1.4"/>
<circle cx="32" cy="36" r="20" fill="#FFE3CC" {S}/>
<path d="M13 32 Q14 16 32 16 Q50 16 51 32 Q46 24 40 25 Q36 20 30 24 Q22 21 13 32 Z" fill="#FFD66B" {S}/>
<path d="M22 37 Q25 34 28 37 M36 37 Q39 34 42 37" fill="none" {S}/>
<ellipse cx="20" cy="43" rx="3.6" ry="2.4" fill="#FFAFC0"/><ellipse cx="44" cy="43" rx="3.6" ry="2.4" fill="#FFAFC0"/>
<path d="M28 44 Q32 48 36 44" fill="none" {S}/>"""


def devil(tail=True):
    """あくまくん（64×64）"""
    t = ""
    if tail:
        t = f"""
<path d="M48 48 Q60 50 58 38" fill="none" {S}/>
<path d="M58 38 L53 36 L59 31 L62 37 Z" fill="#7B3FA0" {S}/>"""
    return f"""{t}
<path d="M17 24 L12 7 L26 18 Z" fill="#7B3FA0" {S}/>
<path d="M47 24 L52 7 L38 18 Z" fill="#7B3FA0" {S}/>
<circle cx="32" cy="36" r="20" fill="#C9A3F0" {S}/>
<path d="M14 30 Q20 18 32 18 Q44 18 50 30 Q42 25 32 27 Q22 25 14 30 Z" fill="#7B3FA0" {S}/>
<path d="M20 33 L28 36 M44 33 L36 36" {S} fill="none"/>
<circle cx="25" cy="39" r="2.4" fill="{INK}"/><circle cx="39" cy="39" r="2.4" fill="{INK}"/>
<ellipse cx="19" cy="45" rx="3.4" ry="2.2" fill="#F48FB1"/><ellipse cx="45" cy="45" rx="3.4" ry="2.2" fill="#F48FB1"/>
<path d="M25 46 Q32 52 39 46" fill="none" {S}/>
<path d="M35 48 L36.5 52 L38 47.5" fill="#FFFFFF" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>"""


def walker():
    """NPC（おさんぽさん）（64×64）"""
    return f"""
<ellipse cx="32" cy="58" rx="16" ry="3.5" fill="{INK}" opacity="0.15"/>
<path d="M24 50 L22 57 M40 50 L42 57" {S}/>
<path d="M14 40 Q14 22 32 22 Q50 22 50 40 Q50 52 32 52 Q14 52 14 40 Z" fill="#FFE8C8" {S}/>
<path d="M15 31 Q18 12 32 12 Q46 12 49 31 Q32 26 15 31 Z" fill="#F0A35A" {S}/>
<path d="M44 29 Q54 28 56 32 Q50 33 46 32" fill="#F0A35A" {S}/>
<circle cx="26" cy="38" r="2.4" fill="{INK}"/><circle cx="38" cy="38" r="2.4" fill="{INK}"/>
<ellipse cx="21" cy="43" rx="3.2" ry="2.2" fill="#FFAFC0"/><ellipse cx="43" cy="43" rx="3.2" ry="2.2" fill="#FFAFC0"/>
<path d="M29 44 Q32 47 35 44" fill="none" {S}/>"""


def heart_pulse():
    """体調ゲージのマーカー（64×64）"""
    return f"""
<path d="M32 56 C10 42 4 30 8 20 C12 10 26 8 32 19 C38 8 52 10 56 20 C60 30 54 42 32 56 Z" fill="#F25C82" {S}/>
<path d="M12 33 L22 33 L26 25 L31 41 L35 29 L38 33 L52 33" fill="none" stroke="#FFFFFF" stroke-width="3.6" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M14 20 Q17 14 23 14" fill="none" stroke="#FFFFFF" stroke-width="2.8" stroke-linecap="round" opacity="0.7"/>"""


def suit_chip(suit, x, y, r=15):
    """お気に入りスートのバッジ"""
    color = "#E0344F" if suit in "♥♦" else INK
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.6"/>'
            f'<text x="{x}" y="{y + r * 0.42:.1f}" text-anchor="middle" font-size="{r * 1.3:.0f}" '
            f'font-weight="bold" fill="{color}" font-family="\'DejaVu Sans\',sans-serif">{suit}</text>')


def star_badge(x, y, text, r=22, fill="#FFC531"):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.62
        a = math.pi * 2 * i / 10 - math.pi / 2
        pts.append(f"{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}")
    return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + 5.5:.1f}" text-anchor="middle" font-size="{r * 0.68:.0f}" font-weight="900" '
            f'fill="{INK}">{text}</text>')


# ---------------------------------------------------------------- 切り札用イラスト
def bottle():
    return f"""
<rect x="26" y="4" width="12" height="8" rx="2" fill="#4C79C8" {S}/>
<path d="M24 12 L40 12 L42 20 Q48 24 48 32 L48 54 Q48 60 42 60 L22 60 Q16 60 16 54 L16 32 Q16 24 22 20 Z" fill="#CFEAFB" {S}/>
<path d="M17 36 L47 36 L47 54 Q47 59 42 59 L22 59 Q17 59 17 54 Z" fill="#8CCBF2"/>
<path d="M16 32 Q16 24 22 20 L24 12 L40 12 L42 20 Q48 24 48 32 L48 54 Q48 60 42 60 L22 60 Q16 60 16 54 Z" fill="none" {S}/>
<path d="M23 40 L23 52" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
<path d="M30 46 Q32 42 34 46 Q34 49 32 49 Q30 49 30 46 Z" fill="#FFFFFF"/>"""


def zzz():
    return f"""
<path d="M10 40 Q12 26 28 26 Q40 26 44 36 Q52 36 54 44 Q56 54 44 56 L18 56 Q8 56 10 40 Z" fill="#E3D8F2" {S}/>
<path d="M20 44 Q23 41 26 44 M32 44 Q35 41 38 44" fill="none" {S}/>
<path d="M30 6 L40 6 L30 16 L40 16" fill="none" stroke="#7B3FA0" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M44 14 L51 14 L44 21 L51 21" fill="none" stroke="#7B3FA0" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M52 2 L57 2 L52 7 L57 7" fill="none" stroke="#7B3FA0" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>"""


def omamori():
    return f"""
<path d="M32 4 Q24 4 26 12" fill="none" stroke="#F2C230" stroke-width="3" stroke-linecap="round"/>
<path d="M32 4 Q40 4 38 12" fill="none" stroke="#F2C230" stroke-width="3" stroke-linecap="round"/>
<path d="M18 16 L32 10 L46 16 L46 56 Q46 60 42 60 L22 60 Q18 60 18 56 Z" fill="#5B9BE0" {S}/>
<rect x="24" y="22" width="16" height="30" rx="3" fill="#FFFFFF" {S}/>
<path d="M32 30 C29 26 24 29 28 33 L32 37 L36 33 C40 29 35 26 32 30 Z" fill="#F25C82"/>
<path d="M27 43 L37 43 M27 47 L35 47" stroke="#C9D6EA" stroke-width="2.4" stroke-linecap="round"/>"""


def pillow():
    return f"""
<path d="M6 26 Q4 14 16 16 L48 14 Q60 13 58 26 Q62 36 58 46 Q60 58 48 56 L16 56 Q4 58 6 46 Q2 36 6 26 Z" fill="#F8C9D6" {S}/>
<path d="M14 24 Q32 20 50 24" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.8"/>
<path d="M22 38 Q25 35 28 38 M36 38 Q39 35 42 38" fill="none" {S}/>
<path d="M28 46 Q32 48 36 46" fill="none" {S}/>"""


def phone_map():
    return f"""
<rect x="14" y="4" width="36" height="56" rx="7" fill="{INK}" {S}/>
<rect x="18" y="11" width="28" height="42" rx="3" fill="#E3F4E9"/>
<path d="M18 30 L46 24 M24 11 L30 53 M18 44 L46 40" stroke="#FFFFFF" stroke-width="3"/>
<path d="M24 52 Q30 36 40 26" fill="none" stroke="#2F7FC8" stroke-width="3" stroke-dasharray="3 3" stroke-linecap="round"/>
<path d="M40 14 Q34 14 34 20 Q34 25 40 31 Q46 25 46 20 Q46 14 40 14 Z" fill="#EF4E6A" stroke="{INK}" stroke-width="2.2"/>
<circle cx="40" cy="20" r="2.4" fill="#FFFFFF"/>"""


def megaphone():
    return f"""
<path d="M10 26 L22 26 L46 12 L46 52 L22 38 L10 38 Z" fill="#FFC531" {S}/>
<rect x="18" y="38" width="8" height="14" rx="2" fill="#F0A35A" {S}/>
<path d="M52 22 Q58 32 52 42 M56 16 Q64 32 56 48" fill="none" stroke="#F25C82" stroke-width="3.2" stroke-linecap="round"/>
<path d="M26 28 L40 20" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.8"/>"""


def alarm():
    return f"""
<path d="M14 18 Q12 8 22 8 M50 18 Q52 8 42 8" fill="none" {S}/>
<path d="M20 56 L16 60 M44 56 L48 60" {S}/>
<circle cx="32" cy="34" r="22" fill="#FFE07A" {S}/>
<circle cx="32" cy="34" r="16" fill="#FFFFFF" {S}/>
<path d="M32 24 L32 34 L39 38" fill="none" {S}/>
<path d="M50 6 L52 2 M56 10 L60 8 M58 16 L62 16" stroke="#F0A35A" stroke-width="2.6" stroke-linecap="round"/>"""


def moon():
    return f"""
<path d="M40 6 Q18 8 16 32 Q16 56 42 58 Q52 58 58 50 Q34 52 30 32 Q28 14 40 6 Z" fill="#FFD84E" {S}/>
<circle cx="50" cy="16" r="2.4" fill="#FFD84E"/><circle cx="56" cy="30" r="1.8" fill="#FFD84E"/><circle cx="44" cy="28" r="1.4" fill="#FFD84E"/>
<path d="M24 34 Q27 37 30 34" fill="none" {S}/>
<ellipse cx="26" cy="42" rx="3" ry="2" fill="#F7A6C2"/>"""


def steam_smell():
    return f"""
<path d="M14 58 Q8 46 20 40 L44 40 Q56 46 50 58 Z" fill="#F2B35B" {S}/>
<ellipse cx="32" cy="40" rx="18" ry="5" fill="#8A4B33" {S}/>
<path d="M20 32 Q14 24 22 18 Q28 12 22 4" fill="none" stroke="#C9A3F0" stroke-width="3.6" stroke-linecap="round"/>
<path d="M32 32 Q26 24 34 18 Q40 12 34 4" fill="none" stroke="#C9A3F0" stroke-width="3.6" stroke-linecap="round"/>
<path d="M44 32 Q38 24 46 18 Q52 12 46 4" fill="none" stroke="#C9A3F0" stroke-width="3.6" stroke-linecap="round"/>"""


ICONS.update({
    "bottle": bottle, "zzz": zzz, "omamori": omamori, "pillow": pillow, "phone_map": phone_map,
    "megaphone": megaphone, "alarm": alarm, "moon": moon, "steam_smell": steam_smell,
})
