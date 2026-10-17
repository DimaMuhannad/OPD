#!/usr/bin/env bash
# Проба стека на фрагменте главы WBS: один исходник wbs.qmd -> html, docx (РИЦ), PDF А5 тремя движками.
# Нужны: quarto, graphviz, TeX Live (xelatex, biber), Times New Roman в системе,
# npm-пакеты pagedjs, playwright-core, @vivliostyle/cli в /opt/stack/npm (см. ROADMAP.md, раздел «Что проверено»).
set -euo pipefail
cd "$(dirname "$0")"
NPM=/opt/stack/npm/node_modules
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

python3 risunki/wbs_tree.py
python3 shablony/make_reference_docx.py
for f in html docx typst pdf; do quarto render wbs.qmd --to "$f"; done

# HTML для движков CSS-вёрстки: печатный рисунок, стиль А5 рядом с файлом (Vivliostyle не читает ресурсы вне корня)
mkdir -p _out/css
cp shablony/a5-paged.css risunki/wbs_print.svg _out/css/
quarto render wbs.qmd --to html --profile pechat
mv _out/wbs-css.html _out/css/index.html
sed -i 's#risunki/wbs_screen.svg#wbs_print.svg#g' _out/css/index.html
NODE_PATH=$NPM node pechat_paged.js _out/css/index.html _out/wbs-pagedjs-a5.pdf
"$NPM/.bin/vivliostyle" build _out/css/index.html -o _out/wbs-vivliostyle-a5.pdf --executable-browser "$CHROME"

# docx -> PDF через LibreOffice: так видно, что получит РИЦ
(cd _out && soffice --headless --convert-to pdf wbs.docx >/dev/null)
for p in _out/*.pdf; do printf '%-32s %s\n' "$(basename "$p")" "$(pdfinfo "$p" | grep -E 'Page size' | sed 's/Page size: *//')"; done
