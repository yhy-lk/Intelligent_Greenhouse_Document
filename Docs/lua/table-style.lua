-- table-style.lua
-- 遍历文档中的所有表格
function Table(tbl)
  return pandoc.walk_block(tbl, {
    -- 找到表格里的普通文本 (Plain)
    Plain = function(el)
      return pandoc.Div(el.content, {['custom-style'] = 'Table Paragraph'})
    end,
    -- 找到表格里的段落 (Para)
    Para = function(el)
      return pandoc.Div(el.content, {['custom-style'] = 'Table Paragraph'})
    end
  })
end
