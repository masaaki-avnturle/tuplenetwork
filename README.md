<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Masaaki Yamaguchi — Global Differential Manifold Research</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500;1,600&family=Shippori+Mincho+B1:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
:root{
  --void:#04060a;--deep:#080c12;--surface:#0d1520;--panel:#111a28;
  --border:rgba(80,120,200,.18);--border2:rgba(80,120,200,.35);
  --gold:#c8a44a;--blue:#4a80d0;--blue2:#6aa0f0;--teal:#40b8c0;
  --text:#d8e4f8;--text2:#8898b8;--text3:#445568;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--void);color:var(--text);font-family:'EB Garamond',serif;line-height:1.7}
nav{position:fixed;top:0;left:0;right:0;background:rgba(4,6,10,.85);backdrop-filter:blur(8px);height:56px;display:flex;align-items:center;padding:0 24px;border-bottom:1px solid var(--border);z-index:100}
.nav-logo{font-family:'JetBrains Mono',monospace;color:var(--gold);font-weight:700;letter-spacing:1px;text-decoration:none;margin-right:auto}
.nav-links{display:flex;gap:8px}
.nav-link{font-family:'JetBrains Mono',monospace;color:var(--text2);text-decoration:none;padding:6px 10px;border-radius:4px;font-size:12px}
.container{max-width:1100px;margin:0 auto;padding:120px 24px 60px}
.hero{display:flex;gap:40px;align-items:flex-start}
.hero-left{flex:1}
.hero-name{font-size:40px;line-height:1.05;margin-bottom:8px}
.hero-name-ja{font-family:'Shippori Mincho B1',serif;color:var(--gold);display:block;margin-bottom:16px}
.hero-desc{color:var(--text2);max-width:640px;margin-bottom:20px}
.hero-tags{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}
.hero-tag{font-family:'JetBrains Mono',monospace;font-size:11px;padding:6px 10px;border-radius:4px;border:1px solid rgba(255,255,255,.04)}
.hero-btns{display:flex;gap:12px}
.btn-primary{background:var(--blue);color:#fff;padding:10px 18px;border-radius:4px;text-decoration:none;font-family:'JetBrains Mono',monospace}
.panel{background:var(--panel);border:1px solid var(--border);padding:18px;border-radius:8px;color:var(--text2)}
.section{margin-top:40px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:16px}
.card{background:var(--panel);border:1px solid var(--border);padding:18px;border-radius:8px}
.eq{font-family:'JetBrains Mono',monospace;background:rgba(255,255,255,.02);padding:8px;border-radius:4px;color:var(--blue2)}
.stats{display:flex;gap:12px;margin-top:16px;flex-wrap:wrap}
.stat{background:rgba(255,255,255,.02);padding:12px;border-radius:6px;min-width:120px;text-align:center}
.footer{padding:40px 24px;color:var(--text2);text-align:center;border-top:1px solid var(--border);margin-top:40px}
@media(max-width:900px){.hero{flex-direction:column}}
</style>
</head>
<body>
<nav>
  <a class="nav-logo" href="#top">MY/GDM</a>
  <div class="nav-links">
    <a class="nav-link" href="#about">理論</a>
    <a class="nav-link" href="#papers">論文</a>
    <a class="nav-link" href="#projects">プロジェクト</a>
    <a class="nav-link" href="#equations">方程式</a>
    <a class="nav-link" href="#contact">連絡</a>
  </div>
  <a class="nav-link" href="https://github.com/MasaakiYamaguchi" target="_blank">GitHub</a>
</nav>

<div class="container" id="top">
  <section class="hero">
    <div class="hero-left">
      <h1 class="hero-name">Masaaki Yamaguchi<br><small style="font-size:14px">山口 雅彰</small></h1>
      <div class="hero-name-ja">Global Differential Manifold Research</div>
      <p class="hero-desc">
        大域的微分多様体とジョーンズ多項式の統一理論を研究し、
        ガンマ・ベータ・ゼータ・シャノンエントロピーの同型性を
        プログラミング言語とAI設計へ応用する独立研究者・開発者。
      </p>
      <div class="hero-tags">
        <span class="hero-tag">Jones Polynomial</span>
        <span class="hero-tag">Gamma · Beta · Zeta</span>
        <span class="hero-tag">Shannon Entropy</span>
        <span class="hero-tag">Bada Language</span>
      </div>
      <div class="hero-btns">
        <a class="btn-primary" href="#papers">論文を読む</a>
        <a class="btn-primary" href="#projects">プロジェクト</a>
      </div>
    </div>
    <div style="width:360px">
      <div class="panel">
        <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--text3);margin-bottom:8px">Core Equations</div>
        <div class="eq">β(p,q) = Γ(p)Γ(q) / Γ(p+q)</div>
        <div class="eq" style="margin-top:8px">ζ(s) = β(p,q) / log x ≈ x log x</div>
        <div class="eq" style="margin-top:8px">π(χ,x) = [iπ(χ,x), f(x)]</div>
        <div class="eq" style="margin-top:8px">⊕(iℏ∇)^⊕L = ∫ e^{-x} x^{1-t} dx_m ≈ e^{-x log x}</div>
      </div>
    </div>
  </section>

  <section id="about" class="section">
    <h2>概要 — Yamaguchi Framework</h2>
    <p class="panel" style="margin-top:12px">
      大域的微分多様体を核として、ガンマ函数・ベータ函数・ゼータ函数を統一する理論。
      非可換作用素・量子化作用素・TupleSpace（アカシックレコード）を組み合わせ、
      理論と実装（Bada 言語・BadaOS・omega_llm）を通じて検証します。
    </p>
  </section>

  <section id="papers" class="section">
    <h2>研究ファイル（抜粋）</h2>
    <div class="grid">
      <div class="card">
        <h3>Beta Function Reveal with Global Differential Manifold</h3>
        <p>ベータ函数と大域的微分多様体の解明。Γ・β・ζ の関係を多様体積分から導出。</p>
      </div>
      <div class="card">
        <h3>DNA of Universe and Human Being Entrance with Zeta Function</h3>
        <p>ゼータ函数とシャノンエントロピーの同型、宇宙・人体のDNA的解釈。</p>
      </div>
      <div class="card">
        <h3>Artificial Intelligence and TupleSpace of Ultranetwork</h3>
        <p>TupleSpace を用いた永続知識基盤と Bada 言語の設計。</p>
      </div>
      <div class="card">
        <h3>Library of Akashic Record</h3>
        <p>多様体理論・コホモロジー・D-ブレーン等を網羅する研究集。</p>
      </div>
    </div>
  </section>

  <section id="projects" class="section">
    <h2>主要プロジェクト</h2>
    <div class="grid">
      <div class="card"><strong>Bada Language</strong><p>独自作用素環プログラミング言語（C 実装）。</p></div>
      <div class="card"><strong>BadaOS</strong><p>Ubuntu 互換 OS シミュレータ。</p></div>
      <div class="card"><strong>omega_llm</strong><p>C ベースの LLM エンジン（π-softmax 等）。</p></div>
      <div class="card"><strong>Jones-NN LLM Apps</strong><p>ジョーンズ多項式を応用した LLM アプリ。</p></div>
    </div>
  </section>

  <section id="equations" class="section">
    <h2>方程式ショーケース</h2>
    <div class="grid">
      <div class="card"><div class="eq">d/df F = ∬ 1/(x log x)^2 dx_m + ∬ 1/(y log y)^{1/2} dy_m = Γ(x,y)</div></div>
      <div class="card"><div class="eq">ζ(s) = β(p,q) / log x = x log x</div></div>
      <div class="card"><div class="eq">π(χ,x) = [iπ(χ,x), f(x)]</div></div>
      <div class="card"><div class="eq">⊕(iℏ∇)^⊕L = e^{-x log x}</div></div>
    </div>
  </section>

  <section id="contact" class="section">
    <h2>連絡</h2>
    <div class="grid">
      <div class="card"><strong>GitHub</strong><p><a href="https://github.com/MasaakiYamaguchi" target="_blank">github.com/MasaakiYamaguchi</a></p></div>
      <div class="card"><strong>Research Papers</strong><p>16 論文・PDF 形式で公開（リポジトリ内）</p></div>
      <div class="card"><strong>Projects</strong><p>Bada / BadaOS / omega_llm / Jones-NN</p></div>
      <div class="card"><strong>Equation Archive</strong><p>54+ 方程式（TeX 形式利用可）</p></div>
    </div>
  </section>

  <div class="stats" aria-hidden="true" style="margin-top:28px;">
    <div class="stat"><div style="font-size:20px;color:var(--gold)">16</div><div style="font-size:12px">Research Files</div></div>
    <div class="stat"><div style="font-size:20px;color:var(--gold)">54</div><div style="font-size:12px">Core Equations</div></div>
    <div class="stat"><div style="font-size:20px;color:var(--gold)">8</div><div style="font-size:12px">Software Projects</div></div>
  </div>

  <div class="footer">
    © 2025 Masaaki Yamaguchi · 山口 雅彰 · Global Differential Manifold Research
  </div>
</div>

</body>
</html>
