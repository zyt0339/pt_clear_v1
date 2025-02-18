#!/usr/bin/env python
# 本脚本支持 配置两个qb (qb1下载 qb2刷流)和一个 tr(保种), 不需的下载器配置瞎写即可(会自己登录失败)
# (MP内已自带)同时安装 pip工具、qb依赖库、tr依赖库:curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py && python -m pip install qbittorrent-api && pip install transmission-rpc -U
# 脚本依赖种子标签中有站点名称,且和MP种站点管理名字相同,(你可以先执行一遍 mp插件<下载任务分类与标签>(勾选 自动站点标签 补全下载历史的标签与分类(一次性任务)) 也可以将下面get_tracker_sites()中的tracker 映射补全我来给你添加站点标签)
QB1 = 'qb1'
QB2 = 'qb2'
TR = 'tr'
TAG_IN_EMBY = 'F-入库'
TAG_NOT_IN_EMBY = 'F-未入库'  # EXCLUDE_CONTAINS_STATIONS、LIMIT_TO_LONG_KEEP_THRESHOLD、condition_to_long_keep三种条件不会添加此标签
TAG_LONG_KEEP = 'F-长期'
# -------以下为配置开关-----
# -------以下为配置开关-----
# -------以下为配置开关-----
# 是否真执行qb标签等, False时只模拟打印日志不真正给 qb 加标签
SWITCH_REAL_INVOKE = True
# 是否增加F-已入库\F-未入库标签\F-长期,填写使用此功能的下载器
SWITCH_EMBY_CLIENT = [QB1, TR]
# 这些文件路径中的种子会增加 F-长期标签，并取消所有种子辅种个数、未入库标记,应对某个站正在考核\长期保种场景，根据自己情况修改
TAG_LONG_KEEP_PATH_List = ["video/down/憨憨", "DouBan.2021.11.11.Top.250.BluRay"]
# 辅种个数标记开关
SWITCH_TORRENT_COUNT_CLIENT = [QB1, TR]
# 只要辅种站点中含有这些标签, 就取消所有种子辅种个数、未入库标记,应对某个站正在考核\长期保种场景
EXCLUDE_CONTAINS_STATIONS = {"保种区", "海豹", TAG_LONG_KEEP, "KEEP"}
LIMIT_TO_DELETE_THRESHOLD = 30  # <= x 的会标记, (<=1 就是单站辅种)， EXCLUDE_CONTAINS_STATIONS、LIMIT_TO_LONG_KEEP_THRESHOLD、condition_to_long_keep三种条件不会添加此标签
LIMIT_TO_LONG_KEEP_THRESHOLD = 30  # >= x 的会添加 F-长期 标签，且取消所有种子辅种个数、未入库标记,应对某个站正在考核\长期保种场景
PRINT_COPY_COUNT = 1000  # 只会打印输出辅种数高于此值的种, >= 1000时不再打印
# 是否增加F-ISO\F-TS\F-m2TS文件类型标记
SWITCH_FILE_SUFFIX_CLIENT = [QB1, TR]
# 是否增加tracker 异常状态标记,无辅种的可以连源文件一起删除
SWITCH_TRACKER_CLIENT = [QB1, QB2, TR]
# 是否对某站种子上传限速,设置到种子粒度
SWITCH_LIMIT_CLIENT = [QB1, TR]
_10K = 10240
_100K = 102400
_1M = 1024 * 1024
_2M = _1M * 2
QB1_UOLOAD_LIMIT_SITE = {'CARPT': _10K, '柠檬': _100K, '大青虫': _1M}
QB2_UOLOAD_LIMIT_SITE = {}
TR_UOLOAD_LIMIT_SITE = QB1_UOLOAD_LIMIT_SITE
# 是否打印下载目录下没有做种的文件列表
SWITCH_PRINT_NOT_UPLOAD_FILE = True
# 下载器根目录。格式：[脚本执行环境视角路径,真实路径,下载器视角路径]，多个盘写多个，结尾不包含/(注意：如果你映射了/media和/media2这种后者完全包含前者的名字，后者/media2写前面行)
DOWNLOAD_DIRS = [
    ['/volume2/video/down', '/volume2/video/down', '/volume2/video/down'],
    ['/volume5/video5/down', '/volume5/video5/down', '/volume5/video5/down']
]
# 是否打印emby 等媒体库下没做种的视频文件
SWITCH_PRING_NOT_TORRENT = True
# 这些路径忽略打印没做种的视频文件
EMBY_IGNORE_PATH_List = ["link/电视剧/国漫/斑马百科", "link/电影AV", "link/audiobooks"]
# 是否打印媒体库下重复的不同清晰度视频文件
SWITCH_PRING_MULTY_VIDEO_FILE = True
# 脚本执行环境视角的emby媒体库根目录。格式：脚本执行环境视角路径:真实路径，多个盘写多个，结尾不包含/(注意：如果你映射了/media和/media2这种后者完全包含前者的名字，后者/media2写前面行)
EMBY_PARENT_DIRS = {
    '/volume2/video/link': '/volume2/video/link',
    '/volume4/video4/link': '/volume4/video4/link'
}
# 是否标记源文件同时在qb\tr做种的种子,会添加标签 F-辅种tr\F-辅种qb
SWITCH_MARK_IN_TR_OR_QB12 = True
# 是否增加 F-volume2 等根路径标签
SWITCH_TAG_ROOT_PATH_CLIENT = []
# 是否打印 debug 详细信息
DEBUG_LOG = not SWITCH_REAL_INVOKE

SERVER_HOST = "192.168.1.111"
USER_NAME = "name"
PASS_WORD = "password"
QB1_CONN_INFO = dict(
    host=SERVER_HOST,
    port=8085,
    username=USER_NAME,
    password=PASS_WORD,
)
QB2_CONN_INFO = dict(
    host=SERVER_HOST,
    port=8086,
    username=USER_NAME,
    password=PASS_WORD,
)
TR_CONN_INFO = dict(
    protocol='http',
    host=SERVER_HOST,
    port=9091,
    username=USER_NAME,
    password=PASS_WORD,
)
# 搜索get_tracker_sites(),可以添加你已有站点的tracker映射,我怕ban我所以我删了
# -------以上为配置开关------
# -------以上为配置开关------
# -------以上为配置开关------

TAG_COPY_COUNT = 'F-辅种%d'

TAG_ISO = 'F-ISO'  # .iso原盘文件标记
TAG_TS = 'F-TS'  # .ts 文件标记
TAG_M2TS = 'F-m2TS'  # .m2ts 文件标记

TAG_TORRENT_ERROR1 = 'F-Error-有辅种'
TAG_TORRENT_ERROR2 = 'F-Error-无辅种'

TAG_NO_WORKING_TRACKER1 = 'F-tracker未工作-有辅种'
TAG_NO_WORKING_TRACKER2 = 'F-tracker未工作-无辅种'
# TAG_TRACKERS_ONLY_Bad_Gateway1 = 'F-Bad_Gateway-有辅种'
# TAG_TRACKERS_ONLY_Bad_Gateway2 = 'F-Bad_Gateway-无辅种'
# Your client is not on the whitelist
TAG_TRACKERS_CLIENT_NOT_WHITE1 = 'F-clientNotWhite-有辅种'
TAG_TRACKERS_CLIENT_NOT_WHITE2 = 'F-clientNotWhite-无辅种'

TAG_EMPTY_TORRENT = 'F-文件不全'
TAG_IN_TR = f'F-辅种{TR}'
TAG_IN_QB1 = f'F-辅种{QB1}'
TAG_IN_QB2 = f'F-辅种{QB2}'

# todo 画质,未完成
SWITCH_TAG_DOLBY = False  # .dolby 文件标记开关
TAG_DOLBY = 'F-dolby'  # .dolby 文件标记

import datetime
import os
import os.path
import socket
import time
from urllib.parse import urlparse

import qbittorrentapi
from qbittorrentapi import TrackerStatus
# tr
from transmission_rpc.client import Client


def condition_to_long_keep(content_path):
    return any(element in content_path for element in TAG_LONG_KEEP_PATH_List)


# 获取本机本机内网 ip
def get_current_device_local_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return str(e)


def readable_file_size(file_size, has_frac=True):
    if has_frac:
        if file_size < 1024:
            return f"{file_size}B"
        elif file_size < 1024 * 1024:
            return f"{file_size / 1024:.2f}KB"
        elif file_size < 1024 * 1024 * 1024:
            return f"{file_size / (1024 * 1024):.2f}MB"
        elif file_size < 1024 * 1024 * 1024 * 1024:
            return f"{file_size / (1024 * 1024 * 1024):.2f}GB"
        else:
            return f"{file_size / (1024 * 1024 * 1024 * 1024):.2f}TB"
    else:
        if file_size < 1024:
            return f"{file_size}B"
        elif file_size < 1024 * 1024:
            return f"{file_size / 1024:.0f}KB"
        elif file_size < 1024 * 1024 * 1024:
            return f"{file_size / (1024 * 1024):.0f}MB"
        elif file_size < 1024 * 1024 * 1024 * 1024:
            return f"{file_size / (1024 * 1024 * 1024):.0f}GB"
        else:
            return f"{file_size / (1024 * 1024 * 1024 * 1024):.0f}TB"


