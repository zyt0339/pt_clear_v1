#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 安装 pip基础下载工具
# curl -O https://bootstrap.pypa.io/get-pip.py
# 然后再执行 python3 get-pip.py
# 成功后删掉 rm get-pip.py
# 安装依赖库:
#  pip3 install pythonping
#  pip3 install retry
#  pip3 install requests
#  pip3 install lxml_html_clean
#  pip3 install requests-html

import os
import re
import json
import subprocess
import time

from datetime import datetime

import requests
from pythonping import ping
from requests_html import HTMLSession
from retry import retry

# dns服务商 https://www.jianshu.com/p/3866055671cd
# https://zhuanlan.zhihu.com/p/246413651?utm_id=0
dnsProvider = [
    "223.5.5.5"  # 阿里
    , "223.6.6.6"  # 阿里
    , "119.29.29.29"  # 腾讯
    , "119.28.28.28"  # 腾讯
    , "182.254.118.118"  # 腾讯
    , "182.254.116.116"  # 腾讯
    , "180.76.76.76"  # 百度
    , "1.2.4.8"  # CNNIC
    , "210.2.4.8"  # CNNIC
    , "101.6.6.6"  # 清华大学 TUNA 协会 DNS 服务器
    , "114.114.114.114"  # 114DNS
    , "114.114.115.115"  # 114DNS
    , "1.1.1.1"  # Cloudflare DNS
    , "156.154.70.1"
    , "208.67.222.222"  # OpenDNS
    , "208.67.220.220"  # OpenDNS
    , "123.207.137.88"
    , "122.114.245.45"
    , "115.159.157.26"
]

HOSTS_TEMPLATE = """# Host Start
# Update time: {update_time}
{content}
# Host End"""


# 写入系统host信息
def append_host_file(append_content: str) -> None:
    hostFile = HOST_PATH
    # 拆分路径和文件名
    directory = os.path.dirname(hostFile)
    # 如果目录不存在，创建目录
    if not os.path.exists(hostFile):
        os.makedirs(directory)
        # 创建空文件
        try:
            open(hostFile, 'w').close()
            print(f"成功创建文件：{hostFile}")
        except Exception as e:
            print(f"创建文件时出错：{e}")

    origin = ""
    with open(hostFile, "r", encoding="utf-8") as f:
        # 之前是否已经写过dns信息
        flag = False
        for eachLine in f.readlines():
            if r"# Host Start" in eachLine:
                flag = True
            elif r"# Host End" in eachLine:
                flag = False
            else:
                if not flag:
                    origin = origin + eachLine
        # 写入新的host记录
        origin = origin.strip()
        origin = origin + '\n' + append_content
    with open(hostFile, "w", encoding="utf-8") as f:
        f.write(origin)
    print('\nHost 修改后如下:')
    print(origin)


PING_TIMEOUT = 2 * 1000


def get_best_ip(ip_list: set):
    best_ip = ''
    min_ms = PING_TIMEOUT
    for ip in ip_list:

        # ping_time = ping_by_ping(ip)
        ping_time = ping_by_subprocess(ip)
        if ping_time >= PING_TIMEOUT:
            # 超时认为 IP 失效
            continue
        else:
            if ping_time < 3.5:  # < 3.5 后不再继续,直接返回
                min_ms = ping_time
                best_ip = ip
                break
            elif ping_time < min_ms:
                min_ms = ping_time
                best_ip = ip
    return best_ip, min_ms


#
# @retry(tries=3)
# def get_json(session: Any) -> Optional[list]:
#     url = 'https://raw.hellogithub.com/hosts.json'
#     try:
#         rs = session.get(url)
#         data = json.loads(rs.text)
#         return data
#     except Exception as ex:
#         print(f"get: {url}, error: {ex}")
#         raise Exception


def ping_by_ping(ip):
    ping_result = ping(ip, timeout=PING_TIMEOUT)
    ping_time = ping_result.rtt_avg_ms
    print(f"Ping {ip} 成功, 延时: {ping_time}s")
    return ping_time


