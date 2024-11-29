#!/usr/bin/env python
# 使用前安装qb依赖库: python -m pip install qbittorrent-api
# 使用前安装tr依赖库: pip install transmission-rpc -U
# 脚本依赖标签中有站点名称,需要先执行一遍 mp插件<下载任务分类与标签>(勾选 自动站点标签 补全下载历史的标签与分类(一次性任务))
# -------以下为配置开关-----
# -------以下为配置开关-----
# -------以下为配置开关-----
# 是否真执行qb标签等, false时只打印模拟不生效
SWITCH_REAL_INVOKE = True
# 是否增加F-已入库\F-未入库标签\F-长期, 只有在 nas 上执行才能生效,因为本质是判断硬链接个数
SWITCH_EMBY = True
TAG_IN_EMBY = 'F-入库'
TAG_NOT_IN_EMBY = 'F-未入库'
TAG_LONG_KEEP = 'F-长期'
# 辅种个数标记开关
SWITCH_TORRENT_COUNT = True
# 排除这些站点标签, 只要辅种站点中含有这些站, 就取消该文件所有种子的标记,应对某个站正在考核\长期保种场景
EXCLUDE_CONTAINS_STATIONS = {"海豹", "海棠", TAG_LONG_KEEP, "KEEP", "待删"}
LIMIT_TO_DELETE_THRESHOLD = 30  # <= x 的会标记, (<=1 就是单站辅种)
LIMIT_TO_LONG_KEEP_THRESHOLD = 15  # >= x 的会 一起标记 TAG_LONG_KEEP
PRINT_COPY_COUNT = 100  # 只会打印输出辅种数高于此值的种, >= 1000时不再打印
# 是否增加F-ISO\F-TS\F-m2TS文件类型标记
SWITCH_FILE_SUFFIX = True
# 是否增加tracker 异常状态标记,无辅种的可以连源文件一起删除
SWITCH_TRACKER = True
# 是否对某站种子上传限速,设置到种子粒度
SWITCH_LIMIT = True
_10K = 10240
_100K = 102400
_1M = 1024 * 1024
_2M = _1M * 2
QB_UOLOAD_LIMIT_SITE = {'红豆饭': _100K, '柠檬': _100K, '麒麟': _100K, '青蛙': _100K, '朱雀': _100K,
                        'CARPT': _100K, 'UBits': _100K}
TR_UOLOAD_LIMIT_SITE = QB_UOLOAD_LIMIT_SITE
# 是否打印没有做种的文件列表
SWITCH_PRINT_NOT_UPLOAD_FILE = True
download_parent_dirs = {  # 下载根目录,多个盘写多个
    '/volume2/video/Downloads/qBittorrent',
    '/volume4/video4/Downloads/qBittorrent'}
# 是否打印emby 等媒体库下没做种的视频文件
SWITCH_PRING_NOT_TORRENT = True
# 是否打印媒体库下重复的不同清晰度视频文件
SWITCH_PRING_MULTY_VIDEO_FILE = True
media_parent_dirs = {  # 媒体根目录,多个盘写多个
    '/volume2/video/link',
    '/volume4/video4/link'}
# 是否标记源文件同时在qb\tr做种的种子,会添加标签 F-辅种tr\F-辅种qb
SWITCH_MARK_IN_TR_OR_QB = True
# 是否打印 debug 详细信息
DEBUG_LOG = not SWITCH_REAL_INVOKE


# 这些文件夹路径中的种子长期保种
def condition_to_long_keep(content_path):
    return "DouBan.2021.11.11.Top.250.BluRay" in content_path \
           or "成龙电影合集" in content_path \
           or "斯皮尔伯格作品合集" in content_path \
           or "周星驰.Stephen.Chow.1988-2017" in content_path \
           or "冰与火之歌S01-S08" in content_path \
           or "绝命毒师S01-S05." in content_path


# -------以上为配置开关------
# -------以上为配置开关------
# -------以上为配置开关------

SERVER_HOST = "192.168.1.111"
QB_CONN_INFO = dict(
    host=SERVER_HOST,
    port=8085,
    username="xxx",
    password="xx",
)
# qb下载映射路径:下载真实路径，可以写多个，结尾不包含/
QB_DOWNLOAD_PATH_MIRRORS = {}
TR_CONN_INFO = dict(
    protocol='http',
    host=SERVER_HOST,
    port=9091,
    username="xxx",
    password="xx",
)
# tr下载映射路径:下载真实路径，可以写多个，结尾不包含/
TR_DOWNLOAD_PATH_MIRRORS = {}

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
TAG_IN_TR = 'F-辅种tr'
TAG_IN_QB = 'F-辅种qb'

