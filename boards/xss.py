'''
@Author: APTX
@Email: NOIR.APTX4869@gmail.com
@Date: 2019-01-20 14:18:23
@LastEditTime: 2019-02-19 18:00:30
@About: 
'''
from bs4 import BeautifulSoup


def xss(content):
    # 白名单，没有恶意的script 标签
    valid_tag = {
        'p': ['class', 'id'],
        'img': ['src'],
        'div': ['class'],
        'title': ['class'],
        'table':[],
        'thead':[],
        'tr':[],
        'td':[],
    }
    # 初始化一个BS对象，还有另一个方法，soup = BeautifulSoup(comment_content,'html.parser')
    soup = BeautifulSoup(content, 'html.parser')

    tags = soup.find_all()  # 拿到当前所有的节点（也就是所有的标签），是一个HTML对象包着很多的标签对象。find_all()里可以指定参数
    # print(tags)
    for tag in tags:  # 进入到HTML对象里，拿到每一个标签对象
        if tag.name not in valid_tag:  # tag.name 是标签名
            #print(tag.name)
            tag.decompose()  # decompose方法将当前节点移除文档树并完全销毁:----就是干死了
        if tag.attrs:  # 有 属性的标签
        #     # {'class': ['sister'], 'href': 'http://example.com/elsie', 'id': 'link1'}
            for k in list(tag.attrs.keys()):
                if k not in valid_tag[tag.name]:
                    del tag.attrs[k]

    # 可以调用 encode() 方法获得字节码或调用 decode() 方法获得Unicode.
    content_str = soup.decode()
    return content_str
