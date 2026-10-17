// Текст для печатного профиля А5: Times New Roman, переносы по-русски, абзацный отступ.
#set text(font: "Times New Roman", size: 10.5pt, lang: "ru", hyphenate: true)
#set par(justify: true, first-line-indent: (amount: 1.25em, all: true))
#show heading: set text(size: 11pt, weight: "bold")
#show figure.caption: set text(size: 9pt)
#show table: set par(justify: false, first-line-indent: 0pt)