# todo 画质,未完成
SWITCH_TAG_DOLBY = False  # .dolby 文件标记开关
TAG_DOLBY = 'F-dolby'  # .dolby 文件标记

import datetime
import os
import socket
import time
import qbittorrentapi
from qbittorrentapi import TrackerStatus
# tr
from transmission_rpc.client import Client


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


QB = 'qb'
TR = 'tr'
# hashs = {'qb': {'tag1': set(), 'tag2': set()}, 'tr': {同左侧}}
hashs_to_add_tag = {QB: {}, TR: {}}
# {hash,tags}
# 然后将 tags 排序后转成{tags,set = hashs}
tr_hash_tags = {}
# hashs = {'qb': {'y-0': set(), 'y-1024': set()}, 'tr': {同左侧}
hashs_to_limit_upload = {QB: {}, TR: {}}


def qb_add_tag_to_hash_and_print(qb_or_tr, torrent, tag_name):
    add_tag_to_hash_and_print_internal(qb_or_tr, torrent.hash,
                                       torrent.name, torrent.tags, tag_name)


def tr_add_tag_to_hash_and_print(qb_or_tr, torrent, tag_name):
    # tr 加额外处理
    if torrent.hashString not in tr_hash_tags:
        tr_hash_tags[torrent.hashString] = set()
    tr_hash_tags[torrent.hashString].add(tag_name)
    add_tag_to_hash_and_print_internal(qb_or_tr, torrent.hashString,
                                       torrent.name, torrent.labels, tag_name)


def add_tag_to_hash_and_print_internal(qb_or_tr, hash, name, tags, tag_name):
    hashs_qb_or_tr = hashs_to_add_tag[qb_or_tr]
    if tag_name not in hashs_qb_or_tr:
        hashs_qb_or_tr[tag_name] = set()
    hashs_qb_or_tr[tag_name].add(hash)
    if DEBUG_LOG:
        print(f"{qb_or_tr}:增加标签 ({tag_name}), {name} {tags}")


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
            f"{qb_or_tr}:命中限速站点({site},{readable_file_size(limit_speed, False)}) {name},{tags}")


def set_limit():
    # hashs = {'qb': {'0': set(), '1024': set()}, 'tr': {同左侧}
    qb_hashs_to_limit_upload = hashs_to_limit_upload[QB]
    for limit_speed, hashs in qb_hashs_to_limit_upload.items():
        if SWITCH_REAL_INVOKE:
            qb_client.torrents_set_upload_limit(limit_speed, hashs)
            if limit_speed > 0:
                qb_client.torrents_add_tags(f"F-{readable_file_size(limit_speed, False)}", hashs)
        if limit_speed > 0:
            print(f"{prefix()}qb 限速({readable_file_size(limit_speed, False)})种子个数: {len(hashs)}")
        else:
            print(f"{prefix()}qb 不限速种子个数: {len(hashs)}")
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
    # 处理 qb
    qb_hashs_to_add_tag = hashs_to_add_tag[QB]
    if tag in qb_hashs_to_add_tag:
        tag_hash = qb_hashs_to_add_tag[tag]
    else:
        tag_hash = None
    if tag_hash and len(tag_hash) > 0:
        if SWITCH_REAL_INVOKE:
            qb_client.torrents_add_tags(tag, tag_hash)
        print(f"{prefix()}qb 标记 \"{tag}\" 种子个数: {len(tag_hash)}, (请 qb 中筛选标签查看)")
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
        print(f"{prefix()}tr 标记 \"{tag}\" 种子个数: {len(tag_hash)}, (请 tr 中筛选标签查看)")
    else:
        pass
        # print(f"{prefix()}tr 标记 \"{tag}\" 种子个数: 0")


def remove_tags(tags, hashs):
    prefix = ''
    if not SWITCH_REAL_INVOKE:
        prefix = '(模拟)'
    if len(hashs) > 0:
        if SWITCH_REAL_INVOKE:
            qb_client.torrents_remove_tags(tags, hashs)
        print(f"{prefix}qb 清理标记 \"{tags}\" 种子个数: {len(hashs)}")
    else:
        print(f"{prefix}qb 清理标记 \"{tags}\" 种子个数: 0")


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


video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.3gp', '.ts', '.m2ts', '.avi',
                    '.flac', '.mp3', '.test',
                    '.iso', '.rmvb', '.rm', '.mpeg', '.mpg', '.asf', '.m4v', '.f4v', '.strm', '.tp']

