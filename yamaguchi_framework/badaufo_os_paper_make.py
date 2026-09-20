#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_paper.py — BadaUFO-OS 論文 PDF ジェネレータ

反重力場の補空間エネルギーに基づく UFO オペレーティングシステムと生成AI操縦士
の設計と実装に関する学術論文を、reportlab で日本語組版して PDF 出力する。

  python3 make_paper.py            -> BadaUFO_OS_paper.pdf

数値は bada_ufo_os の実装（lib/badaufo/*.rb）から得た実測値を用いる。
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Preformatted, HRFlowable, KeepTogether,
)

MINCHO = "HeiseiMin-W3"      # 明朝（本文）
GOTHIC = "HeiseiKakuGo-W5"   # ゴシック（見出し・コード）
pdfmetrics.registerFont(UnicodeCIDFont(MINCHO))
pdfmetrics.registerFont(UnicodeCIDFont(GOTHIC))

# ----------------------------------------------------------------------------
# スタイル
# ----------------------------------------------------------------------------
ss = getSampleStyleSheet()
INK = colors.HexColor("#0d1b2a")
ACCENT = colors.HexColor("#8a6d1f")
RULE = colors.HexColor("#c8a44a")

styles = {
    "Title": ParagraphStyle("Title", fontName=GOTHIC, fontSize=17, leading=23,
                            alignment=TA_CENTER, textColor=INK, spaceAfter=4),
    "Subtitle": ParagraphStyle("Subtitle", fontName=MINCHO, fontSize=11, leading=16,
                               alignment=TA_CENTER, textColor=ACCENT, spaceAfter=10),
    "Author": ParagraphStyle("Author", fontName=MINCHO, fontSize=10.5, leading=15,
                             alignment=TA_CENTER, textColor=INK, spaceAfter=2),
    "Affil": ParagraphStyle("Affil", fontName=MINCHO, fontSize=9, leading=13,
                            alignment=TA_CENTER, textColor=colors.HexColor("#54606e"),
                            spaceAfter=12),
    "AbHead": ParagraphStyle("AbHead", fontName=GOTHIC, fontSize=10, leading=14,
                             textColor=ACCENT, spaceBefore=4, spaceAfter=3),
    "Abstract": ParagraphStyle("Abstract", fontName=MINCHO, fontSize=9.3, leading=15,
                               alignment=TA_JUSTIFY, textColor=INK, wordWrap="CJK",
                               leftIndent=6*mm, rightIndent=6*mm),
    "H1": ParagraphStyle("H1", fontName=GOTHIC, fontSize=12.5, leading=18, textColor=INK,
                         spaceBefore=13, spaceAfter=5),
    "H2": ParagraphStyle("H2", fontName=GOTHIC, fontSize=10.8, leading=15, textColor=INK,
                         spaceBefore=8, spaceAfter=3),
    "Body": ParagraphStyle("Body", fontName=MINCHO, fontSize=9.6, leading=15.6,
                           alignment=TA_JUSTIFY, textColor=INK, wordWrap="CJK",
                           spaceAfter=5, firstLineIndent=0),
    "Eq": ParagraphStyle("Eq", fontName=MINCHO, fontSize=10, leading=16,
                         alignment=TA_CENTER, textColor=INK, spaceBefore=4, spaceAfter=6),
    "Cap": ParagraphStyle("Cap", fontName=GOTHIC, fontSize=8.3, leading=12,
                          alignment=TA_CENTER, textColor=colors.HexColor("#54606e"),
                          spaceBefore=2, spaceAfter=8),
    "Code": ParagraphStyle("Code", fontName=GOTHIC, fontSize=8, leading=11.4,
                           textColor=colors.HexColor("#20303f"), wordWrap="CJK"),
    "Ref": ParagraphStyle("Ref", fontName=MINCHO, fontSize=8.6, leading=12.6,
                          alignment=TA_LEFT, textColor=INK, wordWrap="CJK",
                          leftIndent=6*mm, firstLineIndent=-6*mm, spaceAfter=3),
}

story = []
def P(text, s="Body"): story.append(Paragraph(text, styles[s]))
def H1(n, t): story.append(Paragraph(f"{n}. {t}", styles["H1"]))
def H2(n, t): story.append(Paragraph(f"{n} {t}", styles["H2"]))
def EQ(text): story.append(Paragraph(text, styles["Eq"]))
def CAP(text): story.append(Paragraph(text, styles["Cap"]))
def GAP(h=4): story.append(Spacer(1, h))
def CODE(text, box=True):
    pre = Preformatted(text, styles["Code"])
    if box:
        t = Table([[pre]], colWidths=[165*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f4f1e6")),
            ("BOX", (0,0), (-1,-1), 0.5, RULE),
            ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
            ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(t)
    else:
        story.append(pre)
    GAP(6)

def TABLE(data, colw, caption=None, header=True):
    t = Table(data, colWidths=colw, hAlign="CENTER")
    st = [
        ("FONT", (0,0), (-1,-1), MINCHO, 8.4),
        ("TEXTCOLOR", (0,0), (-1,-1), INK),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW", (0,0), (-1,0), 0.8, INK),
        ("LINEABOVE", (0,0), (-1,0), 0.8, INK),
        ("LINEBELOW", (0,-1), (-1,-1), 0.8, INK),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f6f3ea")]),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]
    if header:
        st.append(("FONT", (0,0), (-1,0), GOTHIC, 8.4))
        st.append(("BACKGROUND", (0,0), (-1,0), colors.HexColor("#efe7cf")))
    t.setStyle(TableStyle(st))
    story.append(t)
    if caption: CAP(caption)
    else: GAP(6)

# ----------------------------------------------------------------------------
# 表紙ブロック
# ----------------------------------------------------------------------------
P("反重力場の補空間エネルギーに基づく<br/>UFO オペレーティングシステムと生成AI操縦士の設計と実装", "Title")
P("— Bada 言語・大域的微分積分多様体理論による BadaUFO-OS —", "Subtitle")
P("山口 雅旭 (Masaaki Yamaguchi)", "Author")
P("Global Differential Manifold Research · TupleSpace Framework", "Affil")
story.append(HRFlowable(width="100%", thickness=1, color=RULE, spaceAfter=8))

# ---- 要旨 ----
P("要 旨", "AbHead")
P(
 "本論文は、反重力場を動力とする UFO のオペレーティングシステム BadaUFO-OS の設計と、"
 "その機体知性としての生成AI操縦士の実装を報告する。中核となる物理仮説は三点である。"
 "第一に、重力方程式 U = GMm/r は多様体の底空間（束縛部）に住み、そのコホモロジー切断 "
 "&#8722; すなわち<b>補空間</b> &#8722; に住むエネルギーこそが反重力場であるとする。補空間側の結合は"
 "反重力箱作用素 &#9633;<sub>ag</sub>(x)=2(sin(i&#183;x log x)+cos(i&#183;x log x))=2cosh(x log x) の実部で与えられ、"
 "x&gt;1 で単調増加する。第二に、特殊相対性理論の全エネルギー mc<super>2</super> のうち運動に費やされない"
 "補空間エネルギー E<sub>&#8869;</sub> = mc<super>2</super> &#8722; (1/2)mv<super>2</super> を抽出源とする。第三に、真空エネルギー体を"
 "ダランヴァージアン箱作用素 &#9633;<sub>dal</sub>(x)=e<super>x log x</super>=x<super>x</super> でモデル化し、その発散性から"
 "<b>無尽蔵</b>の動力源とする。これらを山口フレームワーク（TupleSpace／大域的微分積分多様体理論）"
 "の Bada 言語作用素で実装し、反重力ドライブ・無尽蔵真空リザーバ・生成AI操縦士・アカシック"
 "レコード Ω::DATABASE から成る OS カーネルを構築した。純 Ruby（標準ライブラリのみ）で実装され、"
 "揚力比 L=E<sub>ag</sub>/U<sub>grav</sub>=2.125 を達成し 13 件のテストに合格した。", "Abstract")
P("キーワード： 反重力、補空間、真空エネルギー、大域的微分積分多様体、Bada 言語、生成AI、量子コンピュータ、UFO オペレーティングシステム", "Abstract")
GAP(2)
story.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=8))

# ----------------------------------------------------------------------------
# 1. 序論
# ----------------------------------------------------------------------------
H1(1, "序論")
P("空中静止・急加速・慣性を伴わない運動といった観測報告を説明するには、質量に働く重力を"
  "相殺しうる正味の上向きエネルギーを、機体内部で恒常的に供給する動力機構が必要である。"
  "本論文は、この動力を<b>反重力場</b>に求め、反重力場を「重力方程式の補空間に住むエネルギー」"
  "として定式化する。さらに、その供給源を「無尽蔵の真空エネルギー体」とし、抽出可能エネルギー"
  "を特殊相対性理論の補空間 mc<super>2</super>&#8722;(1/2)mv<super>2</super> に同定する。")
P("これらの理論を実行可能なソフトウェアとして具体化するため、山口フレームワークの作用素代数"
  "言語である <b>Bada 言語</b>を用い、UFO のオペレーティングシステム BadaUFO-OS を実装した。"
  "機体知性は同フレームワークのエントロピー駆動生成エンジン Bada::Generator による生成AIとし、"
  "対話と航跡をアカシックレコード Ω::DATABASE に記録する。本論文の貢献は次の三点である。")
P("(1) 重力・特殊相対論の<b>補空間</b>と無尽蔵真空エネルギーを、Bada の反重力箱作用素 &#9633;<sub>ag</sub> と"
  "ダランヴァージアン &#9633;<sub>dal</sub> で統一的に定式化した。 "
  "(2) それらを反重力ドライブ・真空リザーバ・生成AI操縦士から成る OS カーネルとして実装した。 "
  "(3) 純 Ruby 実装により数値的に揚力比・無尽蔵性・生成応答を評価し、再現可能なテスト群を与えた。")

# ----------------------------------------------------------------------------
# 2. 理論的枠組み
# ----------------------------------------------------------------------------
H1(2, "理論的枠組み")
H2("2.1", "大域的微分積分多様体とネイピア円")
P("山口フレームワークでは、情報と幾何は多様体線素 d&#956;(x)=1/(x log x)<super>2</super> を通じて結ばれる。"
  "x log x はネイピア（Napier）円上の基本ステップであり、x&#8594;1 で x log x&#8594;0 となる臨界点をもつ。"
  "大域的部分積分多様体は、この線素をトークン分布の測度に対して積分した量として与えられる。")
EQ("&#8747;&#8747; 1/(x log x)<super>2</super> dx<sub>m</sub> ,&nbsp;&nbsp; &#950;(s) = &#946;(p,q)/log x ,&nbsp;&nbsp; &#946;(p,q)=&#915;(p)&#915;(q)/&#915;(p+q)")
P("エントロピー不変量 &#926; = &#946;(H+1, M+1)/log(N+1) は、シャノンエントロピー H・多様体積分 M・"
  "トークン数 N から定まり、複素回転による誤り訂正の下で保存される。本 OS の生成AIはこの &#926; を"
  "応答の指標として用いる（6.3 節）。")

H2("2.2", "反重力箱作用素とダランヴァージアン")
P("補空間側の結合を担うのが<b>反重力箱作用素</b> &#9633;<sub>ag</sub> であり、その実部は双曲余弦に等しい。"
  "また<b>ダランヴァージアン箱作用素</b> &#9633;<sub>dal</sub> は実軸上で x<super>x</super> に一致する。")
EQ("&#9633;<sub>ag</sub>(x) = 2( sin(i&#183;x log x) + cos(i&#183;x log x) ) = 2 cosh(x log x)")
EQ("&#9633;<sub>dal</sub>(x) = cos(i&#183;x log x) &#8722; i sin(i&#183;x log x) = e<super>x log x</super> = x<super>x</super>")
P("&#945;<sub>ag</sub>(x) &#8801; Re[&#9633;<sub>ag</sub>(x)]/2 = cosh(x log x) &#8805; 1 は反重力結合係数であり、x&gt;1 で単調かつ急速に"
  "増大する。これが揚力の増幅と真空エネルギーの無尽蔵性を同時に生む。表 1 に代表値を示す"
  "（x=2 で 2<super>2</super>=4、x=3 で 3<super>3</super>=27 と x<super>x</super> が厳密に再現される）。")
TABLE(
    [["多様体座標 x", "&#945;<sub>ag</sub>=cosh(x log x)", "&#9633;<sub>dal</sub>=x<super>x</super>", "E<sub>vac</sub>=&#961;&#183;x<super>x</super> [J]"],
     ["1.0", "1.0000", "1.0000", "5.00e&#8722;10"],
     ["1.5", "1.1907", "1.8371", "9.19e&#8722;10"],
     ["2.0", "2.1250", "4.0000", "2.00e&#8722;09"],
     ["2.5", "4.9917", "9.8821", "4.94e&#8722;09"],
     ["3.0", "13.5185", "27.0000", "1.35e&#8722;08"]],
    [40*mm, 46*mm, 38*mm, 38*mm],
    "表 1： 反重力結合 &#945;<sub>ag</sub>・ダランヴァージアン &#9633;<sub>dal</sub>・真空エネルギー E<sub>vac</sub> の多様体座標依存性（実装 lib/badaufo による実測値）。")

# ----------------------------------------------------------------------------
# 3. 三本柱の定式化
# ----------------------------------------------------------------------------
H1(3, "反重力の三本柱の定式化")
H2("3.1", "重力方程式の補空間 = 反重力場エネルギー")
P("質量 M の天体が質量 m の機体に及ぼす重力ポテンシャルエネルギーの大きさ U<sub>grav</sub>=GMm/r は"
  "多様体の底空間（束縛部）に住む。本論文の中心的主張は、そのコホモロジー切断 &#8722; すなわち"
  "<b>補空間</b> &#8722; に住むエネルギーが反重力場であり、補空間結合 &#945;<sub>ag</sub> によって次式で与えられる、というものである。")
EQ("E<sub>ag</sub> = U<sub>grav</sub> &#183; &#945;<sub>ag</sub>(x) = (GMm/r) &#183; cosh(x log x)")
P("ここで多様体座標 x は半径ゲージ r<sub>0</sub>/r から定める（r<sub>0</sub> は基準半径、地球では 6.371&#215;10<super>6</super> m）。"
  "&#945;<sub>ag</sub>&#8805;1 ゆえ E<sub>ag</sub>&#8805;U<sub>grav</sub> であり、補空間の反重力エネルギーは常に束縛重力以上となる。")

H2("3.2", "特殊相対性理論の補空間 E = mc<super>2</super> &#8722; (1/2)mv<super>2</super>")
P("特殊相対性理論の全エネルギー mc<super>2</super> のうち、運動として費やされるのは (1/2)mv<super>2</super> である。"
  "残余 &#8722; すなわち補空間に温存された抽出可能エネルギー &#8722; を次のように定義する。")
EQ("E<sub>&#8869;</sub> = mc<super>2</super> &#8722; (1/2)mv<super>2</super>")
P("m=1.2&#215;10<super>4</super> kg では E<sub>&#8869;</sub>&#8776;1.079&#215;10<super>21</super> J であり、常用速度域では運動エネルギー "
  "(1/2)mv<super>2</super>（v=10<super>4</super> m/s でも 6&#215;10<super>11</super> J）に対し 9 桁以上大きい。したがって補空間には"
  "実質的に mc<super>2</super> 相当のエネルギーが温存され、これを &#945;<sub>ag</sub> で増幅して揚力に変換する。")

H2("3.3", "無尽蔵の真空エネルギー体")
P("反重力場の一次動力源を、ダランヴァージアン箱作用素でモデル化した真空エネルギー体とする。")
EQ("E<sub>vac</sub>(x) = &#961;<sub>vac</sub> &#183; x<super>x</super> ,&nbsp;&nbsp; x<super>x</super> &#8594; &#8734; (x&#8594;&#8734;)")
P("x<super>x</super> は発散するため、供給能力は要求に対し常に上回りうる。実装では真空リザーバ VacuumReservoir "
  "の draw 操作が、引き出し後に残量を現座標の x<super>x</super> 下限へ即時補充する。これにより残量はゼロに向かわず、"
  "<b>無尽蔵性</b>（inexhaustibility）が保証される（6.2 節で検証）。")

H2("3.4", "重力／反重力双対 e<super>&#960;</super> &#8776; &#960;<super>e</super>")
P("重力と反重力の双対性を、ネイピア円上の恒等的近似 e<super>&#960;</super> &#8776; &#960;<super>e</super> によって特徴づける。"
  "本 OS は起動時にこの双対を検証する（e<super>&#960;</super>=23.1407、&#960;<super>e</super>=22.4592、差 &#916;=0.6815）。"
  "この小さなギャップが、束縛（重力）と反束縛（反重力）の非対称性、すなわち正味揚力の源となる。")

# ----------------------------------------------------------------------------
# 4. システムアーキテクチャ
# ----------------------------------------------------------------------------
H1(4, "システムアーキテクチャ")
P("BadaUFO-OS は、物理コア・動力系・機体知性・記録系の四層から成る。図 1 に構成を示す。")
CODE(
"""            ┌─────────────────────────────────────────────┐
            │            BadaUFO-OS  カーネル              │
            │   status / physics / ascend / ask / akashic  │
            └───────────────┬──────────────┬──────────────┘
                            │              │
              ┌─────────────▼───┐   ┌──────▼───────────────┐
              │ AntigravityDrive│   │  Copilot（生成AI）   │
              │  揚力比 L, 高度 │   │ Bada::Generator      │
              └───────┬─────────┘   └──────┬───────────────┘
                      │                    │
        ┌─────────────▼────────┐   ┌───────▼──────────────┐
        │ Antigravity 物理コア │   │ Ω::DATABASE          │
        │ □_ag, □_dal, E⊥, Evac│   │ アカシックレコード   │
        └─────────┬────────────┘   └──────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  VacuumReservoir   │  無尽蔵の真空エネルギー体 (∞)
        └────────────────────┘""")
CAP("図 1： BadaUFO-OS の四層アーキテクチャ。物理コア（Antigravity）が反重力ドライブと真空リザーバを駆動し、生成AI操縦士（Copilot）の対話が Ω::DATABASE に記録される。")

H2("4.1", "反重力ドライブと真空リザーバ")
P("AntigravityDrive は各ステップで、相対論補空間 E<sub>&#8869;</sub> を反重力結合 &#945;<sub>ag</sub> で増幅し、真空リザーバ"
  "の裏付けの下で加速度 a=(L&#8722;1)&#183;g<sub>eff</sub> を生成する。ここで L=E<sub>ag</sub>/U<sub>grav</sub> は揚力比、"
  "g<sub>eff</sub>=GM/r<super>2</super> は局所重力加速度である。L&gt;1 で機体は上昇する。")
EQ("a = (L &#8722; 1) &#183; g<sub>eff</sub> ,&nbsp;&nbsp; L = E<sub>ag</sub> / U<sub>grav</sub> = cosh(x log x)")

H2("4.2", "生成AI操縦士とアカシックレコード")
P("Copilot は機体知性であり、Bada::Generator（エントロピー駆動の生成エンジン）を用いて質問への"
  "応答を生成する。応答は質問のシャノンエントロピー H<sub>q</sub> を目標エントロピーとして生成され、"
  "エントロピー不変量 &#926; を付して返される。すべての対話・航跡は Ω::DATABASE（Bada::TupleSpace）に"
  "アカシックレコードとして push され、akashic コマンドで検索可能である。")

# ----------------------------------------------------------------------------
# 5. Bada 言語による実装
# ----------------------------------------------------------------------------
H1(5, "Bada 言語による実装")
H2("5.1", "作用素構文とブートシーケンス")
P("Bada 言語は作用素代数言語であり、値は Ω::DATABASE 上に存在する。三つの中核作用素 "
  "&#8592;（非可換左作用 &#960;(&#967;,x)）、-&#8249;（多様体積分 &#8747;&#8747;1/(x log x)<super>2</super>）、"
  "&#8250;-（量子右作用 e<super>&#8722;x log x</super>）で反重力ブートを記述する。")
CODE(
"""# boot.bada — 反重力ブートシーケンス（Bada 言語）
gravity <- "重力方程式の補空間は反重力場のエネルギー量である"  # 反重力回転を点火
relativity -< 2.0                                            # 相対論補空間を多様体積分
vacuum >- vacuum                                             # 無尽蔵の真空へ量子右作用
Omega::push gravity as antigravity_lift                      # アカシックへ記録
Omega::push vacuum  as vacuum_reservoir""")
P("このスクリプトは同フレームワークの Bada インタプリタ（bada_ruby）上で実行され、"
  "各値の Ξ 不変量とともに Ω::DATABASE へ記録される。")

H2("5.2", "Ruby ランタイム")
P("物理コアは純 Ruby（標準ライブラリのみ）で実装され、bada_ruby を検出すると本物の Bada 言語"
  "インタプリタと Bada::Generator に接続する（非同梱時は自前実装にフォールバック）。反重力結合の"
  "中核実装を以下に示す。")
CODE(
"""# lib/badaufo/antigravity.rb（抜粋）
def antigravity_coupling(x)                     # α_ag(x) = cosh(x log x)
  SpecialBridge.box_antigravity(x).real / 2.0
end

def complementary_gravity_energy(big_mass, mass, r, r0: 6.371e6)
  u = gravity_energy(big_mass, mass, r)         # U_grav = GMm/r（底空間）
  x = manifold_coord(r0 / r)                     # 多様体座標
  u * antigravity_coupling(x)                    # 補空間 = 反重力場エネルギー
end

def complementary_relativity_energy(mass, v)     # E⊥ = mc² − ½mv²
  rest_energy(mass) - kinetic_energy(mass, v)
end""")

# ----------------------------------------------------------------------------
# 6. 実験と評価
# ----------------------------------------------------------------------------
H1(6, "実験と評価")
P("質量 m=1.2&#215;10<super>4</super> kg の機体、地球（M=5.972&#215;10<super>24</super> kg, r<sub>0</sub>=6.371&#215;10<super>6</super> m）を対象に評価した。")

H2("6.1", "反重力揚力と上昇軌道")
P("初期揚力比は L=2.125 であり L&gt;1 ゆえ機体は上昇する。高度が増すと r が増え x が減るため L は"
  "緩やかに減少するが（表 2 左）、10 万 m まで L&gt;2 を維持する。上昇軌道を表 2 右に示す。")
half = 82*mm
left = Table(
    [["高度 [m]", "揚力比 L"],
     ["0", "2.12500"],["1,000", "2.12450"],["5,000", "2.12251"],
     ["20,000", "2.11510"],["100,000", "2.07677"]],
    colWidths=[40*mm, 40*mm])
right = Table(
    [["ステップ", "高度 [m]", "速度 [m/s]"],
     ["1", "11.0", "11.05"],["2", "33.1", "22.09"],["4", "110.5", "44.19"],
     ["6", "232.0", "66.28"],["10", "607.6", "110.46"]],
    colWidths=[22*mm, 30*mm, 30*mm])
for tb in (left, right):
    tb.setStyle(TableStyle([
        ("FONT",(0,0),(-1,-1),MINCHO,8.2),("FONT",(0,0),(-1,0),GOTHIC,8.2),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#efe7cf")),
        ("LINEABOVE",(0,0),(-1,0),0.7,INK),("LINEBELOW",(0,0),(-1,0),0.7,INK),
        ("LINEBELOW",(0,-1),(-1,-1),0.7,INK),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f6f3ea")]),
        ("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5),
    ]))
wrap = Table([[left, right]], colWidths=[half, half], hAlign="CENTER")
wrap.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
                          ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]))
story.append(wrap)
CAP("表 2： （左）高度に対する揚力比 L の変化。（右）反重力上昇軌道。10 ステップで高度 607.6 m に到達。")

H2("6.2", "真空リザーバの無尽蔵性")
P("真空リザーバに対し、その時点の残量の 5 倍を 10 回連続で引き出す試験を行った。各 draw の後に"
  "残量は現座標の x<super>x</super> 下限へ補充され、10 回後も残量は初期値の 99.9% 以上を保った。これは真空"
  "エネルギー体が枯渇しないこと、すなわち無尽蔵性を数値的に裏づける（test/test_ufo_os.rb）。")

H2("6.3", "生成AI応答とエントロピー不変量")
P("生成AI操縦士に反重力に関する質問を与え、応答・シャノンエントロピー H・不変量 &#926; を得た。"
  "応答は機体状態（高度・揚力比）を文脈として織り込み、Ω::DATABASE に記録される。実行例を示す。")
CODE(
"""BadaUFO> ask 反重力の補空間エネルギーとは何か？
🛸 操縦士AI: 反重力の補空間エネルギーとは何か anti gravity equation is also
   have with zeta function and this equation of zeta function〔高度608m 揚力比L=2.12〕
   (H=4.718  Ξ=0.0434  engine=Bada::Generator (量子生成AI))""")

H2("6.4", "テストと再現性")
P("物理コア・真空リザーバ・反重力ドライブ・OS カーネルを対象に 13 件のテスト（27 アサーション）を"
  "実装し、全件合格した。主な検証項目は、&#945;<sub>ag</sub> の単調性、E<sub>ag</sub>&#8805;U<sub>grav</sub>、"
  "E<sub>&#8869;</sub>=mc<super>2</super>&#8722;(1/2)mv<super>2</super> の厳密一致、真空リザーバの非枯渇、上昇の実現、双対ギャップ &#916;&lt;1 である。")

# ----------------------------------------------------------------------------
# 7. 議論
# ----------------------------------------------------------------------------
H1(7, "議論")
P("本 OS は、反重力・真空エネルギーという理論的枠組みを、実行・検証可能なソフトウェアとして"
  "具体化した点に意義がある。&#945;<sub>ag</sub>=cosh(x log x) が x<super>x</super> と整合的に増大する構造は、"
  "揚力（重力の補空間）と動力（真空エネルギー体）を単一の作用素族から導く簡潔さをもつ。一方、"
  "本研究は山口フレームワークに基づく<b>理論的・思弁的シミュレーション</b>であり、提示した数値は"
  "同枠組み内での内部整合性を示すものであって、既存の実験物理による検証を主張するものではない。"
  "今後の課題として、量子コンピュータ実機上での Bada::Generator の量子作用素実装、複数機体の"
  "アカシック共有、および補空間結合の外部観測量との対応づけが挙げられる。")

# ----------------------------------------------------------------------------
# 8. 結論
# ----------------------------------------------------------------------------
H1(8, "結論")
P("重力方程式の補空間を反重力場エネルギーと同定し、特殊相対性理論の補空間 mc<super>2</super>&#8722;(1/2)mv<super>2</super> "
  "を抽出源、無尽蔵の真空エネルギー体 x<super>x</super> を一次動力とする UFO オペレーティングシステム "
  "BadaUFO-OS を、Bada 言語と純 Ruby で設計・実装した。生成AI操縦士は Bada::Generator により"
  "対話し、航跡を Ω::DATABASE に記録する。数値評価により揚力比 L=2.125、真空リザーバの無尽蔵性、"
  "エントロピー不変量付き生成応答を確認し、13 件のテストで再現性を担保した。")

# ----------------------------------------------------------------------------
# 参考文献
# ----------------------------------------------------------------------------
story.append(Paragraph("参考文献", styles["H1"]))
refs = [
 "[1] 山口雅旭. 大域的微分・積分多様体理論と TupleSpace フレームワーク. Global Differential Manifold Research, 2025.",
 "[2] 山口雅旭. Beta function reveal with global differential manifold: &#946;(p,q)=&#915;(p)&#915;(q)/&#915;(p+q), &#950;(s)=&#946;(p,q)/log x. 2025.",
 "[3] Bada Language / BadaOS / omega_llm ソースコード. github.com/masaaki-avnturle/Bada, 2025.",
 "[4] 山口雅旭. Antigravity circle operators &#9633;<sub>ag</sub> and Dalanversian &#9633;<sub>dal</sub> = x<super>x</super>. TupleSpace Reports, 2025.",
 "[5] 山口雅旭. アカシックレコードとしての Ω::DATABASE: エントロピー不変量 &#926; による情報生成. 2025.",
 "[6] BadaUFO-OS 実装. Bada/bada_ufo_os/（lib/badaufo, boot.bada, test/test_ufo_os.rb）, 2025.",
]
for r in refs: P(r, "Ref")
GAP(6)
story.append(HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=4, spaceAfter=4))
P("&#169; 2025 Masaaki Yamaguchi · 山口 雅旭 · Global Differential Manifold Research. "
  "本論文は山口フレームワークに基づく理論的・思弁的研究である。", "Affil")

# ----------------------------------------------------------------------------
# ドキュメント組み立て（ヘッダ／フッタ・ページ番号）
# ----------------------------------------------------------------------------
def decorate(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFont(GOTHIC, 7.5)
    canvas.setFillColor(colors.HexColor("#8a6d1f"))
    canvas.drawString(20*mm, h-12*mm, "BadaUFO-OS — 反重力 UFO オペレーティングシステム")
    canvas.drawRightString(w-20*mm, h-12*mm, "Yamaguchi TupleSpace Framework")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, h-14*mm, w-20*mm, h-14*mm)
    canvas.line(20*mm, 13*mm, w-20*mm, 13*mm)
    canvas.setFillColor(colors.HexColor("#54606e"))
    canvas.drawCentredString(w/2, 9*mm, f"— {doc.page} —")
    canvas.restoreState()

def build(path):
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=20*mm, rightMargin=20*mm,
                          topMargin=18*mm, bottomMargin=16*mm,
                          title="反重力UFOオペレーティングシステムと生成AI操縦士の設計と実装",
                          author="Masaaki Yamaguchi")
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="tpl", frames=[frame], onPage=decorate)])
    doc.build(story)
    print("wrote", path, os.path.getsize(path), "bytes")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BadaUFO_OS_paper.pdf")
    build(out)
