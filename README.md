一直错误的记得我分享过了，看来是年纪大脑子瓦特了，我的锅。
求🐱帖很荣幸被咖喱佬选中了送了我好运，我从那时发誓药丸是我家他是我男神。所以我即使是一颗小⭐️，我也牡蛎发点光照亮世界。
这个脚本，是我刚入pt写的第一个脚本，经历了好几个月的增增补补。下面按照 脚本大体介绍，能力列表，详细使用步骤，效果展示 脚本附件 几个模块介绍。
### **大体介绍**
如题，是个帮助清理垃圾资源的脚本，我没有直接帮你delete删除，而是通过给qb、tr打标签，或者日志打印的形式将不同维度的垃圾资源展示出来，你根据日志、标签消费，自行决定要删除哪些，人工同时也是个谨慎的二次确认过程。脚本全python代码（众所周知，python在所有编程语言中就像草履虫在生物界地位一样简单），所以如果哪里不符合你的预期，你还可以借助GPT DIY成你想要的。

### **能力列表**
（排名顺序不分先后，每个能力都有子开关）
1 标记在 qb、tr 做种但是没有入emby库的资源，此类资源有时可优先删除（mp 有时整理资源即使失败也会添加已整理标签，不能作为入库依据）。
2 标记辅种数小于 x 的种子，x=1 就是单站辅种性价比低，磁盘紧张时应该优先清理。
3 标记 ISO、TS 格式的种子，我是设备播不起来原盘。
4 标记 tracker 异常的种子，**重点:**会标明是否有其他辅种存在，让你决定删除时是否要删除源文件。
5 标记源文件已经删除的种子。这个能力好些其他脚本也提供了.
6 标记需要长期保种的种子，按照你的文件路径配置圈选条件。
7 对某些站的所有种子逐个上传限速，让带宽雨露均沾(把带宽留给喜欢的大站)。
8 打印在下载根目录下，但是没有做种的文件。**(这个别人说用途最大)**
9 打印在媒体根文件夹下，但是没有做种的文件。可能是早期迅雷下载的资源，可能是 qb 种子被站点删掉你也删了做种的资源。
10 打印在媒体根文件夹下，重复版本的视频文件，比如 西游记.mkv、西游记.mp4、西游记1080p.mp4、西游记2160p.mp4都会算作重复打印出来。清理哪个你自己决定啦。
11 打印本地辅种数高于 x 的种子名称，你可以把辅种多的资源名字分享给保种档，事半功倍的把ptpp数据搞好。
12 标记是否标记源文件同时在qb\tr做种的种子,会添加标签 F-辅种tr\F-辅种qb1\F-辅种qb2

### **详细使用步骤**
我的下载器分布是这样的，qb1观影下载，qb2刷流，tr保种，所以脚本覆盖这3个下载器，当然，不需的下载器配置瞎写即可(会自己登录失败)。
**1 安装依赖库：**(如果MP内执行已自带，无需安装，如果群辉控制面板-自定义脚本运行就需要安装)
一起qb依赖库、tr依赖库:curl -O https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && rm get-pip.py && python -m pip install qbittorrent-api && pip install transmission-rpc -U
**2 下载脚本文件**
本地新建xxx_clean.py文件，以txt方式打开，将附件中的脚本内容全部复制粘贴进去，保存
**3 修改脚本内配置**
打开py文件，将我的qb 端口 账号密码等修改成你自己的（脚本本地运行，放心改）各个配置项注释介绍很详细很详细，如果有我没表达清楚的截图评论区提问。
```
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
```
**3 运行脚本**
运行入口自己选，下面介绍MP插件运行和群辉自定义脚本运行俩方式
**MP插件运行**：
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846141-630684-image.png]
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846129-169151-image.png]
**群辉自定义脚本**
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846193-154397-image.png]
可以稍微大胆运行，本脚本不会主动删东西，只会加标签或者打印日志。初次运行还有这个开关：
```
# 是否真执行qb标签等, False时只模拟打印日志不真正给 qb 加标签
SWITCH_REAL_INVOKE = True
```

