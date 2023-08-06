
local _M = string

function string.capitalize(self)
    return self:sub(1,1):upper()..self:sub(2):lower()
end

function _M.camel(self)
    local words = {}
    for word in string.gmatch(self, "%S+") do
        table.insert(words, string.capitalize(word))
    end
    return table.concat(words, "")
end

function _M.is_in_array(self, array_string, ignore_case)
    local value = self
    if ignore_case == nil then
        ignore_case = false
    end
    if ignore_case then
        value = string.lower(value)
    end
    for _, value2 in pairs(array_string) do
        if ignore_case then
            value2 = string.lower(value2)
        end
        if value2 == value then
            return true
        end
    end
    return false
end

function _M.startswith(self, starts)
    if string.len(self) < string.len(starts) then
        return false
    end
    if string.sub(self, 1, string.len(starts)) == starts then
        return true
    else
        return false
    end
end

function _M.endswith(self, ends)
    if string.len(self) < string.len(ends) then
        return false
    end
    if string.sub(self, string.len(self)-string.len(ends) + 1) == ends then
        return true
    else
        return false
    end
end

function _M.is_match_patterns(self, array_patterns, match_whole_word)
    if match_whole_word == nil then
        match_whole_word = false
    end
    for _, pattern in pairs(array_patterns) do
        if match_whole_word then
            if not string.startswith(pattern, "^") then
                pattern = "^" .. pattern
            end
            if not string.endswith(pattern, "$") then
                pattern = pattern .. "$"
            end
        end
        local matched = string.match(self, pattern)
        if matched ~= nil then
            return true
        end
    end
    return false
end

function _M.trim(self)
    local value, _ = string.gsub(self, "^%s*(.-)%s*$", "%1")
    return value
end

function _M.ltrim(self)
    local value, _ = string.gsub(self, "^%s*(.-)$", "%1")
    return value
end

function _M.rtrim(self)
    local value, _ = string.gsub(self, "^(.-)%s*$", "%1")
    return value
end

function _M.trim_strings(table_strings)
    local new_table_strings = {}
    for _, value in pairs(table_strings) do
        value = _M.trim(value)
        table.insert(new_table_strings, value)
    end
    return new_table_strings
end

function _M.remove_empty_string_from_table(table_strings)
    local new_table_strings = {}
    for _, value in pairs(table_strings) do
        if not _M.is_empty(value) then
            table.insert(new_table_strings, value)
        end
    end
    return new_table_strings
end

function _M.split2(self, separator)
    if separator == nil then
        separator = "="
    end
    local pstart, pend = self:find(separator)
    if pstart ~= nil then
        local k = string.sub(self, 0, pstart-1)
        local v = string.sub(self, pend+1)
        return k, v
    else
        return nil, self
    end
end

function _M.split(self, separator, n)
    local words = {}
    local left = self
    local word = nil
    local counter = 1
    repeat
        word, left = _M.split2(left, separator)
        if word ~= nil then
            table.insert(words, word)
        else
            table.insert(words, left)
            break
        end
        counter = counter + 1
        if counter == n then
            if word ~= nil and left ~= "" then
                table.insert(words, left)
            end
            break
        end
    until word == nil
    return words
end



function _M.is_empty(self)
    return self == nil or _M.trim(self) == ""
end


return _M
