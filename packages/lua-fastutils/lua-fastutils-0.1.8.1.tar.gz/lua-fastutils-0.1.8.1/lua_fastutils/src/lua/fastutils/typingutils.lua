local typingutils = {}


function typingutils.is_string(value)
    local type_name = type(value)
    if type_name == "string" then
        return true
    else
        return false
    end
end

function typingutils.is_number(value)
    local type_name = type(value)
    if type_name == "number" then
        return true
    else
        return false
    end
end

function typingutils.is_boolean(value)
    local type_name = type(value)
    if type_name == "boolean" then
        return true
    else
        return false
    end
end

function typingutils.is_nil(value)
    local type_name = type(value)
    if type_name == "nil" then
        return true
    else
        return false
    end
end

function typingutils.is_function(value)
    local type_name = type(value)
    if type_name == "function" then
        return true
    else
        return false
    end
end

function typingutils.is_table(value)
    local type_name = type(value)
    if type_name == "table" then
        return true
    else
        return false
    end
end

function typingutils.is_list(value)
    local type_name = type(value)
    if type_name ~= "table" then
        return false
    end
    for k, v in pairs(value) do
        if type(k) ~= "number" then
            return false
        end
    end
    return true
end

function typingutils.is_map(value)
    local type_name = type(value)
    if type_name ~= "table" then
        return false
    end
    for k, v in pairs(value) do
        if type(k) == "number" then
            return false
        end
    end
    return true
end

function typingutils.tostring(value)
    local type_value = type(value)
    if type_value == "string" then
        return value
    elseif type_value == "table" then
        if typingutils.is_map(value) then
            local result = "{"
            local kvs = {}
            for k, v in pairs(value) do
                local kvstring = typingutils.tostring(k) .. "=" .. typingutils.tostring(v)
                table.insert(kvs, kvstring)
            end
            result = result .. table.concat(kvs, ", ")
            result = result .. "}"
            return result
        else
            local result = "["
            local vs = {}
            for i, v in pairs(value) do
                table.insert(vs, typingutils.tostring(v))
            end
            result = result .. table.concat(vs, ", ")
            result = result .. "]"
            return result
        end
    else
        return tostring(value)
    end
end


return typingutils
