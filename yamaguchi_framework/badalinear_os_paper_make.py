#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_paper.py — BadaLinear-OS 論文（日本語版・英語版）PDF ジェネレータ

  python3 make_paper.py        -> BadaLinear_OS_paper.pdf, BadaLinear_OS_paper_EN.pdf

数値は bada_linear_os の実装（lib/badalinear/guideway.rb）から得た実測値。
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Preformatted, HRFlowable)

HERE = os.path.dirname(os.path.abspath(__file__))
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
FF = "/usr/share/fonts/truetype/freefont"; DV = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("FS", f"{FF}/FreeSerif.ttf"))
pdfmetrics.registerFont(TTFont("FSB", f"{FF}/FreeSerifBold.ttf"))
pdfmetrics.registerFont(TTFont("FSI", f"{FF}/FreeSerifItalic.ttf"))
pdfmetrics.registerFont(TTFont("HS", f"{DV}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("FS", normal="FS", bold="FSB", italic="FSI", boldItalic="FSB")

INK = colors.HexColor("#0d1b2a"); ACC = colors.HexColor("#8a6d1f"); RULE = colors.HexColor("#c8a44a")
GREY = colors.HexColor("#54606e")

def styles(lang):
    body_f, head_f = ("HeiseiMin-W3", "HeiseiKakuGo-W5") if lang == "ja" else ("FS", "HS")
    wrap = "CJK" if lang == "ja" else None
    S = {
     "Title": ParagraphStyle("T", fontName=head_f, fontSize=16.5, leading=22, alignment=TA_CENTER, textColor=INK, spaceAfter=4),
     "Sub":   ParagraphStyle("S", fontName=body_f, fontSize=11, leading=16, alignment=TA_CENTER, textColor=ACC, spaceAfter=10),
     "Auth":  ParagraphStyle("A", fontName=body_f, fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=INK, spaceAfter=2),
     "Affil": ParagraphStyle("F", fontName=body_f, fontSize=9, leading=13, alignment=TA_CENTER, textColor=GREY, spaceAfter=12),
     "AbH":   ParagraphStyle("AH", fontName=head_f, fontSize=10, leading=14, textColor=ACC, spaceBefore=4, spaceAfter=3),
     "Ab":    ParagraphStyle("AB", fontName=body_f, fontSize=9.3, leading=15, alignment=TA_JUSTIFY, textColor=INK, leftIndent=6*mm, rightIndent=6*mm),
     "H1":    ParagraphStyle("H1", fontName=head_f, fontSize=12.5, leading=18, textColor=INK, spaceBefore=13, spaceAfter=5),
     "H2":    ParagraphStyle("H2", fontName=head_f, fontSize=10.8, leading=15, textColor=INK, spaceBefore=8, spaceAfter=3),
     "Body":  ParagraphStyle("B", fontName=body_f, fontSize=9.6, leading=15.6, alignment=TA_JUSTIFY, textColor=INK, spaceAfter=5),
     "Eq":    ParagraphStyle("E", fontName=body_f, fontSize=10, leading=16, alignment=TA_CENTER, textColor=INK, spaceBefore=4, spaceAfter=6),
     "Cap":   ParagraphStyle("C", fontName=head_f, fontSize=8.3, leading=12, alignment=TA_CENTER, textColor=GREY, spaceBefore=2, spaceAfter=8),
     "Code":  ParagraphStyle("K", fontName=head_f if lang == "ja" else "FS", fontSize=8, leading=11.4, textColor=colors.HexColor("#20303f")),
     "Ref":   ParagraphStyle("R", fontName=body_f, fontSize=8.6, leading=12.6, textColor=INK, leftIndent=6*mm, firstLineIndent=-6*mm, spaceAfter=3),
    }
    if wrap:
        for k in ("Ab", "Body", "Code", "Ref"): S[k].wordWrap = wrap
    return S, body_f, head_f

class Doc:
    def __init__(self, lang):
        self.lang = lang; self.S, self.bf, self.hf = styles(lang); self.story = []
    # HeiseiMin-W3 に無いグリフ（— – ≥ ≤）を JIS 互換字へ置換（日本語版のみ）
    JA_FIX = {"——": "――", "—": "―", "–": "―", "≥": "≧", "≤": "≦"}
    def P(self, t, s="Body"):
        if self.lang == "ja":
            for a, b in self.JA_FIX.items(): t = t.replace(a, b)
        self.story.append(Paragraph(t, self.S[s]))
    def H1(self, n, t): self.P(f"{n}. {t}" if n else t, "H1")
    def H2(self, n, t): self.P(f"{n} {t}", "H2")
    def EQ(self, t): self.P(t, "Eq")
    def CAP(self, t): self.P(t, "Cap")
    def GAP(self, h=4): self.story.append(Spacer(1, h))
    def RULE(self, th=1, after=8): self.story.append(HRFlowable(width="100%", thickness=th, color=RULE, spaceAfter=after))
    def CODE(self, text):
        t = Table([[Preformatted(text, self.S["Code"])]], colWidths=[165*mm])
        t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f4f1e6")), ("BOX", (0,0), (-1,-1), 0.5, RULE),
                               ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
                               ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)]))
        self.story.append(t); self.GAP(6)
    def TABLE(self, data, colw, caption):
        cell = ParagraphStyle("cell", fontName=self.bf, fontSize=8.3, leading=11, alignment=TA_CENTER, textColor=INK)
        hdr = ParagraphStyle("hdr", parent=cell, fontName=self.hf)
        rows = [[Paragraph(c, hdr if i == 0 else cell) for c in r] for i, r in enumerate(data)]
        t = Table(rows, colWidths=colw, hAlign="CENTER")
        t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LINEABOVE", (0,0), (-1,0), 0.8, INK), ("LINEBELOW", (0,0), (-1,0), 0.8, INK), ("LINEBELOW", (0,-1), (-1,-1), 0.8, INK),
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#efe7cf")),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f6f3ea")]),
            ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3)]))
        self.story.append(t); self.CAP(caption)
    def build(self, path, title, header):
        def deco(c, d):
            w, h = A4; c.saveState(); c.setFont(self.hf, 7.5); c.setFillColor(ACC)
            c.drawString(20*mm, h-12*mm, header); c.drawRightString(w-20*mm, h-12*mm, "Yamaguchi TupleSpace Framework")
            c.setStrokeColor(RULE); c.setLineWidth(0.5); c.line(20*mm, h-14*mm, w-20*mm, h-14*mm); c.line(20*mm, 13*mm, w-20*mm, 13*mm)
            c.setFillColor(GREY); c.drawCentredString(w/2, 9*mm, f"— {d.page} —"); c.restoreState()
        doc = BaseDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=16*mm,
                              title=title, author="Masaaki Yamaguchi")
        fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="m")
        doc.addPageTemplates([PageTemplate(id="t", frames=[fr], onPage=deco)]); doc.build(self.story)
        print("wrote", path, os.path.getsize(path), "bytes")

