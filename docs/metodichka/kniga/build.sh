#!/usr/bin/env bash
# Сборка книги (пилот — глава 3.2 WBS): рисунки -> проверка -> веб, рукопись docx для РИЦ, PDF А5.
# Нужен стек из ../proba-steka/ustanovka.sh. Результат — _out/glavy/, копия для просмотра — rezultat/.
set -euo pipefail
cd "$(dirname "$0")"

python3 risunki/g3_2_wbs.py            # упадёт, если печатный рисунок шире 114 мм или не тем шрифтом
python3 shablony/make_reference_docx.py 2>/dev/null
python3 proverka.py                     # тон, даты, подписи, ссылки, рубрикация, рисунки

for f in html docx typst; do quarto render glavy/3-2-wbs.qmd --to "$f" --quiet; done
python3 posle_docx.py _out/glavy/3-2-wbs.docx   # гиперссылки, подписи, ячейки, маркеры + проверка
python3 posle_docx.py _out/glavy/3-2-wbs.html

# рукопись глазами РИЦ: docx -> PDF через LibreOffice
(cd _out/glavy && soffice --headless --convert-to pdf 3-2-wbs.docx >/dev/null)

mkdir -p rezultat
cp _out/glavy/3-2-wbs-a5.pdf rezultat/3-2-wbs_pechat-A5.pdf
cp _out/glavy/3-2-wbs.docx rezultat/3-2-wbs_rukopis-RIC.docx
cp _out/glavy/3-2-wbs.pdf rezultat/3-2-wbs_rukopis-RIC_LibreOffice.pdf
cp _out/glavy/3-2-wbs.html rezultat/3-2-wbs_veb.html
for p in rezultat/*.pdf; do printf '%-45s %s стр., %s\n' "$p" "$(pdfinfo "$p" | awk '/Pages/{print $2}')" \
  "$(pdffonts "$p" | tail -n +3 | awk '{print $1}' | sed 's/.*+//' | sort -u | tr '\n' ' ')"; done