def ping_by_subprocess(destination_ip):
    start = time.time()
    # status, result = subprocess.getstatusoutput(['ping', '-c', '4', destination_ip], capture_output=True)
    result = subprocess.run(['ping', '-c', '4', destination_ip], capture_output=True)
    if result.returncode == 0:
        cost2 = time.time() - start
        # print(f"Ping {destination_ip} 成功, 耗时: {cost2}s, {result.stdout.decode('utf-8')}")
        print(f"Ping {destination_ip} 成功, 耗时: {cost2}s")
        return cost2
    else:
        cost2 = time.time() - start
        print(f"Ping 失败: {destination_ip}, 耗时: {cost2}s, {result.stderr.decode('utf-8')}")
        return PING_TIMEOUT


def get_ip(github_url):
    ips_set = set()
    ip_list0 = get_ip_by_alidns(github_url)
    if ip_list0:
        for ip in ip_list0:
            ips_set.add(ip)

    ip_list1 = get_ip_by_api1(github_url)
    if ip_list1:
        for ip in ip_list1:
            ips_set.add(ip)

    ip_list2 = get_ip_by_dnsProvider(github_url)
    if ip_list2:
        for ip in ip_list2:
            ips_set.add(ip)

    print(f"组合后为 {github_url} 共获取到 {len(ips_set)} 个 ip, {ips_set}")

    best_ip, min_ms = get_best_ip(ips_set)
    if best_ip:
        print(f"->域名 {github_url} 最快 ip 为 {best_ip}, 延迟 {min_ms}s")
        return best_ip
    else:
        raise Exception(f"url: {github_url}, ipaddress empty")


