#!/usr/bin/env python3
"""reference.docx для рукописи РИЦ: А4, Times New Roman 14, интервал 1,5, абзацный отступ 1,25 см.

Берёт стандартный reference.docx Pandoc и переписывает в нём стили (python-docx).
Запуск: python3 shablony/make_reference_docx.py  (из папки proba-steka)
"""
import subprocess

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.shared import Cm, Pt, RGBColor

OUT = "shablony/reference.docx"
subprocess.run(["pandoc", "-o", OUT, "--print-default-data-file", "reference.docx"], check=True)

doc = Document(OUT)
for s in doc.sections:
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2)

BLACK = RGBColor(0, 0, 0)
for st in doc.styles:
    if st.type not in (1, 2):  # стили абзацев и символов
        continue
    st.font.name = "Times New Roman"
    st.font.color.rgb = BLACK
    rpr = st.element.get_or_add_rPr()
    rf = rpr.get_or_add_rFonts()
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    for k in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        rf.attrib.pop(W + k, None)  # тема Word иначе подставляет Calibri в заголовки
    for k in ("ascii", "hAnsi", "eastAsia", "cs"):
        rf.set(W + k, "Times New Roman")
    if st.type == 2:
        continue
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if st.name.startswith("Heading"):
        st.font.size = Pt(14)
        st.font.bold = True
        st.font.italic = False
        pf.space_before, pf.space_after = Pt(12), Pt(6)
    elif st.name == "Compact":  # ячейки таблиц и плотные списки: без абзацного отступа
        st.font.size = Pt(14)
        pf.first_line_indent = Cm(0)
        pf.space_before = pf.space_after = Pt(0)
    elif st.name in ("Normal", "Body Text", "First Paragraph"):
        st.font.size = Pt(14)
        pf.first_line_indent = Cm(1.25)
        pf.space_before = pf.space_after = Pt(0)
    else:
        st.font.size = Pt(14)

# Шрифт по умолчанию документа (docDefaults) — тоже без темы Word
Wn = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
for rf in doc.styles.element.iter(Wn + "rFonts"):
    for k in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        rf.attrib.pop(Wn + k, None)
    for k in ("ascii", "hAnsi", "eastAsia", "cs"):
        rf.set(Wn + k, "Times New Roman")

# Подписи: «Рис. 1. Название», без курсива
for name in ("Caption", "Image Caption", "Table Caption"):
    if name in [s.name for s in doc.styles]:
        [x for x in doc.styles if x.name == name][0].font.italic = False
        [x for x in doc.styles if x.name == name][0].paragraph_format.first_line_indent = Cm(0)

# Гиперссылки без подчёркивания и цвета (памятка: выделение не подчёркиванием)
for st in doc.styles:
    if st.name == "Hyperlink":
        st.font.underline = False
        st.font.color.rgb = BLACK
# Стиль «Врезка» для определений и примеров: рамка, без абзацного отступа (в docx — custom-style)
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

vr = doc.styles.add_style("Врезка", WD_STYLE_TYPE.PARAGRAPH)
vr.base_style = [x for x in doc.styles if x.name == "Body Text"][0]
vr.paragraph_format.first_line_indent = Cm(0)
vr.paragraph_format.space_before = vr.paragraph_format.space_after = Pt(3)
bdr = OxmlElement("w:pBdr")
for side in ("top", "left", "bottom", "right"):
    e = OxmlElement(f"w:{side}")
    e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:space"), "4"); e.set(qn("w:color"), "000000")
    bdr.append(e)
vr.element.get_or_add_pPr().append(bdr)
doc.save(OUT)
print(OUT)
