#!/usr/bin/env bash
# Установка стека методических указаний в облачной среде Claude Code (Ubuntu 24.04, root).
# Контейнер эфемерный: после перезапуска всё, что ниже, нужно ставить заново (или вынести в setup-скрипт среды).
# Проверено 17.10.2026. Время: ≈ 5–8 минут, ≈ 3,5 ГБ на диске (TeX Live ≈ 2,2 ГБ, из них шрифты texlive-fonts-extra — основная часть; /opt/stack ≈ 1 ГБ).
set -euo pipefail
mkdir -p /opt/stack && cd /opt/stack

# Typst (отдельный, свежий) и Quarto — с GitHub Releases (HEAD-запрос прокси отклоняет, GET проходит)
curl -sSL -o typst.tar.xz https://github.com/typst/typst/releases/download/v0.14.2/typst-x86_64-unknown-linux-musl.tar.xz
tar xf typst.tar.xz && ln -sf /opt/stack/typst-x86_64-unknown-linux-musl/typst /usr/local/bin/typst
curl -sSL -o quarto.tar.gz https://github.com/quarto-dev/quarto-cli/releases/download/v1.8.26/quarto-1.8.26-linux-amd64.tar.gz
tar xzf quarto.tar.gz && ln -sf /opt/stack/quarto-1.8.26/bin/quarto /usr/local/bin/quarto

# Graphviz, rsvg, TeX Live (XeLaTeX/LuaLaTeX, кириллица, biblatex-gost, biber) — из apt Ubuntu
apt-get update -qq
apt-get install -y -qq --no-install-recommends graphviz librsvg2-bin cabextract \
  texlive-xetex texlive-luatex texlive-lang-cyrillic texlive-latex-extra texlive-fonts-recommended \
  texlive-fonts-extra texlive-bibtex-extra biber latexmk fonts-paratype

# Times New Roman и Arial (Microsoft core fonts, EULA: ставить можно, класть в репозиторий нельзя).
# Пакет ttf-mscorefonts-installer в этой среде падает на postinst — распаковываем сами.
mkdir -p msfonts /usr/share/fonts/truetype/msttcorefonts && cd msfonts
for f in times32 arial32; do curl -sSL -O "https://downloads.sourceforge.net/corefonts/$f.exe"; cabextract -q -L -F '*.ttf' "$f.exe"; done
cp ./*.ttf /usr/share/fonts/truetype/msttcorefonts/ && fc-cache -f >/dev/null && cd ..

# Python: правка reference.docx, QR-коды, графики
pip install -q python-docx segno matplotlib

# Node: Paged.js (полифил) + Playwright для печати в установленном Chromium, Vivliostyle CLI
mkdir -p npm && cd npm && npm init -y >/dev/null && npm i --silent pagedjs playwright-core @vivliostyle/cli

quarto --version; typst --version; xelatex --version | head -1; dot -V

# Плагин pisatel (/progress и др.) из этого репозитория — для всех проектов пользователя
REPO="$(cd "$(dirname "$0")/../../.." && pwd)"
claude plugin marketplace add "$REPO" && claude plugin install pisatel@opd || echo "плагин pisatel не установлен — см. tools/pisatel/README.md"