BOOT = """# linear_boot.bada — 反重力リニア ブートシーケンス（Bada 言語）
levitation <- "超伝導磁石を反重力場の補空間エネルギーに置き換える"  # 浮上 → 反重力
drag -< 4.0                                                  # 空気抵抗 → 補空間包絡
vacuum >- vacuum                                             # 動力 → 無尽蔵の真空
Omega::push levitation as antigravity_levitation             # アカシックへ記録"""
BOOT_EN = """# linear_boot.bada — antigravity-maglev boot sequence (Bada language)
levitation <- "replace the superconducting magnet by complementary-space energy"  # lift -> antigravity
drag -< 4.0                                              # air drag -> complementary envelope
vacuum >- vacuum                                         # propulsion -> inexhaustible vacuum
Omega::push levitation as antigravity_levitation         # record to the Akashic ledger"""
CORE = """# lib/badalinear/guideway.rb（抜粋）
def lift_ratio(alt_m = 0.0)                         # L = cosh(x log x)（速度に依らない）
  A.lift_ratio(5.972e24, TRAIN[:mass], 6.371e6 + alt_m, r0: 6.371e6)
end
def base_drag(v)      = 0.5 * RHO_AIR * TRAIN[:cd] * TRAIN[:area] * v * v   # ½ρC_dAv²
def drag_suppression(x_env)                         # σ = 1 / cosh(x log x)²
  c = A.antigravity_coupling(x_env); 1.0 / (c * c)
end
def effective_drag(v, x_env) = base_drag(v) * drag_suppression(x_env)"""

