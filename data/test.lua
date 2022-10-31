abspath = os.getenv("PWD")
package.path = abspath .. "/?.lua;"

local xdb = require("xdb_searcher")

-- 1、从 db_path 创建基于文件的 xdb 查询对象
local db_path = abspath .. "/ip2region.xdb"
local searcher, err = xdb.new_with_file_only(db_path)
if err ~= nil then
    print(string.format("failed to create searcher: %s", err))
    return
end

-- 2、调用查询 API 进行查询
local ip_str = "223.88.69.87"
local s_time = xdb.now()
region, err = searcher:search(ip_str)
if err ~= nil then
    print(string.format("failed to search(%s): %s", ip_str, err))
    return
end

-- 备注：并发使用，每个协程需要创建单独的 xdb 查询对象
print(string.format("{region: %s, took: %.5f μs}", region, xdb.now() - s_time))