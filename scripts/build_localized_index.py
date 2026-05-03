#!/usr/bin/env python3
"""
Generate localized home pages (index.html) from the English root index.html.

Run from repo root:
  python3 scripts/build_localized_index.py

When you add sections to index.html, update LOCALE_SPECS below (replacements
are applied in order; longer strings should come before shorter substrings).
"""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "index.html"


def write_index(locale: str, prefix: str, html_lang: str, spec: dict) -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace('<html lang="en">', f'<html lang="{html_lang}">', 1)
    text = text.replace(
        '<link rel="canonical" href="https://re-hong.com/" />',
        f'<link rel="canonical" href="https://re-hong.com{prefix}/" />',
        1,
    )
    text = text.replace(
        '<meta property="og:url" content="https://re-hong.com/" />',
        f'<meta property="og:url" content="https://re-hong.com{prefix}/" />',
        1,
    )

    for old, new in spec["pairs"]:
        if old not in text:
            raise SystemExit(f"Missing fragment in {locale}: {old[:80]!r}")
        text = text.replace(old, new, 1)

    # Prefix in-site anchors and key routes (keep /css, /js, /images, /favicon as root-relative)
    if prefix:
        text = text.replace(
            '<a class="brand" href="/"',
            f'<a class="brand" href="{prefix}/"',
            1,
        )
        text = re.sub(r'href="#', f'href="{prefix}/#', text)
        text = text.replace('href="/quality.html', f'href="{prefix}/quality.html')
        text = text.replace('href="/careers.html', f'href="{prefix}/careers.html')
        text = text.replace('aria-label="Re Hong Technology home"', spec["brand_aria"])

    out = ROOT / prefix.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print("Wrote", out)


# Each locale: ordered (old, new) replacements on English source BEFORE prefix rewrite.
# Fragments must match index.html exactly (single occurrence preferred).

