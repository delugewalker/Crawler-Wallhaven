import time
import argparse

local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def wallhaven_argparse():
    parser = argparse.ArgumentParser()

    # Basic Information
    parser.add_argument('--user', default='yuhong', type=str)
    parser.add_argument('--date', default=local_time.split(' ')[0], type=str)
    parser.add_argument('--time', default=local_time.split(' ')[1].replace(':', '-'), type=str)
    parser.add_argument('--description', default='Download pictures from wallhaven.cc!', type=str)

    # Folders Information
    parser.add_argument('--save_path', default='E:\Pictures\PictureSites\Wallhaven\Pictures', type=str)
    parser.add_argument('--login_url_get', default='https://wallhaven.cc/login', type=str)
    parser.add_argument('--login_url_post', default='https://wallhaven.cc/auth/login', type=str)

    # Network Information
    parser.add_argument('--use_proxy', default=True, type=bool)
    parser.add_argument('--proxy', default='127.0.0.1:2021', type=str)
    parser.add_argument('--proxy_http', default=True, type=bool)
    parser.add_argument('--proxy_https', default=False, type=bool)

    parser.add_argument('--start_page', default=1, type=int)
    parser.add_argument('--end_page', default=20, type=int)

    # Download Information
    parser.add_argument('--General', default=True, type=bool)
    parser.add_argument('--Anime', default=True, type=bool)
    parser.add_argument('--People', default=True, type=bool)

    parser.add_argument('--SFW', default=True, type=bool)
    parser.add_argument('--Sketchy', default=True, type=bool)
    parser.add_argument('--NSFW', default=True, type=bool)

    parser.add_argument('--sorting', default='toplist', choices=['favorites', 'toplist'], type=str)
    parser.add_argument('--order', default='desc', type=str)
    parser.add_argument('--topRange', default='1M', type=str, help='最近时间，1d-一天、3d-三天、1W-一周、1M-一个月、1y-一年')

    return parser
