#!/usr/bin/env python3
"""Постобработка рукописи docx для РИЦ и проверка по памятке.

Правит (на месте):
  - снимает гиперссылки с номеров рисунков, таблиц и источников (памятка: «не делать гиперссылок»),
    текст ссылки остаётся обычным текстом;
  - «Рис. 1.. Название» -> «Рис. 1. Название» (Quarto 1.8 в docx ставит точку дважды);
  - ячейки таблиц: убирает второй w:jc («left», затем «center» — Quarto 1.8; выигрывал center);
  - маркеры списков: «–» шрифтом Times New Roman вместо символа из шрифта Symbol;
Проверяет и печатает замечания (код выхода 1, если есть):
  - подчёркивание; мягкий перенос строки (Shift+Enter) в абзацах текста;
  - шрифт не Times New Roman, кегль основного текста не 14, интервал не 1,5, лист не А4.

Запуск: python3 posle_docx.py _out/glavy/3-2-wbs.docx   (или .html — только подписи)
"""
import re
import shutil
import sys
import tempfile
import zipfile

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def unwrap_hyperlinks(xml):
    """<w:hyperlink ...>runs</w:hyperlink> -> runs; стиль «Hyperlink» у этих runs убирается."""
    n = len(re.findall(r"<w:hyperlink\b", xml))

    def inner(m):
        return re.sub(r'<w:rStyle w:val="Hyperlink"\s*/>', "", m.group(1))

    xml = re.sub(r"<w:hyperlink\b[^>]*>(.*?)</w:hyperlink>", inner, xml, flags=re.S)
    return xml, n


def fix_captions(xml):
    """Двойная точка после номера (между «Рис.» и номером — неразрывный пробел) и два w:pPr подряд
    у абзаца подписи рисунка (так пишет Quarto 1.8; Word такой абзац может не открыть)."""
    pat = r"(Рис\.|Таблица)(\s)(\d+)\.\."
    n = len(re.findall(pat, xml))
    xml = re.sub(pat, r"\1\2\3.", xml)
    xml = re.sub(r'<w:pPr><w:jc w:val="center" /></w:pPr><w:pPr>\s*<w:jc w:val="left"/>',
                 '<w:pPr><w:jc w:val="center"/>', xml)
    return xml, n


def fix_cells(xml):
    pat = r'(<w:jc w:val="left" />)<w:jc w:val="center" />'
    return re.sub(pat, r"\1", xml), len(re.findall(pat, xml))


def fix_bullets(numbering):
    """Уровни с w:numFmt="bullet": текст маркера «–», шрифт Times New Roman."""
    def lvl(m):
        x = m.group(0)
        if 'w:numFmt w:val="bullet"' not in x:
            return x
        x = re.sub(r'<w:lvlText w:val="[^"]*"\s*/>', '<w:lvlText w:val="–" />', x)
        x = re.sub(r"<w:rFonts [^>]*/>", '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" />', x)
        return x
    return re.sub(r"<w:lvl .*?</w:lvl>", lvl, numbering, flags=re.S)


def check(document, styles):
    issues = []
    if re.search(r'<w:u w:val="(?!none)', document) or re.search(r'<w:u w:val="(?!none)', styles):
        issues.append("есть подчёркивание")
    # мягкий перенос: <w:br/> без типа (разрыв страницы — w:type="page" — допустим)
    soft = len(re.findall(r"<w:br\s*/>", document))
    if re.search(r"</w:pPr>\s*<w:pPr>", document):
        issues.append("абзац с двумя w:pPr подряд")
    if re.search(r"<w:jc [^>]*/>\s*<w:jc ", document):
        issues.append("абзац с двумя w:jc подряд")
    if soft:
        issues.append(f"мягких переносов строки (Shift+Enter): {soft}")
    fonts = set(re.findall(r'w:ascii="([^"]+)"', document + styles)) - {"Times New Roman"}
    if fonts:
        issues.append(f"шрифты кроме Times New Roman: {sorted(fonts)}")
    if re.search(r'w:asciiTheme=', document + styles):
        issues.append("шрифт из темы Word (asciiTheme) — подменит Times New Roman")
    m = re.search(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"', document)
    if m and (abs(int(m.group(1)) - 11906) > 20 or abs(int(m.group(2)) - 16838) > 20):
        issues.append(f"лист не А4: {m.group(1)}×{m.group(2)} twip")
    body = re.search(r'<w:style [^>]*w:styleId="BodyText".*?</w:style>', styles, re.S)
    if body and '<w:sz w:val="28"' not in body.group(0):
        issues.append("кегль основного текста не 14")
    if body and 'w:line="360"' not in body.group(0):
        issues.append("межстрочный интервал основного текста не 1,5")
    return issues


def fix_html(path):
    """Та же двойная точка в подписях веб-версии."""
    x = open(path, encoding="utf-8").read()
    x, n = re.subn(r"(Рис\.|Таблица)(\s|&nbsp;)(\d+)\.\.", r"\1\2\3.", x)
    open(path, "w", encoding="utf-8").write(x)
    print(f"{path}: исправлено подписей — {n}")
    return 0


def main(path):
    if path.endswith(".html"):
        return fix_html(path)
    with zipfile.ZipFile(path) as z:
        files = {n: z.read(n) for n in z.namelist()}
    doc = files["word/document.xml"].decode()
    doc, n = unwrap_hyperlinks(doc)
    doc, nc = fix_captions(doc)
    doc, nj = fix_cells(doc)
    files["word/document.xml"] = doc.encode()
    if "word/numbering.xml" in files:
        files["word/numbering.xml"] = fix_bullets(files["word/numbering.xml"].decode()).encode()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    shutil.move(tmp, path)
    print(f"{path}: снято гиперссылок — {n}, исправлено подписей — {nc}, ячеек — {nj}")
    issues = check(doc, files["word/styles.xml"].decode())
    for i in issues:
        print("  !", i)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
