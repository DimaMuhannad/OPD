-- Фильтр книги: один исходник .qmd -> веб, рукопись docx для РИЦ, PDF А5 (Typst).
--
-- 1. Рисунки: путь с меткой «@P» получает профиль под формат:
--      risunki/out/g3_2_derevo_@P.svg -> _ekran.svg (веб) | _pechat.svg (docx, Typst) | _pechat.pdf (LaTeX).
-- 2. Врезки ::: {.vrezka} (определение, пример): ч/б рамка в Typst, стиль «Врезка» в docx, класс в вебе.
-- 3. Развороты ::: {.razvorot-levaya} / {.razvorot-pravaya}: в Typst начинаются с чётной (левой) /
--    нечётной (правой) страницы; в docx и вебе ничего не делают.

local function is(fmt) return FORMAT:match(fmt) ~= nil end

function Image(img)
  if img.src:find("@P") then
    local prof
    if is("html") then prof = "ekran.svg"
    elseif is("latex") then prof = "pechat.pdf"
    else prof = "pechat.svg" end
    img.src = img.src:gsub("@P%.svg", prof)
  end
  return img
end

function Div(div)
  if div.classes:includes("vrezka") then
    if is("typst") then
      local out = { pandoc.RawBlock("typst", "#block(stroke: 0.5pt, inset: (x: 2.5mm, y: 2mm), width: 100%, breakable: false)[") }
      for _, b in ipairs(div.content) do table.insert(out, b) end
      table.insert(out, pandoc.RawBlock("typst", "]"))
      return out
    elseif is("docx") then
      div.attributes["custom-style"] = "Врезка"
      return div
    end
  elseif div.classes:includes("razvorot-levaya") or div.classes:includes("razvorot-pravaya") then
    if is("typst") then
      local to = div.classes:includes("razvorot-levaya") and "even" or "odd"
      local out = { pandoc.RawBlock("typst", '#pagebreak(to: "' .. to .. '", weak: true)') }
      for _, b in ipairs(div.content) do table.insert(out, b) end
      return out
    end
    return div.content
  end
end
