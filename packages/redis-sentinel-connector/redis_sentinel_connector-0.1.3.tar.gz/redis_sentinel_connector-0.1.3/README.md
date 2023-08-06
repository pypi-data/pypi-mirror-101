The idea behind this package is possibility to you use some client or something like the Metabase for collect and analyse logs of your application.  
  
Its need two environments variables:  

* TYPE = 'TEST' or 'DEV'  
    * TEST: You will use fakeredis and not need use Redis instance. **_(Don't need environment REDIS_URL)_**
    * DEV: Use this if You has a local Redis like Docker Redis. **_(Don't need environment REDIS_URL)_**
    
* REDIS_URL = 'complete_redis_sentinel_url'
    * Sample:
        sentinel://:testefoobar@host1.sentinel.domain.com:26379,host2.sentinel.domain.com:26379,host3-155915407905.sentinel.domain.com:26379/service_name:redisservice     

Sample:
~~~python
from redis_sentinel_connector import RedisConnector
redis_connector = RedisConnector().connect()
~~~

Or pass a variable with the complete url to the connect function

Sample:

~~~python
from redis_sentinel_connector import RedisConnector
SENTINEL_URL = "sentinel://:testefoobar@host1.sentinel.domain.com:26379,host2.sentinel.domain.com:26379,host3-155915407905.sentinel.domain.com:26379/service_name:redisservice"
redis_connector = RedisConnector().connect(SENTINEL_URL)
~~~

