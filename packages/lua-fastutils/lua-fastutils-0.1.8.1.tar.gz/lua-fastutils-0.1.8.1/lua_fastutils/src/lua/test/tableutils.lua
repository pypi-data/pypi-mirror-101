local tableutils = require("fastutils.tableutils")
require("luaunit")

TestTableUtils = {}


function TestTableUtils:test01()
    local table = {
        a=1,
        b=2,
    }
    assertEquals(table["a"], 1)
    assertEquals(table["b"], 2)
    assertEquals(table["c"], nil)
end

function TestTableUtils:test02()
    assertEquals(tableutils.concat({1, true, nil}), "1true")
    assertEquals(tableutils.concat({1, true, nil}, ","), "1,true")
end


LuaUnit:run()