def prefix():
    if SWITCH_REAL_INVOKE:
        return ''
    else:
        return '(模拟)'


# hashs = {'qb': {'tag1': set(hashs), 'tag2': set(hashs)}, 'tr': {同左侧}}
hashs_to_add_tag = {QB1: {}, QB2: {}, TR: {}}
# {hash,tags} 后续然后将 tags 排序后转成{tags,set = hashs}
tr_hash_tags = {}
tr_hash_tags_old = {}  # 只有有变化的再去更新 hash:[tags]
# hashs = {'qb': {'y-0': set(), 'y-1024': set()}, 'tr': {同左侧}, tr 单位是 k 所以这里 tr 是/1024 的
hashs_to_limit_upload = {QB1: {}, QB2: {}, TR: {}}


def qb_add_tag_to_hash_and_print(qb_or_tr, site_tag, torrent, tag_name):
    add_tag_to_hash_and_print_internal(qb_or_tr, torrent.hash,
                                       torrent.name, site_tag, tag_name)


def tr_add_tag_to_hash_and_print(qb_or_tr, site_tag, torrent, tag_name):
    # tr 加额外处理
    if torrent.hashString not in tr_hash_tags:
        tr_hash_tags[torrent.hashString] = set()
    tr_hash_tags[torrent.hashString].add(tag_name)
    add_tag_to_hash_and_print_internal(qb_or_tr, torrent.hashString,
                                       torrent.name, site_tag, tag_name)


def add_tag_to_hash_and_print_internal(qb_or_tr, hash, name, site_tag, tag_name):
    hashs_qb_or_tr = hashs_to_add_tag[qb_or_tr]
    if tag_name not in hashs_qb_or_tr:
        hashs_qb_or_tr[tag_name] = set()
    hashs_qb_or_tr[tag_name].add(hash)
    if DEBUG_LOG:
        print(f"{qb_or_tr}:增加标签 [{tag_name}], {name} [{site_tag}]")


def qb_add_limit_upload_to_hash_and_print(site, qb_or_tr, torrent, limit_speed: int):
    add_limit_upload_to_hash_and_print_internal(site, qb_or_tr, torrent.hash,
                                                torrent.name, torrent.tags, limit_speed)


def tr_add_limit_upload_to_hash_and_print(site, qb_or_tr, torrent, limit_speed: int):
    add_limit_upload_to_hash_and_print_internal(site, qb_or_tr, torrent.hashString,
                                                torrent.name, torrent.labels, limit_speed)


def add_limit_upload_to_hash_and_print_internal(site, qb_or_tr, hash, name, tags, limit_speed: int):
    hashs_qb_or_tr = hashs_to_limit_upload[qb_or_tr]
    if limit_speed not in hashs_qb_or_tr:
        hashs_qb_or_tr[limit_speed] = set()
    hashs_qb_or_tr[limit_speed].add(hash)
    if DEBUG_LOG and limit_speed > 0:
        print(
            f"{qb_or_tr}:命中限速站点({site},{readable_file_size(limit_speed * 1024, False)}) {name},{tags}")


def set_limit():
    # hashs = {'qb1': {'0': set(), '1024': set()}, 'tr': {同左侧}
    qb1_hashs_to_limit_upload = hashs_to_limit_upload[QB1]
    for limit_speed, hashs in qb1_hashs_to_limit_upload.items():
        if SWITCH_REAL_INVOKE:
            qb1_client.torrents_set_upload_limit(limit_speed, hashs)
            if limit_speed > 0:
                qb1_client.torrents_add_tags(f"F-{readable_file_size(limit_speed, False)}", hashs)
        if limit_speed > 0:
            print(f"{prefix()}{QB1} 限速({readable_file_size(limit_speed, False)})种子个数: {len(hashs)}")
        else:
            print(f"{prefix()}{QB1} 不限速种子个数: {len(hashs)}")
    qb2_hashs_to_limit_upload = hashs_to_limit_upload[QB2]
    for limit_speed, hashs in qb2_hashs_to_limit_upload.items():
        if SWITCH_REAL_INVOKE:
            qb2_client.torrents_set_upload_limit(limit_speed, hashs)
            if limit_speed > 0:
                qb2_client.torrents_add_tags(f"F-{readable_file_size(limit_speed, False)}", hashs)
        if limit_speed > 0:
            print(f"{prefix()}{QB2} 限速({readable_file_size(limit_speed, False)})种子个数: {len(hashs)}")
        else:
            print(f"{prefix()}{QB2} 不限速种子个数: {len(hashs)}")
    tr_hashs_to_limit_upload = hashs_to_limit_upload[TR]
    for limit_speed, hashs in tr_hashs_to_limit_upload.items():
        if limit_speed > 0:
            if SWITCH_REAL_INVOKE:
                tr_client.change_torrent(ids=list(hashs), upload_limit=limit_speed,
                                         upload_limited=True)
                # tr tag 特殊处理
                for hash in hashs:
                    if hash not in tr_hash_tags:
                        tr_hash_tags[hash] = set()
                    tr_hash_tags[hash].add(f"F-{readable_file_size(limit_speed * 1024, False)}")
            print(
                f"{prefix()}tr 限速({readable_file_size(limit_speed * 1024, False)})种子个数: {len(hashs)}")
        else:
            if SWITCH_REAL_INVOKE:
                tr_client.change_torrent(ids=list(hashs), upload_limit=0, upload_limited=False)
            print(f"{prefix()}tr 不限速种子个数: {len(hashs)}")


def add_tags(tag):
    # 处理 qb1
    qb1_hashs_to_add_tag = hashs_to_add_tag[QB1]
    if tag in qb1_hashs_to_add_tag:
        tag_hash = qb1_hashs_to_add_tag[tag]
    else:
        tag_hash = None
    if tag_hash and len(tag_hash) > 0:
        if SWITCH_REAL_INVOKE:
            qb1_client.torrents_add_tags(tag, tag_hash)
        print(f"{prefix()}{QB1} 标记 [{tag}] 种子个数: {len(tag_hash)}")
    else:
        pass
        # print(f"{prefix()}{QB1} 标记 \"{tag}\" 种子个数: 0")
    # 处理 qb2
    qb2_hashs_to_add_tag = hashs_to_add_tag[QB2]
    if tag in qb2_hashs_to_add_tag:
        tag_hash = qb2_hashs_to_add_tag[tag]
    else:
        tag_hash = None
    if tag_hash and len(tag_hash) > 0:
        if SWITCH_REAL_INVOKE:
            qb2_client.torrents_add_tags(tag, tag_hash)
        print(f"{prefix()}{QB2} 标记 [{tag}] 种子个数: {len(tag_hash)}")
    else:
        pass
        # print(f"{prefix()}qb 标记 \"{tag}\" 种子个数: 0")
    # 处理 tr {hash,tags} 然后将 tags 排序后转成{tags,hashs}
    tr_hashs_to_add_tag = hashs_to_add_tag[TR]
    if tag in tr_hashs_to_add_tag:
        tag_hash = tr_hashs_to_add_tag[tag]
    else:
        tag_hash = None
    if tag_hash and len(tag_hash) > 0:
        if SWITCH_REAL_INVOKE:
            # tr 标记换一种思路生效,此处只打印,处理在 tr_add_tag_to_hash_and_print
            pass
        print(f"{prefix()}{TR} 标记 [{tag}] 种子个数: {len(tag_hash)}")
    else:
        pass
        # print(f"{prefix()}tr 标记 [{tag}] 种子个数: 0")


def torrent_files_contains(torrent_files, suffix) -> bool:
    for f in torrent_files:
        if f.name.endswith(suffix):
            return True
    # for data in t.files.data:
    #     if data.name.endswith(suffix):
    #         return True
    return False


# 判断是否所有 tracker 全是一个状态
def qb_trackers_only_msg(trackers, msg) -> bool:
    working_trackers = [tracker for tracker in trackers if tracker.status != TrackerStatus.DISABLED]
    for tracker in working_trackers:
        if msg not in tracker.msg:
            return False
    return True


# 判断是否所有 tracker 全是一个状态
def tr_trackers_only_msg(tracker_stats, msg) -> bool:
    for tracker_stat in tracker_stats:
        tracker_msg = tracker_stat.last_announce_result
        if msg not in tracker_msg:
            return False
    return True


video_extensions_for_emby = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.3gp', '.ts', '.m2ts', '.avi',
                             '.flac', '.mp3', '.test',
                             '.iso', '.rmvb', '.rm', '.mpeg', '.mpg', '.asf', '.m4v', '.f4v', '.strm', '.tp']

no_effective_extensions = ['.png', '.PNG', '.jpg', '.jpeg', '.JPG', '.nfo', '.DS_Store', '.ass', '.xml', '.torrent']


def is_effective_file(file_path):
    file_extension = os.path.splitext(file_path)[1]
    return file_extension not in no_effective_extensions


def is_effective_file_in_down(file_path):
    return True


def get_root_parent_dir(path):
    normalized_path = os.path.normpath(path)
    parts = normalized_path.split('/')
    if len(parts) > 1:
        first_part = parts[1]
        return first_part


