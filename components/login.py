from lxml import etree

def login(args, session, response, headers):


    # print(response.status_code)
    html_text = response.text
    tree = etree.HTML(html_text)

    # 获取登录token, 后续post登录
    token = tree.xpath('//*[@id="login"]/input[1]/@value')[0]
    token = str(token)
    # print(token)

    # 模拟登录
    post_url = 'https://wallhaven.cc/auth/login'
    data = {
        '_token': token,
        'username': 'FloodWalker',
        'password': 'YuHong19970304'
    }

    response = session.post(url=post_url, data=data, headers=headers)

    return response