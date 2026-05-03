#!/usr/bin/env python3
"""Assemble zh-TW/ja/ko/es/quality.html from root quality.html + _i18n/quality-main-*.html."""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "quality.html"
MAIN_RE = re.compile(r'(<main id="main">)(.*?)(</main>)', re.DOTALL)


def splice_main(html: str, fragment: str) -> str:
    m = MAIN_RE.search(html)
    if not m:
        raise SystemExit("Could not find <main id=\"main\"> in quality.html")
    return html[: m.end(1)] + "\n" + fragment.rstrip("\n") + "\n" + html[m.start(3) :]


def apply(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        if old not in html:
            raise SystemExit(f"Replacement anchor not found: {old[:80]!r}…")
        html = html.replace(old, new, 1)
    return html


LOCALES: dict[str, dict] = {
    "zh-TW": {
        "out": ROOT / "zh-TW" / "quality.html",
        "fragment": ROOT / "_i18n" / "quality-main-zh-TW.html",
        "pairs": [
            ('<html lang="en">', '<html lang="zh-TW">'),
            (
                """    <title>
      Quality assurance &amp; ISO 9001 / IATF 16949 alignment | Re Hong Technology · Taiwan CNC
    </title>""",
                """    <title>
      品質保證與 ISO 9001／IATF 16949 對應｜瑞鋐科技 · 桃園 CNC
    </title>""",
            ),
            (
                '      content="Re Hong Technology—Taoyuan CNC machining with ISO 9001–oriented quality management, automotive programs aligned with IATF 16949 (ISO/TS 16949), automated inspection, SPC process capability, visual measurement, and Renishaw CMM metrology."',
                '      content="桃園瑞鋐：ISO 9001 品質管理思維、對應 IATF 16949（ISO／TS 16949）的汽車專案、自動檢驗、製程能力（SPC）、視覺量測與 Renishaw CMM 量測實務。"',
            ),
            (
                '<link rel="canonical" href="https://re-hong.com/quality.html" />',
                '<link rel="canonical" href="https://re-hong.com/zh-TW/quality.html" />',
            ),
            (
                '<meta property="og:url" content="https://re-hong.com/quality.html" />',
                '<meta property="og:url" content="https://re-hong.com/zh-TW/quality.html" />',
            ),
            (
                '      content="Quality · ISO 9001 &amp; IATF 16949 | Re Hong Technology Taiwan CNC"',
                '      content="品質 · ISO 9001 與 IATF 16949｜瑞鋐科技 桃園 CNC"',
            ),
            (
                '      content="Preventive quality planning, supplier integration, automated measurement, process capability reporting, and modern metrology—supporting demanding automotive and industrial programs from Taiwan."',
                '      content="預防性品質規劃、供應商協作、自動量測、製程能力文件與現代量測—支援嚴苛的汽車與工業專案。"',
            ),
            (
                '    <meta name="twitter:title" content="Quality &amp; standards | Re Hong Technology" />',
                '    <meta name="twitter:title" content="品質與標準｜瑞鋐科技" />',
            ),
            (
                '      content="ISO 9001–based QMS, IATF 16949 automotive alignment, automated inspection &amp; SPC evidence from our Taoyuan facility."',
                '      content="以 ISO 9001 為基礎的 QMS、IATF 16949 汽車對應、自動檢驗與 SPC 佐證（桃園廠）。"',
            ),
            (
                '        "name": "Quality assurance | Re Hong Technology"',
                '        "name": "品質保證｜瑞鋐科技"',
            ),
            (
                '        "url": "https://re-hong.com/quality.html"',
                '        "url": "https://re-hong.com/zh-TW/quality.html"',
            ),
            (
                '        "description": "Taiwan precision CNC quality management with ISO 9001 orientation and automotive alignment to IATF 16949 / ISO/TS 16949, automated inspection and metrology."',
                '        "description": "台灣精密 CNC 品質管理：ISO 9001 取向、IATF 16949／ISO／TS 16949 汽車對應、自動檢驗與量測。"',
            ),
            ('<a class="skip-link" href="#main">Skip to content</a>', '<a class="skip-link" href="#main">跳至主要內容</a>'),
            (
                '<a class="brand" href="/" aria-label="Re Hong Technology home">',
                '<a class="brand" href="/zh-TW/" aria-label="瑞鋐科技首頁">',
            ),
            ('alt="Re Hong Technology logo"', 'alt="瑞鋐科技標誌"'),
            (
                """          <span class="brand-text">
            Re Hong Technology
            <small>Taiwan · CNC machining</small>
          </span>""",
                """          <span class="brand-text">
            瑞鋐科技
            <small>台灣 · CNC 加工</small>
          </span>""",
            ),
            (
                """        <nav id="site-nav" class="site-nav" aria-label="Primary">
          <ul>
            <li><a href="/#industries">Work samples</a></li>
            <li><a href="/#story">About</a></li>
            <li><a href="/#capabilities">Capabilities</a></li>
            <li><a href="/quality.html" aria-current="page">Quality</a></li>
            <li><a href="/careers.html">Careers</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </nav>""",
                """        <nav id="site-nav" class="site-nav" aria-label="主要導覽">
          <ul>
            <li><a href="/zh-TW/#industries">作品與應用</a></li>
            <li><a href="/zh-TW/#story">關於</a></li>
            <li><a href="/zh-TW/#capabilities">核心能力</a></li>
            <li><a href="/zh-TW/quality.html" aria-current="page">品質</a></li>
            <li><a href="/zh-TW/careers.html">徵才</a></li>
            <li><a href="/zh-TW/#contact">聯絡</a></li>
          </ul>
        </nav>""",
            ),
            ('<span class="lang-toggle__label">English</span>', '<span class="lang-toggle__label">繁體中文</span>'),
            ('aria-label="Open menu"', 'aria-label="開啟選單"'),
            (
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/">Home</a>
        <a href="/careers.html">Careers</a>
        <a href="/#contact">Contact</a>
      </div>
    </footer>""",
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/zh-TW/">首頁</a>
        <a href="/zh-TW/careers.html">徵才</a>
        <a href="/zh-TW/#contact">聯絡</a>
      </div>
    </footer>""",
            ),
        ],
    },
    "ja": {
        "out": ROOT / "ja" / "quality.html",
        "fragment": ROOT / "_i18n" / "quality-main-ja.html",
        "pairs": [
            ('<html lang="en">', '<html lang="ja">'),
            (
                """    <title>
      Quality assurance &amp; ISO 9001 / IATF 16949 alignment | Re Hong Technology · Taiwan CNC
    </title>""",
                """    <title>
      品質保証と ISO 9001／IATF 16949 対応｜瑞鋐科技 · 台湾桃園 CNC
    </title>""",
            ),
            (
                '      content="Re Hong Technology—Taoyuan CNC machining with ISO 9001–oriented quality management, automotive programs aligned with IATF 16949 (ISO/TS 16949), automated inspection, SPC process capability, visual measurement, and Renishaw CMM metrology."',
                '      content="桃園の瑞鋐：ISO 9001 に沿った品質管理、IATF 16949（ISO／TS 16949）の自動車プログラム、自動検査、SPC、ビジョン測定、Renishaw CMM。"',
            ),
            (
                '<link rel="canonical" href="https://re-hong.com/quality.html" />',
                '<link rel="canonical" href="https://re-hong.com/ja/quality.html" />',
            ),
            (
                '<meta property="og:url" content="https://re-hong.com/quality.html" />',
                '<meta property="og:url" content="https://re-hong.com/ja/quality.html" />',
            ),
            (
                '      content="Quality · ISO 9001 &amp; IATF 16949 | Re Hong Technology Taiwan CNC"',
                '      content="品質 · ISO 9001 と IATF 16949｜瑞鋐科技 桃園 CNC"',
            ),
            (
                '      content="Preventive quality planning, supplier integration, automated measurement, process capability reporting, and modern metrology—supporting demanding automotive and industrial programs from Taiwan."',
                '      content="予防的品質計画、サプライヤ連携、自動測定、工程能力、最新計測—厳しい自動車・産業プログラムを台湾から支援。"',
            ),
            (
                '    <meta name="twitter:title" content="Quality &amp; standards | Re Hong Technology" />',
                '    <meta name="twitter:title" content="品質と規格｜瑞鋐科技" />',
            ),
            (
                '      content="ISO 9001–based QMS, IATF 16949 automotive alignment, automated inspection &amp; SPC evidence from our Taoyuan facility."',
                '      content="ISO 9001 ベースの QMS、IATF 16949 自動車対応、自動検査と SPC の実証（桃園拠点）。"',
            ),
            (
                '        "name": "Quality assurance | Re Hong Technology"',
                '        "name": "品質保証｜瑞鋐科技"',
            ),
            (
                '        "url": "https://re-hong.com/quality.html"',
                '        "url": "https://re-hong.com/ja/quality.html"',
            ),
            (
                '        "description": "Taiwan precision CNC quality management with ISO 9001 orientation and automotive alignment to IATF 16949 / ISO/TS 16949, automated inspection and metrology."',
                '        "description": "台湾の精密 CNC：ISO 9001、IATF 16949／ISO／TS 16949 自動車対応、自動検査と計測。"',
            ),
            ('<a class="skip-link" href="#main">Skip to content</a>', '<a class="skip-link" href="#main">本文へスキップ</a>'),
            (
                '<a class="brand" href="/" aria-label="Re Hong Technology home">',
                '<a class="brand" href="/ja/" aria-label="瑞鋐科技ホーム">',
            ),
            ('alt="Re Hong Technology logo"', 'alt="瑞鋐科技ロゴ"'),
            (
                """          <span class="brand-text">
            Re Hong Technology
            <small>Taiwan · CNC machining</small>
          </span>""",
                """          <span class="brand-text">
            瑞鋐科技
            <small>台湾 · CNC 加工</small>
          </span>""",
            ),
            (
                """        <nav id="site-nav" class="site-nav" aria-label="Primary">
          <ul>
            <li><a href="/#industries">Work samples</a></li>
            <li><a href="/#story">About</a></li>
            <li><a href="/#capabilities">Capabilities</a></li>
            <li><a href="/quality.html" aria-current="page">Quality</a></li>
            <li><a href="/careers.html">Careers</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </nav>""",
                """        <nav id="site-nav" class="site-nav" aria-label="メインメニュー">
          <ul>
            <li><a href="/ja/#industries">製作事例</a></li>
            <li><a href="/ja/#story">概要</a></li>
            <li><a href="/ja/#capabilities">技術・設備</a></li>
            <li><a href="/ja/quality.html" aria-current="page">品質</a></li>
            <li><a href="/ja/careers.html">採用</a></li>
            <li><a href="/ja/#contact">お問い合わせ</a></li>
          </ul>
        </nav>""",
            ),
            ('<span class="lang-toggle__label">English</span>', '<span class="lang-toggle__label">日本語</span>'),
            ('aria-label="Open menu"', 'aria-label="メニューを開く"'),
            (
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/">Home</a>
        <a href="/careers.html">Careers</a>
        <a href="/#contact">Contact</a>
      </div>
    </footer>""",
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/ja/">ホーム</a>
        <a href="/ja/careers.html">採用</a>
        <a href="/ja/#contact">お問い合わせ</a>
      </div>
    </footer>""",
            ),
        ],
    },
    "ko": {
        "out": ROOT / "ko" / "quality.html",
        "fragment": ROOT / "_i18n" / "quality-main-ko.html",
        "pairs": [
            ('<html lang="en">', '<html lang="ko">'),
            (
                """    <title>
      Quality assurance &amp; ISO 9001 / IATF 16949 alignment | Re Hong Technology · Taiwan CNC
    </title>""",
                """    <title>
      품질 보증 및 ISO 9001／IATF 16949 대응 | 루이홍 테크놀로지 · 대만 타오위안 CNC
    </title>""",
            ),
            (
                '      content="Re Hong Technology—Taoyuan CNC machining with ISO 9001–oriented quality management, automotive programs aligned with IATF 16949 (ISO/TS 16949), automated inspection, SPC process capability, visual measurement, and Renishaw CMM metrology."',
                '      content="타오위안 루이홍: ISO 9001 품질 관리, IATF 16949(ISO/TS 16949) 자동차 프로그램, 자동 검사, SPC 공정 능력, 비전 측정, Renishaw CMM."',
            ),
            (
                '<link rel="canonical" href="https://re-hong.com/quality.html" />',
                '<link rel="canonical" href="https://re-hong.com/ko/quality.html" />',
            ),
            (
                '<meta property="og:url" content="https://re-hong.com/quality.html" />',
                '<meta property="og:url" content="https://re-hong.com/ko/quality.html" />',
            ),
            (
                '      content="Quality · ISO 9001 &amp; IATF 16949 | Re Hong Technology Taiwan CNC"',
                '      content="품질 · ISO 9001 및 IATF 16949 | 루이홍 테크놀로지 타오위안 CNC"',
            ),
            (
                '      content="Preventive quality planning, supplier integration, automated measurement, process capability reporting, and modern metrology—supporting demanding automotive and industrial programs from Taiwan."',
                '      content="예방 품질 계획, 공급사 연계, 자동 측정, 공정 능력, 최신 계측—엄격한 자동차·산업 프로그램을 대만에서 지원."',
            ),
            (
                '    <meta name="twitter:title" content="Quality &amp; standards | Re Hong Technology" />',
                '    <meta name="twitter:title" content="품질 및 표준 | 루이홍 테크놀로지" />',
            ),
            (
                '      content="ISO 9001–based QMS, IATF 16949 automotive alignment, automated inspection &amp; SPC evidence from our Taoyuan facility."',
                '      content="ISO 9001 기반 QMS, IATF 16949 자동차 정렬, 자동 검사 및 SPC 근거(타오위안 시설)."',
            ),
            (
                '        "name": "Quality assurance | Re Hong Technology"',
                '        "name": "품질 보증 | 루이홍 테크놀로지"',
            ),
            (
                '        "url": "https://re-hong.com/quality.html"',
                '        "url": "https://re-hong.com/ko/quality.html"',
            ),
            (
                '        "description": "Taiwan precision CNC quality management with ISO 9001 orientation and automotive alignment to IATF 16949 / ISO/TS 16949, automated inspection and metrology."',
                '        "description": "대만 정밀 CNC 품질 관리: ISO 9001, IATF 16949/ISO/TS 16949 자동차 정렬, 자동 검사 및 계측."',
            ),
            ('<a class="skip-link" href="#main">Skip to content</a>', '<a class="skip-link" href="#main">본문 바로가기</a>'),
            (
                '<a class="brand" href="/" aria-label="Re Hong Technology home">',
                '<a class="brand" href="/ko/" aria-label="루이홍 테크놀로지 홈">',
            ),
            ('alt="Re Hong Technology logo"', 'alt="루이홍 테크놀로지 로고"'),
            (
                """          <span class="brand-text">
            Re Hong Technology
            <small>Taiwan · CNC machining</small>
          </span>""",
                """          <span class="brand-text">
            Re Hong Technology
            <small>대만 · CNC 가공</small>
          </span>""",
            ),
            (
                """        <nav id="site-nav" class="site-nav" aria-label="Primary">
          <ul>
            <li><a href="/#industries">Work samples</a></li>
            <li><a href="/#story">About</a></li>
            <li><a href="/#capabilities">Capabilities</a></li>
            <li><a href="/quality.html" aria-current="page">Quality</a></li>
            <li><a href="/careers.html">Careers</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </nav>""",
                """        <nav id="site-nav" class="site-nav" aria-label="주 메뉴">
          <ul>
            <li><a href="/ko/#industries">작업 사례</a></li>
            <li><a href="/ko/#story">소개</a></li>
            <li><a href="/ko/#capabilities">역량</a></li>
            <li><a href="/ko/quality.html" aria-current="page">품질</a></li>
            <li><a href="/ko/careers.html">채용</a></li>
            <li><a href="/ko/#contact">문의</a></li>
          </ul>
        </nav>""",
            ),
            ('<span class="lang-toggle__label">English</span>', '<span class="lang-toggle__label">한국어</span>'),
            ('aria-label="Open menu"', 'aria-label="메뉴 열기"'),
            (
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/">Home</a>
        <a href="/careers.html">Careers</a>
        <a href="/#contact">Contact</a>
      </div>
    </footer>""",
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/ko/">홈</a>
        <a href="/ko/careers.html">채용</a>
        <a href="/ko/#contact">문의</a>
      </div>
    </footer>""",
            ),
        ],
    },
    "es": {
        "out": ROOT / "es" / "quality.html",
        "fragment": ROOT / "_i18n" / "quality-main-es.html",
        "pairs": [
            ('<html lang="en">', '<html lang="es">'),
            (
                """    <title>
      Quality assurance &amp; ISO 9001 / IATF 16949 alignment | Re Hong Technology · Taiwan CNC
    </title>""",
                """    <title>
      Garantía de calidad e ISO 9001 / IATF 16949 | Re Hong Technology · CNC en Taoyuán, Taiwán
    </title>""",
            ),
            (
                '      content="Re Hong Technology—Taoyuan CNC machining with ISO 9001–oriented quality management, automotive programs aligned with IATF 16949 (ISO/TS 16949), automated inspection, SPC process capability, visual measurement, and Renishaw CMM metrology."',
                '      content="Re Hong en Taoyuán: gestión de calidad orientada a ISO 9001, programas automotrices alineados con IATF 16949 (ISO/TS 16949), inspección automatizada, capacidad de proceso (SPC), medición visual y CMM Renishaw."',
            ),
            (
                '<link rel="canonical" href="https://re-hong.com/quality.html" />',
                '<link rel="canonical" href="https://re-hong.com/es/quality.html" />',
            ),
            (
                '<meta property="og:url" content="https://re-hong.com/quality.html" />',
                '<meta property="og:url" content="https://re-hong.com/es/quality.html" />',
            ),
            (
                '      content="Quality · ISO 9001 &amp; IATF 16949 | Re Hong Technology Taiwan CNC"',
                '      content="Calidad · ISO 9001 e IATF 16949 | Re Hong Technology CNC Taoyuán"',
            ),
            (
                '      content="Preventive quality planning, supplier integration, automated measurement, process capability reporting, and modern metrology—supporting demanding automotive and industrial programs from Taiwan."',
                '      content="Planificación preventiva, integración con proveedores, medición automatizada, capacidad de proceso y metrología moderna—programas automotrices e industriales exigentes desde Taiwán."',
            ),
            (
                '    <meta name="twitter:title" content="Quality &amp; standards | Re Hong Technology" />',
                '    <meta name="twitter:title" content="Calidad y normas | Re Hong Technology" />',
            ),
            (
                '      content="ISO 9001–based QMS, IATF 16949 automotive alignment, automated inspection &amp; SPC evidence from our Taoyuan facility."',
                '      content="SGC basado en ISO 9001, alineación automotriz IATF 16949, inspección automatizada y evidencia SPC desde Taoyuán."',
            ),
            (
                '        "name": "Quality assurance | Re Hong Technology"',
                '        "name": "Garantía de calidad | Re Hong Technology"',
            ),
            (
                '        "url": "https://re-hong.com/quality.html"',
                '        "url": "https://re-hong.com/es/quality.html"',
            ),
            (
                '        "description": "Taiwan precision CNC quality management with ISO 9001 orientation and automotive alignment to IATF 16949 / ISO/TS 16949, automated inspection and metrology."',
                '        "description": "Gestión de calidad CNC de precisión en Taiwán con ISO 9001 e IATF 16949 / ISO/TS 16949, inspección automatizada y metrología."',
            ),
            ('<a class="skip-link" href="#main">Skip to content</a>', '<a class="skip-link" href="#main">Ir al contenido</a>'),
            (
                '<a class="brand" href="/" aria-label="Re Hong Technology home">',
                '<a class="brand" href="/es/" aria-label="Inicio Re Hong Technology">',
            ),
            ('alt="Re Hong Technology logo"', 'alt="Logotipo de Re Hong Technology"'),
            (
                """          <span class="brand-text">
            Re Hong Technology
            <small>Taiwan · CNC machining</small>
          </span>""",
                """          <span class="brand-text">
            Re Hong Technology
            <small>Taiwán · mecanizado CNC</small>
          </span>""",
            ),
            (
                """        <nav id="site-nav" class="site-nav" aria-label="Primary">
          <ul>
            <li><a href="/#industries">Work samples</a></li>
            <li><a href="/#story">About</a></li>
            <li><a href="/#capabilities">Capabilities</a></li>
            <li><a href="/quality.html" aria-current="page">Quality</a></li>
            <li><a href="/careers.html">Careers</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </nav>""",
                """        <nav id="site-nav" class="site-nav" aria-label="Principal">
          <ul>
            <li><a href="/es/#industries">Referencias</a></li>
            <li><a href="/es/#story">Empresa</a></li>
            <li><a href="/es/#capabilities">Capacidades</a></li>
            <li><a href="/es/quality.html" aria-current="page">Calidad</a></li>
            <li><a href="/es/careers.html">Carreras</a></li>
            <li><a href="/es/#contact">Contacto</a></li>
          </ul>
        </nav>""",
            ),
            ('<span class="lang-toggle__label">English</span>', '<span class="lang-toggle__label">Español</span>'),
            ('aria-label="Open menu"', 'aria-label="Abrir menú"'),
            (
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/">Home</a>
        <a href="/careers.html">Careers</a>
        <a href="/#contact">Contact</a>
      </div>
    </footer>""",
                """    <footer class="site-footer-meta">
      <div class="wrap">
        <a href="/es/">Inicio</a>
        <a href="/es/careers.html">Carreras</a>
        <a href="/es/#contact">Contacto</a>
      </div>
    </footer>""",
            ),
        ],
    },
}


def main() -> None:
    raw = SRC.read_text(encoding="utf-8")
    for _locale, cfg in LOCALES.items():
        frag = cfg["fragment"].read_text(encoding="utf-8")
        html = splice_main(raw, frag)
        html = apply(html, cfg["pairs"])
        cfg["out"].parent.mkdir(parents=True, exist_ok=True)
        cfg["out"].write_text(html, encoding="utf-8")
        print("Wrote", cfg["out"].relative_to(ROOT))


if __name__ == "__main__":
    main()
