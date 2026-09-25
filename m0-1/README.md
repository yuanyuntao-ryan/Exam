# M0-1任务总结及踩坑实录

## 一.知识学习，资料查找及任务完成
1.我通过搜索bilibili教学视频学习了git的概念，git的安装，基本命令及其用法；学习了Github的基本知识。
2.我通过deepseek获取了各个环境的配置及检验的相关命令。
3.我在WSL上完成了Ubuntu,ROS2,Python虚拟环境（uv），Cmake，VScode及git的安装及配置。


## 二.本机踩坑实录

### 踩坑 1：选错 Ubuntu 版本
**问题描述**：WSL 默认装的是 Ubuntu 26.04，导致 ROS2 Humble 无法安装（只支持 22.04）。
**定位分析**：通过 `lsb_release -a` 查看版本号，发现版本不匹配。
**解决方法**：使用 `wsl --unregister Ubuntu` 卸载，重新执行 `wsl --install -d Ubuntu-22.04` 指定版本安装。

### 踩坑 2：换源后报 403 Forbidden
**问题描述**：配置清华源后，`sudo apt update` 频繁报 403 错误。
报错原文：`E: Failed to fetch https://mirrors.tuna.tsinghua.edu.cn/... 403  Forbidden [IP: 101.6.15.130 443]`
**定位分析**：排查发现 Windows 主机的 VPN 代理干扰了 WSL 的网络请求。
**解决方法**：彻底关闭 Windows 代理，换用阿里云源 `mirrors.aliyun.com`，网络恢复畅通。

### 踩坑 3：ROS2 官方源连接超时
**问题描述**：添加 ROS2 官方源 `packages.ros.org` 时，网络一直超时。
**定位分析**：国内网络无法直连 ROS 官方源。
**解决方法**：手动将 `/etc/apt/sources.list.d/ros2.list` 中的源替换为阿里云镜像。
报错原文：
```text
Err:5 http://packages.ros.org/ros2/ubuntu jammy InRelease Cannot initiate the connection to packages.ros.org:80 ... connection timed out
W: Failed to fetch http://packages.ros.org/ros2/ubuntu/dists/jammy/InRelease ... connection timed out
```


## 三.参考资料链接
【【GeekHour】一小时Git教程】https://www.bilibili.com/video/BV1HM411377j?p=19&vd_source=15fa3f7c2c539d07f18051ce6ef36e6f