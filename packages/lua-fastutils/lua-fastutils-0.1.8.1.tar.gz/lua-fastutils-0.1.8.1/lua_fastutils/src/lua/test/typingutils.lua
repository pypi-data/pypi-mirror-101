local typingutils = require("fastutils.typingutils")
require("luaunit")

TestTypingUtils = {}

function test01()
    return true
end

function TestTypingUtils:test01()
    assertEquals(typingutils.is_string("a"), true)
    assertEquals(typingutils.is_number(1), true)
    assertEquals(typingutils.is_boolean(true), true)
    assertEquals(typingutils.is_nil(nil), true)
    assertEquals(typingutils.is_table({1,2,3}), true)
    assertEquals(typingutils.is_table({a=1, b=2}), true)
    assertEquals(typingutils.is_function(test01), true)
end

function TestTypingUtils:test02()
    assertEquals(typingutils.is_string(1), false)
    assertEquals(typingutils.is_number(true), false)
    assertEquals(typingutils.is_boolean(nil), false)
    assertEquals(typingutils.is_nil(false), false)
    assertEquals(typingutils.is_table("hello"), false)
    assertEquals(typingutils.is_function({a=1, b=2}), false)
end

function TestTypingUtils:test03()
    assertEquals(typingutils.is_list({1,2,3}), true)
    assertEquals(typingutils.is_map({a=1, b=2}), true)

    assertEquals(typingutils.is_list(true), false)
    assertEquals(typingutils.is_map("hello"), false)
end

function TestTypingUtils:test04()
    assertEquals(typingutils.tostring({1,2,3}), "[1, 2, 3]")
    assertEquals(typingutils.tostring({a=1, b=2}), "{a=1, b=2}")
    assertEquals(typingutils.tostring(true), "true")
    assertEquals(typingutils.tostring(false), "false")
    assertEquals(typingutils.tostring(nil), "nil")
    assertEquals(typingutils.tostring(0), "0")
    assertEquals(typingutils.tostring(1), "1")
    assertEquals(typingutils.tostring(1.2), "1.2")
    assertEquals(typingutils.tostring(0.3), "0.3")
    assertEquals(typingutils.tostring("hello"), "hello")
    assertEquals(typingutils.tostring({a={1,2,3}, b=1}), "{a=[1, 2, 3], b=1}")
end


LuaUnit:run()
