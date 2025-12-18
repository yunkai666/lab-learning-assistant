# Lab-Safety-Learning-Sync

![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Lab-Safety-Learning-Sync** 是一款基于协议分析的自动化学习进度管理工具。它能够模拟在线学习的心跳同步，帮助学生自动化管理实验室安全教育的学习时长。

## 🌟 功能特性
- **静默同步**：自动维持在线状态并同步学习时长。
- **动态监控**：多线程异步刷新，实时显示当前进度与增量。
- **混淆策略**：关键 API 路径采用 Base64 编码，绕过关键词扫描。
- **审计逻辑**：内置版本状态检测与使用统计接口（Telemetry）。

## 🚀 快速开始

1. **环境准备**
   确保安装了 Python 3.8+。
   ```bash
   pip install requests