def get_hard_link_count(file_path):
    try:
        # 获取文件的状态信息
        file_stat = os.stat(file_path)
        # 返回硬链接个数
        return file_stat.st_nlink
    except FileNotFoundError:
        return "文件不存在"


_cache_has_linked_torrent_content = {}  # -1 or 1


# 用于判断是否已入库
def has_linked_video_file(torrent_content_path) -> bool:
    cache = _cache_has_linked_torrent_content.get(torrent_content_path, 0)
    if cache:
        return cache == 1
    # 方案一: 寻找一个种子内视频文件路径,判断硬链接个数 (不行,这是 api 调用, 文件路径在服务端)
    # 方案二(不行): 判断同时包含 2 个标签,(不行, 有些辅种的不包含MOVIEPILOT, 而已整理的不一定都入库了(入库失败 & 辅种瞎标记))
    # has_into_emby = all(item in torrent.tags.split(',') for item in ['MOVIEPILOT', '已整理'])
    if os.path.isfile(torrent_content_path):
        file_abs_path = torrent_content_path
        if is_effective_file(file_abs_path):
            link_count = get_hard_link_count(file_abs_path)
            if link_count > 1:
                _cache_has_linked_torrent_content[torrent_content_path] = 1
                return True
        # file_extension = os.path.splitext(file_abs_path)[1]
        # if file_extension in video_extensions:
        #     link_count = get_hard_link_count(file_abs_path)
        #     if link_count > 1:
        #         return True

        # for extension in video_extensions:
        #     if folder_path.endswith(extension):
        #         file_abs_path = folder_path
        #         link_count = get_hard_link_count(file_abs_path)
        #         if link_count > 1:
        #             return True
        _cache_has_linked_torrent_content[torrent_content_path] = -1
        return False
    for root, dirs, files in os.walk(torrent_content_path):
        for file in files:
            file_abs_path = os.path.join(root, file)
            if is_effective_file(file_abs_path):
                link_count = get_hard_link_count(file_abs_path)
                if link_count > 1:
                    _cache_has_linked_torrent_content[torrent_content_path] = 1
                    return True

            # file_extension = os.path.splitext(file_abs_path)[1]
            # if file_extension in video_extensions:
            #     link_count = get_hard_link_count(file_abs_path)
            #     if link_count > 1:
            #         return True

            # for extension in video_extensions:
            #     if file.endswith(extension):
            #         file_abs_path = os.path.join(root, file)
            #         link_count = get_hard_link_count(file_abs_path)
            #         if link_count > 1:
            #             return True
    _cache_has_linked_torrent_content[torrent_content_path] = -1
    return False


def specific_process_tr_tags():
    if tr_client:
        # {hash,tags} 然后将 tags 排序后转成{tags,list = hashs}
        tr_tags_hash2 = {}
        for hash, tags in tr_hash_tags.items():
            if set(tr_hash_tags_old[hash]) == tags:
                continue  # 标签无变化,跳过重新标记
            sorted_tags_tuple = tuple(sorted(tags, reverse=False))
            # sorted_tags =  sorted(tags, key=lambda p: p)
            if sorted_tags_tuple not in tr_tags_hash2:
                tr_tags_hash2[sorted_tags_tuple] = list()
            tr_tags_hash2[sorted_tags_tuple].append(hash)
        if DEBUG_LOG:
            print(f"specific_process_tr_tags:  len={len(tr_tags_hash2)},{tr_tags_hash2}")
        else:
            print(f"specific_process_tr_tags:  len={len(tr_tags_hash2)}")
        if SWITCH_REAL_INVOKE:
            for sorted_tags_tuple, hashs in tr_tags_hash2.items():
                tr_client.change_torrent(ids=list(hashs), labels=list(sorted_tags_tuple))


def print_no_link_internal_in_emby(folder_path):
    all_file_size = 0
    dirt_file_size = {}
    for root, dirs, files in os.walk(folder_path):
        if any(element in root for element in EMBY_IGNORE_PATH_List):
            if DEBUG_LOG:
                print(f"------配置为忽略检查路径:{convert_emby_mirror_to_real_path(root)}")
            continue
        for file in files:
            for extension in video_extensions_for_emby:
                if file.endswith(extension):
                    file_abs_path = os.path.join(root, file)
                    link_count = get_hard_link_count(file_abs_path)
                    # print(file_abs_path)
                    # print(link_count)
                    if link_count > 1:
                        # print(f"{file_abs_path} link count : {link_count}")
                        pass
                    else:
                        size = os.path.getsize(file_abs_path)
                        all_file_size = all_file_size + size
                        dirt_file_size.update({file_abs_path: size})
                    break
    print(
        f"---{convert_emby_mirror_to_real_path(folder_path)} 下所有没有做种文件总大小: {readable_file_size(all_file_size)}, 列表如下:")
    # 排序打印
    sorted_keys = sorted(dirt_file_size.keys(), key=lambda p: p)
    sorted_dict = {key: dirt_file_size[key] for key in sorted_keys}
    for path, size in sorted_dict.items():
        print(f"------没有做种:{convert_emby_mirror_to_real_path(path)} | {readable_file_size(size)}")


def print_mulity_video_file_internal_in_emby(directory):
    file_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            abs_paths = os.path.join(root, file)
            abs_name, ext = os.path.splitext(abs_paths)
            # 去除名字中的 1080p、2160p 等字符
            abs_name = ''.join(
                [part for part in abs_name.split() if part not in ['720p', '1080p', '2160p']])
            if ext in video_extensions_for_emby:
                if abs_name in file_dict:
                    file_dict[abs_name].append(abs_paths)
                else:
                    file_dict[abs_name] = [abs_paths]
    for abs_name, files in file_dict.items():
        if len(files) > 1:
            print("-")
            for index, file in enumerate(files):
                print(convert_emby_mirror_to_real_path(file))
                # 删除后面的
                # if index != 0:
                #     os.remove(file)


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")


def get_tracker_sites():
    return {
            "tracker.cyanbug.net": "大青虫"
            }


def convert_script_download_mirror_to_real_path(mirror_path):
    if IS_MIRROR_SCRIPT_DOWN_PATH:
        for item in DOWNLOAD_DIRS:
            script_path = item[0]
            real_path = item[1]
            if mirror_path.startswith(script_path):
                return mirror_path.replace(script_path, real_path)
        return mirror_path
    else:
        return mirror_path


def convert_download_mirror_to_real_path(mirror_path):
    if IS_MIRROR_DOWN_PATH:
        for item in DOWNLOAD_DIRS:
            real_path = item[1]
            downloader_path = item[2]
            if mirror_path.startswith(downloader_path):
                return mirror_path.replace(downloader_path, real_path)
        return mirror_path
    else:
        return mirror_path


def convert_emby_mirror_to_real_path(mirror_path):
    if IS_MIRROR_EMBY_PATH:
        for mirror, realPath in EMBY_PARENT_DIRS.items():
            if mirror_path.startswith(mirror):
                return mirror_path.replace(mirror, realPath)
        return mirror_path
    else:
        return mirror_path