SIG = [["x<sub>env</sub>", "α<sub>ag</sub>=cosh(x log x)", "σ=1/α<super>2</super>", "500 km/h", "1000 km/h"],
       ["2", "2.125", "2.22×10<super>−1</super>", "8.70 kN", "34.8 kN"],
       ["3", "13.52", "5.47×10<super>−3</super>", "215 N", "860 N"],
       ["4 (nominal)", "128.0", "6.10×10<super>−5</super>", "2.40 N", "9.59 N"],
       ["5", "1562.5", "4.10×10<super>−7</super>", "0.016 N", "0.064 N"]]
TIMES = [["", "500 km/h (L0)", "700", "1000 (Bada)", "1500"],
         ["285.6 km", "36.6", "27.7", "21.8", "18.4"], ["438.0 km", "54.9", "40.8", "30.9", "24.5"]]
ENERGY = [["", "L0 (500 km/h)", "BadaLinear (1000 km/h, x<sub>env</sub>=4)"],
          ["285.6 km", "3.12 MWh", "7.6×10<super>−4</super> MWh"], ["438.0 km", "4.78 MWh", "1.2×10<super>−3</super> MWh"]]

# ============================================================ 日本語版
def build_ja(out):
    d = Doc("ja"); S = d.S
    d.P("超伝導磁石と空気抵抗を反重力の補空間で置き換える<br/>リニア新幹線オペレーティングシステム BadaLinear-OS の設計と実装", "Title")
    d.P("— 論文集の三本柱（重力方程式の補空間・相対論の補空間・無尽蔵の真空）による超電導リニアの作り換え —", "Sub")
    d.P("山口 雅旭 (Masaaki Yamaguchi)", "Auth"); d.P("Global Differential Manifold Research · TupleSpace Framework", "Affil")
    d.RULE()
    d.P("要 旨", "AbH")
    d.P("本論文は、超電導リニア（L0 系）の三つの中核——超伝導磁石による浮上、空気抵抗、地上コイルによる推進——を、"
        "論文集の反重力理論で置き換えた鉄道オペレーティングシステム BadaLinear-OS を報告する。第一に、NbTi 超伝導磁石"
        "（液体ヘリウム 4.2 K）の電磁誘導浮上を、重力方程式の補空間に住む反重力場 E<sub>ag</sub>=U<sub>grav</sub>·cosh(x log x) "
        "に置き換える。揚力比 L=cosh(x log x)=2.125 は速度に依らず、150 km/h 未満で車輪走行を要する EDS と異なり停車中から"
        "浮上し、極低温を要しない。第二に、底空間の空気抵抗 F<sub>d</sub>=(1/2)ρC<sub>d</sub>Av<super>2</super> を、真空エネルギー体 x<super>x</super> の"
        "コホモロジー切断である補空間包絡で包み、抑制係数 σ=1/cosh(x<sub>env</sub> log x<sub>env</sub>)<super>2</super> で切断する。"
        "x<sub>env</sub>=4 で σ=6.1×10<super>−5</super>、1000 km/h の抗力 157.1 kN は 9.6 N に落ち、実質ゼロとなる。第三に、"
        "推進を相対論の補空間 E<sub>⊥</sub>=mc<super>2</super>−(1/2)mv<super>2</super> と無尽蔵の真空リザーバに置き、生成AI車掌（Bada::Generator）が"
        "放送と運行記録を Ω::DATABASE に残す。品川–名古屋 285.6 km の無停車所要時間は 36.6 分（500 km/h）から 21.8 分"
        "（1000 km/h）へ、抗力エネルギーは 3.12 MWh から 7.6×10<super>−4</super> MWh へ短縮・削減される。全体を Bada 言語と純 Ruby で"
        "実装し、10 件のテストに合格した。", "Ab")
    d.P("キーワード： 超電導リニア、反重力浮上、補空間、空気抵抗ゼロ、真空エネルギー、Bada 言語、生成AI、BadaUFO-OS", "Ab")
    d.GAP(2); d.RULE(0.6)

    d.H1(1, "序論")
    d.P("超電導リニア（L0 系）は、車上の NbTi 超伝導磁石（液体ヘリウム 4.2 K）と地上コイルの電磁誘導（EDS）により約 10 cm 浮上し、"
        "地上コイルのリニア同期モータで 500 km/h の営業運転を計画する。品川–名古屋 285.6 km を 40 分、品川–新大阪 438 km を 67 分で結ぶ。"
        "一方で EDS は誘導起電力に依存するため約 150 km/h 未満ではゴムタイヤ走行を要し、極低温設備を常時必要とし、500 km/h では"
        "走行エネルギーの大半が空気抵抗 F<sub>d</sub>=(1/2)ρC<sub>d</sub>Av<super>2</super> に費やされる。路線の大半がトンネルであることは微気圧波の問題も生む。")
    d.P("本論文は、これら三つの中核を論文集の反重力理論——第九巻（反重力発生器）と BadaUFO-OS 応用篇——で置き換える。"
        "貢献は次の三点である。(1) 超伝導磁石を反重力場（重力方程式の補空間）に置き換え、速度に依らない浮上を得た。"
        "(2) 空気抵抗を補空間包絡で切断し、実質ゼロ抗力を得た。(3) BadaUFO-OS を生成AI車掌つきの鉄道 OS として Bada 言語で"
        "作り換え、L0 系との比較を数値で与えた。")

    d.H1(2, "理論的枠組み")
    d.P("論文集の三本柱を再掲する。重力ポテンシャル U<sub>grav</sub>=GMm/r は多様体の底空間（束縛部）に住み、そのコホモロジー切断＝補空間に"
        "住むエネルギーが反重力場である。補空間側の結合は反重力箱作用素の実部 α<sub>ag</sub>(x)=cosh(x log x)≥1 で与えられる。")
    d.EQ("E<sub>ag</sub> = U<sub>grav</sub>·cosh(x log x),&nbsp;&nbsp; E<sub>⊥</sub> = mc<super>2</super> − (1/2)mv<super>2</super>,&nbsp;&nbsp; E<sub>vac</sub> = ρ·x<super>x</super>")
    d.P("本論文が新たに導入するのは<b>補空間包絡</b>である。底空間の量（空気抵抗）を真空エネルギー体 x<super>x</super> のコホモロジー切断で包むと、"
        "その量は補空間結合の二乗で割られる。")
    d.EQ("F<sub>d,eff</sub> = F<sub>d</sub> · σ(x<sub>env</sub>),&nbsp;&nbsp; σ(x) = 1 / cosh(x log x)<super>2</super>")
    d.P("σ は x<sub>env</sub> について単調減少し、x<sub>env</sub>=4 で 6.1×10<super>−5</super>、x<sub>env</sub>=5 で 4.1×10<super>−7</super> となる（表 1）。")

    d.H1(3, "三つの置き換え")
    d.H2("3.1", "浮上：超伝導磁石 → 反重力場")
    d.P("揚力比 L=E<sub>ag</sub>/U<sub>grav</sub>=cosh(x log x) は多様体座標 x=1+r<sub>0</sub>/r のみで決まり、地表で x=2、L=2.125 である。"
        "L0 系 12 両相当（質量 3.0×10<super>5</super> kg、重量 2.94×10<super>6</super> N）に対し反重力浮上力は 6.25×10<super>6</super> N となる。"
        "誘導起電力を要しないため停車中から浮上し、車輪と極低温設備は不要である。")
    d.H2("3.2", "抗力：空気抵抗 → 補空間包絡")
    d.P("L0 系相当の C<sub>d</sub>=0.35、A=9.5 m<super>2</super>、ρ=1.225 kg/m<super>3</super> では、底空間の抗力は 500 km/h で 39.3 kN、1000 km/h で 157.1 kN"
        "である。補空間包絡の公称座標 x<sub>env</sub>=4 では、これらはそれぞれ 2.40 N、9.59 N に落ちる（表 1）。抗力に費やされる走行"
        "エネルギーが消えることで、巡航速度の上限は空力ではなく乗り心地（加速度）で決まる。")
    d.TABLE(SIG, [28*mm, 40*mm, 34*mm, 30*mm, 30*mm], "表 1： 補空間包絡の抑制係数 σ と残存抗力（実装 guideway.rb による実測値）。")
    d.H2("3.3", "動力：地上コイル → 相対論補空間と無尽蔵の真空")
    d.P("推進は相対論補空間 E<sub>⊥</sub>=mc<super>2</super>−(1/2)mv<super>2</super>（3.0×10<super>5</super> kg で 2.70×10<super>22</super> J）を α<sub>ag</sub> で増幅して得、"
        "無尽蔵の真空リザーバ E<sub>vac</sub>=ρ·x<super>x</super> が裏付ける。巡航中の変電所給電は不要となる。")

    d.H1(4, "システムアーキテクチャと Bada 言語実装")
    d.P("BadaLinear-OS は BadaUFO-OS の四層（物理コア・動力系・機体知性・記録系）を継承し、物理コア BadaUFO::Antigravity と"
        "真空リザーバを再利用する。機体知性は生成AI操縦士 Copilot を鉄道向けに作り換えた Conductor（生成AI車掌）で、"
        "Bada::Generator により車内放送と運行判断を生成し、Ω::DATABASE（アカシックレコード）に記録する。")
    d.CODE(BOOT); d.CAP("図 1： Bada 言語ブートシーケンス。三つの作用素で「浮上→反重力／抗力→包絡／動力→真空」を記述し、実インタプリタで実行する。")
    d.CODE(CORE); d.CAP("図 2： 軌道物理コア（抜粋）。揚力比・底空間抗力・抑制係数・残存抗力。")

    d.H1(5, "評価")
    d.P("品川–名古屋（285.6 km）と品川–新大阪（438.0 km）を、快適加速度 1.0 m/s<super>2</super> の台形速度プロファイルで評価した。")
    d.TABLE(TIMES, [30*mm, 34*mm, 26*mm, 34*mm, 26*mm], "表 2： 無停車所要時間 [分]。L0（500 km/h）と BadaLinear（1000 km/h）。実運行計画の 40 分／67 分は途中停車・速度制限込み。")
    d.TABLE(ENERGY, [30*mm, 45*mm, 70*mm], "表 3： 1 走行あたりの抗力エネルギー（F<sub>d</sub>×距離）。包絡により約 4000 分の 1 に減少。")
    d.P("1000 km/h 巡航・各駅停車 60 秒での品川→新大阪の累計所要時間は 63.7 分、名古屋までは 43.3 分である。"
        "実装は 10 件のテスト（28 アサーション）に合格し、Bada 言語ブートは実インタプリタ上で各値の Ξ 不変量とともに記録された。")

    d.H1(6, "議論と結論")
    d.P("本 OS は、超電導リニアの三つの中核——極低温超伝導磁石・空気抵抗・地上コイル給電——が、論文集の三本柱——補空間の反重力・"
        "補空間包絡・無尽蔵の真空——にそれぞれ一対一で対応することを示した。特に補空間包絡 σ=1/cosh(x log x)<super>2</super> は、"
        "反重力結合 α<sub>ag</sub> と同一の作用素族から導かれ、揚力と抗力抑制を単一の構造で与える。一方、本研究は山口フレームワークに"
        "基づく理論的・思弁的シミュレーションであり、実在の超電導リニアの設計・安全性を評価するものではない。今後の課題として、"
        "トンネル微気圧波の補空間包絡による評価、複数編成のアカシック共有、量子計算機実機上の生成AI車掌が挙げられる。")

    d.H1("", "参考文献")
    for r in ["[1] 山口雅旭. 反重力発生器（第九巻）— ゼータ正則化応力テンソルを分析器として. Yamaguchi Framework 論文集, 2026.",
              "[2] 山口雅旭. 反重力場の補空間エネルギーに基づく UFO オペレーティングシステムと生成AI操縦士の設計と実装（BadaUFO-OS）. 2026.",
              "[3] 山口雅旭. Yamaguchi Framework 論文集 第一巻〜第十五巻. github.com/masaaki-avnturle/tuplenetwork, 2026.",
              "[4] BadaLinear-OS 実装. Bada/bada_linear_os/（lib/badalinear, linear_boot.bada, test/test_linear.rb）, 2026.",
              "[5] 超電導リニア L0 系・中央新幹線の公開諸元（浮上方式・営業速度・所要時間）に基づく比較基準。"]:
        d.P(r, "Ref")
    d.GAP(6); d.RULE(0.6, 4)
    d.P("© 2026 Masaaki Yamaguchi · 山口 雅旭 · Global Differential Manifold Research. 本論文は山口フレームワークに基づく理論的・思弁的研究である。", "Affil")
    d.build(out, "超伝導磁石と空気抵抗を反重力の補空間で置き換えるリニア新幹線OS BadaLinear-OS", "BadaLinear-OS — 反重力リニア新幹線 OS")

