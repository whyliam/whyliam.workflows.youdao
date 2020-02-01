# whyliam.workflows.youdao

## 有道翻译 workflow v2.2.5

默认快捷键 `yd`，查看翻译结果。

1. 英译中
2. 中译英
3. 翻译短语句子
4. 打开有道翻译页面，查看详细内容
5. 直接在打出翻译结果
6. 显示历史查询记录
7. 同步单词到有道在线单词本

### 功能

1. 按`回车` 复制
2. 按`Control ⌃+回车` 打开有道翻译页面
3. 按`Command ⌘+回车` 直接在打出翻译结果
4. 按`Shift ⇧+回车` 直接发音
5. 选中文字 双击`Option ⌥`进行翻译（需要另行设置）
6. `yd *` 显示历史查询记录
7. 按`Alt+回车`, 同步单词到有道在线单词本

### 下载

[Alfred 3 版本](https://github.com/whyliam/whyliam.workflows.youdao/releases/download/2.2.5/whyliam.workflows.youdao.alfred3workflow)

[Alfred 4 版本](https://github.com/whyliam/whyliam.workflows.youdao/releases/download/2.2.5/whyliam.workflows.youdao.alfredworkflow)

### 安装

1\. [下载](https://github.com/whyliam/whyliam.workflows.youdao/releases)最新版本双击安装

2\. [注册](http://ai.youdao.com/appmgr.s)有道智云应用

3\. 在 Alfred 的设置中填入对应的`应用ID`和`应用密钥`

![](https://tva1.sinaimg.cn/large/006tNbRwly1g9oapg37t0j31am0sgjxr.jpg)

4\. 在 Alfred 的设置中设置快捷方式键
![](http://ww2.sinaimg.cn/large/006tNbRwgy1feno6pzaxdj31a60p0jsl.jpg)

### 问题

如果新版本有道智云遇到问题，请参见 [错误代码列表](http://ai.youdao.com/docs/doc-trans-api.s#p08)。

### 演示

#### 英译中

![](http://ww3.sinaimg.cn/large/006tNbRwgy1fenonlxdjwg30sv0r7wkd.gif)

#### 中译英

![](http://ww1.sinaimg.cn/large/006tNbRwgy1fenonzclvfg30sw0r90zo.gif)

#### 翻译短语

![](http://ww3.sinaimg.cn/large/006tNbRwgy1fenooolrkpg30t00r47bg.gif)

#### 发音 - 按`Shift ⇧+回车`

![](http://ww3.sinaimg.cn/large/006tNbRwgy1fenooolrkpg30t00r47bg.gif)

#### 打开有道翻译页面 - 按`Control ⌃+回车`

![](http://ww2.sinaimg.cn/large/006tNbRwgy1fenopnjw9qg30tj0r5n8k.gif)

#### 直接在打出翻译结果 - 按`Command ⌘+回车`

![](http://ww3.sinaimg.cn/large/006tNbRwgy1fenomln8jdg30sx0r4wg2.gif)

#### 双击快速翻译 - 双击`Option ⌥`

![](http://ww1.sinaimg.cn/large/006tNbRwgy1fenosusv0bg30qn0qpq7a.gif)

#### 同步单词到有道在线单词本 - `Alt+回车`

![](https://ws4.sinaimg.cn/large/006tNc79ly1g01esa4p4bj31ig0u0atl.jpg)

分别在`username`, `password`中输入有道的用户名和密码。

在`filepath`中输入有道单词本离线保存的位置，默认在`~/Documents`中。

查询单词后按 `Alt+回车` 将单词保存到有道词典的单词本，在保存失败的时候单词将保存在离线单词本中。

### 其他配置

| 关键字         | 说明                   | 默认                                   |
| -------------- | ---------------------- | -------------------------------------- |
| username       | 有道在线单词本用户名   |                                        |
| password       | 有道在线单词本密码     |                                        |
| filepath       | 有道离线单词本保存位置 | ~/Documents/Alfred-youdao-wordbook.xml |
| youdao_key     | 老版有道翻译Key        |                                        |
| youdao_keyfrom | 老版有道翻译Keyfrom    |                                        |
| zhiyun_id      | 有道智云ID             |                                        |
| zhiyun_key     | 有道智云Key            |                                        |

### 问题说明

1 . **macOS** catalina  需要在 系统设置-安全性与隐私-辅助功能，重新授权`Alfred 4`权限。

### 更多

更多问题参见[Alfred 有道翻译简介](https://blog.naaln.com/2017/04/alfred-youdao-intro/)

---

## The MIT License (MIT)

Copyright (c) 2015

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