### **效果展示**
（部分效果）
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846295-59813-image.png]
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846348-982001-image.png]
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846367-913817-image.png]
[upl-image-preview url=https://invites.fun/assets/files/2025-02-18/1739846434-703597-image.png]
```
2025-02-18 10:07:35 当前运行主机 ip:192.168.1.111, 服务端 ip:192.168.1.111
qb1共1248个种子; qb2共428个种子; tr共4509个种子;
IS_MIRROR_SCRIPT_DOWN_PATH=False,IS_MIRROR_DOWN_PATH=False,IS_MIRROR_EMBY_PATH=False,
2025-02-18 10:07:40 步骤1.第一遍遍历, 收集要标记的信息...
qb2下载中跳过标记: Oh,.Canada.2024.BluRay.1080p.DTS-HDMA5.1.x264-
qb2下载中跳过标记: V.H.S.Beyond.2024.1080p.BluRay.x264.DTS-
qb2下载中跳过标记: 巴克叔叔.Uncle.Buck.1989.2160p.UHD.Blu-ray.DoVi.HDR10.HEVC.DTS-HD.MA.5.1-DIY@
qb2下载中跳过标记: 隐形将军.Yin.Xing.Jiang.Jun.2010.V2.WEB-DL.4k.H265.AAC-
2025-02-18 10:08:12 步骤2.第二遍遍历,标记收集完的信息...
2025-02-18 10:08:12 开始收集 qb1 中待标记信息...
2025-02-18 10:08:15 开始收集 qb2 中待标记信息...
2025-02-18 10:08:15 开始收集 tr 中待标记信息...
2025-02-18 10:08:16 步骤3.开始添加标记...
---qb1:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:0
---qb2:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:0
---tr:做种文件不全,可能是已删除或者拆包或者其他,请手动检查. torrent总个数:0
---下载目录下未做种文件(去除冗余小文件)共1个: 19651(所有下载目录文件数,包含冗余小文件) - 19372(做种文件数) = 1
------未做种文件:/volume2/video/down/test.mkv
------未做种文件共 800KB
---开始打印媒体库下未做种文件
---/volume2/video/link 下所有没有做种文件总大小: 0B, 列表如下:
---开始打印媒体库下重复版本视频文件
---开始给下载器添加标签
---开始标记辅种个数
标记辅种数小于等于30 文件体积共10.60TB, 辅种体积共95.76TB(关联这些标签的种子未计算:{'保种区', 'KEEP', '海豹', 'F-长期'})
qb1 标记 [F-辅种1] 种子个数: 40
tr 标记 [F-辅种29] 种子个数: 58
---开始标记ISO、ts文件类型
tr 标记 [F-TS] 种子个数: 79
qb1 标记 [F-m2TS] 种子个数: 28
tr 标记 [F-m2TS] 种子个数: 65
---开始标记异常 tracker 状态
qb1 标记 [F-Error-有辅种] 种子个数: 2
qb2 标记 [F-Error-有辅种] 种子个数: 4
tr 标记 [F-Error-有辅种] 种子个数: 5
qb2 标记 [F-Error-无辅种] 种子个数: 1
---开始标记已入库、未入库、长期保种
qb1 标记 [F-入库] 种子个数: 1235
tr 标记 [F-入库] 种子个数: 3202
qb1 标记 [F-未入库] 种子个数: 13
tr 标记 [F-长期] 种子个数: 4272
---开始标记是否在 qb1/qb2/tr 跨端辅种
tr 标记 [F-辅种qb2] 种子个数: 9
qb2 标记 [F-辅种tr] 种子个数: 2
---开始标记站点标签
---开始对站点种子设置限速,限速配置见UOLOAD_LIMIT_SITE
qb1 不限速种子个数: 755
qb1 限速(1MB)种子个数: 117
tr 限速(100KB)种子个数: 1419
tr 限速(1MB)种子个数: 234
specific_process_tr_tags:  len=1088
---SUCCESS 标记完成,耗时: 51s
```
### **脚本附件** 
全在这一个py文件里了
```
教程字数超65535了,改为放附件区。qb-torrent-mark.py文件（文件名不重要，一开始只给qb写的，后面加上了tr的支持）
```
### **番外篇**
qb添加了这么多标签，日常观感挺难受的，所以我的食用方式是要清理资源前手动执行一下标签，清理完一波后将这些标签清理了，所以还有个清理这堆标签的脚本，使用方式也是打开改端口号用户名啥的成你的，运行。
```
教程字数超65535了,改为放附件区 qb-delete-tag.py文件
```

