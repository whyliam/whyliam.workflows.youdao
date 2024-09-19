# whyliam.workflows.youdao
>
> 原来的版本使用的是有道智云的 API，但是目前这个 API 接口不在支持字典查询，只支持翻译。
> 但是，在我的日常过程中，对于字典的使用频率大于翻译。所以，我重新写了一个版本。
> 同时，未来我不在使用 Alfred，主要使用 Raycast，因此这个 Workflow 也不会再维护。

## 有道翻译 workflow v4.0.0

默认快捷键 `yd`，查看翻译结果。

1. 英译中
2. 中译英
3. 翻译短语句子
4. 打开有道翻译页面，查看详细内容
5. 直接在打出翻译结果
6. 显示历史查询记录
7. ~~同步单词到有道在线单词本~~

### 功能

1. 按`回车` 复制
2. 按`Control ⌃+回车` 打开有道翻译页面
3. 按`Command ⌘+回车` 直接在打出翻译结果
4. 按`Shift ⇧+回车` 直接发音
5. 选中文字 双击`Option ⌥`进行翻译（需要另行设置）
6. `yd *` 显示历史查询记录
7. 按`Alt+回车`, 同步单词到有道在线单词本

### 下载

[Python 3 版本](https://github.com/whyliam/whyliam.workflows.youdao/releases/download/4.0.0/whyliam.workflows.youdao.alfredworkflow) 

### 使用说明

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

### 问题说明

1 . **macOS** Catalina  需要在 系统设置-安全性与隐私-辅助功能，重新授权`Alfred 4`权限。

### 更多

更多问题参见 [Alfred 有道翻译简介](https://blog.naaln.com/2017/04/alfred-youdao-intro/)

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
