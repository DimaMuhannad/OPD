# Переезд направления «методичка и РПД» на рабочую машину

Проверено 17.10.2026 в облачной среде: чистый клон ветки `claude/metodichka-rpd` с GitHub собирает пилотную главу и проходит все проверки. Текст печатной версии и рукописи совпадает с закоммиченным. Всё, что нужно для работы, лежит в репозитории. Вне репозитория — только установленные программы.

## 1. Что в репозитории

| Что | Где |
| --- | --- |
| Состояние, решения, открытые вопросы | `docs/metodichka/STATE.md` — читать первым |
| Правила содержания (PMBOK 8 и 6, термины, ГОСТ Р 7.0.100–2018) | `docs/metodichka/PRAVILA_KONTENTA.md` |
| Структура книги, дорожная карта, концепция | `STRUKTURA.md`, `ROADMAP.md`, `docs/Metodichka_Koncepciya.md` |
| Книга: главы, рисунки, шаблоны, сборка и проверки | `docs/metodichka/kniga/` (`build.sh`, `proverka.py`, `posle_docx.py`) |
| Черновик РПД и его проверка | `docs/metodichka/rpd/` (`proverka_rpd.py`) |
| Проба стека (архив сравнения движков) | `docs/metodichka/proba-steka/` |
| Навыки Claude Code | `.claude/skills/glava/`, `.claude/skills/rpd/` (и `zanyatie/` сессии занятий) |
| Правила курса | `CLAUDE.md` (ведёт сессия занятий) |
| Зависимости | `docs/metodichka/package.json` (Node), `docs/metodichka/requirements.txt` (Python) |

**В git намеренно нет** (собирается заново): `kniga/_out/`, `kniga/risunki/out/`, `kniga/shablony/reference.docx`, `node_modules/`. Готовые результаты для просмотра лежат в `kniga/rezultat/`. Сборка обновляет их, только если изменилось содержимое, поэтому повторная сборка не создаёт «изменений» в git.

## 2. Клонирование

```bash
git clone <адрес репозитория> OPD && cd OPD
git checkout claude/metodichka-rpd                     # ветка направления
git fetch origin claude/archive-to-repository-heyt7z   # ветка занятий: вливать merge, не rebase
```

Работа идёт в двух ветках: занятия (`claude/archive-to-repository-heyt7z`) и методичка с РПД (`claude/metodichka-rpd`). Ветка направления периодически вливает в себя ветку занятий. Обратного вливания не было: решите, нужна ли общая ветка `main`.

## 3. Программы

Windows: удобнее всего через **WSL (Ubuntu)** — тогда работают `build.sh` и команды из облака без изменений. Без WSL скрипты `.sh` запускаются из Git Bash.

| Программа | Зачем | Windows | macOS | Linux |
| --- | --- | --- | --- | --- |
| Quarto 1.8 (внутри Pandoc и Typst) | сборка книги | установщик с quarto.org | `brew install --cask quarto` | `.deb` с quarto.org |
| Python 3 + `pip install -r docs/metodichka/requirements.txt` | рисунки, шаблон docx, проверки | python.org | `brew install python` | apt |
| Graphviz (`dot`) | рисунки | `winget install graphviz` | `brew install graphviz` | `apt install graphviz` |
| Poppler (`pdftotext`, `pdffonts`, `pdfinfo`) | проверки шрифтов и сравнение PDF | `scoop install poppler` | `brew install poppler` | `apt install poppler-utils` |
| LibreOffice (`soffice`) | показать рукопись docx так, как её откроет РИЦ | установщик | `brew install --cask libreoffice` | apt |
| Node 18+ и `npm install` в `docs/metodichka` | `md_to_docx.js` (docx из .md) | nodejs.org | `brew install node` | apt |
| Шрифты Times New Roman, Arial | печать и экран | есть в системе | есть в системе | `ttf-mscorefonts-installer` или вручную |
| TeX Live (не обязательно) | только запасной путь печати через LaTeX | MiKTeX / TeX Live | MacTeX | apt |

Переменные окружения на своей машине:

| Переменная | Значение | Где нужна |
| --- | --- | --- |
| `NODE_PATH` | `<путь к OPD>/docs/metodichka/node_modules` | `tools/docx-konspekt/md_to_docx.js`, навык `/rpd` |
| `CHROME_PATH` | путь к Chrome или Chromium | только проба Paged.js в `proba-steka/` |

В облачной среде вместо этого работает `proba-steka/ustanovka.sh`; на своей машине он не нужен.

## 4. Плагин pisatel (прогресс и общие команды)

Плагин лежит в репозитории (`tools/pisatel/`, описание — `tools/pisatel/README.md`). Ставится один раз на машину и работает во всех ваших проектах:

```bash
claude plugin marketplace add /путь/к/OPD
claude plugin install pisatel@opd
```

Проверка: в Claude Code команда `/progress` показывает прогресс по `docs/metodichka/progress.toml`. Без Claude Code: `python3 tools/pisatel/scripts/progress.py docs/metodichka/progress.toml`.

## 5. Проверка после переезда

```bash
cd docs/metodichka/kniga && ./build.sh      # в конце: «Ошибок: 0», PDF и docx только на Times New Roman
cd .. && python3 rpd/proverka_rpd.py         # «Ошибок: 0»
git status                                   # пусто: сборка не должна ничего менять
```

Если `git status` после сборки показывает изменения в `rezultat/`, значит, изменилось содержимое. Тогда посмотреть, что именно: другая версия Quarto, Graphviz или шрифтов может дать другие переносы строк.

## 6. Известные ловушки

- **Graphviz и «Times New Roman».** Шрифт задаётся как `Times New Roman,` с запятой (функция `pango()` в `kniga/risunki/profil.py`). Генератор проверяет шрифты печатного PDF и остановит сборку, если подставится другой. На Windows без WSL Graphviz может искать шрифты иначе — проверка это покажет.
- **Версии.** Проверено на Quarto 1.8.26 (Typst 0.13 внутри), Graphviz 2.43, Pandoc 3.6. Исправления дефектов Quarto в `posle_docx.py` рассчитаны на 1.8. Если в новой версии дефекты исчезнут, скрипт просто ничего не исправит.
- **«PDF» РПД — это zip.** Файлы `source-pdfs/03_03_0102_О_ОПД_2025_0_3_1.pdf`, `…ОПДВП_2026…pdf` и `source-pdfs/Уч_пособие_ОПД.pdf` на самом деле zip-архивы со сканами страниц (`N.jpeg`) и текстом (`N.txt`). Открывать распаковкой: `unzip <файл> -d <папка>`. Программа просмотра PDF их не откроет. `Уч_пособие_ОПД.pdf` — пособие СПбПУ 2018 года (С. Г. Редько и др.), не пособие Акопяна.
- **Кириллица в именах файлов** (`source-pdfs/`). На Windows включите `git config core.quotepath false`, чтобы git показывал имена читаемо.
- **Claude Code локально** сам подхватит `CLAUDE.md` и навыки из `.claude/skills/`. Правила сессии («не трогать занятия», «PR не создавать», «вопросы опросником») записаны в `STATE.md` и навыках, а не в настройках облака — они переезжают вместе с репозиторием.