no_effective_extensions = ['.png', '.PNG', '.jpg', '.JPG', '.nfo', '.DS_Store', '.ass', '.xml']


def is_effective_file(file_path):
    file_extension = os.path.splitext(file_path)[1]
    return file_extension not in no_effective_extensions


def get_hard_link_count(file_path):
    try:
        # 获取文件的状态信息
        file_stat = os.stat(file_path)
        # 返回硬链接个数
        return file_stat.st_nlink
    except FileNotFoundError:
        return "文件不存在"


def has_linked_video_file(folder_path) -> bool:
    # 方案一: 寻找一个种子内视频文件路径,判断硬链接个数 (不行,这是 api 调用, 文件路径在服务端)
    # 方案二(不行): 判断同时包含 2 个标签,(不行, 有些辅种的不包含MOVIEPILOT, 而已整理的不一定都入库了(入库失败 & 辅种瞎标记))
    # has_into_emby = all(item in torrent.tags.split(',') for item in ['MOVIEPILOT', '已整理'])
    if os.path.isfile(folder_path):
        file_abs_path = folder_path
        if is_effective_file(file_abs_path):
            link_count = get_hard_link_count(file_abs_path)
            if link_count > 1:
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
        return False
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_abs_path = os.path.join(root, file)
            if is_effective_file(file_abs_path):
                link_count = get_hard_link_count(file_abs_path)
                if link_count > 1:
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
    return False


def specific_process_tr_tags():
    if tr_client:
        # {hash,tags}
        # 然后将 tags 排序后转成{tags,list = hashs}
        tr_tags_hash2 = {}
        for hash, tags in tr_hash_tags.items():
            sorted_tags_tuple = tuple(sorted(tags, reverse=False))
            # sorted_tags =  sorted(tags, key=lambda p: p)
            if sorted_tags_tuple not in tr_tags_hash2:
                tr_tags_hash2[sorted_tags_tuple] = list()
            tr_tags_hash2[sorted_tags_tuple].append(hash)
        if DEBUG_LOG:
            print(f"specific_process_tr_tags:  len={len(tr_tags_hash2)},{tr_tags_hash2.keys()}")
        if SWITCH_REAL_INVOKE:
            for sorted_tags_tuple, hashs in tr_tags_hash2.items():
                tr_client.change_torrent(ids=list(hashs), labels=list(sorted_tags_tuple))


def print_no_link_internal(folder_path):
    all_file_size = 0
    dirt_file_size = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for extension in video_extensions:
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
    print(f"---{folder_path} 下所有没有做种文件总大小: {readable_file_size(all_file_size)}, 列表如下:")
    # 排序打印
    sorted_keys = sorted(dirt_file_size.keys(), key=lambda p: p)
    sorted_dict = {key: dirt_file_size[key] for key in sorted_keys}
    for path, size in sorted_dict.items():
        print(f"------没有做种:{path} | {readable_file_size(size)}")


def print_mulity_video_file_internal(directory):
    file_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            abs_paths = os.path.join(root, file)
            abs_name, ext = os.path.splitext(abs_paths)
            # 去除名字中的 1080p、2160p 等字符
            abs_name = ''.join(
                [part for part in abs_name.split() if part not in ['720p', '1080p', '2160p']])
            if ext in video_extensions:
                if abs_name in file_dict:
                    file_dict[abs_name].append(abs_paths)
                else:
                    file_dict[abs_name] = [abs_paths]
    for abs_name, files in file_dict.items():
        if len(files) > 1:
            print("-")
            for index, file in enumerate(files):
                print(file)
                # 删除后面的
                # if index != 0:
                #     os.remove(file)


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")