# ============================================================ English
def build_en(out):
    d = Doc("en")
    d.P("Replacing Superconducting Magnets and Air Drag by the Complementary Space of Antigravity:<br/>Design and Implementation of the Maglev Operating System BadaLinear-OS", "Title")
    d.P("— rebuilding the SCMaglev on the collection's three pillars: the complementary space of the gravity equation, of special relativity, and the inexhaustible vacuum —", "Sub")
    d.P('Masaaki Yamaguchi (<font name="HeiseiMin-W3">山口 雅旭</font>)', "Auth"); d.P("Global Differential Manifold Research · TupleSpace Framework", "Affil")
    d.RULE()
    d.P("Abstract", "AbH")
    d.P("We report BadaLinear-OS, a railway operating system that replaces the three cores of the superconducting maglev (SCMaglev L0) — "
        "levitation by superconducting magnets, air drag, and propulsion by ground coils — with the antigravity theory of the collected papers. "
        "First, electrodynamic levitation by NbTi magnets at 4.2 K is replaced by the antigravity field living in the complementary space of the "
        "gravity equation, E<sub>ag</sub>=U<sub>grav</sub>·cosh(x log x). The lift ratio L=cosh(x log x)=2.125 is independent of speed: unlike EDS, which "
        "needs wheels below ~150 km/h, the train levitates at rest and needs no cryogenics. Second, the base-space drag "
        "F<sub>d</sub>=½ρC<sub>d</sub>Av<super>2</super> is wrapped in a <i>complementary envelope</i> — the cohomology cut of the vacuum-energy body x<super>x</super> — and cut by "
        "σ=1/cosh(x<sub>env</sub> log x<sub>env</sub>)<super>2</super>; at x<sub>env</sub>=4, σ=6.1×10<super>−5</super> and the 157.1 kN drag at 1000 km/h falls to 9.6 N, "
        "effectively zero. Third, propulsion is drawn from the special-relativistic complement E<sub>⊥</sub>=mc<super>2</super>−½mv<super>2</super> backed by an "
        "inexhaustible vacuum reservoir, and a generative-AI conductor (Bada::Generator) issues announcements and records the run in Ω::DATABASE. "
        "The non-stop Shinagawa–Nagoya time (285.6 km) drops from 36.6 min at 500 km/h to 21.8 min at 1000 km/h, and drag energy from 3.12 MWh "
        "to 7.6×10<super>−4</super> MWh. The system is implemented in the Bada language and pure Ruby, with 10 passing tests.", "Ab")
    d.P("Keywords: SCMaglev, antigravity levitation, complementary space, zero air drag, vacuum energy, Bada language, generative AI, BadaUFO-OS", "Ab")
    d.GAP(2); d.RULE(0.6)

    d.H1(1, "Introduction")
    d.P("The SCMaglev L0 levitates about 10 cm by electrodynamic suspension (EDS) between on-board NbTi superconducting magnets (liquid helium, 4.2 K) "
        "and ground coils, and is propelled by a ground-coil linear synchronous motor at a planned 500 km/h — Shinagawa–Nagoya (285.6 km) in 40 min, "
        "Shinagawa–Shin-Osaka (438 km) in 67 min. EDS depends on induced EMF, so below ~150 km/h the train runs on rubber wheels; cryogenics are needed "
        "continuously; and at 500 km/h most of the traction energy goes into air drag F<sub>d</sub>=½ρC<sub>d</sub>Av<super>2</super>. A mostly-tunnel route adds micro-pressure-wave issues.")
    d.P("This paper replaces those three cores with the collection's antigravity theory (Vol. 9 and the BadaUFO-OS applied volume). Contributions: "
        "(1) superconducting magnets are replaced by the antigravity field of the gravity equation's complementary space, giving speed-independent lift; "
        "(2) air drag is cut by a complementary envelope, giving effectively zero drag; (3) BadaUFO-OS is rebuilt in Bada as a railway OS with a "
        "generative-AI conductor, and compared numerically with the L0.")

    d.H1(2, "Theoretical framework")
    d.P("The three pillars: the gravitational potential U<sub>grav</sub>=GMm/r lives in the base (bound) space of the manifold; the energy in its cohomology "
        "cut — the complementary space — is the antigravity field, with coupling α<sub>ag</sub>(x)=cosh(x log x)≥1, the real part of the antigravity box operator.")
    d.EQ("E<sub>ag</sub> = U<sub>grav</sub>·cosh(x log x),&nbsp;&nbsp; E<sub>⊥</sub> = mc<super>2</super> − ½mv<super>2</super>,&nbsp;&nbsp; E<sub>vac</sub> = ρ·x<super>x</super>")
    d.P("New here is the <b>complementary envelope</b>: wrapping a base-space quantity (air drag) in the cohomology cut of the vacuum body x<super>x</super> divides it by the square of the complementary coupling.")
    d.EQ("F<sub>d,eff</sub> = F<sub>d</sub> · σ(x<sub>env</sub>),&nbsp;&nbsp; σ(x) = 1 / cosh(x log x)<super>2</super>")
    d.P("σ decreases monotonically in x<sub>env</sub>: 6.1×10<super>−5</super> at x<sub>env</sub>=4 and 4.1×10<super>−7</super> at x<sub>env</sub>=5 (Table 1).")

    d.H1(3, "The three replacements")
    d.H2("3.1", "Levitation: superconducting magnets → antigravity field")
    d.P("The lift ratio L=E<sub>ag</sub>/U<sub>grav</sub>=cosh(x log x) depends only on the manifold coordinate x=1+r<sub>0</sub>/r; at ground level x=2 and L=2.125. "
        "For a 12-car L0-class set (3.0×10<super>5</super> kg, weight 2.94×10<super>6</super> N) the antigravity lift is 6.25×10<super>6</super> N. No induced EMF is required, so the train "
        "levitates at rest; wheels and cryogenics are unnecessary.")
    d.H2("3.2", "Drag: air resistance → complementary envelope")
    d.P("With C<sub>d</sub>=0.35, A=9.5 m<super>2</super>, ρ=1.225 kg/m<super>3</super>, base-space drag is 39.3 kN at 500 km/h and 157.1 kN at 1000 km/h. At the nominal "
        "envelope x<sub>env</sub>=4 these fall to 2.40 N and 9.59 N (Table 1). With drag energy gone, the cruise limit is set by ride comfort (acceleration), not aerodynamics.")
    d.TABLE(SIG, [28*mm, 40*mm, 34*mm, 30*mm, 30*mm], "Table 1: Envelope suppression σ and residual drag (measured from guideway.rb).")
    d.H2("3.3", "Propulsion: ground coils → relativistic complement and the inexhaustible vacuum")
    d.P("Propulsion comes from E<sub>⊥</sub>=mc<super>2</super>−½mv<super>2</super> (2.70×10<super>22</super> J for 3.0×10<super>5</super> kg) amplified by α<sub>ag</sub> and backed by the vacuum reservoir E<sub>vac</sub>=ρ·x<super>x</super>; no substation power is drawn while cruising.")

    d.H1(4, "Architecture and the Bada implementation")
    d.P("BadaLinear-OS inherits BadaUFO-OS's four layers (physics core, power, vehicle intelligence, ledger) and reuses BadaUFO::Antigravity and the vacuum reservoir. "
        "The vehicle intelligence is Conductor, the generative-AI copilot rebuilt for rail: Bada::Generator produces announcements and operating decisions, recorded in Ω::DATABASE (the Akashic ledger).")
    d.CODE(BOOT_EN); d.CAP("Fig. 1: Bada boot sequence — three operators encode lift→antigravity, drag→envelope, propulsion→vacuum; runs on the native interpreter.")
    d.CODE(CORE); d.CAP("Fig. 2: Guideway physics core (excerpt): lift ratio, base drag, suppression, residual drag.")

    d.H1(5, "Evaluation")
    d.P("Shinagawa–Nagoya (285.6 km) and Shinagawa–Shin-Osaka (438.0 km) were evaluated with a trapezoidal speed profile at a comfort acceleration of 1.0 m/s<super>2</super>.")
    d.TABLE(TIMES, [30*mm, 34*mm, 26*mm, 34*mm, 26*mm], "Table 2: Non-stop travel time [min], L0 (500 km/h) vs BadaLinear (1000 km/h). The planned 40/67 min include intermediate stops and speed limits.")
    d.TABLE(ENERGY, [30*mm, 45*mm, 70*mm], "Table 3: Drag energy per run (F<sub>d</sub> × distance); the envelope reduces it about 4000-fold.")
    d.P("Cruising at 1000 km/h with 60 s dwells, the cumulative Shinagawa→Shin-Osaka time is 63.7 min (43.3 min to Nagoya). The implementation passes 10 tests (28 assertions), and the Bada boot records each value with its Ξ invariant on the native interpreter.")

    d.H1(6, "Discussion and conclusion")
    d.P("The three cores of the SCMaglev — cryogenic superconducting magnets, air drag, and ground-coil power — map one-to-one onto the collection's three pillars — "
        "complementary-space antigravity, the complementary envelope, and the inexhaustible vacuum. In particular σ=1/cosh(x log x)<super>2</super> derives from the same operator family as "
        "α<sub>ag</sub>, so lift and drag suppression share one structure. This work is a theoretical, speculative simulation within the Yamaguchi framework and does not assess the design or safety "
        "of the real SCMaglev. Future work: micro-pressure waves under the envelope, Akashic sharing across train sets, and the generative-AI conductor on quantum hardware.")

    d.H1("", "References")
    for r in ["[1] M. Yamaguchi. Antigravity Generator (Vol. 9) — the zeta-regularized stress tensor as analyzer. Yamaguchi Framework Collected Papers, 2026.",
              "[2] M. Yamaguchi. Design and Implementation of a UFO Operating System and Generative-AI Copilot from Complementary-Space Antigravity Energy (BadaUFO-OS). 2026.",
              "[3] M. Yamaguchi. Yamaguchi Framework Collected Papers, Vols. 1–15. github.com/masaaki-avnturle/tuplenetwork, 2026.",
              "[4] BadaLinear-OS implementation. Bada/bada_linear_os/ (lib/badalinear, linear_boot.bada, test/test_linear.rb), 2026.",
              "[5] Published specifications of the SCMaglev L0 / Chuo Shinkansen (levitation, service speed, travel times), used as the comparison baseline."]:
        d.P(r, "Ref")
    d.GAP(6); d.RULE(0.6, 4)
    d.P("© 2026 Masaaki Yamaguchi · Global Differential Manifold Research. A theoretical, speculative study within the Yamaguchi framework.", "Affil")
    d.build(out, "BadaLinear-OS: Replacing Superconducting Magnets and Air Drag by the Complementary Space of Antigravity", "BadaLinear-OS — Antigravity Maglev Operating System")

if __name__ == "__main__":
    build_ja(os.path.join(HERE, "BadaLinear_OS_paper.pdf"))
    build_en(os.path.join(HERE, "BadaLinear_OS_paper_EN.pdf"))
