local httputils = require("fastutils.httputils")

require("luaunit")

TestHttpUtils = {}


function TestHttpUtils:test01()
    assertEquals(httputils.get_request_data("token"), nil)
    assertEquals(httputils.get_request_data("token", {}), nil)
    assertEquals(httputils.get_request_data("token", {}, {}), nil)
    assertEquals(httputils.get_request_data("token", {}, {}, {}), nil)
end

function TestHttpUtils:test02()
    assertEquals(httputils.get_request_data("token", {token="hi"}), "hi")
    assertEquals(httputils.get_request_data("token", {}, {token="hi"}), "hi")
    assertEquals(httputils.get_request_data("token", {}, {}, {token="hi"}), "hi")
end

function TestHttpUtils:test03()
    local header_lines = {"a:b", "c:d"}
    local headders = httputils.header_lines_to_headers_mapping(header_lines)
    assertEquals(headders["a"], "b")
    assertEquals(headders["c"], "d")

end


function TestHttpUtils:test04()
    local header_lines = {
        "reqid: 1234",
        "reqts: 2345",
        "reqcode: 3456",
    }
    local headers = httputils.header_lines_to_headers_mapping(header_lines)
    assertEquals(headers["reqid"], "1234")
    assertEquals(headers["reqts"], "2345")
    assertEquals(headers["reqcode"], "3456")
end

function TestHttpUtils:test05()
    assertEquals(httputils.url_path_match("http://abc.com/api/ping?ts=1234", "/api/ping"), true)
    assertEquals(httputils.url_path_match("://abc.com/api/ping?ts=1234", "/api/ping"), true)
    assertEquals(httputils.url_path_match("/api/ping?ts=1234", "/api/ping"), true)
    assertEquals(httputils.url_path_match("/api/ping", "/api/ping"), true)

    assertEquals(httputils.url_path_match("http://abc.com/api/echo?ts=1234", "/api/ping"), false)
    assertEquals(httputils.url_path_match("://abc.com/api/echo?ts=1234", "/api/ping"), false)
    assertEquals(httputils.url_path_match("/api/echo?ts=1234", "/api/ping"), false)
    assertEquals(httputils.url_path_match("/api/echo", "/api/ping"), false)
end

LuaUnit:run()
