// Текст для печатного профиля А5: Times New Roman, переносы по-русски, абзацный отступ.
#set text(font: "Times New Roman", size: 10.5pt, lang: "ru", hyphenate: true)
#set par(justify: true, first-line-indent: (amount: 1.25em, all: true))
#show heading: set text(size: 11pt, weight: "bold")
#show figure.caption: set text(size: 9pt)
#show table: set par(justify: false, first-line-indent: 0pt)
#set bibliography(title: none) // заголовок «Библиографический список» задаётся в тексте
// Таблицы: 9 пт, влево, плотнее — чтобы пример помещался на правую страницу разворота
#show table: set text(size: 9pt)
#show table.cell: set align(left)
#set table(inset: (x: 2.5pt, y: 2pt))
