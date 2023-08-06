
local tableutils = {}

function tableutils.concat(list, sep)
    local typingutils = require("fastutils.typingutils")
    if sep == nil then
        sep = ""
    end
    local list2 = {}
    for i, v in ipairs(list) do
        table.insert(list2, typingutils.tostring(v))
    end
    return table.concat(list2, sep)
end

return tableutils
