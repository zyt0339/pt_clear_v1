#!/usr/bin/env python
from urllib.parse import urlparse

from qbittorrentapi import TrackerStatus
_10K = 10240
_100K = 102400
_1M = 1024 * 1024
_2M = _1M * 2
# -------以下为配置开关-----
# -------以下为配置开关-----
# -------以下为配置开关-----
SWITCH_REAL_INVOKE = True
other_remove_old_tags = []

# 是否对某站种子上传限速,设置到种子粒度,-1是解除限速
SWITCH_LIMIT = True
QB1_UOLOAD_LIMIT_SITE = {'CARPT': _10K}
QB2_UOLOAD_LIMIT_SITE = {}
TR_UOLOAD_LIMIT_SITE = QB1_UOLOAD_LIMIT_SITE
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
# -------以上为配置开关------
# -------以上为配置开关------
# -------以上为配置开关------
import datetime
import time

import qbittorrentapi
# tr
from transmission_rpc.client import Client


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


QB1 = 'qb1'
QB2 = 'qb2'
TR = 'tr'
# {hash,tags}
# 然后将 tags 排序后转成{tags,set = hashs}
tr_hash_tags = {}
# hashs = {'qb1': {'y-0': set(), 'y-1024': set()}, 'tr': {同左侧}, tr 单位是 k 所以这里 tr 是/1024 的
hashs_to_limit_upload = {QB1: {}, QB2: {}, TR: {}}


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
        if SWITCH_REAL_INVOKE:
            for sorted_tags_tuple, hashs in tr_tags_hash2.items():
                tr_client.change_torrent(ids=list(hashs), labels=list(sorted_tags_tuple))


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")


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
            # if limit_speed > 0:
            #     qb1_client.torrents_add_tags(f"F-{readable_file_size(limit_speed, False)}", hashs)
        if limit_speed > 0:
            print(f"{prefix()}{QB1} 限速({readable_file_size(limit_speed, False)})种子个数: {len(hashs)}")
        else:
            print(f"{prefix()}{QB1} 不限速种子个数: {len(hashs)}")
    qb2_hashs_to_limit_upload = hashs_to_limit_upload[QB2]
    for limit_speed, hashs in qb2_hashs_to_limit_upload.items():
        if SWITCH_REAL_INVOKE:
            qb2_client.torrents_set_upload_limit(limit_speed, hashs)
            # if limit_speed > 0:
            #     qb2_client.torrents_add_tags(f"F-{readable_file_size(limit_speed, False)}", hashs)
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
                # # tr tag 特殊处理
                # for hash in hashs:
                #     if hash not in tr_hash_tags:
                #         tr_hash_tags[hash] = set()
                #     tr_hash_tags[hash].add(f"F-{readable_file_size(limit_speed * 1024, False)}")
            print(
                f"{prefix()}tr 限速({readable_file_size(limit_speed * 1024, False)})种子个数: {len(hashs)}")
        else:
            if SWITCH_REAL_INVOKE:
                tr_client.change_torrent(ids=list(hashs), upload_limit=0, upload_limited=False)
            print(f"{prefix()}tr 不限速种子个数: {len(hashs)}")


def get_tracker_sites():
    return {
            "1ptba.com": "1PTBA",
            }


