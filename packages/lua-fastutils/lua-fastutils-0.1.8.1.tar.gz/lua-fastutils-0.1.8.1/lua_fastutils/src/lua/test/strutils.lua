local strutils = require("fastutils.strutils")
require("luaunit")


TestStrUtils = {}

function TestStrUtils:test01()
    assertEquals(string.capitalize("a"), "A")
    assertEquals(string.capitalize("ab"), "Ab")
    assertEquals(string.capitalize("abc"), "Abc")
    assertEquals(string.capitalize("abc d"), "Abc d")
    assertEquals(string.capitalize("abc de"), "Abc de")
    assertEquals(string.capitalize("abc def"), "Abc def")
end

function TestStrUtils:test02()
    assertEquals(string.camel("a"), "A")
    assertEquals(string.camel("ab"), "Ab")
    assertEquals(string.camel("abc"), "Abc")
    assertEquals(string.camel("abc d"), "AbcD")
    assertEquals(string.camel("abc de"), "AbcDe")
    assertEquals(string.camel("abc def"), "AbcDef")
end

function TestStrUtils:test03()
    assertEquals(true, string.is_in_array("a", {"a"}))
    assertEquals(true, string.is_in_array("a", {"a", "b"}))
    assertEquals(false, string.is_in_array("c", {"a"}))
    assertEquals(false, string.is_in_array("c", {"a", "b"}))
    assertEquals(false, string.is_in_array("b", {"a"}))
    assertEquals(true, string.is_in_array("b", {"a", "b"}))

    assertEquals(false, string.is_in_array("A", {"a"}))
    assertEquals(false, string.is_in_array("A", {"a", "b"}))
    assertEquals(false, string.is_in_array("B", {"a", "b"}))

    assertEquals(true, string.is_in_array("A", {"a"}, true))
    assertEquals(true, string.is_in_array("A", {"a", "b"}, true))
    assertEquals(true, string.is_in_array("B", {"a", "b"}, true))
end

function TestStrUtils:test04()
    assertEquals(true, string.startswith("a", "a"))
    assertEquals(true, string.startswith("ab", "a"))
    assertEquals(true, string.startswith("ab", "ab"))
    assertEquals(true, string.endswith("a", "a"))
    assertEquals(true, string.endswith("ab", "b"))
    assertEquals(true, string.endswith("ab", "ab"))

    assertEquals(false, string.startswith("b", "c"))
    assertEquals(false, string.startswith("ab", "c"))
    assertEquals(false, string.startswith("ab", "cd"))
    assertEquals(false, string.endswith("a", "c"))
    assertEquals(false, string.endswith("ab", "c"))
    assertEquals(false, string.endswith("ab", "cd"))
end

function TestStrUtils:test05()
    assertEquals(true, string.is_match_patterns("hello", {"hello"}))
    assertEquals(true, string.is_match_patterns("hello world", {"hello"}))
    assertEquals(false, string.is_match_patterns("hello world", {"hello"}, true))
    assertEquals(true, string.is_match_patterns("hello world", {"hello.*", "world.*"}, true))
end

function TestStrUtils:test06()
    assertEquals("a", string.trim("a"))
    assertEquals("a b", string.trim(" a b"))
    assertEquals("a b", string.trim("a b "))
    assertEquals("a b", string.trim(" a b "))
    
    assertEquals("a", string.ltrim("a"))
    assertEquals("a b", string.ltrim(" a b"))
    assertEquals("a b ", string.ltrim("a b "))
    assertEquals("a b ", string.ltrim(" a b "))

    assertEquals("a", string.rtrim("a"))
    assertEquals(" a b", string.rtrim(" a b"))
    assertEquals("a b", string.rtrim("a b "))
    assertEquals(" a b", string.rtrim(" a b "))
end


function TestStrUtils:test07()
    local k, v = string.split2("a=b")
    assertEquals(k, "a")
    assertEquals(v, "b")

    local k, v = string.split2("a = b")
    assertEquals(k, "a ")
    assertEquals(v, " b")

    local k, v = string.split2("abc = abc")
    assertEquals(k, "abc ")
    assertEquals(v, " abc")

    local k, v = string.split2("abc = abc=abc")
    assertEquals(k, "abc ")
    assertEquals(v, " abc=abc")

    local k, v = string.split2("abc = abc=abc", ":")
    assertEquals(k, nil)
    assertEquals(v, "abc = abc=abc")

    local k, v = string.split2("a:=b", ":=")
    assertEquals(k, "a")
    assertEquals(v, "b")
end

function TestStrUtils:test08()
    local words = string.split("a,b,c", ",")
    assertEquals(words[1], "a")
    assertEquals(words[2], "b")
    assertEquals(words[3], "c")

    local words = string.split("a,b,", ",")
    assertEquals(words[1], "a")
    assertEquals(words[2], "b")
    assertEquals(words[3], "")

    local words = string.split(",a,b,", ",")
    assertEquals(words[1], "")
    assertEquals(words[2], "a")
    assertEquals(words[3], "b")
    assertEquals(words[4], "")

    local words = string.split("a", ",")
    assertEquals(words[1], "a")
    assertEquals(table.getn(words), 1)

    local words = string.split("a,b,c", ",", 2)
    assertEquals(words[1], "a")
    assertEquals(words[2], "b,c")
    assertEquals(table.getn(words), 2)

    local words = string.split("a", ",", 2)
    assertEquals(words[1], "a")
    assertEquals(table.getn(words), 1)

    local words = string.split("a,b", ",", 2)
    assertEquals(words[1], "a")
    assertEquals(words[2], "b")
    assertEquals(table.getn(words), 2)

    local words = string.split("a,b,", ",", 2)
    assertEquals(words[1], "a")
    assertEquals(words[2], "b,")
    assertEquals(table.getn(words), 2)
end

function TestStrUtils:test09()
    local words = string.remove_empty_string_from_table({" ", "a",  nil, "", "b", " "})
    assertEquals(words[1], "a")
    assertEquals(words[2], "b")
    assertEquals(table.getn(words), 2)
end

function TestStrUtils:test10()
    local words = string.trim_strings({"   ", " a ", "   b ", "    "})
    assertEquals(words[1], "")
    assertEquals(words[2], "a")
    assertEquals(words[3], "b")
    assertEquals(words[4], "")
    assertEquals(table.getn(words), 4)
end


function TestStrUtils:test13()
    assertEquals(string.is_empty(nil), true)
    assertEquals(string.is_empty(""), true)
    assertEquals(string.is_empty("   "), true)
    assertEquals(string.is_empty("a"), false)
end



LuaUnit:run()

