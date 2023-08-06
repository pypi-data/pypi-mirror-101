local httputils = {}


function httputils.get_request_data(name, body, queries, headers, cookies, get_name, header_name, cookie_name)
    local value = nil

    if body == nil then
        body = {}
    end
    if headers == nil then
        headers = {}
    end
    if queries == nil then
        queries = {}
    end
    if cookies == nil then
        cookies = {}
    end
    if get_name == nil then
        get_name = name
    end
    if header_name == nil then
        header_name = name
    end
    if cookie_name == nil then
        cookie_name = name
    end

    value = body[name]
    if value ~= nil then
        return value
    end

    value = queries[get_name]
    if value ~= nil then
        return value
    end

    value = headers[header_name]
    if value ~= nil then
        return value
    end

    value = cookies[cookie_name]
    if value ~= nil then
        return value
    end

    return nil
end


function httputils.header_lines_to_headers_mapping(header_lines)
    local strutils = require("fastutils.strutils")
    local headers = {}
    for _, header_line in pairs(header_lines) do
        local k, v = strutils.split2(header_line, ":")
        if k ~= nil and v ~= nil then
            k = strutils.trim(k)
            v = strutils.trim(v)
            headers[k] = v
        end
    end
    return headers
end

function httputils.url_path_match(url, path)
    local strutils = require("fastutils.strutils")
    local schema, left = strutils.split2(url, "://")
    local host, left = strutils.split2(left, "/")
    local url_path, params = strutils.split2(left, "?")
    if url_path == nil then
        url_path = params
    end
    local url_path = "/" .. url_path
    if url_path == path then
        return true
    else
        return false
    end
end

return httputils
