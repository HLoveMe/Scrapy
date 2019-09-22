
"""
    安装 brew install redis   //4.0版本 这是服务端
    配置路径
        echo 'export PATH="/usr/local/opt/redis@4.0/bin:$PATH"' >> ~/.bash_profile
        source ~/.bash_profile
    开启服务器
        redis-server即可开启   监听6379
    配置文件
        /usr/local/etc/redis.conf

    连接服务器
        redis-cli 连接本地默认地址
        redis-cli -h 127.0.0.1 -p 6379
        Redis 是基于Key value存储的
        Key：
            del Key
            exists key
            ....

        字符串
            set name value  设置值
            get name        得到值
            getrange  name index_0 index_1   得到子字符串 （0,1）
            append name ""  在原有基础上增加
            。。。
        hash
            hset Key name value
                设置一个hash 表 Key(不存在会创建) 存放name属性 值为value
                hset Key age 12
                hset Key name "SSAS"
            hgetall Key 得到所有键值
            hvals Key  得到所有值
            hlen
            hkeys
            hexits Key field 是否存在field
            hdel Key field

        列表
            lpush Key value  放在第一个
            lpush Key value  放在最后
            blpop/brpop Key t : 删除左侧/右侧的一个值  是阻塞线程直到操作完成  最多T秒
            lpop/rpop Key : 删除左侧/右侧的一个值
            llen Key 长度
            lindex Key Index  去key中的第几个元素
            ...

        Set 不重复的
            sadd Key V  增加值
            scard Key  长度
            sdiff Key1 Key2  两个set相减
            sinter Key1 Key2  两个set相加
            spop Key 随机删除
            srandmember Key count   随机得到count个元素

        可排序集合 sort set
            set 表示不重复
            sort 便是有顺序

            zadd Key source value source1 value
                source 是一个数字 不是所有 可以重复
                value 不能重复
            zrange Key min max  得到sort 中范围索引的所有值
            zcard Key 所有
            zcount key min max 范围内 有多少个
            zrank key value  得到指定值的索引
            zrem key value1,2
            ZREMRANGEBYLEX key min max 移除范围所有
            .....

"""