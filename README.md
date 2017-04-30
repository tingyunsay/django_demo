# django_demo

## 本项目基于django的版权信息检索页面设计

### 主要功能包括
1.前端提供搜索接口 , 接受用户传递的参数<br>
2.从sphinx建立好的索引文件中 , 查询相关参数的oid , 再拿这些oid从mysql中直接读取 , 在前端显示<br>
3.分页<br>
4.登录验证<br>

### 2017-04-29 根据关键词对词库进行更新

使用者可以在关键词的list中添加指定的关键词,比如我专业查询领域是歌曲,歌手,我把这个两个关键词添加到key_word中<br>
    
    #备选词库,关键词相关,可手动添加<br>
    key_word = ["明星","歌手"]<br>

之后直接在目录下python get_dict.py即可从搜狗官网更新所有相关的词库到原生的词库中<br>

同时,其会生成两个文件夹:
    
    /index_update/sougou/  保存了所有下载到本地的词典,格式为scel
    /usr/local/mmseg3/bak/  保存上一次的词典相关文件:unigram.txt / uni.lib