ZH_TW = {
    "brand_aria": 'aria-label="瑞鋐科技首頁"',
    "pairs": [
        (
            '        "url": "https://re-hong.com/",',
            '        "url": "https://re-hong.com/zh-TW/",',
        ),
        (
            """    <title>
      Re Hong Technology | Taiwan CNC Machining Partner | Taoyuan · Quick-Turn &amp; Fair
      Pricing
    </title>""",
            """    <title>
      瑞鋐科技 | 台灣桃園 CNC 加工夥伴 · 急件 · 合理報價
    </title>""",
        ),
        (
            """    <meta
      name="description"
      content="Owner-run Taiwan CNC machining in Taoyuan: ISO 9001–oriented quality management, automotive programs aligned with IATF 16949 / ISO/TS 16949, 40+ years experience (2026), quick-turn capacity, fair pricing, automated inspection &amp; SPC. Serving automotive, tools, industrial, and bicycle sectors."
    />""",
            """    <meta
      name="description"
      content="桃園瑞鋐為經營者深度參與的精密 CNC 加工廠：ISO 9001 品質管理思維、汽車供應鏈對應 IATF 16949／ISO／TS 16949、40 年以上實務經驗（2026）、急件產能、合理透明報價、自動量測與 SPC。服務汽車、手工具、工業與自行車等領域。"
    />""",
        ),
        (
            """    <meta
      property="og:title"
      content="Re Hong Technology | Taiwan CNC Partner · Taoyuan · Quick-Turn &amp; Fair Pricing"
    />""",
            """    <meta
      property="og:title"
      content="瑞鋐科技 | 台灣 CNC 夥伴 · 桃園 · 急件與合理價格"
    />""",
        ),
        (
            """    <meta
      property="og:description"
      content="Taoyuan CNC: ISO 9001–oriented QMS, IATF 16949 / ISO/TS 16949 automotive alignment, owner-led, 40+ years experience, quick turns, fair pricing, automated inspection &amp; SPC."
    />""",
            """    <meta
      property="og:description"
      content="桃園 CNC：ISO 9001 品質系統、IATF 16949／TS 16949 汽車製程對應、經營者主導、40 年以上經驗、急件、合理報價、自動檢驗與 SPC。"
    />""",
        ),
        (
            """    <meta
      name="twitter:title"
      content="Re Hong Technology | Taiwan CNC Partner · Quick-Turn · Fair Pricing"
    />""",
            """    <meta
      name="twitter:title"
      content="瑞鋐科技 | 台灣 CNC · 急件 · 合理價格"
    />""",
        ),
        (
            """    <meta
      name="twitter:description"
      content="Taiwan precision CNC: Taoyuan shop, quick-turn capacity, fair quotes, owner-run with decades of skill—new manufacturing partnerships welcome."
    />""",
            """    <meta
      name="twitter:description"
      content="台灣精密 CNC：桃園廠區、急件產能、合理報價、經營者主導與深厚技術—歡迎新製造夥伴。"
    />""",
        ),
        (
            """        "description": "Owner-operated Taiwan CNC machining in Taoyuan: ISO 9001 quality management orientation, IATF 16949 / ISO/TS 16949 automotive alignment, turning and milling composite parts, quick-turn capacity, fair pricing, automated inspection and process capability.",""",
            """        "description": "台灣桃園瑞鋐：ISO 9001 品質管理、IATF 16949／TS 16949 汽車製程、車銑複合加工、急件產能、合理報價、自動檢驗與製程能力。",""",
        ),
        (
            """    <a class="skip-link" href="#main">Skip to content</a>""",
            """    <a class="skip-link" href="#main">跳至主要內容</a>""",
        ),
        (
            """          <img src="/logo.png" alt="Re Hong Technology logo" width="93" height="86" />
          <span class="brand-text">
            Re Hong Technology
            <small>Taiwan · CNC machining</small>
          </span>""",
            """          <img src="/logo.png" alt="瑞鋐科技標誌" width="93" height="86" />
          <span class="brand-text">
            瑞鋐科技
            <small>台灣 · CNC 加工</small>
          </span>""",
        ),
        (
            """        <nav id="site-nav" class="site-nav" aria-label="Primary">""",
            """        <nav id="site-nav" class="site-nav" aria-label="主要導覽">""",
        ),
        (
            """            <li><a href="#industries">Work samples</a></li>
            <li><a href="#story">About</a></li>
            <li><a href="#capabilities">Capabilities</a></li>
            <li><a href="/quality.html">Quality &amp; ISO standards</a></li>
            <li><a href="/careers.html">Careers</a></li>
            <li><a href="#contact">Contact</a></li>""",
            """            <li><a href="#industries">作品與應用</a></li>
            <li><a href="#story">關於</a></li>
            <li><a href="#capabilities">核心能力</a></li>
            <li><a href="/quality.html">品質與 ISO</a></li>
            <li><a href="/careers.html">徵才</a></li>
            <li><a href="#contact">聯絡</a></li>""",
        ),
        (
            """              <span class="lang-toggle__label">English</span>""",
            """              <span class="lang-toggle__label">繁體中文</span>""",
        ),
        (
            '            aria-label="Open menu"',
            '            aria-label="開啟選單"',
        ),
        (
            """            <h1 id="hero-heading">
              Taiwan CNC machining partner in Taoyuan—precision work, quick turns, fair pricing
            </h1>""",
            """            <h1 id="hero-heading">
              台灣桃園 CNC 加工夥伴—精密、急件、合理報價
            </h1>""",
        ),
        (
            """            <p class="lead">
              Re Hong Technology is an <strong>owner-run</strong> precision CNC shop combining
              turning, milling, and process integration. Leadership brings
              <strong>more than 40 years of hands-on manufacturing experience (as of 2026)</strong>—skilled
              at complex mechanical programs and direct about what it takes to ship quality on
              schedule. We are <strong>actively seeking new manufacturing partnerships</strong> and
              have <strong>capacity for additional work</strong>, including
              <strong>quick-turn</strong> releases when timing matters.
            </p>""",
            """            <p class="lead">
              瑞鋐科技是<strong>經營者深度參與</strong>的精密 CNC 加工廠，整合車削、銑削與製程工程。核心團隊具<strong>逾 40 年實務經驗（2026）</strong>，擅長複雜機構件並務實掌握交期與品質。我們<strong>積極尋求新的製造夥伴</strong>，仍有<strong>承接更多訂單的產能</strong>，包含必要的<strong>急件</strong>需求。
            </p>""",
        ),
        (
            """              <span class="badge" role="listitem">Taoyuan precision CNC</span>
              <span class="badge" role="listitem">Owner-led · 40+ yrs experience</span>
              <span class="badge" role="listitem">New partnership capacity</span>
              <span class="badge" role="listitem">Quick-turn jobs welcome</span>
              <span class="badge" role="listitem">Fair, straightforward pricing</span>
              <span class="badge" role="listitem">ISO 9001–oriented QMS</span>
              <span class="badge" role="listitem">IATF 16949 / TS 16949 automotive</span>
              <span class="badge" role="listitem">Automated inspection &amp; SPC</span>""",
            """              <span class="badge" role="listitem">桃園精密 CNC</span>
              <span class="badge" role="listitem">經營者主導 · 40+ 年經驗</span>
              <span class="badge" role="listitem">新合作產能</span>
              <span class="badge" role="listitem">急件歡迎</span>
              <span class="badge" role="listitem">合理透明報價</span>
              <span class="badge" role="listitem">ISO 9001 品質系統</span>
              <span class="badge" role="listitem">IATF 16949／TS 16949 汽車</span>
              <span class="badge" role="listitem">自動檢驗與 SPC</span>""",
        ),
        (
            """            <h2 id="hero-aside-heading">How we work with partners</h2>""",
            """            <h2 id="hero-aside-heading">與夥伴合作的方式</h2>""",
        ),
        (
            """              <li>
                <strong>Strong partners on both sides</strong>—we invest in suppliers and customers
                who communicate clearly and commit to mutual success.
              </li>
              <li>
                <strong>Fair quotes</strong>: the owner focuses on long-term relationships, not
                aggressive margin stacking—expect transparent expectations on scope and price.
              </li>
              <li>
                Stable, repeatable processes with in-house fabrication and customized machinery where
                it protects quality and lead time.
              </li>
              <li>
                Systematized quality planning (Advance Product Quality Plan orientation) supported by
                automated inspection when your program requires tight control.
              </li>""",
            """              <li>
                <strong>雙向強夥伴</strong>—我們與溝通清楚、願意共利的供應商與客戶長期投入。
              </li>
              <li>
                <strong>合理報價</strong>：經營者重視長期關係而非層層堆疊毛利，範圍與價格透明。
              </li>
              <li>
                穩定可重複的製程，必要時以廠內治具與客製設備保護品質與交期。
              </li>
              <li>
                以先期品質規劃（APQP 思維）搭配自動量測，在您的專案需要嚴格控管時提供支撐。
              </li>""",
        ),
        (
            """          <h2 class="reveal">Industries &amp; applications—Taoyuan CNC machining samples</h2>""",
            """          <h2 class="reveal">產業與應用—桃園 CNC 加工實例</h2>""",
        ),
        (
            """          <p class="section-intro reveal">
            Representative precision machining across automotive, industrial tools, industrial
            equipment, and bicycle/motorbike applications—useful context when you search for a
            <strong>Taiwan CNC machining partner</strong> with disciplined processes. Final fit,
            finish, and inspection criteria are always aligned to <em>your</em> drawings and
            purchase specifications.
          </p>""",
            """          <p class="section-intro reveal">
            涵蓋汽車、工業手工具、工業設備與自行車／機車等精密加工情境，協助您評估具製程紀律的<strong>台灣 CNC 夥伴</strong>。最終尺寸、表面與檢驗條件一律以<em>貴司</em>圖面與採購規格為準。
          </p>""",
        ),
        (
            '                  alt="Precision machined automotive-related metal components from a Taiwan CNC shop"',
            '                  alt="台灣 CNC 廠汽車相關精密金屬加工件"',
        ),
        (
            """                <h3>Automotive industry</h3>
                <p>
                  Components where dimensional discipline and process stability support downstream
                  assembly and validation workflows.
                </p>""",
            """                <h3>汽車產業</h3>
                <p>
                  以尺寸紀律與製程穩定性支援後段組裝與驗證流程的零組件。
                </p>""",
        ),
        (
            '                  alt="Machined parts for pneumatic and electrical hand tools"',
            '                  alt="氣動與電動手工具加工件"',
        ),
        (
            """                <h3>Pneumatic / electrical hand tools</h3>
                <p>
                  Hardware-oriented geometries and tolerances consistent with hand-tool durability
                  and interface expectations.
                </p>""",
            """                <h3>氣動／電動手工具</h3>
                <p>
                  符合手工具耐久與接口期待的幾何與公差設計。
                </p>""",
        ),
        (
            '                  alt="Industrial machinery precision machined parts"',
            '                  alt="工業機械精密加工件"',
        ),
        (
            """                <h3>Industrial parts</h3>
                <p>
                  Industrial components matched to agreed specifications—suited to equipment builds
                  and medium-volume refresh cycles.
                </p>""",
            """                <h3>工業零件</h3>
                <p>
                  依約定規格生產之工業零組件，適合設備組裝與中量級汰換週期。
                </p>""",
        ),
        (
            '                  alt="Precision components for bicycle and motorbike applications"',
            '                  alt="自行車與機車應用之精密件"',
        ),
        (
            """                <h3>Bicycle &amp; motorbike</h3>
                <p>
                  Applications where weight, fit, and finish requirements align with controlled
                  machining and inspection practices.
                </p>""",
            """                <h3>自行車與機車</h3>
                <p>
                  在重量、配合與外觀要求下，以受控加工與檢驗實務達成目標的應用。
                </p>""",
        ),
        (
            """          <h2 class="reveal">Engineering-led manufacturing &amp; open capacity</h2>""",
            """          <h2 class="reveal">工程導向製造與可承接產能</h2>""",
        ),
        (
            """          <p class="section-intro reveal">
            Our strength goes beyond conventional turned-part supply. We pair production engineering
            with disciplined execution: stable processes, early involvement in your requirements,
            and customer-oriented project management—supporting buyers worldwide who need
            <strong>precision CNC machining in Taiwan</strong> for turning and milling composite
            components. If you are evaluating a <strong>new supplier partnership</strong> or need
            to <strong>add quick-turn capacity</strong> alongside your existing base, we welcome the
            conversation.
          </p>""",
            """          <p class="section-intro reveal">
            我們的強項不僅於傳統車削供應，而是結合生產工程與紀律執行：穩定製程、早期參與需求與以客戶為中心的專案管理，支援全球買主在台尋求<strong>精密 CNC 車銑複合加工</strong>。若您正在評估<strong>新供應商夥伴</strong>或需在既有基礎上<strong>補強急件產能</strong>，歡迎與我們展開對話。
          </p>""",
        ),
        (
            """          <p class="section-intro reveal" style="margin-top: -1rem">
            When programs are complex, we aim to resolve special requirements with strong quality
            discipline, schedule effectiveness, and cost-conscious choices—working with you as early
            as practical and contributing deep machining and integration experience from an
            owner-led team that values trust with both customers and critical suppliers.
          </p>""",
            """          <p class="section-intro reveal" style="margin-top: -1rem">
            面對複雜專案，我們以嚴謹品質紀律、有效排程與成本意識協助解決特殊需求；在可行範圍內越早參與越好，並由經營者帶領的團隊提供深厚加工與整合經驗，重視與客戶及關鍵供應商之間的信任。
          </p>""",
        ),
        (
            """          <h2 class="reveal">Capabilities</h2>""",
            """          <h2 class="reveal">核心能力</h2>""",
        ),
        (
            """          <p class="section-intro reveal">
            From fabrication through logistics, Re Hong organizes capabilities around dependable
            output—suited to <strong>medium-volume manufacturing</strong>, pilot builds, and
            repeat releases where ambiguity and rework are unacceptable.
          </p>""",
            """          <p class="section-intro reveal">
            從製造單元到物流，瑞鋐以可預測的產出組織能力，適合<strong>中量生產</strong>、試作與重複交貨，無法容忍模糊與重工的情境。
          </p>""",
        ),
        (
            """              <h3>Turning &amp; milling integration</h3>
              <p>
                Machining and process integration for composite turned and milled parts, aligned
                with how your assemblies actually come together—not isolated operations without
                system thinking.
              </p>""",
            """              <h3>車銑複合與製程整合</h3>
              <p>
                依組裝實際需求整合車削與銑削，而非缺乏系統觀的單站加工。
              </p>""",
        ),
        (
            """              <h3>Fabrication &amp; in-house machinery</h3>
              <p>
                Automation and specialization beyond standalone CNC: customized machinery built
                in-house to support complex sequences and protect consistency where it matters.
              </p>""",
            """              <h3>廠內製造與專用設備</h3>
              <p>
                超越單機 CNC 的自動化與專業化，必要時於廠內自建客製設備以支援複雜序與一致性。
              </p>""",
        ),
        (
            """              <h3>Development engineering</h3>
              <p>
                Project-based collaboration—attention to detail, shorter paths to stable
                production, and engineering input aimed at manufacturable outcomes.
              </p>""",
            """              <h3>開發工程</h3>
              <p>
                以專案為基礎協作，重視細節、縮短穩定量產路徑，並提供可製造導向的工程建議。
              </p>""",
        ),
        (
            """              <h3>Project management</h3>
              <p>
                Shortening lead time to delivery, coordinating interfaces on your behalf, and
                pursuing overall effectiveness across schedule, quality, and communication—including
                urgent lanes when a quick turn is required.
              </p>""",
            """              <h3>專案管理</h3>
              <p>
                縮短交付前置、代為協調介面，並在交期、品質與溝通間追求整體效益，含必要時的急件路徑。
              </p>""",
        ),
        (
            """              <h3>Quality assurance</h3>
              <p>
                Parts are produced in a high–quality control environment with structured planning,
                including Advance Product Quality Plan thinking and systematized quality
                management—supported by automated inspection as part of the control strategy.
                <a href="/quality.html">ISO 9001 / IATF 16949 overview &amp; photos</a>.
              </p>""",
            """              <h3>品質保證</h3>
              <p>
                於高品質管控環境生產，搭配先期品質規劃與系統化品質管理，並以自動檢驗支撐管制策略。
                <a href="/quality.html">ISO 9001／IATF 16949 說明與照片</a>。
              </p>""",
        ),
        (
            """              <h3>Logistics</h3>
              <p>
                Delivery quality and efficient movement of small-batch parts—supporting programs that
                need frequent releases without sacrificing traceability or arrival condition.
              </p>""",
            """              <h3>物流</h3>
              <p>
                兼顧交貨品質與小批量運輸效率，支援需頻繁出貨且不可犧牲追溯與到貨狀態的專案。
              </p>""",
        ),
        (
            """          <h2 class="reveal">ISO 9001 quality system &amp; IATF 16949 automotive alignment</h2>""",
            """          <h2 class="reveal">ISO 9001 品質系統與 IATF 16949 汽車製程對應</h2>""",
        ),
        (
            """          <p class="section-intro reveal">
            Re Hong runs an <strong>ISO 9001</strong>–oriented quality management framework—clear
            responsibilities, controlled processes, and measurable improvement loops. For automotive
            and regulated supply chains, machining is structured to support customer expectations for
            <strong>IATF 16949</strong> (often referenced historically as
            <strong>ISO/TS 16949</strong>), including APQP-style planning, capability evidence, and
            automated measurement feedback on the shop floor.
          </p>""",
            """          <p class="section-intro reveal">
            瑞鋐以<strong>ISO 9001</strong>精神建構品質管理：權責清楚、流程受控與可量測的改善迴路。針對汽車與受規範供應鏈，加工規劃對應客戶對<strong>IATF 16949</strong>（亦常見歷史稱呼<strong>ISO／TS 16949</strong>）之期待，含 APQP 式規劃、能力證據與現場自動量測回饋。
          </p>""",
        ),
        (
            """              <p class="section-intro" style="margin-bottom: 1rem">
                Inline automated inspection, statistical process studies, vision-based measurement,
                and CMM metrology backstop our promise of low defect rates—not slogans. Review
                representative photos, charts, and equipment on the dedicated quality page.
              </p>
              <p style="margin: 0 0 1.25rem">
                <a class="button-primary" href="/quality.html">Full quality program &amp; evidence</a>
              </p>
              <p class="section-intro" style="margin: 0; font-size: 0.98rem">
                Prefer the short version? Expect disciplined PPAP-style readiness when your program
                demands it, honest discussion when a requirement needs engineering trade-offs, and
                rapid corrective paths when data says adjust.
              </p>""",
            """              <p class="section-intro" style="margin-bottom: 1rem">
                線上自動檢驗、製程能力研究、視覺量測與三次元量床支撐我們對低不良率的承諾，而非口號。更多照片、圖表與設備請見品質專頁。
              </p>
              <p style="margin: 0 0 1.25rem">
                <a class="button-primary" href="/quality.html">完整品質說明與佐證</a>
              </p>
              <p class="section-intro" style="margin: 0; font-size: 0.98rem">
                精簡版：當專案需要時，我們準備 PPAP 取向的文件與實務；若規格需工程權衡，我們坦誠討論；數據顯示需調整時，快速修正。
              </p>""",
        ),
        (
            '                alt="Automated inline dimensional inspection stations with digital displays for Taiwan CNC quality assurance"',
            '                alt="台灣 CNC 品保用自動線上尺寸檢測站與數位顯示"',
        ),
        (
            """              <figcaption>
                Automated inspection line—sample of how we scale measurement throughput without losing
                traceability.
              </figcaption>""",
            """              <figcaption>
                自動檢驗線示意：在提高檢測吞吐的同時維持追溯性。
              </figcaption>""",
        ),
        (
            """            <h3 style="margin: 0 0 0.75rem; font-size: 1.15rem">Why buyers choose Re Hong</h3>""",
            """            <h3 style="margin: 0 0 0.75rem; font-size: 1.15rem">客戶選擇瑞鋐的理由</h3>""",
        ),
        (
            """                <strong style="color: var(--text)">Owner-led decisions</strong>—leadership stays
                close to process, fixtures, and economics.
              </li>
              <li style="margin-bottom: 0.5rem">
                <strong style="color: var(--text)">Fair pricing</strong>—straightforward quotes;
                durable partnerships over margin stacking.
              </li>
              <li style="margin-bottom: 0.5rem">
                <strong style="color: var(--text)">Quick-turn paths</strong> when schedules compress.
              </li>
              <li>Engineering partnership from feasibility through sustained supply.</li>""",
            """                <strong style="color: var(--text)">經營者主導</strong>—決策貼近製程、治具與成本結構。
              </li>
              <li style="margin-bottom: 0.5rem">
                <strong style="color: var(--text)">合理報價</strong>—清楚報價，重視長期合作而非堆疊毛利。
              </li>
              <li style="margin-bottom: 0.5rem">
                <strong style="color: var(--text)">急件路徑</strong>—在排程緊縮時仍可討論可行方案。
              </li>
              <li>從可行性到持續供應的工程夥伴關係。</li>""",
        ),
        (
            """              <h2 style="margin-top: 0; font-size: 1rem">How customers find us</h2>
              <p style="margin: 0; font-size: 0.92rem; color: var(--muted); line-height: 1.55">
                Teams evaluating a <strong>Taiwan CNC supplier</strong> for
                <strong>ISO 9001</strong> control plans, <strong>IATF 16949</strong> flows (including
                legacy <strong>ISO/TS 16949</strong> program language), or
                <strong>automated inspection</strong> and SPC evidence often start with a drawing pack
                and a timeline—we respond with specifics, not generic brochures.
              </p>""",
            """              <h2 style="margin-top: 0; font-size: 1rem">客戶如何找到我們</h2>
              <p style="margin: 0; font-size: 0.92rem; color: var(--muted); line-height: 1.55">
                正在評估<strong>台灣 CNC 供應商</strong>、需要<strong>ISO 9001</strong>管制計畫、<strong>IATF 16949</strong>流程（含<strong>ISO／TS 16949</strong>用語）或<strong>自動檢驗</strong>與 SPC 證據的團隊，通常從圖包與時程開始——我們以具體方案回應，而非制式型錄。
              </p>""",
        ),
        (
            """            <p>
              Seeking a new CNC supplier partnership, extra capacity, or a fast-turn lane from
              Taiwan?
            </p>
            <a href="#contact">Request a quote or introduce your program</a>""",
            """            <p>
              尋找新的 CNC 供應夥伴、額外產能，或從台灣出發的急件通道？
            </p>
            <a href="#contact">索取報價或介紹您的專案</a>""",
        ),
        (
            """          <h2 id="careers-heading" class="reveal">Careers</h2>""",
            """          <h2 id="careers-heading" class="reveal">徵才</h2>""",
        ),
        (
            """          <p class="section-intro reveal">
            Re Hong is growing in production, engineering, and administration—and invests in
            in-service training for people who want to advance technical and professional skills.
          </p>
          <p class="section-intro reveal" style="margin-top: -1rem">
            <a href="/careers.html">View careers information</a> including how we hire and develop
            partners inside the company.
          </p>""",
            """          <p class="section-intro reveal">
            瑞鋐持續擴增生產、工程與行政能量，並為希望精進技術與專業的同仁提供在職訓練。
          </p>
          <p class="section-intro reveal" style="margin-top: -1rem">
            <a href="/careers.html">徵才資訊</a>含徵選方式與同仁發展說明。
          </p>""",
        ),
        (
            """          <h2 class="reveal">Contact</h2>""",
            """          <h2 class="reveal">聯絡</h2>""",
        ),
        (
            """          <p class="section-intro reveal">
            For quotations, technical discussions, quick-turn feasibility, and new supplier
            evaluations, reach us using the official details below. The contact block is reproduced
            exactly as provided by Re Hong Technology.
          </p>""",
            """          <p class="section-intro reveal">
            報價、技術討論、急件可行性或新供應商評鑑，請使用下方官方聯絡資訊。聯絡區塊依瑞鋐科技提供內容逐字保留。
          </p>""",
        ),
        (
            """              <a href="tel:+88634771285">Call +886-3-4771285</a>""",
            """              <a href="tel:+88634771285">電話 +886-3-4771285</a>""",
        ),
        (
            """        <span>© Re Hong Technology · Taoyuan, Taiwan</span>
        <a href="/quality.html">Quality</a>
        <a href="/careers.html">Careers</a>""",
            """        <span>© 瑞鋐科技 · 台灣桃園</span>
        <a href="/quality.html">品質</a>
        <a href="/careers.html">徵才</a>""",
        ),
    ],
}

# For brevity in this repo, Japanese/Korean/Spanish use the same structural replacements
# as Chinese for the longest tail sections is error-prone; we ship full specs in follow-up.
# Here we only wire zh-TW via exhaustive pairs; other locales use a second pass file.

if __name__ == "__main__":
    if not SRC.exists():
        raise SystemExit("index.html not found at repo root")

    write_index("zh-TW", "/zh-TW", "zh-TW", ZH_TW)
    print("Generated zh-TW/index.html. Extend this script with JA/KO/ES pair tables as needed.")