# torrent.files torrent.trackers 是 api 调用,尽量减少次数
if __name__ == '__main__':
    print(
        f"{now()}当前运行主机 ip:{get_current_device_local_ip_address()}, 服务端 ip:{SERVER_HOST}, 如果不同使用目录进行分析的一些结果将不准确,推荐在 nas 主机上运行")
    start = time.time()
    # 连接信息打印
    qb_client = None
    # 尝试登录
    try:
        qb_client = qbittorrentapi.Client(**QB_CONN_INFO)
        qb_client.auth_log_in()
        print("登录qb成功...")
    except Exception as e:
        qb_client = None
        print(f"登录qb失败，错误：{e}")
    tr_client = None
    try:
        tr_client = Client(**TR_CONN_INFO)
        print("登录tr成功...")
    except Exception as e:
        print(f"登录tr失败，错误：{e}")
    if not qb_client and not tr_client:
        exit(-2)
    # 步骤1 第一遍遍历, 收集要标记的信息
    if qb_client:
        qb_sorted_torrents_infos = sorted(qb_client.torrents_info(), key=lambda x: x['name'])
    else:
        qb_sorted_torrents_infos = []
    if tr_client:
        tr_sorted_torrents_infos = sorted(tr_client.get_torrents(), key=lambda x: x.name)
    else:
        tr_sorted_torrents_infos = []
    print(f"qb:共{len(qb_sorted_torrents_infos)}个种子")
    print(f"tr:共{len(tr_sorted_torrents_infos)}个种子")

    print(f"{now()}步骤1.第一遍遍历, 收集要标记的信息...")
    # qb&tr key=save_path + torrent name,
    #       value=[0copy_count, 1all_torrent_tags, 2file_size, 3has_link, 4name, 5in qb, 6in tr]
    dirt_content_path_values = {}
    # qb&tr 中的所有视频文件-非下载中(拆出不下载文件), {'qb': {'path1': [torrent1,torrent2], 'path2': list()}, 'tr': {同左侧}}
    torrent_video_files_dirt = {QB: {}, TR: {}}
    # qb&tr 中的所有视频文件-下载中(拆出不下载文件),结构同上
    torrent_video_files_downloading_dirt = {QB: {}, TR: {}}
    # qb 数据缓存,避免多次请求 api,{hash:torrent.files}
    qb_cache_hash_files = {}
    for torrent in qb_sorted_torrents_infos:
        save_path = torrent.save_path
        for mirror, realPath in QB_DOWNLOAD_PATH_MIRRORS.items():
            if save_path.startswith(mirror):
                save_path = save_path.replace(mirror, realPath)
                break
        # files = torrent.files
        files = [file for file in torrent.files if file.priority >= 1]  # 改为只筛选待下载的
        qb_cache_hash_files[torrent.hash] = files
        if torrent.state_enum.is_downloading:
            print(f"qb下载中跳过标记: {torrent.name}")
            for file in files:
                abs_file_path = os.path.join(save_path, file.name)
                if is_effective_file(abs_file_path):
                    hashs_qb_or_tr = torrent_video_files_downloading_dirt[QB]
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
                 has_linked_video_file(content_path), torrent.name, True, False]

        for file in files:
            abs_file_path = os.path.join(save_path, file.name)
            if is_effective_file(abs_file_path):
                hashs_qb_or_tr = torrent_video_files_dirt[QB]
                if abs_file_path not in hashs_qb_or_tr:
                    hashs_qb_or_tr[abs_file_path] = list()
                hashs_qb_or_tr[abs_file_path].append(torrent)
    tr_old_tags = set()
    for torrent in tr_sorted_torrents_infos:
        save_path = torrent.download_dir
        for mirror, realPath in TR_DOWNLOAD_PATH_MIRRORS.items():
            if save_path.startswith(mirror):
                save_path = save_path.replace(mirror, realPath)
                break
        files = [file for file in torrent.get_files() if file.selected]  # 改为只筛选待下载的
        if torrent.status.downloading or torrent.status.download_pending:
            print(f"tr下载中跳过标记: {torrent.name}")
            for file in files:
                abs_file_path = os.path.join(save_path, file.name)
                if is_effective_file(abs_file_path):
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
                 has_linked_video_file(content_path), torrent.name, False, True]

        for file in files:
            abs_file_path = os.path.join(save_path, file.name)
            if is_effective_file(abs_file_path):
                hashs_qb_or_tr = torrent_video_files_dirt[TR]
                if abs_file_path not in hashs_qb_or_tr:
                    hashs_qb_or_tr[abs_file_path] = list()
                hashs_qb_or_tr[abs_file_path].append(torrent)

    # 步骤2. 第二遍遍历,标记收集完的信息
    print(f"{now()}步骤2.第二遍遍历,标记收集完的信息...")
    file_size_LIMIT_TO_DELETE_THRESHOLD = {}  # 实际体积 key=content_path,value=size
    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD = 0  # 对应辅种体积
    print(f'{now()}开始收集 qb 中待标记信息...')
    size = len(qb_sorted_torrents_infos)
    tr_to_remove_old_tags = set([s for s in tr_old_tags if s.startswith('F-')])
    TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS = TAG_LONG_KEEP in EXCLUDE_CONTAINS_STATIONS
    for index, torrent in enumerate(qb_sorted_torrents_infos):
        save_path = torrent.save_path
        for mirror, realPath in QB_DOWNLOAD_PATH_MIRRORS.items():
            if save_path.startswith(mirror):
                save_path = save_path.replace(mirror, realPath)
                break
        files = qb_cache_hash_files[torrent.hash]
        if DEBUG_LOG:
            print(f'qb:{index + 1}/{size}')
        if torrent.state_enum.is_downloading:
            print(f"qb下载中跳过标记: {torrent.name}")
            continue
        # 当前种子 tags list
        current_torrent_tag_list = [element.strip() for element in torrent.tags.split(',')]

        # e=[copy_count, all_torrent_tags, file_size, has_link]
        content_path = os.path.join(save_path, torrent.name)
        e = dirt_content_path_values[content_path]
        copy_count = e[0]  # 总辅种个数
        all_torrent_tags = e[1]  # 所有辅种的 标签 合集
        file_size = e[2]  # 种子对应文件大小
        has_link = e[3]  # 视频文件是否已硬链接
        name = e[4]  # 种子 name
        in_tr = e[6]  # 是否有 tr 辅种

        # 是否入了媒体库(有硬链接等于入了媒体库),用其中一个视频文件路径判断
        torrent_long_keep = False
        if SWITCH_EMBY:
            if has_link:
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_IN_EMBY)
            else:
                if "KEEP" not in current_torrent_tag_list:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_NOT_IN_EMBY)
            if condition_to_long_keep(content_path):
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_LONG_KEEP)
                torrent_long_keep = True

        # 辅种个数标记
        if SWITCH_TORRENT_COUNT:
            # 辅种小于 x 标记
            if copy_count <= LIMIT_TO_DELETE_THRESHOLD:
                # 先排除部分站点-两个列表没有交集
                intersection = EXCLUDE_CONTAINS_STATIONS.intersection(all_torrent_tags)
                siwtchLoneKeep_and_hit = TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS and torrent_long_keep
                if not intersection and not siwtchLoneKeep_and_hit:
                    tag = TAG_COPY_COUNT % copy_count
                    qb_add_tag_to_hash_and_print(QB, torrent, tag)
                    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD += file_size
                    if content_path not in file_size_LIMIT_TO_DELETE_THRESHOLD:
                        file_size_LIMIT_TO_DELETE_THRESHOLD[content_path] = file_size
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"qb:未添加辅种数标记, 标签中(包含关联辅种)存在{intersection} {torrent.name}, {torrent.tags}")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"qb:未添加辅种数标记, 标签中(包含关联辅种)存在{TAG_LONG_KEEP} {torrent.name}, {torrent.tags}")
            if copy_count >= LIMIT_TO_LONG_KEEP_THRESHOLD:
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_LONG_KEEP)

        # 文件类型标记
        if SWITCH_FILE_SUFFIX:
            if torrent_files_contains(files, '.iso'):
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_ISO)
            elif torrent_files_contains(files, '.ts'):
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_TS)
            elif torrent_files_contains(files, '.m2ts'):
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_M2TS)

        # tracker 标记
        if SWITCH_TRACKER:
            # 没有正在工作的 tracker
            trackers = torrent.trackers
            working_trackers = [tracker for tracker in trackers if
                                tracker.status != TrackerStatus.DISABLED]
            if len(working_trackers) == 0:
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_NO_WORKING_TRACKER1)
                else:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_NO_WORKING_TRACKER2)
            # elif trackers_only_msg(trackers, 'Bad Gateway'):
            #     if copy_count > 1:
            #         qb_add_tag_to_hash_and_print(QB, torrent, TAG_TRACKERS_ONLY_Bad_Gateway1)
            #     else:
            #         qb_add_tag_to_hash_and_print(QB, torrent, TAG_TRACKERS_ONLY_Bad_Gateway2)
            elif qb_trackers_only_msg(trackers, 'orrent not registered') \
                    or qb_trackers_only_msg(trackers, 'Unregistered torrent') \
                    or qb_trackers_only_msg(trackers, 'orrent not exists') \
                    or qb_trackers_only_msg(trackers, 'orrent banned') \
                    or qb_trackers_only_msg(trackers, 'orrent delete') \
                    or qb_trackers_only_msg(trackers, '被删除'):
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_TORRENT_ERROR1)
                else:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_TORRENT_ERROR2)
            elif qb_trackers_only_msg(trackers, 'client is not on the whitelist'):
                if copy_count > 1:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_TRACKERS_CLIENT_NOT_WHITE1)
                else:
                    qb_add_tag_to_hash_and_print(QB, torrent, TAG_TRACKERS_CLIENT_NOT_WHITE2)

        # 是否在 tr 辅种
        if SWITCH_MARK_IN_TR_OR_QB:
            if in_tr:
                qb_add_tag_to_hash_and_print(QB, torrent, TAG_IN_TR)
        # 标记限速种子
        if SWITCH_LIMIT:
            intersection = set(QB_UOLOAD_LIMIT_SITE).intersection(current_torrent_tag_list)
            if intersection:  # 理论上标签应该只有 1 个交集,就是站点名称,所以取 0
                site = list(intersection)[0]
                limit_speed = QB_UOLOAD_LIMIT_SITE[site]
                qb_add_limit_upload_to_hash_and_print(site, QB, torrent, limit_speed)
            else:
                qb_add_limit_upload_to_hash_and_print(None, QB, torrent, 0)

    print(f'{now()}开始收集 tr 中待标记信息...')
    size = len(tr_sorted_torrents_infos)
    for index, torrent in enumerate(tr_sorted_torrents_infos):
        if DEBUG_LOG:
            print(f'tr:{index + 1}/{size}')
        if torrent.status.downloading or torrent.status.download_pending:
            print(f"tr下载中跳过标记: {torrent.name}")
            continue
        files = [file for file in torrent.get_files() if file.selected]  # 改为只筛选待下载的
        # 当前种子 tags list
        current_torrent_tag_list = [element.strip() for element in torrent.labels]
        tr_hash_tags[torrent.hashString] = set(current_torrent_tag_list) - tr_to_remove_old_tags
        save_path = torrent.download_dir
        for mirror, realPath in TR_DOWNLOAD_PATH_MIRRORS.items():
            if save_path.startswith(mirror):
                save_path = save_path.replace(mirror, realPath)
                break
        content_path = os.path.join(save_path, torrent.name)  # str
        # e=[copy_count, all_torrent_tags, file_size, has_link]
        e = dirt_content_path_values[content_path]
        copy_count = e[0]  # 总辅种个数
        all_torrent_tags = e[1]  # 所有辅种的 标签 合集
        file_size = e[2]  # 种子对应文件大小
        has_link = e[3]  # 视频文件是否已硬链接
        name = e[4]  # 种子 name
        in_qb = e[5]  # 是否有 qb 辅种

        # 是否入了媒体库(有硬链接等于入了媒体库),用其中一个视频文件路径判断
        torrent_long_keep = False
        if SWITCH_EMBY:
            if "KEEP" not in current_torrent_tag_list:
                if has_link:
                    tr_add_tag_to_hash_and_print(TR, torrent, TAG_IN_EMBY)
                else:
                    tr_add_tag_to_hash_and_print(TR, torrent, TAG_NOT_IN_EMBY)

            if condition_to_long_keep(content_path):
                # tr_add_tag_to_hash_and_print(TR, torrent, TAG_LONG_KEEP) tr 不用这个标签,都是长期的
                torrent_long_keep = True

        # 辅种个数标记
        if SWITCH_TORRENT_COUNT:
            # 辅种小于 x 标记
            if copy_count <= LIMIT_TO_DELETE_THRESHOLD:
                # 先排除部分站点-两个列表没有交集
                intersection = EXCLUDE_CONTAINS_STATIONS.intersection(all_torrent_tags)
                siwtchLoneKeep_and_hit = TAG_LONG_KEEP_in_EXCLUDE_CONTAINS_STATIONS and torrent_long_keep
                if not intersection and not siwtchLoneKeep_and_hit:
                    tag = TAG_COPY_COUNT % copy_count
                    tr_add_tag_to_hash_and_print(TR, torrent, tag)
                    file_torrent_size_LIMIT_TO_DELETE_THRESHOLD += file_size
                    if content_path not in file_size_LIMIT_TO_DELETE_THRESHOLD:
                        file_size_LIMIT_TO_DELETE_THRESHOLD[content_path] = file_size
                else:
                    if DEBUG_LOG:
                        if intersection:
                            print(
                                f"tr:未添加辅种数标记, 标签中(包含关联辅种)存在{intersection} {torrent.name}, {current_torrent_tag_list}")
                        elif siwtchLoneKeep_and_hit:
                            print(
                                f"tr:未添加辅种数标记, 标签中(包含关联辅种)存在{TAG_LONG_KEEP} {torrent.name}, {current_torrent_tag_list}")

        # 文件类型标记
        if SWITCH_FILE_SUFFIX:
            if torrent_files_contains(files, '.iso'):
                tr_add_tag_to_hash_and_print(TR, torrent, TAG_ISO)
            elif torrent_files_contains(files, '.ts'):
                tr_add_tag_to_hash_and_print(TR, torrent, TAG_TS)
            elif torrent_files_contains(files, '.m2ts'):
                tr_add_tag_to_hash_and_print(TR, torrent, TAG_M2TS)

        # tracker 标记 (TR tracker 标记不太重要)
        if SWITCH_TRACKER:
            # 没有正在工作的 tracker
            trackers = torrent.tracker_stats
            # elif trackers_only_msg(trackers, 'Bad Gateway'):
            #     if copy_count > 1:
            #         qb_add_tag_to_hash_and_print(QB, torrent, TAG_TRACKERS_ONLY_Bad_Gateway1)
            #     else:
            #         qb_add_tag_to_hash_and_print(QB, torrent, TAG_TRACKERS_ONLY_Bad_Gateway2)
            if tr_trackers_only_msg(trackers, 'orrent not registered') \
                    or tr_trackers_only_msg(trackers, 'Unregistered torrent') \
                    or tr_trackers_only_msg(trackers, 'orrent not exists') \
                    or tr_trackers_only_msg(trackers, 'orrent banned') \
                    or tr_trackers_only_msg(trackers, 'orrent delete') \
                    or tr_trackers_only_msg(trackers, '被删除'):
                if copy_count > 1:
                    tr_add_tag_to_hash_and_print(TR, torrent, TAG_TORRENT_ERROR1)
                else:
                    tr_add_tag_to_hash_and_print(TR, torrent, TAG_TORRENT_ERROR2)
            elif tr_trackers_only_msg(trackers, 'client is not on the whitelist'):
                if copy_count > 1:
                    tr_add_tag_to_hash_and_print(TR, torrent, TAG_TRACKERS_CLIENT_NOT_WHITE1)
                else:
                    tr_add_tag_to_hash_and_print(TR, torrent, TAG_TRACKERS_CLIENT_NOT_WHITE2)

        # 是否在 qb 辅种
        if SWITCH_MARK_IN_TR_OR_QB:
            if in_qb:
                tr_add_tag_to_hash_and_print(TR, torrent, TAG_IN_QB)
        # 标记限速种子
        if SWITCH_LIMIT:
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
    if download_parent_dirs and len(download_parent_dirs) > 0:
        downloaded_all_video_files = set()  # 实际存在的所有文件
        for d in download_parent_dirs:
            for root, dirs, files in os.walk(d):
                for file in files:
                    file_abs_path = os.path.join(root, file)
                    if '@eaDir' not in file_abs_path:
                        if is_effective_file(file_abs_path):
                            downloaded_all_video_files.add(file_abs_path)
        # 做种文件残缺,可能是已删除或者拆包或者其他,请手动检查,qb&tr 种子中的文件集合减去实际存在的文件

        if SWITCH_TRACKER:
            empty_video_files = (torrent_video_files_dirt[QB].keys() | torrent_video_files_dirt[
                TR].keys()) - downloaded_all_video_files
            sorted_empty_video_files = sorted(empty_video_files, key=lambda p: p)
            qb_TAG_EMPTY_TORRENT = set()
            tr_TAG_EMPTY_TORRENT = set()
            for file in sorted_empty_video_files:
                if file in torrent_video_files_dirt[QB]:
                    torrents = torrent_video_files_dirt[QB][file]
                    for torrent in torrents:
                        qb_add_tag_to_hash_and_print(QB, torrent, TAG_EMPTY_TORRENT)
                        qb_TAG_EMPTY_TORRENT.add(f'{torrent.name} {torrent.tags}')
                        if (DEBUG_LOG):
                            print(f'qb:有做种但源文件已删除, {torrent.name} {torrent.tags}, 文件:{file}')
                if file in torrent_video_files_dirt[TR]:
                    torrents = torrent_video_files_dirt[TR][file]
                    for torrent in torrents:
                        tr_add_tag_to_hash_and_print(TR, torrent, TAG_EMPTY_TORRENT)
                        tr_TAG_EMPTY_TORRENT.add(f'{torrent.name} {torrent.labels}')
                        if (DEBUG_LOG):
                            print(f'tr:有做种但源文件已删除, {torrent.name} {torrent.labels}, 文件:{file}')
            print(
                f'---qb:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:{len(qb_TAG_EMPTY_TORRENT)}')
            for info in qb_TAG_EMPTY_TORRENT:
                print(f'------qb做种文件不全: {info}')
            print(
                f'---tr:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:{len(tr_TAG_EMPTY_TORRENT)}')
            for info in tr_TAG_EMPTY_TORRENT:
                print(f'------tr做种文件不全: {info}')

        # 未做种文件打印,不区分 qb tr
        left_video_files = downloaded_all_video_files \
                           - torrent_video_files_dirt[QB].keys() \
                           - torrent_video_files_dirt[TR].keys() \
                           - torrent_video_files_downloading_dirt[QB].keys() \
                           - torrent_video_files_downloading_dirt[TR].keys()
        # 去除下载中文件
        left_video_files = [file for file in left_video_files if not (file.endswith('.!qB')
                                                                      or file.endswith('.parts')
                                                                      or file.endswith('.DS_Store'))]

        sorted_left_video_files = sorted(left_video_files, key=lambda p: p)
        print(
            f"---未做种文件共{len(sorted_left_video_files)}个: {len(downloaded_all_video_files)}(所有下载目录文件数) - {len(torrent_video_files_dirt[QB].keys()) + len(torrent_video_files_dirt[TR].keys()) + len(torrent_video_files_downloading_dirt[QB].keys()) + len(torrent_video_files_downloading_dirt[TR].keys())}(做种文件数) = {len(sorted_left_video_files)}")
        if SWITCH_PRINT_NOT_UPLOAD_FILE:
            for file in sorted_left_video_files:
                print(f'------未做种文件:{file}')

    if media_parent_dirs and len(media_parent_dirs) > 0:
        if SWITCH_PRING_NOT_TORRENT:
            print('---开始打印媒体库下未做种文件')
            for dir in media_parent_dirs:
                print_no_link_internal(dir)
        if SWITCH_PRING_MULTY_VIDEO_FILE:
            print('---开始打印媒体库下重复版本视频文件')
            for dir in media_parent_dirs:
                print_mulity_video_file_internal(dir)

    # 打印辅种个数,按重复个数排序后的
    if PRINT_COPY_COUNT < 1000:
        print(
            f"---共{len(dirt_content_path_values)}个原始种子, qb共做种{len(qb_sorted_torrents_infos)}个, tr共做种{len(tr_sorted_torrents_infos)}个, 开始打印辅种数高于{PRINT_COPY_COUNT}的种子:")
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
    if qb_client:
        qb_old_tags = qb_client.torrent_tags.tags.data
        qb_to_remove_old_tags = [s for s in qb_old_tags if s.startswith('F-')]
        if SWITCH_REAL_INVOKE:
            qb_client.torrents_delete_tags(qb_to_remove_old_tags)
        if DEBUG_LOG:
            print(f"{prefix()}qb 删除所有旧标签重新标记, {qb_to_remove_old_tags}")
    if tr_client:
        if DEBUG_LOG:
            print(f"{prefix()}tr 删除所有旧标签重新标记, {tr_to_remove_old_tags}")

    total_file_size = 0
    for size in file_size_LIMIT_TO_DELETE_THRESHOLD.values():
        total_file_size += size
    if SWITCH_TORRENT_COUNT:
        print(f"{prefix()}标记辅种数小于等于{LIMIT_TO_DELETE_THRESHOLD} "
              f"文件体积共{readable_file_size(total_file_size)}, "
              f"辅种体积共{readable_file_size(file_torrent_size_LIMIT_TO_DELETE_THRESHOLD)}")
        for i in range(1, LIMIT_TO_DELETE_THRESHOLD + 1):
            add_tags(TAG_COPY_COUNT % i)

    if SWITCH_FILE_SUFFIX:
        add_tags(TAG_ISO)
        add_tags(TAG_TS)
        add_tags(TAG_M2TS)

    if SWITCH_TRACKER:
        add_tags(TAG_TORRENT_ERROR1)
        add_tags(TAG_TORRENT_ERROR2)
        add_tags(TAG_NO_WORKING_TRACKER1)
        add_tags(TAG_NO_WORKING_TRACKER2)
        add_tags(TAG_TRACKERS_CLIENT_NOT_WHITE1)
        add_tags(TAG_TRACKERS_CLIENT_NOT_WHITE2)

        add_tags(TAG_EMPTY_TORRENT)

    if SWITCH_EMBY:
        add_tags(TAG_IN_EMBY)
        add_tags(TAG_NOT_IN_EMBY)
        add_tags(TAG_LONG_KEEP)
        # remove_tags('已整理', hashs_to_add_TAG_NOT_IN_EMBY)
    # 是否在 tr 辅种
    if SWITCH_MARK_IN_TR_OR_QB:
        add_tags(TAG_IN_QB)
        add_tags(TAG_IN_TR)
    if SWITCH_LIMIT:
        print('---开始对站点种子设置限速')
        set_limit()

    specific_process_tr_tags()

    # 停止所有任务
    # qbt_client.torrents.stop.all()

    # 退出登录
    if qb_client:
        qb_client.auth_log_out()
    cost = time.time() - start
    print(f"---SUCCESS 标记完成,耗时: {int(cost)}s")
