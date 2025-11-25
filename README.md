**中文** | [English](README_en.md) <!-- lang -->
# Minecraft服务器玩家UUID和在线模式转换器

## 📖 简介
当我们游玩自己开设的JAVA服务器时，有时会遇到这么一个问题：大家都是MC正版玩家，服务器默认开着`Online-Mode`。有一位没有正版的玩家对这个服务器很感兴趣，想要加入。为了让他加入，`Online-Mode`必须要改成`false`。此时就出现了一个问题：原先的几位玩家背包物品、成就、以及ftb相关的任务、组队等内容就会丢失（如果有ftb相关模组的话），必须从头开始。

解决此问题的方法就是必须修改服务器中所有含有玩家UUID的文件，将玩家在线UUID改为离线的UUID。

这个转换器就是起这个作用的！它可以在切换`Online-Mode`的同时按照你配置好的信息切换修改玩家UUID相关的文件。

## 🔩 文件说明

目录中有三个文件：

1. `Info.json`

    *   **必须**，这是你要配置的文件，需要你自己增添每位服务器玩家的UUID，配置需要改玩家UUID文件名的地方，以及是否需要修改那些文件内的玩家UUID内容

2. `MCServer UUID and Online-mode Conventer_vanilla.py`

    *   **可选**，这是我自己写的代码（因此注释为中文），可以用于原版服务器UUID和Online-Mode的切换。只不过代码不太优美，if-elif语句偏多，且没有错误检测，可以学习我的算法思路，小白不推荐使用

2. `MCServer UUID and Online-mode Conventer.py`

    *   **必须且推荐**，此文件基于`MCServer UUID and Online-mode Conventer_vanilla.py`修改而成，增加了需求，并借助DeekSeek进行完善（注释为英文），有输出日志和错误检测，可以根据需求对原版服或模组服进行切换

## 🔑 如何使用

1. **关闭并备份你的服务器以及world存档文件夹！！！**（如果因没有备份服务器以及存档文件而使用本工具造成的存档损坏不能修以及服务器损坏不能修复，请自行承担后果！！！）

2. 安装最新版Python

3. git本库或者直接下载zip，并将`Info.json`和`MCServer UUID and Online-mode Conventer.py`两个文件置于同一目录下

4. 打开`Info.json`，根据你的服务器玩家UUID和需要修改的文件进行配置

   * 可参考wiki中对`Info.json`的介绍来配置

      * `root_dir`为你的服务器根目录，如`D:/MC Server`

      * `changeUUID_folder_name`是你需要修改玩家UUID的文件夹名称，需要根据实际情况和是否需要修改文件中的内容进行修改。

          例如：原版存档中只需要修改`advancements`、`playerdata`、`stats`这三个文件夹内*每个文件名中的*玩家UUID部分，模组存档例如安装了ftb相关的既要修改*文件中*的玩家UUID，也需要打开这些文件修改*替换文件内的玩家UUID*

      * `player`是玩家信息，这里你需要填写玩家的昵称（`name`），`online-Mode=true`时的玩家UUID（`Online_uuid`），以及`online-Mode=false`时的玩家UUID（`Offline_uuid`）。

5. 在Python下运行`MCServer UUID and Online-mode Conventer.py`即可

## 📄 相关文档
   * [wiki](https://github.com/skwdpy/Minecraft-Server-Player-UUID-and-Online-Mode-Converter/wiki/Info.json文件参数详解) - 有关`Info.json`文件的详细说明
