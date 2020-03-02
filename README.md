# 全国肺炎疫情确诊人数采集器
## 声明
本数据采集器修改自github项目：
[2019新型冠状病毒疫情实时爬虫](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)
<br/>数据格式与其兼容：
[2019新型冠状病毒疫情时间序列数据仓库](https://github.com/BlankerL/DXY-2019-nCoV-Data)
<br/>数据来自于[丁香园](https://ncov.dxy.cn/ncovh5/view/pneumonia)。

<br/>由于在武汉被困太久纯粹无聊而写。

<br/>只采集了**全国的确诊人数**数据，保存为csv文件，数据半个小时采集一次，最后一列为时间戳。
<br/>csv文件跟ncov.py在同一目录。


## 使用方法
安装python3 <br/>
pip install pandas <br/>
pip install bs4 <br/>
python ncov <br/>

## 更新日志
* **2020年3月2日更新 <br/>**
1. 数据记录从**2020-02-02 01:30:02**到2020-03-02 23:30:00
2. 由于程序放在很老的windows平板里，记录的时间可能有一点点误差，不过影响不大
3. 不知不觉一个月采集过去了，所以搞了个统计图

<br/>

* **2020年2月6日更新 <br/>**
1. 修改定时方式，使用定时器实现
2. 去除DXYOverall.csv文件内的重复数据
3. 数据记录从**2020-02-02 01:30:02**到至今
4. 修复有时导出记录重复的bug

<br/>

* **2020年2月5日更新 <br/>**
1. 基础功能实现，github建库

