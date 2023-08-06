package = "lua-fastutils"
version = "0.1.8-1"
source = {
    url = "lua-fastutils-0.1.8-1.zip"
}
description = {
    summary = "Collection of simple utils.",
}
dependencies = {
    "lua >= 5.1, < 5.4",
}
build = {
    type = "builtin",
    modules = {
        ["fastutils.httputils"] = "lua/fastutils/httputils.lua",
        ["fastutils.strutils"] = "lua/fastutils/strutils.lua",
        ["fastutils.tableutils"] = "lua/fastutils/tableutils.lua",
        ["fastutils.typingutils"] = "lua/fastutils/typingutils.lua",
    }
}
