# Yamaguchi Framework 論文集

スペクトル解析器——固有値の列から極・有限部・ゼロモードを読み出す一つの計算体系——の到達点と限界を、クレイ数学研究所の七つのミレニアム問題をめぐって記録した論文集。全巻に Python による再現可能な数値検証を付し、証明できた事柄と証明できていない事柄を標識(検証済/古典/予想/未検証/否定)で分離する。

**本論文集はいずれの未解決ミレニアム問題についても証明を主張しない。** 各巻が主張するのは、解析器がそれぞれの問題についてどこまで届き、どこで止まるかである。

著者:山口 正明(Masaaki Yamaguchi)/ 数値検証・文書化補助:Claude (Anthropic)

## 収録論文(2026年9月)

| 日付 | 表題 | ファイル |
|---|---|---|
| 9/6 | 方程式の記号形状エントロピーによるアプリケーション合成 — BadaGPT の構成機構 | [form_entropy_badagpt_paper.pdf](form_entropy_badagpt_paper.pdf) |
| 9/6 | 修正されたベータ・ゼータ方程式と、その言語生成アルゴリズム | [corrected_beta_zeta_language_generation.pdf](corrected_beta_zeta_language_generation.pdf) |
| 9/6 | 修正核 Λ(x,y) の量子計算への応用 — LCU 準備・量子暗号・Bada 量子言語 | [quantum_kernel_algorithms_crypto_bada.pdf](quantum_kernel_algorithms_crypto_bada.pdf) |
| 9/7 | ゼータ・エントロピー・生成 論文集 | [zeta_entropy_generation_volume.pdf](zeta_entropy_generation_volume.pdf) |
| 9/7 | 多様体積分と量子工学の結婚 論文集 | [manifold_integral_quantum_engineering.pdf](manifold_integral_quantum_engineering.pdf) |
| 9/7 | スペクトル統一 — 一般相対性理論と量子力学の統合に向けた提案 | [spectral_unification_proposal.pdf](spectral_unification_proposal.pdf) |
| 9/7 | HΨ = ⊕(iℏ∇)⊕L の同定と、球面族への拡張 | [hpsi_multiplicity_sphere_family.pdf](hpsi_multiplicity_sphere_family.pdf) |
| 9/8 | ガウスの曲面論の量子化(第八巻)— χ = 6(ζ(0)+1)、そして形は決まらない | [gauss_surface_quantization.pdf](gauss_surface_quantization.pdf) |
| 9/8 | ガウスからサーストン・ペレルマンへ — Ricci フロー・8 幾何・準同型の正確な所在 | [thurston_perelman_ricci_flow.pdf](thurston_perelman_ricci_flow.pdf) |
| 9/8 | ゼータ関数の圏 — 極が古典、原点が量子、積は畳み込みになる | [zeta_category_gr_qm.pdf](zeta_category_gr_qm.pdf) |
| 9/9 | 反重力発生器(第九巻)— ゼータ正則化応力テンソルを分析器として | [antigravity_zeta_analyzer.pdf](antigravity_zeta_analyzer.pdf) |
| 9/12 | ゼロモードの数としての充足可能性と P ≠ NP 予想(第十二巻) | [pnp_zeromodes.pdf](pnp_zeromodes.pdf) |
| 9/12 | 調和形式のゼロモードとホッジ予想(第十三巻) | [hodge_zeromodes.pdf](hodge_zeromodes.pdf) |
| 9/12 | ゼータの s → ∞ 端としての質量ギャップとヤン・ミルズ問題(第十四巻) | [ym_massgap.pdf](ym_massgap.pdf) |
| 9/12 | 零を保存するもの — 論文集 第一巻〜第十四巻(要約版) | [yamaguchi_framework_ronbunshu.pdf](yamaguchi_framework_ronbunshu.pdf) |
| 9/12 | 零を保存するもの — 十四の短篇(随筆) | [zero_wo_hozon_suru_mono.pdf](zero_wo_hozon_suru_mono.pdf) |
| 9/14 | 臨界線の中心零点としての BSD 予想と、七つのミレニアム問題の総括(第十五巻) | [vol15_millennium_synthesis.md](vol15_millennium_synthesis.md) |
| 9/14 | 第十五巻 再現コード(BSD 数値検証、Python 3 + mpmath) | [vol15_bsd_verification.py](vol15_bsd_verification.py) |

## ミレニアム問題との対応

| 問題 | 巻 | 状態 |
|---|---|---|
| ポアンカレ予想 | サーストン・ペレルマン篇 | 解決済(Perelman 2003 の数値的確認) |
| ナヴィエ・ストークス正則性 | 第十巻(要約版に収録) | 未解決 — 隙間は非線形項の一冪 |
| リーマン予想 | 第十一巻(要約版に収録) | 未解決 — 隙間は Euler 積の正値性 |
| P 対 NP | 第十二巻 | 未解決 — 隙間は相対化しない下界 |
| ホッジ予想 | 第十三巻 | 未解決 — 隙間はサイクルの構成 |
| ヤン・ミルズ質量ギャップ | 第十四巻 | 未解決 — 隙間は作用素の存在と連続極限 |
| Birch–Swinnerton-Dyer 予想 | 第十五巻 | 未解決 — 隙間は位数 ≥ 2 と階数の橋、Ш の有限性 |
