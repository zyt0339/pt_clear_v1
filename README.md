本文档，编辑于2024年10月18日13:20:14，如有更新教程请忽略此文档
分享一个标记打印 nas 垃圾劣质资源的 python 脚本，通过给 qb、tr 打标签的方式以及日志打印的方式使用。纯本地运行，只会给qb、tr增加标签或者打印日志，不会自动删种或删文件，需要你参考打完的标签和打印日志手动检查后再自己删，这样更稳妥。能实现诸如以下功能：

1. 标记在 qb、tr 做种但是没有入emby库的资源，此类资源应当被删除（mp 整理资源即使失败也会添加已整理标签，不能作为入库依据）。
2. 标记辅种数小于 x 的种子，x=1 就是单站辅种性价比低，磁盘紧张时应该优先清理。
3. 标记 ISO、TS 格式的资源，垃圾资源优先清理。
4. 标记 tracker 异常的种子，且会标明是否有其他辅种存在，让你决定删除时是否要删除源文件。（tr 不需要，tr 自带的异常 tracker 归类就够用）
5. 标记源文件已经删除的种子。
6. 标记需要长期保种的种子，按照保存路径中包含固定字符圈选。
7. 对某站点下的所有种子逐个上传限速，把带宽留给喜欢的大站。
8. 打印在下载根文件夹下，但是没有做种的文件。
9. 打印在媒体根文件夹下，但是没有做种的文件。可能是早期迅雷下载的资源，可能是 qb 种子被站点删掉你也删了做种的资源。
10. 打印在媒体根文件夹下，重复版本的视频文件，比如 西游记.mkv、西游记.mp4、西游记1080p.mp4、西游记2160p.mp4都会算作重复打印出来。清理哪个你自己决定啦。
11. 打印辅种数高于 x 的种子名称，你可以把辅种多的资源名字分享给我，事半功倍的把ptpp数据搞好。
12. 标记是否标记源文件同时在qb\tr做种的种子,会添加标签 F-辅种tr\F-辅种qb

# 使用步骤
### 站点标签依赖
脚本依赖标签中有站点名称,需要先执行一遍 mp插件<下载任务分类与标签>(勾选 自动站点标签 补全下载历史的标签与分类(一次性任务))，让每个种子都添加上站点中文名标签。
### 下载脚本

1. 方式一，打开```https://github.com/zyt0339/pt_clear_v1```,下载-下载ZIP，然后解压出pt_clear_v1.py。
2. 方式二，打开```https://github.com/zyt0339/pt_clear_v1/blob/main/pt_clear_v1.py```复制全部脚本文字，在电脑新建pt_clear_v1.txt将前面文字粘贴进去，关闭保存，后缀名改为.py

注意：这脚本在 nas 执行能使用全部能力，在电脑运行不能进行文件路径分析这些能力（没法用路径判断文件状态）

### 安装脚本依赖的 qb、tr 库
在哪运行就在哪安装，都是 github 开源的 qb、tr python 依赖库，体积很小，无安全风险。

如果电脑运行就打开电脑命令行，或者 nas 运行就 ssh 连接到 nas。“ssh 连接到 nas”是一个基础技能好多脚本都要用到，这里不展开讲了，分别运行以下两行指令，不报红字错误就是成功了。

```pip install qbittorrent-api```
```pip install transmission-rpc -U```
### 修改配置字段
以 txt 格式打开pt_clear_v1.py文件，修改保存。（开关在脚本中也有详细的注释介绍）

- 配置 qb、tr 链接信息，内外网、ip 域名都支持。如果只使用 qb 可以只配置一个，另一个让他自然登录失败。

```
SERVER_HOST = "192.168.1.100"
QB_CONN_INFO = dict(
	    host=SERVER_HOST,
	    port=8085,
	    username="xxx",
	    password="xxx",
)
TR_CONN_INFO = dict(
	    protocol='http',
	    host=SERVER_HOST,
	    port=9091,
	    username="xxx",
	    password="xxx",
)
```

- ```SWITCH_REAL_INVOKE = True```是否只是模拟打印,不真正给 qb\tr 添加标签等

- ```SWITCH_EMBY = True```是否增加F-已入库\F-未入库标签\F-长期, 只有在 nas 上执行才能生效,因为本质是判断硬链接个数

- ```SWITCH_TORRENT_COUNT = True```辅种个数标记开关,打开后辅种个数小于LIMIT_TO_DELETE_THRESHOLD的种子会添加(F-辅种3)这种标签
```LIMIT_TO_DELETE_THRESHOLD = 5```<= x 的才会标记 (<=1 就是单站辅种)

- ```PRINT_COPY_COUNT = 20```只会打印输出辅种数高于此值的种, >= 1000时不再打印

- ```SWITCH_FILE_SUFFIX = True```是否增加F-ISO\F-TS\F-m2TS文件类型标记

- ```SWITCH_TRACKER = True```是否增加tracker 异常状态标记,无辅种的可以连源文件一起删除

- ```SWITCH_LIMIT = True```是否对某站种子上传限速,设置到种子粒度
```UOLOAD_LIMIT_SITE = {'麒麟': _100K, '青蛙': _100K, '朱雀': _100K, 'CARPT': _100K}```限速站点及速度

- ```SWITCH_PRINT_NOT_UPLOAD_FILE = True``` 是否打印没有做种的文件列表，只有download_parent_dirs配置了才会有效;
	```download_parent_dirs = {"/volume2/video/Downloads/qBittorrent","/volume4/video4/Downloads/qBittorrent"}``` 下载根目录,多个盘写多个
 
- ```SWITCH_PRING_NOT_TORRENT = True```是否打印emby 等媒体库下没做种的视频文件
	```SWITCH_PRING_MULTY_VIDEO_FILE = True```是否打印媒体库下重复的不同清晰度视频文件
	```media_parent_dirs = {"/volume2/video/link","/volume4/video4/link"}```媒体根目录,多个盘写多个
 
- ```SWITCH_MARK_IN_TR_OR_QB = True```是否标记源文件同时在qb\tr做种的种子,会添加标签 F-辅种tr\F-辅种qb
    
### 执行
1. 在电脑执行，前面提到了在电脑运行不能进行文件路径分析这些能力。配置完后直接```python3 pt_clear_v1.py```就可以啦，qb 5000 种大概要运行 1 分钟。
2. 在群晖定时任务，也是配置```python3 /volume3/develop/pt_clear_v1.py```就行啦，要写全路径。周期你自己决定吧，可以要一次也可以一周来 2 次。
3. 在 mp 命令执行器中，有个插件就叫命令执行器。也是配置```python3 /volume3/develop/pt_clear_v1.py```全路径，周期自己决定，好处是执行完能给手机发通知（前提你得搭建了通知），但有个需要额外注意的，代码里路径判断都是基于绝对路径的，如果 docker 映射换了假路径得自己做好路径转换，我没转，我脑容量小转不过来。

# 效果展示
![](https://picture.agsvpt.com/i/2024/10/24/67192f0be54ad.png)
![](https://picture.agsvpt.com/i/2024/10/24/6719302f424d3.png)
# 其他
欢迎好心人将这个脚本弄成 mp 插件，能帮助到别人是我滴荣幸。
