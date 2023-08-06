
local httputils = require("fastutils.httputils")
local cookieutils = require("resty.cookie")

local kong = kong
local kongutils = {
    OK = true,
    ERROR = false,
}

function kongutils.set_request_header(headers)
    if headers == nil then
        headers = {}
    end
    for name, value in pairs(headers) do
        kong.service.request.set_header(name, value)
    end
end

function kongutils.get_request_data(name, use_body, get_name, header_name, cookie_name)
    local data = nil;
    local err = nil;

    if use_body == nil then
        use_body = false
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

    local body = nil
    if use_body then
        body = kong.request.get_body()
        if body ~= nil then
            data = body[name]
            if data ~= nil then
                return data
            end
        end
    end

    local queries = kong.request.get_query()
    data = queries[get_name]
    if data ~= nil then
        return data
    end

    local headers = kong.request.get_headers()
    data = headers[header_name]
    if data ~= nil then
        return data
    end

    local cookie_table = nil
    local cookie, err = cookieutils.new()
    if cookie then
        data, err = cookie:get(cookie_name)
        if data ~= nil then
            return data
        end
    end

    return nil
end


return kongutils