# torrent.files torrent.trackers 是 api 调用,尽量减少次数
if __name__ == '__main__':
    print(
        f"{now()}当前运行主机 ip:{get_current_device_local_ip_address()}, 服务端 ip:{SERVER_HOST}")
    start = time.time()
    # 连接信息打印
    qb1_client = None
    # 尝试登录
    try:
        qb1_client = qbittorrentapi.Client(**QB1_CONN_INFO)
        qb1_client.auth_log_in()
    except Exception as e:
        qb1_client = None
        print(f"登录{QB1}失败")
    qb2_client = None
    # 尝试登录
    try:
        qb2_client = qbittorrentapi.Client(**QB2_CONN_INFO)
        qb2_client.auth_log_in()
    except Exception as e:
        qb2_client = None
        print(f"登录{QB2}失败")
    tr_client = None
    try:
        tr_client = Client(**TR_CONN_INFO)
    except Exception as e:
        print(f"登录{TR}失败")
    if not qb1_client and not qb2_client and not tr_client:
        exit(-2)
    # 步骤1 第一遍遍历, 收集要标记的信息
    if qb1_client:
        qb1_sorted_torrents_infos = sorted(qb1_client.torrents_info(), key=lambda x: x['name'])
    else:
        qb1_sorted_torrents_infos = []
    if qb2_client:
        qb2_sorted_torrents_infos = sorted(qb2_client.torrents_info(), key=lambda x: x['name'])
    else:
        qb2_sorted_torrents_infos = []
    if tr_client:
        # 参考transmission web，仅查询需要的参数，加速种子搜索
        tr_sorted_torrents_infos = sorted(tr_client.get_torrents(), key=lambda x: x.name)
    else:
        tr_sorted_torrents_infos = []
    print(
        f"{QB1}共{len(qb1_sorted_torrents_infos)}个种子; {QB2}共{len(qb2_sorted_torrents_infos)}个种子; {TR}共{len(tr_sorted_torrents_infos)}个种子;")
    # 加载tracker 站点标签配置
    tracker_sites = get_tracker_sites()
    # tracker_sites = {}
    # file_path = Path(__file__).parent / "qb_trackers.txt"
    # if os.path.exists(file_path):
    #     with open(file_path, 'r', encoding='utf-8') as file:
    #         for line in file.readlines():
    #             key, value = line.strip().split(':')
    #             tracker_sites[key] = value
    all_sites = set(tracker_sites.values())
    # [脚本执行环境视角路径,真实路径,下载器视角路径]
    # 如果路径映射有相同就认为是在 docker 内执行
    IS_MIRROR_SCRIPT_DOWN_PATH = False
    IS_MIRROR_DOWN_PATH = False
    for item in DOWNLOAD_DIRS:
        script_path = item[0]
        real_path = item[1]
        downloader_path = item[2]
        if script_path != real_path:
            IS_MIRROR_SCRIPT_DOWN_PATH = True
        if downloader_path != real_path:
            IS_MIRROR_DOWN_PATH = True
    IS_MIRROR_EMBY_PATH = False
    for key, value in EMBY_PARENT_DIRS.items():
        if key != value:
            IS_MIRROR_EMBY_PATH = True
            break
    print(
        f"IS_MIRROR_SCRIPT_DOWN_PATH={IS_MIRROR_SCRIPT_DOWN_PATH},IS_MIRROR_DOWN_PATH={IS_MIRROR_DOWN_PATH},IS_MIRROR_EMBY_PATH={IS_MIRROR_EMBY_PATH},")
    SWITCH_EMBY_QB1 = QB1 in SWITCH_EMBY_CLIENT
    SWITCH_EMBY_QB2 = QB2 in SWITCH_EMBY_CLIENT
    SWITCH_EMBY_TR = TR in SWITCH_EMBY_CLIENT
    SWITCH_TORRENT_COUNT_QB1 = QB1 in SWITCH_TORRENT_COUNT_CLIENT
    SWITCH_TORRENT_COUNT_QB2 = QB2 in SWITCH_TORRENT_COUNT_CLIENT
    SWITCH_TORRENT_COUNT_TR = TR in SWITCH_TORRENT_COUNT_CLIENT
    SWITCH_FILE_SUFFIX_QB1 = QB1 in SWITCH_FILE_SUFFIX_CLIENT
    SWITCH_FILE_SUFFIX_QB2 = QB2 in SWITCH_FILE_SUFFIX_CLIENT
    SWITCH_FILE_SUFFIX_TR = TR in SWITCH_FILE_SUFFIX_CLIENT
    SWITCH_TRACKER_QB1 = QB1 in SWITCH_TRACKER_CLIENT
    SWITCH_TRACKER_QB2 = QB2 in SWITCH_TRACKER_CLIENT
    SWITCH_TRACKER_TR = TR in SWITCH_TRACKER_CLIENT
    SWITCH_LIMIT_QB1 = QB1 in SWITCH_LIMIT_CLIENT
    SWITCH_LIMIT_QB2 = QB2 in SWITCH_LIMIT_CLIENT
    SWITCH_LIMIT_TR = TR in SWITCH_LIMIT_CLIENT
    SWITCH_TAG_ROOT_PATH_QB1 = QB1 in SWITCH_TAG_ROOT_PATH_CLIENT
    SWITCH_TAG_ROOT_PATH_QB2 = QB2 in SWITCH_TAG_ROOT_PATH_CLIENT
    SWITCH_TAG_ROOT_PATH_TR = TR in SWITCH_TAG_ROOT_PATH_CLIENT

    print(f"{now()}步骤1.第一遍遍历, 收集要标记的信息...")
    # qb&tr key=save_path + torrent name,
    #       value=[0copy_count, 1all_torrent_tags, 2file_size, 3has_link, 4name, 5in qb1, 6in tr, 7in qb2]
    dirt_content_path_values = {}
    # qb&tr 中的所有视频文件-非下载中(拆出不下载文件), {'qb1': {'path1': [torrent1,torrent2], 'path2': list()}, 'tr': {同左侧}}
    torrent_video_files_dirt = {QB1: {}, QB2: {}, TR: {}}
    # qb&tr 中的所有视频文件-下载中(拆出不下载文件),结构同上
    torrent_video_files_downloading_dirt = {QB1: {}, QB2: {}, TR: {}}
    # qb1 数据缓存,避免多次请求 api,{hash:torrent.files}
    qb1_cache_hash_files = {}
    qb2_cache_hash_files = {}
    # qb2 数据缓存,避免多次请求 api,{hash:torrent.trackers}
    qb1_cache_hash_trackers = {}
    qb2_cache_hash_trackers = {}
    # qb12+tr site_tag 缓存 {hash:site_tag},会在第二遍遍历补充
    cache_site_tag_hashs = {}
    for torrent in qb1_sorted_torrents_infos:
        save_path = convert_download_mirror_to_real_path(torrent.save_path)
        # files = torrent.files
        files = [file for file in torrent.files if file.priority >= 1]  # 改为只筛选待下载的
        qb1_cache_hash_files[torrent.hash] = files
        qb1_cache_hash_trackers[torrent.hash] = torrent.trackers
        if torrent.state_enum.is_downloading:
            print(f"{QB1}下载中跳过标记: {torrent.name}")
            for file in files:
                abs_file_path = os.path.join(save_path, file.name)
                if is_effective_file_in_down(abs_file_path):
                    hashs_qb_or_tr = torrent_video_files_downloading_dirt[QB1]
                    if abs_file_path not in hashs_qb_or_tr:
                        hashs_qb_or_tr[abs_file_path] = list()
                    hashs_qb_or_tr[abs_file_path].append(torrent)
            continue
        # 辅种个数累加
        current_torrent_tag_list = [element.strip() for element in torrent.tags.split(',')]
        # '/volume2/video/Downloads/qBittorrent/电影/127.Hours.2010.1080p.BluRay.AVC.DTS-HD.MA.5.1-DIY@Audies'
        # content_path = torrent.content_path  # str 有 bug,qb 下单视频文件会带上视频名称,所以换成 save_path+torrent name
        content_path = os.path.join(save_path, torrent.name)  # str
        if content_path in dirt_content_path_values:
            old_entity = dirt_content_path_values[content_path]
            old_entity[0] = old_entity[0] + 1
            old_entity[1].update(current_torrent_tag_list)
            old_entity[5] = True  # 假如 tr 遍历再前边,qb 后设置
        else:
            dirt_content_path_values[content_path] = \
                [1, set(current_torrent_tag_list), torrent.size,
                 has_linked_video_file(content_path), torrent.name, True, False, False]

        for file in files:
            abs_file_path = os.path.join(save_path, file.name)
            if is_effective_file_in_down(abs_file_path):
                hashs_qb_or_tr = torrent_video_files_dirt[QB1]
                if abs_file_path not in hashs_qb_or_tr:
                    hashs_qb_or_tr[abs_file_path] = list()
                hashs_qb_or_tr[abs_file_path].append(torrent)
    for torrent in qb2_sorted_torrents_infos:
        save_path = convert_download_mirror_to_real_path(torrent.save_path)
        # files = torrent.files
        files = [file for file in torrent.files if file.priority >= 1]  # 改为只筛选待下载的
        qb2_cache_hash_files[torrent.hash] = files
        qb2_cache_hash_trackers[torrent.hash] = torrent.trackers
        if torrent.state_enum.is_downloading:
            print(f"{QB2}下载中跳过标记: {torrent.name}")
            for file in files:
                abs_file_path = os.path.join(save_path, file.name)
                if is_effective_file_in_down(abs_file_path):
                    hashs_qb_or_tr = torrent_video_files_downloading_dirt[QB2]
                    if abs_file_path not in hashs_qb_or_tr:
                        hashs_qb_or_tr[abs_file_path] = list()
                    hashs_qb_or_tr[abs_file_path].append(torrent)
            continue
        # 辅种个数累加
        current_torrent_tag_list = [element.strip() for element in torrent.tags.split(',')]
        # '/volume2/video/Downloads/qBittorrent/电影/127.Hours.2010.1080p.BluRay.AVC.DTS-HD.MA.5.1-DIY@Audies'
        # content_path = torrent.content_path  # str 有 bug,qb 下单视频文件会带上视频名称,所以换成 save_path+torrent name
        content_path = os.path.join(save_path, torrent.name)  # str
        if content_path in dirt_content_path_values:
            old_entity = dirt_content_path_values[content_path]
            old_entity[0] = old_entity[0] + 1
            old_entity[1].update(current_torrent_tag_list)
            old_entity[7] = True  # 假如 tr 遍历再前边,qb 后设置
        else:
            dirt_content_path_values[content_path] = \
                [1, set(current_torrent_tag_list), torrent.size,
                 has_linked_video_file(content_path), torrent.name, False, False, True]

        for file in files:
            abs_file_path = os.path.join(save_path, file.name)
            if is_effective_file_in_down(abs_file_path):
                hashs_qb_or_tr = torrent_video_files_dirt[QB2]
                if abs_file_path not in hashs_qb_or_tr:
                    hashs_qb_or_tr[abs_file_path] = list()
                hashs_qb_or_tr[abs_file_path].append(torrent)
    tr_old_tags = set()
    for torrent in tr_sorted_torrents_infos:
        save_path = convert_download_mirror_to_real_path(torrent.download_dir)
        files = [file for file in torrent.get_files() if file.selected]  # 改为只筛选待下载的
        if torrent.status.downloading or torrent.status.download_pending:
            print(f"tr下载中跳过标记: {torrent.name}")
            for file in files:
                abs_file_path = os.path.join(save_path, file.name)
                if is_effective_file_in_down(abs_file_path):
                    hashs_qb_or_tr = torrent_video_files_downloading_dirt[TR]
                    if abs_file_path not in hashs_qb_or_tr:
                        hashs_qb_or_tr[abs_file_path] = list()
                    hashs_qb_or_tr[abs_file_path].append(torrent)
            continue
        # 辅种个数累加
        current_torrent_tag_list = [element.strip() for element in torrent.labels]
        tr_old_tags.update(current_torrent_tag_list)
        content_path = os.path.join(save_path, torrent.name)  # str
        if content_path in dirt_content_path_values:
            old_entity = dirt_content_path_values[content_path]
            old_entity[0] = old_entity[0] + 1
            old_entity[1].update(current_torrent_tag_list)
            old_entity[6] = True
        else:
            dirt_content_path_values[content_path] = \
                [1, set(current_torrent_tag_list), torrent.total_size,
                 has_linked_video_file(content_path), torrent.name, False, True, False]

        for file in files:
            abs_file_path = os.path.join(save_path, file.name)
            if is_effective_file_in_down(abs_file_path):
                hashs_qb_or_tr = torrent_video_files_dirt[TR]
                if abs_file_path not in hashs_qb_or_tr:
                    hashs_qb_or_tr[abs_file_path] = list()
                hashs_qb_or_tr[abs_file_path].append(torrent)

    # 步骤2. 第二遍遍历,标记收集完的信息
    print(f"{now()}步骤2.第二遍遍历,标记收集完的信息...")
    file_size_LIMIT_TO_DELETE_THRESHOLD = {}  # 实际体积 key=content_path,value=size
    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD = 0  # 对应辅种体积
    tr_to_remove_old_tags = set([s for s in tr_old_tags if s.startswith('F-')])
    to_add_site_tags = set()  # qb1&qb2&tr待补充站点标签的标签列表
    TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS = TAG_LONG_KEEP in EXCLUDE_CONTAINS_STATIONS
    if qb1_client:
        print(f'{now()}开始收集 {QB1} 中待标记信息...')
    qb1_torrent_count = len(qb1_sorted_torrents_infos)
    for index, torrent in enumerate(qb1_sorted_torrents_infos):
        if DEBUG_LOG:
            print(f'{QB1}:{index + 1}/{qb1_torrent_count}')
        qb_trackers = qb1_cache_hash_trackers[torrent.hash]
        # 当前种子 tags list
        current_torrent_tag_list = [element.strip() for element in torrent.tags.split(',')]
        # qb 补充站点标签
        intersection = all_sites.intersection(current_torrent_tag_list)
        site_tag = None
        if intersection:
            site_tag = list(intersection)[0]
        else:  # 无站点标签
            working_trackers = [tracker for tracker in qb_trackers if
                                tracker.status != TrackerStatus.DISABLED]
            for tracker in working_trackers:
                domain = urlparse(tracker.url).netloc
                site_tag = tracker_sites.get(domain, None)
                if site_tag:
                    break
            # 更新站点标签
            if site_tag:
                to_add_site_tags.add(site_tag)
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, site_tag)
        cache_site_tag_hashs[torrent.hash] = site_tag

        if torrent.state_enum.is_downloading:
            if DEBUG_LOG:
                print(f"{QB1}下载中跳过标记: {torrent.name}")
            continue
        save_path = convert_download_mirror_to_real_path(torrent.save_path)
        files = qb1_cache_hash_files[torrent.hash]

        # e=[copy_count, all_torrent_tags, file_size, has_link]
        content_path = os.path.join(save_path, torrent.name)
        e = dirt_content_path_values[content_path]
        copy_count = e[0]  # 总辅种个数
        all_torrent_tags = e[1]  # 所有辅种的 标签 合集
        file_size = e[2]  # 种子对应文件大小
        has_link = e[3]  # 视频文件是否已硬链接
        name = e[4]  # 种子 name
        in_tr = e[6]  # 是否有 tr 辅种
        in_qb2 = e[7]  # 是否有 qb2 辅种

        if SWITCH_TAG_ROOT_PATH_QB1:
            qb_add_tag_to_hash_and_print(QB1, site_tag, torrent,
                                         f'F-{get_root_parent_dir(save_path)}')
        # 是否通过了 condition_to_long_keep 和 EXCLUDE_CONTAINS_STATIONS 和 copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD 的检查，通过之后才能添加‘未入库’和‘F-辅种x’标签
        intersection = EXCLUDE_CONTAINS_STATIONS.intersection(all_torrent_tags)
        copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD = copy_count >= LIMIT_TO_LONG_KEEP_THRESHOLD
        siwtchLoneKeep_and_hit = False
        if condition_to_long_keep(content_path):
            if SWITCH_EMBY_QB1 or SWITCH_TORRENT_COUNT_QB1:
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_LONG_KEEP)
            siwtchLoneKeep_and_hit = TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS

        # 是否入了媒体库(有硬链接等于入了媒体库),用其中一个视频文件路径判断
        if SWITCH_EMBY_QB1:
            if has_link:
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_IN_EMBY)
            else:
                if not intersection and not siwtchLoneKeep_and_hit and not copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_NOT_IN_EMBY)
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"{QB1}:未添加[{TAG_NOT_IN_EMBY}]标记, 标签中(包含关联辅种)存在\"{intersection}\" {torrent.name} [{site_tag}]")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"{QB1}:未添加[{TAG_NOT_IN_EMBY}]标记, 标签中(包含关联辅种)存在\"{TAG_LONG_KEEP}\" {torrent.name} [{site_tag}]")
                        elif copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                            print(
                                f"{QB1}:未添加[{TAG_NOT_IN_EMBY}]标记, 辅种数{copy_count}大于{LIMIT_TO_LONG_KEEP_THRESHOLD} {torrent.name} [{site_tag}]")
        # 辅种个数标记
        if SWITCH_TORRENT_COUNT_QB1:
            # 辅种小于 x 标记
            if copy_count <= LIMIT_TO_DELETE_THRESHOLD:
                # 先排除部分站点-两个列表没有交集
                if not intersection and not siwtchLoneKeep_and_hit and not copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    tag = TAG_COPY_COUNT % copy_count
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, tag)
                    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD += file_size
                    if content_path not in file_size_LIMIT_TO_DELETE_THRESHOLD:
                        file_size_LIMIT_TO_DELETE_THRESHOLD[content_path] = file_size
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"{QB1}:未添加辅种数标记, 标签中(包含关联辅种)存在\"{intersection}\" {torrent.name} [{site_tag}]")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"{QB1}:未添加辅种数标记, 标签中(包含关联辅种)存在\"{TAG_LONG_KEEP}\" {torrent.name} [{site_tag}]")
                        elif copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                            print(
                                f"{QB1}:未添加辅种数标记, 辅种数{copy_count}大于{LIMIT_TO_LONG_KEEP_THRESHOLD} {torrent.name} [{site_tag}]")
            if copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_LONG_KEEP)

        # 文件类型标记
        if SWITCH_FILE_SUFFIX_QB1:
            if torrent_files_contains(files, '.iso'):
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_ISO)
            elif torrent_files_contains(files, '.ts'):
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_TS)
            elif torrent_files_contains(files, '.m2ts'):
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_M2TS)

        # tracker 标记
        if SWITCH_TRACKER_QB1:
            # 没有正在工作的 tracker
            working_trackers = [tracker for tracker in qb_trackers if
                                tracker.status != TrackerStatus.DISABLED]
            if len(working_trackers) == 0:
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_NO_WORKING_TRACKER1)
                else:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_NO_WORKING_TRACKER2)
            # elif trackers_only_msg(trackers, 'Bad Gateway'):
            #     if copy_count > 1:
            #         qb_add_tag_to_hash_and_print(QB, site_tag, torrent, TAG_TRACKERS_ONLY_Bad_Gateway1)
            #     else:
            #         qb_add_tag_to_hash_and_print(QB, site_tag, torrent, TAG_TRACKERS_ONLY_Bad_Gateway2)
            elif qb_trackers_only_msg(qb_trackers, 'orrent not registered') \
                    or qb_trackers_only_msg(qb_trackers, 'Unregistered torrent') \
                    or qb_trackers_only_msg(qb_trackers, 'orrent not exists') \
                    or qb_trackers_only_msg(qb_trackers, 'orrent banned') \
                    or qb_trackers_only_msg(qb_trackers, 'orrent delete') \
                    or qb_trackers_only_msg(qb_trackers, '被删除'):
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_TORRENT_ERROR1)
                else:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_TORRENT_ERROR2)
            elif qb_trackers_only_msg(qb_trackers, 'client is not on the whitelist'):
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent,
                                                 TAG_TRACKERS_CLIENT_NOT_WHITE1)
                else:
                    qb_add_tag_to_hash_and_print(QB1, site_tag, torrent,
                                                 TAG_TRACKERS_CLIENT_NOT_WHITE2)

        # 是否在 tr 辅种
        if SWITCH_MARK_IN_TR_OR_QB12:
            if in_tr:
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_IN_TR)
            if in_qb2:
                qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_IN_QB2)
        # 标记限速种子
        if SWITCH_LIMIT_QB1:
            if site_tag in QB1_UOLOAD_LIMIT_SITE:  # 理论上标签应该只有 1 个交集,就是站点名称,所以取 0
                limit_speed = QB1_UOLOAD_LIMIT_SITE[site_tag]
                qb_add_limit_upload_to_hash_and_print(site_tag, QB1, torrent, limit_speed)
            else:
                qb_add_limit_upload_to_hash_and_print(None, QB1, torrent, 0)
    if qb2_client:
        print(f'{now()}开始收集 {QB2} 中待标记信息...')
    qb2_torrent_count = len(qb2_sorted_torrents_infos)
    for index, torrent in enumerate(qb2_sorted_torrents_infos):
        if DEBUG_LOG:
            print(f'{QB2}:{index + 1}/{qb2_torrent_count}')
        qb_trackers = qb2_cache_hash_trackers[torrent.hash]
        # 当前种子 tags list
        current_torrent_tag_list = [element.strip() for element in torrent.tags.split(',')]
        # qb 补充站点标签
        intersection = all_sites.intersection(current_torrent_tag_list)
        site_tag = None
        if intersection:
            site_tag = list(intersection)[0]
        else:  # 无站点标签
            working_trackers = [tracker for tracker in qb_trackers if
                                tracker.status != TrackerStatus.DISABLED]
            for tracker in working_trackers:
                domain = urlparse(tracker.url).netloc
                site_tag = tracker_sites.get(domain, None)
                if site_tag:
                    break
            # 更新站点标签
            if site_tag:
                to_add_site_tags.add(site_tag)
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, site_tag)
        cache_site_tag_hashs[torrent.hash] = site_tag

        if torrent.state_enum.is_downloading:
            if DEBUG_LOG:
                print(f"{QB2}下载中跳过标记: {torrent.name}")
            continue
        save_path = convert_download_mirror_to_real_path(torrent.save_path)
        files = qb2_cache_hash_files[torrent.hash]

        # e=[copy_count, all_torrent_tags, file_size, has_link]
        content_path = os.path.join(save_path, torrent.name)
        e = dirt_content_path_values[content_path]
        copy_count = e[0]  # 总辅种个数
        all_torrent_tags = e[1]  # 所有辅种的 标签 合集
        file_size = e[2]  # 种子对应文件大小
        has_link = e[3]  # 视频文件是否已硬链接
        name = e[4]  # 种子 name
        in_qb1 = e[5]  # 是否有 qb1 辅种
        in_tr = e[6]  # 是否有 tr 辅种

        if SWITCH_TAG_ROOT_PATH_QB2:
            qb_add_tag_to_hash_and_print(QB2, site_tag, torrent,
                                         f'F-{get_root_parent_dir(save_path)}')
        # 是否通过了 condition_to_long_keep 和 EXCLUDE_CONTAINS_STATIONS 和 copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD 的检查，通过之后才能添加‘未入库’和‘F-辅种x’标签
        intersection = EXCLUDE_CONTAINS_STATIONS.intersection(all_torrent_tags)
        copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD = copy_count >= LIMIT_TO_LONG_KEEP_THRESHOLD
        siwtchLoneKeep_and_hit = False
        if condition_to_long_keep(content_path):
            if SWITCH_EMBY_QB2 or SWITCH_TORRENT_COUNT_QB2:
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_LONG_KEEP)
            siwtchLoneKeep_and_hit = TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS

        # 是否入了媒体库(有硬链接等于入了媒体库),用其中一个视频文件路径判断
        if SWITCH_EMBY_QB2:
            if has_link:
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_IN_EMBY)
            else:
                if not intersection and not siwtchLoneKeep_and_hit and not copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_NOT_IN_EMBY)
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"{QB2}:未添加[{TAG_NOT_IN_EMBY}]标记, 标签中(包含关联辅种)存在\"{intersection}\" {torrent.name} [{site_tag}]")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"{QB2}:未添加[{TAG_NOT_IN_EMBY}]标记, 标签中(包含关联辅种)存在\"{TAG_LONG_KEEP}\" {torrent.name} [{site_tag}]")
                        elif copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                            print(
                                f"{QB2}:未添加[{TAG_NOT_IN_EMBY}]标记, 辅种数{copy_count}大于{LIMIT_TO_LONG_KEEP_THRESHOLD} {torrent.name} [{site_tag}]")
        # 辅种个数标记
        if SWITCH_TORRENT_COUNT_QB2:
            # 辅种小于 x 标记
            if copy_count <= LIMIT_TO_DELETE_THRESHOLD:
                # 先排除部分站点-两个列表没有交集
                if not intersection and not siwtchLoneKeep_and_hit and not copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    tag = TAG_COPY_COUNT % copy_count
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, tag)
                    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD += file_size
                    if content_path not in file_size_LIMIT_TO_DELETE_THRESHOLD:
                        file_size_LIMIT_TO_DELETE_THRESHOLD[content_path] = file_size
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"{QB2}:未添加辅种数标记, 标签中(包含关联辅种)存在\"{intersection}\" {torrent.name} [{site_tag}]")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"{QB2}:未添加辅种数标记, 标签中(包含关联辅种)存在\"{TAG_LONG_KEEP}\" {torrent.name} [{site_tag}]")
                        elif copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                            print(
                                f"{QB2}:未添加辅种数标记, 辅种数{copy_count}大于{LIMIT_TO_LONG_KEEP_THRESHOLD} {torrent.name} [{site_tag}]")
            if copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_LONG_KEEP)

        # 文件类型标记
        if SWITCH_FILE_SUFFIX_QB2:
            if torrent_files_contains(files, '.iso'):
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_ISO)
            elif torrent_files_contains(files, '.ts'):
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_TS)
            elif torrent_files_contains(files, '.m2ts'):
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_M2TS)

        # tracker 标记
        if SWITCH_TRACKER_QB2:
            # 没有正在工作的 tracker
            working_trackers = [tracker for tracker in qb_trackers if
                                tracker.status != TrackerStatus.DISABLED]
            if len(working_trackers) == 0:
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_NO_WORKING_TRACKER1)
                else:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_NO_WORKING_TRACKER2)
            # elif trackers_only_msg(trackers, 'Bad Gateway'):
            #     if copy_count > 1:
            #         qb_add_tag_to_hash_and_print(QB, site_tag, torrent, TAG_TRACKERS_ONLY_Bad_Gateway1)
            #     else:
            #         qb_add_tag_to_hash_and_print(QB, site_tag, torrent, TAG_TRACKERS_ONLY_Bad_Gateway2)
            elif qb_trackers_only_msg(qb_trackers, 'orrent not registered') \
                    or qb_trackers_only_msg(qb_trackers, 'Unregistered torrent') \
                    or qb_trackers_only_msg(qb_trackers, 'orrent not exists') \
                    or qb_trackers_only_msg(qb_trackers, 'orrent banned') \
                    or qb_trackers_only_msg(qb_trackers, 'orrent delete') \
                    or qb_trackers_only_msg(qb_trackers, '被删除'):
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_TORRENT_ERROR1)
                else:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_TORRENT_ERROR2)
            elif qb_trackers_only_msg(qb_trackers, 'client is not on the whitelist'):
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent,
                                                 TAG_TRACKERS_CLIENT_NOT_WHITE1)
                else:
                    qb_add_tag_to_hash_and_print(QB2, site_tag, torrent,
                                                 TAG_TRACKERS_CLIENT_NOT_WHITE2)

        # 是否在 tr 辅种
        if SWITCH_MARK_IN_TR_OR_QB12:
            if in_qb1:
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_IN_QB1)
            if in_tr:
                qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_IN_TR)
        # 标记限速种子
        if SWITCH_LIMIT_QB2:
            if site_tag in QB2_UOLOAD_LIMIT_SITE:  # 理论上标签应该只有 1 个交集,就是站点名称,所以取 0
                limit_speed = QB2_UOLOAD_LIMIT_SITE[site_tag]
                qb_add_limit_upload_to_hash_and_print(site_tag, QB2, torrent, limit_speed)
            else:
                qb_add_limit_upload_to_hash_and_print(None, QB2, torrent, 0)
    if tr_client:
        print(f'{now()}开始收集 tr 中待标记信息...')
    size = len(tr_sorted_torrents_infos)
    for index, torrent in enumerate(tr_sorted_torrents_infos):
        if DEBUG_LOG:
            print(f'tr:{index + 1}/{size}')
        tr_trackers = torrent.tracker_stats
        # 当前种子 tags list
        current_torrent_tag_list = [element.strip() for element in torrent.labels]
        tr_hash_tags_old[torrent.hashString] = current_torrent_tag_list
        tr_hash_tags[torrent.hashString] = set(current_torrent_tag_list) - tr_to_remove_old_tags  # 这行要放前边
        # tr 补充站点标签
        intersection = all_sites.intersection(current_torrent_tag_list)
        site_tag = None
        if intersection:
            site_tag = list(intersection)[0]
        else:  # 无站点标签
            for tracker in tr_trackers:
                domain = urlparse(tracker.announce).netloc
                site_tag = tracker_sites.get(domain, None)
                if site_tag:
                    break
            # 更新站点标签
            if site_tag:
                to_add_site_tags.add(site_tag)
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, site_tag)
        cache_site_tag_hashs[torrent.hashString] = site_tag
        if torrent.status.downloading or torrent.status.download_pending:
            print(f"tr下载中跳过标记: {torrent.name}")
            continue
        files = [file for file in torrent.get_files() if file.selected]  # 改为只筛选待下载的
        save_path = convert_download_mirror_to_real_path(torrent.download_dir)
        content_path = os.path.join(save_path, torrent.name)  # str
        # e=[copy_count, all_torrent_tags, file_size, has_link]
        e = dirt_content_path_values[content_path]
        copy_count = e[0]  # 总辅种个数
        all_torrent_tags = e[1]  # 所有辅种的 标签 合集
        file_size = e[2]  # 种子对应文件大小
        has_link = e[3]  # 视频文件是否已硬链接
        name = e[4]  # 种子 name
        in_qb1 = e[5]  # 是否有 qb1 辅种
        in_qb2 = e[7]  # 是否有 qb2 辅种

        if SWITCH_TAG_ROOT_PATH_TR:
            tr_add_tag_to_hash_and_print(TR, site_tag, torrent,
                                         f'F-{get_root_parent_dir(save_path)}')

        # 是否通过了 condition_to_long_keep 和 EXCLUDE_CONTAINS_STATIONS 和 copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD 的检查，通过之后才能添加‘未入库’和‘F-辅种x’标签
        intersection = EXCLUDE_CONTAINS_STATIONS.intersection(all_torrent_tags)
        copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD = copy_count >= LIMIT_TO_LONG_KEEP_THRESHOLD
        siwtchLoneKeep_and_hit = False
        if condition_to_long_keep(content_path):
            if SWITCH_EMBY_TR or SWITCH_TORRENT_COUNT_TR:
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_LONG_KEEP)
            siwtchLoneKeep_and_hit = TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS

        # 是否入了媒体库(有硬链接等于入了媒体库),用其中一个视频文件路径判断
        torrent_long_keep = False
        if SWITCH_EMBY_TR:
            if has_link:
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_IN_EMBY)
            else:
                if not intersection and not siwtchLoneKeep_and_hit and not copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_NOT_IN_EMBY)
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"tr:未添加[{TAG_NOT_IN_EMBY}]标记, 标签中(包含关联辅种)存在\"{intersection}\" {torrent.name} [{site_tag}]")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"tr:未添加[{TAG_NOT_IN_EMBY}]标记, 标签中(包含关联辅种)存在\"{TAG_LONG_KEEP}\" {torrent.name} [{site_tag}]")
                        elif copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                            print(
                                f"tr:未添加[{TAG_NOT_IN_EMBY}]标记, 辅种数{copy_count}大于{LIMIT_TO_LONG_KEEP_THRESHOLD} {torrent.name} [{site_tag}]")

        # 辅种个数标记
        if SWITCH_TORRENT_COUNT_TR:
            # 辅种小于 x 标记
            if copy_count <= LIMIT_TO_DELETE_THRESHOLD:
                # 先排除部分站点-两个列表没有交集
                intersection = EXCLUDE_CONTAINS_STATIONS.intersection(all_torrent_tags)
                siwtchLoneKeep_and_hit = TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS and torrent_long_keep
                if not intersection and not siwtchLoneKeep_and_hit and not copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    tag = TAG_COPY_COUNT % copy_count
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent, tag)
                    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD += file_size
                    if content_path not in file_size_LIMIT_TO_DELETE_THRESHOLD:
                        file_size_LIMIT_TO_DELETE_THRESHOLD[content_path] = file_size
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"tr:未添加辅种数标记, 标签中(包含关联辅种)存在{intersection} {torrent.name}, [{site_tag}]")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"tr:未添加辅种数标记, 标签中(包含关联辅种)存在{TAG_LONG_KEEP} {torrent.name}, [{site_tag}]")
                        elif copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                            print(
                                f"tr:未添加辅种数标记, 辅种数{copy_count}大于{LIMIT_TO_LONG_KEEP_THRESHOLD} {torrent.name} [{site_tag}]")
                if copy_count_more_than_LIMIT_TO_LONG_KEEP_THRESHOLD:
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_LONG_KEEP)

        # 文件类型标记
        if SWITCH_FILE_SUFFIX_TR:
            if torrent_files_contains(files, '.iso'):
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_ISO)
            elif torrent_files_contains(files, '.ts'):
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_TS)
            elif torrent_files_contains(files, '.m2ts'):
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_M2TS)

        # tracker 标记
        if SWITCH_TRACKER_TR:
            if tr_trackers_only_msg(tr_trackers, 'orrent not registered') \
                    or tr_trackers_only_msg(tr_trackers, 'Unregistered torrent') \
                    or tr_trackers_only_msg(tr_trackers, 'orrent not exists') \
                    or tr_trackers_only_msg(tr_trackers, 'orrent banned') \
                    or tr_trackers_only_msg(tr_trackers, 'orrent delete') \
                    or tr_trackers_only_msg(tr_trackers, '被删除'):
                if copy_count > 1:
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_TORRENT_ERROR1)
                else:
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_TORRENT_ERROR2)
            elif tr_trackers_only_msg(tr_trackers, 'client is not on the whitelist'):
                if copy_count > 1:
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent,
                                                 TAG_TRACKERS_CLIENT_NOT_WHITE1)
                else:
                    tr_add_tag_to_hash_and_print(TR, site_tag, torrent,
                                                 TAG_TRACKERS_CLIENT_NOT_WHITE2)

        # 是否在 qb 辅种
        if SWITCH_MARK_IN_TR_OR_QB12:
            if in_qb1:
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_IN_QB1)
            if in_qb2:
                tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_IN_QB2)
        # 标记限速种子
        if SWITCH_LIMIT_TR:
            intersection = set(TR_UOLOAD_LIMIT_SITE).intersection(current_torrent_tag_list)
            if intersection:  # 理论上标签应该只有 1 个交集,就是站点名称,所以取 0
                site = list(intersection)[0]
                limit_speed = int(TR_UOLOAD_LIMIT_SITE[site] / 1024)
                tr_add_limit_upload_to_hash_and_print(site, TR, torrent, limit_speed)
            else:
                tr_add_limit_upload_to_hash_and_print(None, TR, torrent, 0)

    # 步骤3.开始标记,多个种子请求一次 API 效率更高
    print(f"{now()}步骤3.开始添加标记...")
    #  获取已经被删除源文件的种子
    if DOWNLOAD_DIRS and len(DOWNLOAD_DIRS) > 0:
        downloaded_all_video_files = set()  # 实际存在的所有文件
        for item in DOWNLOAD_DIRS:
            script_path_dir = item[0]
            if os.path.exists(script_path_dir):
                for root, dirs, files in os.walk(script_path_dir):
                    for file in files:
                        file_mirror_path = os.path.join(root, file)
                        # if '@eaDir' not in file_mirror_path:
                        if is_effective_file_in_down(file_mirror_path):
                            downloaded_all_video_files.add(
                                convert_script_download_mirror_to_real_path(file_mirror_path))
        # 做种文件残缺,可能是已删除或者拆包或者其他,请手动检查,qb&tr 种子中的文件集合减去实际存在的文件

        if SWITCH_TRACKER_CLIENT:
            # 所有种的文件列表 - 下载目录下实际存在所有文件列表
            empty_video_files = (torrent_video_files_dirt[QB1].keys() |
                                 torrent_video_files_dirt[QB2].keys() |
                                 torrent_video_files_dirt[TR].keys()) \
                                - downloaded_all_video_files
            sorted_empty_video_files = sorted(empty_video_files, key=lambda p: p)
            qb1_TAG_EMPTY_TORRENT = set()  # 改为{torrent:[path,]}?
            qb2_TAG_EMPTY_TORRENT = set()
            tr_TAG_EMPTY_TORRENT = set()
            for file in sorted_empty_video_files:
                if file in torrent_video_files_dirt[QB1]:
                    torrents = torrent_video_files_dirt[QB1][file]
                    for torrent in torrents:
                        site_tag = cache_site_tag_hashs.get(torrent.hash, '未知站')
                        qb_add_tag_to_hash_and_print(QB1, site_tag, torrent, TAG_EMPTY_TORRENT)
                        qb1_TAG_EMPTY_TORRENT.add(f'{torrent.name} [{site_tag}]')
                        print(f'{QB1}:有做种但源文件已删除, {torrent.name} [{site_tag}], 文件:{file}')
                if file in torrent_video_files_dirt[QB2]:
                    torrents = torrent_video_files_dirt[QB2][file]
                    for torrent in torrents:
                        site_tag = cache_site_tag_hashs.get(torrent.hash, '未知站')
                        qb_add_tag_to_hash_and_print(QB2, site_tag, torrent, TAG_EMPTY_TORRENT)
                        qb2_TAG_EMPTY_TORRENT.add(f'{torrent.name} [{site_tag}]')
                        print(f'{QB2}:有做种但源文件已删除, {torrent.name} [{site_tag}], 文件:{file}')
                if file in torrent_video_files_dirt[TR]:
                    torrents = torrent_video_files_dirt[TR][file]
                    for torrent in torrents:
                        site_tag = cache_site_tag_hashs.get(torrent.hashString, '未知站')
                        tr_add_tag_to_hash_and_print(TR, site_tag, torrent, TAG_EMPTY_TORRENT)
                        tr_TAG_EMPTY_TORRENT.add(f'{torrent.name} [{site_tag}]')
                        print(f'tr:有做种但源文件已删除, {torrent.name} [{site_tag}], 文件:{file}')
            if qb1_client:
                print(
                    f'---{QB1}:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:{len(qb1_TAG_EMPTY_TORRENT)}')
                for info in qb1_TAG_EMPTY_TORRENT:
                    print(f'------{QB1}做种文件不全: {info}')
            if qb2_client:
                print(
                    f'---{QB2}:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:{len(qb2_TAG_EMPTY_TORRENT)}')
                for info in qb2_TAG_EMPTY_TORRENT:
                    print(f'------{QB2}做种文件不全: {info}')
            if tr_client:
                print(
                    f'---{TR}:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:{len(tr_TAG_EMPTY_TORRENT)}')
                for info in tr_TAG_EMPTY_TORRENT:
                    print(f'------tr做种文件不全: {info}')

        # 未做种文件打印,不区分 qb tr
        all_no_torrent_files = downloaded_all_video_files \
                               - torrent_video_files_dirt[QB1].keys() \
                               - torrent_video_files_dirt[QB2].keys() \
                               - torrent_video_files_dirt[TR].keys() \
                               - torrent_video_files_downloading_dirt[QB1].keys() \
                               - torrent_video_files_downloading_dirt[QB2].keys() \
                               - torrent_video_files_downloading_dirt[TR].keys()
        left_video_files = []
        # 去除下载中文件,去除小文件
        for file in all_no_torrent_files:
            if file.endswith('.!qB') or file.endswith('.parts') or file.endswith('.DS_Store'):
                continue
            if '@eaDir' in file:
                continue
            if is_effective_file(file):
                left_video_files.append(file)
        sorted_left_video_files = sorted(left_video_files, key=lambda p: p)
        print(
            f"---下载目录下未做种文件(去除冗余小文件)共{len(sorted_left_video_files)}个: {len(downloaded_all_video_files)}(所有下载目录文件数,包含冗余小文件) - {len(torrent_video_files_dirt[QB1].keys()) + len(torrent_video_files_dirt[QB2].keys()) + len(torrent_video_files_dirt[TR].keys()) + len(torrent_video_files_downloading_dirt[QB1].keys()) + len(torrent_video_files_downloading_dirt[QB2].keys()) + len(torrent_video_files_downloading_dirt[TR].keys())}(做种文件数) = {len(sorted_left_video_files)}")
        if SWITCH_PRINT_NOT_UPLOAD_FILE:
            all_file_size = 0
            for file in sorted_left_video_files:
                all_file_size += os.path.getsize(file)
                print(f'------未做种文件:{file}')
            print(f'------未做种文件共 {readable_file_size(all_file_size)}')

    if EMBY_PARENT_DIRS and len(EMBY_PARENT_DIRS) > 0:
        if SWITCH_PRING_NOT_TORRENT:
            print('---开始打印媒体库下未做种文件')
            for dir in EMBY_PARENT_DIRS:
                if os.path.exists(dir):
                    print_no_link_internal_in_emby(dir)
        if SWITCH_PRING_MULTY_VIDEO_FILE:
            print('---开始打印媒体库下重复版本视频文件')
            for dir in EMBY_PARENT_DIRS:
                if os.path.exists(dir):
                    print_mulity_video_file_internal_in_emby(dir)

    # 打印辅种个数,按重复个数排序后的
    if PRINT_COPY_COUNT < 1000:
        print(
            f"---共{len(dirt_content_path_values)}个原始种子, {QB1}共做种{len(qb1_sorted_torrents_infos)}个, {QB2}共做种{len(qb2_sorted_torrents_infos)}个, {TR}共做种{len(tr_sorted_torrents_infos)}个, 开始打印辅种数高于{PRINT_COPY_COUNT}的种子:")
        sorted_dirt_content_path_values \
            = sorted(dirt_content_path_values.items(), key=lambda x: x[1][0], reverse=True)
        more_than_PRINT_COPY_COUNT_count = 0
        for content_path, e in sorted_dirt_content_path_values:
            copy_count = e[0]  # 总辅种个数
            # all_torrent_tags = e[1]  # 所有辅种的 标签 合集
            file_size = e[2]  # 种子对应文件大小
            # has_link = e[3]  # 视频文件是否已硬链接
            torrent_name = e[4]  # 种子 name
            if copy_count < PRINT_COPY_COUNT:
                break
            readable_size = readable_file_size(file_size)
            print(f"{copy_count} 个辅种 | {torrent_name} | {readable_size}")
            more_than_PRINT_COPY_COUNT_count += 1
        print(f"辅种数大于{PRINT_COPY_COUNT}原始种子共{more_than_PRINT_COPY_COUNT_count}个。")

    # 将上次 tag 全部清理, 重新标记
    print('---开始给下载器添加标签')
    if qb1_client:
        qb_old_tags = qb1_client.torrent_tags.tags.data
        qb1_to_remove_old_tags = [s for s in qb_old_tags if s.startswith('F-')]
        if SWITCH_REAL_INVOKE:
            qb1_client.torrents_delete_tags(qb1_to_remove_old_tags)
        if DEBUG_LOG:
            print(f"{prefix()}{QB1} 删除所有旧标签重新标记, {qb1_to_remove_old_tags}")
    if qb2_client:
        qb_old_tags = qb2_client.torrent_tags.tags.data
        qb2_to_remove_old_tags = [s for s in qb_old_tags if s.startswith('F-')]
        if SWITCH_REAL_INVOKE:
            qb2_client.torrents_delete_tags(qb2_to_remove_old_tags)
        if DEBUG_LOG:
            print(f"{prefix()}{QB2} 删除所有旧标签重新标记, {qb2_to_remove_old_tags}")
    if tr_client:
        if DEBUG_LOG:
            print(f"{prefix()}{TR} 删除所有旧标签重新标记, {tr_to_remove_old_tags}")

    total_file_size = 0
    for size in file_size_LIMIT_TO_DELETE_THRESHOLD.values():
        total_file_size += size
    if SWITCH_TORRENT_COUNT_CLIENT:
        print('---开始标记辅种个数')
        print(f"{prefix()}标记辅种数小于等于{LIMIT_TO_DELETE_THRESHOLD} "
              f"文件体积共{readable_file_size(total_file_size)}, "
              f"辅种体积共{readable_file_size(file_torrent_size_LIMIT_TO_DELETE_THRESHOLD)}"
              f"(关联这些标签的种子未计算:{EXCLUDE_CONTAINS_STATIONS})")
        for i in range(1, LIMIT_TO_DELETE_THRESHOLD + 1):
            add_tags(TAG_COPY_COUNT % i)

    if SWITCH_FILE_SUFFIX_CLIENT:
        print('---开始标记ISO、ts文件类型')
        add_tags(TAG_ISO)
        add_tags(TAG_TS)
        add_tags(TAG_M2TS)

    if SWITCH_TRACKER_CLIENT:
        print('---开始标记异常 tracker 状态')
        add_tags(TAG_TORRENT_ERROR1)
        add_tags(TAG_TORRENT_ERROR2)
        add_tags(TAG_NO_WORKING_TRACKER1)
        add_tags(TAG_NO_WORKING_TRACKER2)
        add_tags(TAG_TRACKERS_CLIENT_NOT_WHITE1)
        add_tags(TAG_TRACKERS_CLIENT_NOT_WHITE2)

        add_tags(TAG_EMPTY_TORRENT)

    if SWITCH_TAG_ROOT_PATH_CLIENT:
        print('---开始标记所在根目录')
        for item in DOWNLOAD_DIRS:
            script_path_dir = item[0]
            add_tags(f'F-{get_root_parent_dir(script_path_dir)}')
    if SWITCH_EMBY_CLIENT:
        print('---开始标记已入库、未入库、长期保种')
        add_tags(TAG_IN_EMBY)
        add_tags(TAG_NOT_IN_EMBY)
        add_tags(TAG_LONG_KEEP)
    # 是否在 tr 辅种
    if SWITCH_MARK_IN_TR_OR_QB12:
        print(f'---开始标记是否在 {QB1}/{QB2}/{TR} 跨端辅种')
        add_tags(TAG_IN_QB1)
        add_tags(TAG_IN_QB2)
        add_tags(TAG_IN_TR)
    # 更新站点标签
    print('---开始标记站点标签')
    for to_add_site_tag in to_add_site_tags:
        add_tags(to_add_site_tag)
    if SWITCH_LIMIT_CLIENT:
        print(f'---开始对站点种子设置限速,限速配置见UOLOAD_LIMIT_SITE')
        set_limit()

    specific_process_tr_tags()

    # 停止所有任务
    # qbt_client.torrents.stop.all()

    # 退出登录
    if qb1_client:
        qb1_client.auth_log_out()
    if qb2_client:
        qb2_client.auth_log_out()
    cost = time.time() - start
    print(f"---SUCCESS 标记完成,耗时: {int(cost)}s")
