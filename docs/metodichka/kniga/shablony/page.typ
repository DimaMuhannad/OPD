// Партиал Quarto (заменяет page.typ шаблона): А5, развороты — внутреннее поле шире наружного.
// Поле набора 148 - 20 - 14 = 114 мм по ширине, 210 - 20 - 25 = 165 мм по высоте (памятка РИЦ).
#set page(
  paper: "a5",
  margin: (inside: 20mm, outside: 14mm, top: 20mm, bottom: 25mm),
  numbering: "1",
  number-align: center,
)
