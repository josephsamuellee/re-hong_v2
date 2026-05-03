#!/usr/bin/env python3
"""Assemble ja/ko/es/index.html from zh-TW/index.html + translated <main> fragments."""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
ZH = ROOT / "zh-TW" / "index.html"
MAIN_RE = re.compile(r"(<main id=\"main\">)(.*?)(</main>)", re.DOTALL)


def base_head(prefix: str, html_lang: str, label: str) -> list[tuple[str, str]]:
    base = f"https://re-hong.com{prefix}/"
    return [
        ('<html lang="zh-TW">', f'<html lang="{html_lang}">'),
        ("https://re-hong.com/zh-TW/", base),
        ("/zh-TW/", f"{prefix}/"),
        ("繁體中文", label),
    ]


LOCALES: dict[str, dict] = {
    "ja": {
        "prefix": "/ja",
        "html_lang": "ja",
        "label": "日本語",
        "fragment": ROOT / "_i18n" / "main-ja.html",
        "extras": [
            ('aria-label="瑞鋐科技首頁"', 'aria-label="瑞鋐科技ホーム"'),
            ('alt="瑞鋐科技標誌"', 'alt="瑞鋐科技ロゴ"'),
            ('aria-label="主要導覽"', 'aria-label="メインメニュー"'),
            ("跳至主要內容", "本文へスキップ"),
            ("開啟選單", "メニューを開く"),
            ("作品與應用", "製作事例"),
            ("關於", "概要"),
            ("核心能力", "技術・設備"),
            ("品質與 ISO", "品質"),
            ("徵才", "採用"),
            ("聯絡", "お問い合わせ"),
            (
                """    <title>
      瑞鋐科技 | 台灣桃園 CNC 加工夥伴 · 急件 · 合理報價
    </title>""",
                """    <title>
      瑞鋐科技 | 台湾桃園の CNC パートナー · 短納期・公正な価格
    </title>""",
            ),
            (
                'content="桃園瑞鋐為經營者深度參與的精密 CNC 加工廠：ISO 9001 品質管理思維、汽車供應鏈對應 IATF 16949／ISO／TS 16949、40 年以上實務經驗（2026）、急件產能、合理透明報價、自動量測與 SPC。服務汽車、手工具、工業與自行車等領域。"',
                'content="桃園の瑞鋐はオーナー主導の精密 CNC 工場。ISO 9001 の品質管理、IATF 16949／ISO／TS 16949 に沿った自動車サプライチェーン、2026 年時点で 40 年以上の実務経験、短納期対応、公正な見積、自動測定と SPC。自動車、工具、産業、自転車分野を支援。"',
            ),
            (
                'content="瑞鋐科技 | 台灣 CNC 夥伴 · 桃園 · 急件與合理價格"',
                'content="瑞鋐科技 | 台湾 CNC パートナー · 桃園 · 短納期と公正価格"',
            ),
            (
                'content="桃園 CNC：ISO 9001 品質系統、IATF 16949／TS 16949 汽車製程對應、經營者主導、40 年以上經驗、急件、合理報價、自動檢驗與 SPC。"',
                'content="桃園 CNC：ISO 9001、IATF 16949／TS 16949 自動車プロセス、オーナー主導、40 年以上の経験、短納期、公正な価格、自動検査と SPC。"',
            ),
            (
                'content="瑞鋐科技 | 台灣 CNC · 急件 · 合理價格"',
                'content="瑞鋐科技 | 台湾 CNC · 短納期 · 公正価格"',
            ),
            (
                'content="台灣精密 CNC：桃園廠區、急件產能、合理報價、經營者主導與深厚技術—歡迎新製造夥伴。"',
                'content="台湾の精密 CNC：桃園拠点、短納期余力、公正な見積、オーナー主導と豊富な技術—新しい製造パートナーを歓迎。"',
            ),
            (
                '        "description": "台灣桃園瑞鋐：ISO 9001 品質管理、IATF 16949／TS 16949 汽車製程、車銑複合加工、急件產能、合理報價、自動檢驗與製程能力。"',
                '        "description": "台湾桃園の瑞鋐：ISO 9001、IATF 16949／TS 16949 自動車プロセス、旋削／フライス複合、短納期、公正価格、自動検査と工程能力。"',
            ),
            ("© 瑞鋐科技 · 台灣桃園", "© Re Hong Technology · Taoyuán, Taiwán"),
        ],
    },
    "ko": {
        "prefix": "/ko",
        "html_lang": "ko",
        "label": "한국어",
        "fragment": ROOT / "_i18n" / "main-ko.html",
        "extras": [
            ('aria-label="瑞鋐科技首頁"', 'aria-label="루이홍 테크놀로지 홈"'),
            ('alt="瑞鋐科技標誌"', 'alt="루이홍 테크놀로지 로고"'),
            ('aria-label="主要導覽"', 'aria-label="주 메뉴"'),
            ("跳至主要內容", "본문 바로가기"),
            ("開啟選單", "메뉴 열기"),
            ("作品與應用", "작업 사례"),
            ("關於", "소개"),
            ("核心能力", "역량"),
            ("品質與 ISO", "품질"),
            ("徵才", "채용"),
            ("聯絡", "문의"),
            (
                """    <title>
      瑞鋐科技 | 台灣桃園 CNC 加工夥伴 · 急件 · 合理報價
    </title>""",
                """    <title>
      루이홍 테크놀로지 | 대만 타오위안 CNC 파트너 · 긴급 납품 · 합리적 견적
    </title>""",
            ),
            (
                'content="桃園瑞鋐為經營者深度參與的精密 CNC 加工廠：ISO 9001 品質管理思維、汽車供應鏈對應 IATF 16949／ISO／TS 16949、40 年以上實務經驗（2026）、急件產能、合理透明報價、自動量測與 SPC。服務汽車、手工具、工業與自行車等領域。"',
                'content="타오위안의 루이홍은 경영자 주도 정밀 CNC 공장입니다. ISO 9001 품질 관리, IATF 16949／ISO／TS 16949 자동차 공급망, 2026년 기준 40년 이상의 경험, 긴급 납품, 투명한 합리 견적, 자동 측정과 SPC. 자동차·공구·산업·자전거 분야를 지원합니다."',
            ),
            (
                'content="瑞鋐科技 | 台灣 CNC 夥伴 · 桃園 · 急件與合理價格"',
                'content="루이홍 테크놀로지 | 대만 CNC 파트너 · 타오위안 · 긴급 납품과 합리적 가격"',
            ),
            (
                'content="桃園 CNC：ISO 9001 品質系統、IATF 16949／TS 16949 汽車製程對應、經營者主導、40 年以上經驗、急件、合理報價、自動檢驗與 SPC。"',
                'content="타오위안 CNC: ISO 9001, IATF 16949／TS 16949 자동차 공정, 경영자 주도, 40년 이상 경험, 긴급 납품, 합리적 가격, 자동 검사와 SPC."',
            ),
            (
                'content="瑞鋐科技 | 台灣 CNC · 急件 · 合理價格"',
                'content="루이홍 테크놀로지 | 대만 CNC · 긴급 납품 · 합리적 가격"',
            ),
            (
                'content="台灣精密 CNC：桃園廠區、急件產能、合理報價、經營者主導與深厚技術—歡迎新製造夥伴。"',
                'content="대만 정밀 CNC: 타오위안 공장, 긴급 납품 여력, 합리적 견적, 경영자 주도와 깊은 기술—새로운 제조 파트너를 환영합니다."',
            ),
            (
                '        "description": "台灣桃園瑞鋐：ISO 9001 品質管理、IATF 16949／TS 16949 汽車製程、車銑複合加工、急件產能、合理報價、自動檢驗與製程能力。"',
                '        "description": "대만 타오위안 루이홍: ISO 9001, IATF 16949／TS 16949 자동차 공정, 선반·밀링 복합, 긴급 납품, 합리적 가격, 자동 검사와 공정 능력."',
            ),
            ("© 瑞鋐科技 · 台灣桃園", "© Re Hong Technology · Taoyuán, Taiwán"),
        ],
    },
    "es": {
        "prefix": "/es",
        "html_lang": "es",
        "label": "Español",
        "fragment": ROOT / "_i18n" / "main-es.html",
        "extras": [
            ('aria-label="瑞鋐科技首頁"', 'aria-label="Inicio de Re Hong Technology"'),
            ('alt="瑞鋐科技標誌"', 'alt="Logotipo de Re Hong Technology"'),
            ('aria-label="主要導覽"', 'aria-label="Navegación principal"'),
            ("跳至主要內容", "Ir al contenido"),
            ("開啟選單", "Abrir menú"),
            ("作品與應用", "Referencias"),
            ("關於", "Empresa"),
            ("核心能力", "Capacidades"),
            ("品質與 ISO", "Calidad"),
            ("徵才", "Carreras"),
            ("聯絡", "Contacto"),
            (
                """    <title>
      瑞鋐科技 | 台灣桃園 CNC 加工夥伴 · 急件 · 合理報價
    </title>""",
                """    <title>
      Re Hong Technology | Socio CNC en Taoyuán, Taiwán · entrega rápida · precios justos
    </title>""",
            ),
            (
                'content="桃園瑞鋐為經營者深度參與的精密 CNC 加工廠：ISO 9001 品質管理思維、汽車供應鏈對應 IATF 16949／ISO／TS 16949、40 年以上實務經驗（2026）、急件產能、合理透明報價、自動量測與 SPC。服務汽車、手工具、工業與自行車等領域。"',
                'content="Re Hong en Taoyuán es un taller CNC de precisión dirigido por su propietario: gestión de calidad ISO 9001, cadena de suministro automotriz alineada con IATF 16949／ISO／TS 16949, más de 40 años de experiencia (2026), capacidad de giro rápido, precios transparentes, medición automática y SPC. Sectores automoción, herramientas, industria y bicicleta."',
            ),
            (
                'content="瑞鋐科技 | 台灣 CNC 夥伴 · 桃園 · 急件與合理價格"',
                'content="Re Hong Technology | Socio CNC en Taiwán · Taoyuán · rapidez y precios justos"',
            ),
            (
                'content="桃園 CNC：ISO 9001 品質系統、IATF 16949／TS 16949 汽車製程對應、經營者主導、40 年以上經驗、急件、合理報價、自動檢驗與 SPC。"',
                'content="CNC en Taoyuán: ISO 9001, IATF 16949／TS 16949 automoción, gestión directa, más de 40 años de experiencia, giros rápidos, precios justos, inspección automática y SPC."',
            ),
            (
                'content="瑞鋐科技 | 台灣 CNC · 急件 · 合理價格"',
                'content="Re Hong Technology | CNC en Taiwán · rapidez · precios justos"',
            ),
            (
                'content="台灣精密 CNC：桃園廠區、急件產能、合理報價、經營者主導與深厚技術—歡迎新製造夥伴。"',
                'content="CNC de precisión en Taiwán: planta en Taoyuán, capacidad rápida, precios justos, liderazgo del propietario y gran experiencia técnica—nuevas alianzas de fabricación bienvenidas."',
            ),
            (
                '        "description": "台灣桃園瑞鋐：ISO 9001 品質管理、IATF 16949／TS 16949 汽車製程、車銑複合加工、急件產能、合理報價、自動檢驗與製程能力。"',
                '        "description": "Re Hong en Taoyuán, Taiwán: ISO 9001, IATF 16949／TS 16949 automoción, mecanizado compuesto torneado-fresado, capacidad de giro rápido, precios justos, inspección automática y capacidad de proceso."',
            ),
            ("© 瑞鋐科技 · 台灣桃園", "© Re Hong Technology · Taoyuán, Taiwán"),
        ],
    },
}


def main() -> None:
    zh_text = ZH.read_text(encoding="utf-8")
    if not MAIN_RE.search(zh_text):
        raise SystemExit("Could not find <main> in zh-TW/index.html")

    for key, cfg in LOCALES.items():
        frag_path = cfg["fragment"]
        if not frag_path.exists():
            raise SystemExit(f"Missing fragment: {frag_path}")
        inner = frag_path.read_text(encoding="utf-8").strip()
        text = MAIN_RE.sub(r"\1" + inner + r"\3", zh_text, count=1)
        for a, b in base_head(cfg["prefix"], cfg["html_lang"], cfg["label"]):
            text = text.replace(a, b)
        for a, b in cfg.get("extras", []):
            if a == b:
                continue
            if a not in text:
                raise SystemExit(f"[{key}] missing fragment: {a[:100]!r}")
            text = text.replace(a, b, 1)
        out = ROOT / key / "index.html"
        out.write_text(text, encoding="utf-8")
        print("Wrote", out)


if __name__ == "__main__":
    main()