ip_pattern = re.compile(
    r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')


def get_ip_by_alidns(github_url: str):
    url = f'https://dns.alidns.com/resolve?name={github_url}&type=1'
    start1 = time.time()
    try:
        response = requests.get(url=url, timeout=10)
        Answers = json.loads(response.text)["Answer"]
        ip_list = []
        for Answer in Answers:
            ip = Answer['data']
            if ip_pattern.match(ip):
                ip_list.append(ip)
        cost1 = int(time.time() - start1)
        print(f"从 alidns DNS 供应商获取到 ip列表 {len(ip_list)}个：{github_url}, {ip_list}, 耗时: {cost1}s")
        return ip_list
    except Exception as e:
        cost1 = int(time.time() - start1)
        print(f"从 alidns DNS 供应商获获取 ip 列表失败: {github_url}, 耗时: {cost1}s, error：{e}")
        return None


@retry(tries=3)
def get_ip_by_api1(github_url: str):
    session = HTMLSession()
    url = f'https://sites.ipaddress.com/{github_url}'
    headers = {'User-Agent': USR_AGENT}
    start1 = time.time()
    try:
        rs = session.get(url, headers=headers, timeout=5)
        table = rs.html.find('#dns', first=True)
        pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        ip_list = re.findall(pattern, table.text)
        cost1 = int(time.time() - start1)
        print(f"从 sites DNS 供应商获取到 ip列表 {len(ip_list)}个：{github_url}, {ip_list}, 耗时: {cost1}s")
        return ip_list
    except Exception as e:
        cost1 = int(time.time() - start1)
        print(f"从 sites DNS 供应商获获取 ip 列表失败: {github_url}, 耗时: {cost1}s, error：{e}")
        return None


# USR_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
USR_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"


# 获取域名所有 ip
@retry(tries=3)
def get_ip_by_dnsProvider(github_url: str):
    # dns解析用到的api
    api = "http://api.ip33.com/dns/resolver"
    all_dnd_ip_list = set()
    start_dns_list = time.time()
    for dns in dnsProvider:
        start1 = time.time()
        params = {
            "domain": github_url,
            "type": "A",
            "dns": dns
        }
        headers = {'User-Agent': USR_AGENT}
        try:
            response = requests.post(url=api, data=params, headers=headers, timeout=10)
            html = response.text
            ipDics = json.loads(html)["record"]
            cost1 = int(time.time() - start1)
            print(
                f"从 ip33 DNS 供应商({dns})获取到 ip列表 {len(all_dnd_ip_list)}个：{github_url}, {all_dnd_ip_list}, 耗时: {cost1}s")
            for dic in ipDics:
                all_dnd_ip_list.add(dic["ip"])
        except Exception as e:
            cost1 = int(time.time() - start1)
            print(f"从 ip33 DNS 供应商({dns})获取 ip 列表失败: {github_url}, 耗时: {cost1}s, error：{e}")
            print(e)
            continue
    print(
        f"从 ip33 DNS 供应商为 {github_url} 共获取到 {len(all_dnd_ip_list)} 个 ip, 耗时: {int(time.time() - start_dns_list)}s, {all_dnd_ip_list}")
    return all_dnd_ip_list


TO_DOH_HOST_PATH = '/volume3/develop/PythonScript/append_hosts.txt'
# HOST_PATH = '/volume1/homes/zyt/PythonScript/hosts.txt'
HOST_PATH = '/etc/hosts'
# HOST_PATH = 'hosts.txt'
# 单个域名粒度,举例上次查询超过这个时间后才会刷新,单位秒
CYCLE_S = 24 * 60 * 60
if __name__ == '__main__':
    start = time.time()

    update_time = datetime.now()
    print(f'Start script: {update_time}')
    append_hosts_content = ''
    content = ""
    GITHUB_URLS = set()
    last_host_ip_dirt = {}
    with open(TO_DOH_HOST_PATH, "r", encoding="utf-8") as f:
        for eachLine in f.readlines():
            eachLine = eachLine.strip()
            if eachLine:
                if not eachLine.startswith('#'):
                    if '@' in eachLine:
                        splits = eachLine.split('@')
                        # api4.thetvdb.com@114.114.114.114@555555
                        host = splits[0]
                        last_ip = splits[1]
                        last_time = int(splits[2])
                        last_host_ip_dirt[host] = last_ip
                        if start - last_time > CYCLE_S:  # 过期了
                            GITHUB_URLS.add(host)
                        else:
                            content += f"{last_ip}	{host}\n"
                            append_hosts_content += f"{eachLine}\n"
                    else:
                        GITHUB_URLS.add(eachLine)
                else:
                    append_hosts_content += f"{eachLine}\n"

    print(f'本次待更新域名{len(GITHUB_URLS)}个: {GITHUB_URLS} \n')

    for index, github_url in enumerate(GITHUB_URLS):
        try:
            ip = get_ip(github_url)
            content += f"{ip}	{github_url}\n"
            append_hosts_content += f"{github_url}@{ip}@{int(time.time())}\n"
        except Exception as e:
            if github_url in last_host_ip_dirt:
                content += f"{last_host_ip_dirt[github_url]}	{github_url}\n"
                print(f'error get_ip for : {github_url},使用上次查询的ip{last_host_ip_dirt[github_url]}, error={e}')
            else:
                print(f'error get_ip for : {github_url}, error={e}')
            append_hosts_content += f"{github_url}\n"
            continue
        print(f'更新进度: {index + 1}/共{len(GITHUB_URLS)}\n')

    if content:
        hosts_content = HOSTS_TEMPLATE.format(content=content, update_time=update_time)
        append_host_file(hosts_content)
        # 更新获取时间
        with open(TO_DOH_HOST_PATH, "w", encoding="utf-8") as f:
            f.write(append_hosts_content)
        print(f'SUCCESS End script, 共耗时:{int(time.time() - start)}s')
    else:
        print(f'FAIL, End script, 共耗时:{int(time.time() - start)}s')

#  cp /volume1/homes/zyt/PythonScript/hosts.txt /etc/hosts
