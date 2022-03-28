import os
from lxml import etree
# from components.headers import get_headers


def get_picture_list(args, page_number, session, headers):
    search_url = 'https://wallhaven.cc/search?'

    if args.sorting == 'favorites':
        params = {
            'categories': str(int(args.General)) + str(int(args.Anime)) + str(int(args.People)),
            'purity': str(int(args.SFW)) + str(int(args.Sketchy)) + str(int(args.NSFW)),
            'sorting': args.sorting,
            'order': args.order,
            'page': str(page_number)
        }

    elif args.sorting == 'toplist':
        params = {
            'categories': str(int(args.General)) + str(int(args.Anime)) + str(int(args.People)),
            'purity': str(int(args.SFW)) + str(int(args.Sketchy)) + str(int(args.NSFW)),
            'topRange': '1M',  # 最近时间，1d-一天、3d-三天、1W-一周、1M-一个月、1y-一年
            'sorting': args.sorting,
            'order': args.order,
            'page': str(page_number)
        }

    else:
        raise EOFError('Sorting choice error!')

    page_response = session.get(url=search_url, params=params, headers=headers)
    page_response_text = page_response.text
    page_response_text_tree = etree.HTML(page_response_text)
    picture_list = page_response_text_tree.xpath('//*[@id="thumbs"]/section/ul/li')

    return picture_list


def get_picture_url(args, picture_list, picture_index):
    li = picture_list[picture_index]
    picture_url = li.xpath('figure/a[2]/@href')[0]

    return picture_url


def get_picture_info(args, picture_url, session, headers, proxies):

    picture_response = session.get(url=picture_url, headers=headers, proxies=proxies)
    picture_response_text = picture_response.text
    picture_response_text_tree = etree.HTML(picture_response_text)
    catagory = picture_response_text_tree.xpath('//*[@id="showcase-sidebar"]/div/div[1]/div[3]/dl/dd[2]')
    purity = picture_response_text_tree.xpath('//*[@id="showcase-sidebar"]/div/div[1]/div[3]/dl/dd[3]/span')
    favorites = picture_response_text_tree.xpath('//*[@id="showcase-sidebar"]/div/div[1]/div[3]/dl/dd[6]/a')
    picture_srcs = picture_response_text_tree.xpath('//*[@id="wallpaper"]/@src')

    return catagory, purity, favorites, picture_srcs


def download_picture(args, picture_src, catagory, purity, session, headers, proxies):
    name = str(picture_src)[-10:].split('.')[0]
    extension = str(picture_src)[-10:].split('.')[1]
    file_name = name + '-' + catagory + '-' + purity + '.' + extension

    save_path_favorites = os.path.join(args.save_path, purity, catagory)
    save_path_toplist = os.path.join(args.save_path, 'toplist')
    if args.sorting == 'favorites':
        save_path = save_path_favorites
    elif args.sorting == 'toplist':
        save_path = save_path_toplist
    else:
        raise EOFError('Sorting choice error!')
    save_name = os.path.join(save_path, file_name)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_list_favorites = os.listdir(save_path_favorites)
    file_list_toplist = os.listdir(save_path_toplist)

    if (file_name in file_list_favorites) or (file_name in file_list_toplist):
        print('File {} exists, skip this download!'.format(file_name))
    else:
        picture_data = session.get(url=picture_src, headers=headers, proxies=proxies).content
        # picture_data = session.get(url=picture_src, headers=headers).content
        with open(save_name, 'wb') as fp:
            fp.write(picture_data)
        print('Successfully save {}!'.format(save_name))


def download(args, session, response, headers, proxies):

    file_list_toplist = os.listdir(os.path.join(args.save_path, 'toplist'))
    # if args.sorting == 'toplist':
    #     args.start_page = len(file_list_toplist) // 24 + 1

    for page_number in range(args.start_page, args.end_page + 1):

        picture_list = get_picture_list(args=args, page_number=page_number, session=session, headers=headers)

        picture_index = 0
        while picture_index < len(picture_list):

            picture_url = get_picture_url(args, picture_list, picture_index)

            print('picture_url:', picture_url)

            catagory, purity, favorites, picture_srcs = get_picture_info(args, picture_url=picture_url, session=session, headers=headers, proxies=proxies)
            if len(catagory) == 0:
                print('Falied index {}, retry{}'.format(picture_index, picture_url))
                continue
            catagory = str(catagory[0].text)
            purity = str(purity[0].text)
            favorites = str(favorites[0].text).replace(',', '')
            picture_src = picture_srcs[0]

            if args.sorting == 'favorites' and int(favorites) < 200:
                print('favorites too small!!!')
                import sys
                sys.exit()

            download_picture(args=args, picture_src=picture_src, catagory=catagory, purity=purity, session=session, headers=headers, proxies=proxies)

            picture_index += 1