# torrent.files torrent.trackers 是 api 调用,尽量减少次数
if __name__ == '__main__':
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
        # _trarg = ["id", "name", "status", "labels", "hashString", "totalSize", "percentDone", "addedDate", "trackerList",
        #           "trackerStats",
        #           "leftUntilDone", "rateDownload", "rateUpload", "recheckProgress", "rateDownload", "rateUpload",
        #           "peersGettingFromUs", "peersSendingToUs", "uploadRatio", "uploadedEver", "downloadedEver", "downloadDir",
        #           "error", "errorString", "doneDate", "queuePosition", "activityDate", "trackers", "fileStats", "desiredAvailable"]
        _trarg = ["id", "name", "labels", "hashString"]
        tr_sorted_torrents_infos = sorted(tr_client.get_torrents(arguments=_trarg),
                                          key=lambda x: x.name)
    else:
        tr_sorted_torrents_infos = []

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

    tr_old_tags = set()
    for torrent in tr_sorted_torrents_infos:
        current_torrent_tag_list = [element.strip() for element in torrent.labels]
        tr_old_tags.update(current_torrent_tag_list)

    tr_to_remove_old_tags = set([s for s in tr_old_tags if s.startswith('F-')])
    tr_to_remove_old_tags.update(other_remove_old_tags)
    # ↑ tr 待删除标签收集完毕
    qb1_to_remove_yizhengli_hashs = []
    qb1_to_add_site_tag_hashs = {}  # 待补充站点标签的种子,key 站点标签名称，value hashs
    for torrent in qb1_sorted_torrents_infos:
        # qb1 如果没有 MP 标签就删除已整理标签
        current_torrent_tag_list = [element.strip() for element in torrent.tags.split(',')]
        if '已整理' in current_torrent_tag_list and 'MP' not in current_torrent_tag_list and 'MoviePilot' not in current_torrent_tag_list:
            qb1_to_remove_yizhengli_hashs.append(torrent.hash)
        # qb 补充站点标签
        intersection = all_sites.intersection(current_torrent_tag_list)
        site_tag = None
        if intersection:
            site_tag = list(intersection)[0]
        else:  # 无站点标签
            working_trackers = [tracker for tracker in torrent.trackers if
                                tracker.status != TrackerStatus.DISABLED]
            for tracker in working_trackers:
                domain = urlparse(tracker.url).netloc
                if domain in tracker_sites:
                    site_tag = tracker_sites[domain]
                    break
            # 更新站点标签
            if site_tag:
                if site_tag not in qb1_to_add_site_tag_hashs:
                    qb1_to_add_site_tag_hashs[site_tag] = list()
                qb1_to_add_site_tag_hashs[site_tag].append(torrent.hash)
            if DEBUG_LOG:
                print(f'更新站点标签 {torrent.name} {site_tag}')

        # 标记限速种子
        if SWITCH_LIMIT:
            if site_tag in QB1_UOLOAD_LIMIT_SITE:  # 理论上标签应该只有 1 个交集,就是站点名称,所以取 0
                limit_speed = QB1_UOLOAD_LIMIT_SITE[site_tag]
                qb_add_limit_upload_to_hash_and_print(site_tag, QB1, torrent, limit_speed)
            else:
                qb_add_limit_upload_to_hash_and_print(None, QB1, torrent, 0)

    for torrent in tr_sorted_torrents_infos:
        # 当前种子 tags list
        current_torrent_tag_list = [element.strip() for element in torrent.labels]
        tr_hash_tags[torrent.hashString] = set(current_torrent_tag_list) - tr_to_remove_old_tags
        # 标记限速种子
        if SWITCH_LIMIT:
            intersection = set(TR_UOLOAD_LIMIT_SITE).intersection(current_torrent_tag_list)
            if intersection:  # 理论上标签应该只有 1 个交集,就是站点名称,所以取 0
                site = list(intersection)[0]
                limit_speed = int(TR_UOLOAD_LIMIT_SITE[site] / 1024)
                tr_add_limit_upload_to_hash_and_print(site, TR, torrent, limit_speed)
            else:
                tr_add_limit_upload_to_hash_and_print(None, TR, torrent, 0)

    print(f"{prefix()}删除所有F-xx旧标签")
    # 步骤3.开始标记,多个种子请求一次 API 效率更高
    # 将上次 tag 全部清理, 重新标记
    if qb1_client:
        qb1_old_tags = qb1_client.torrent_tags.tags.data
        qb1_to_remove_old_tags = set([s for s in qb1_old_tags if s.startswith('F-')])
        qb1_to_remove_old_tags.update(other_remove_old_tags)
        if SWITCH_REAL_INVOKE:
            qb1_client.torrents_delete_tags(qb1_to_remove_old_tags)
        if DEBUG_LOG:
            print(f"{prefix()}{QB1} 删除所有旧标签, {qb1_to_remove_old_tags}")
        if SWITCH_REAL_INVOKE:
            qb1_client.torrents_remove_tags('已整理', qb1_to_remove_yizhengli_hashs)
        print(f"{prefix()}{QB1} 删除所有无 [MP]|[MoviePilot] 标签的 [已整理] 标签.")
        if qb1_to_add_site_tag_hashs:
            print(f'---{QB1} 开始标记缺少的站点标签')
            for tag, hashs in qb1_to_add_site_tag_hashs.items():
                if SWITCH_REAL_INVOKE:
                    qb1_client.torrents_add_tags(tag, hashs)
                print(f"{prefix()}{QB1} 标记 \"{tag}\" 种子个数: {len(hashs)}")
    if qb2_client:
        qb2_old_tags = qb2_client.torrent_tags.tags.data
        qb2_to_remove_old_tags = set([s for s in qb2_old_tags if s.startswith('F-')])
        # qb2_to_remove_old_tags.update(other_remove_old_tags)
        if SWITCH_REAL_INVOKE:
            qb2_client.torrents_delete_tags(qb2_to_remove_old_tags)
        if DEBUG_LOG:
            print(f"{prefix()}{QB2} 删除所有旧标签, {qb2_to_remove_old_tags}")

    if tr_client:
        if DEBUG_LOG:
            print(f"{prefix()}{TR} 删除所有旧标签, {tr_to_remove_old_tags}")

    if SWITCH_LIMIT:
        print('---开始对站点种子设置限速')
        set_limit()

    specific_process_tr_tags()

    # 退出登录
    if qb1_client:
        qb1_client.auth_log_out()
    if qb2_client:
        qb2_client.auth_log_out()
    cost = time.time() - start
    print(f"---SUCCESS ,耗时: {int(cost)}s")
