#!/usr/bin/env bash
# Сборка книги (готовые шаги — список GLAVY): рисунки -> проверка -> веб, рукопись docx для РИЦ, PDF А5.
# Нужен стек из ../proba-steka/ustanovka.sh. Результат — _out/glavy/, копия для просмотра — rezultat/.
set -euo pipefail
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-$(git log -1 --format=%ct)}"  # docx без даты сборки

python3 risunki/g3_2_wbs.py            # упадёт, если печатный рисунок шире 114 мм или не тем шрифтом
python3 shablony/make_reference_docx.py 2>/dev/null   # шаблон рукописи генерируется, в git не хранится
python3 proverka.py                     # тон, даты, подписи, ссылки, рубрикация, рисунки

GLAVY="1-3-principy 3-2-wbs"           # готовые шаги; новая глава — сюда и в _quarto.yml
for g in $GLAVY; do
  for f in html docx typst; do quarto render "glavy/$g.qmd" --to "$f" --quiet; done
  python3 posle_docx.py "_out/glavy/$g.docx"   # гиперссылки, подписи, ячейки, маркеры + проверка
  python3 posle_docx.py "_out/glavy/$g.html"
  # рукопись глазами РИЦ: docx -> PDF через LibreOffice
  (cd _out/glavy && soffice --headless --convert-to pdf "$g.docx" >/dev/null)
done

# rezultat/ — в git для просмотра. Копируем, только если изменилось содержимое: PDF и docx при каждой
# сборке получают новые внутренние метки, и без этой проверки git видел бы «изменения» после любой сборки.
docx_sum() {  # текст и рисунки docx; глава без рисунков — только текст
  { unzip -p "$1" word/document.xml; unzip -p "$1" 'word/media/*' 2>/dev/null || true; } | md5sum
}
kopiya() {  # kopiya <откуда> <куда>
  local a b
  case "$1" in
    *.pdf)  a=$(pdftotext "$1" - | md5sum); b=$( [ -f "$2" ] && pdftotext "$2" - | md5sum || true ) ;;
    *.docx) a=$(docx_sum "$1"); b=$( [ -f "$2" ] && docx_sum "$2" || true ) ;;
    *)      a=$(md5sum < "$1"); b=$( [ -f "$2" ] && md5sum < "$2" || true ) ;;
  esac
  if [ "$a" != "$b" ]; then cp "$1" "$2"; echo "обновлён $2"; fi
}
mkdir -p rezultat
for g in $GLAVY; do
  kopiya "_out/glavy/$g-a5.pdf" "rezultat/${g}_pechat-A5.pdf"
  kopiya "_out/glavy/$g.docx" "rezultat/${g}_rukopis-RIC.docx"
  kopiya "_out/glavy/$g.pdf" "rezultat/${g}_rukopis-RIC_LibreOffice.pdf"
  kopiya "_out/glavy/$g.html" "rezultat/${g}_veb.html"
done
for p in rezultat/*.pdf; do printf '%-45s %s стр., %s\n' "$p" "$(pdfinfo "$p" | awk '/Pages/{print $2}')" \
  "$(pdffonts "$p" | tail -n +3 | awk '{print $1}' | sed 's/.*+//' | sort -u | tr '\n' ' ')"; done
