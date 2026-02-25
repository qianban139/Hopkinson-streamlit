# 数智化电磁驱动霍普金森杆测试系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red.svg)](https://streamlit.io/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 一个基于Streamlit的Web应用，集成了电磁驱动、数字孪生和人工智能技术，用于材料动态力学性能测试。

## 📋 项目简介

数智化电磁驱动霍普金森杆多场耦合动态测试系统通过电磁驱动-数字孪生-人工智能的深度融合，实现：

- 🔥 **热-力-电多场耦合动态加载**
- 🤖 **智能波形自适应调控**
- 📊 **全链条数据融合分析**

构建从"材料特性感知—动态加载控制—本构关系提取"的全流程数智化测试平台。

## ✨ 核心功能

### 1. 项目介绍模块
- 系统概述与技术架构展示
- 应用场景案例（土木工程、矿业工程、安全科学）
- 3D模型可视化展示

### 2. 控制系统模块
- 实时波形监控
- LSTM时序预测分析
- GAN波形生成控制
- 高压安全监控与预警

### 3. 数据分析模块
- 材料行为分析与预测
- Johnson-Cook本构模型拟合
- 小波变换数据去噪与特征提取
- CSV数据上传与可视化

### 4. 智能助手模块
- AI对话交互
- 智能文本生成
- 数据自动分析

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 20.0+

### 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd optimized_project

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 运行项目

```bash
# 启动Streamlit应用
streamlit run main.py
```

应用将在浏览器中自动打开，默认地址: http://localhost:8501

## 📁 项目结构

```
optimized_project/
├── 📄 main.py                 # 主程序入口
├── 📄 config.py               # 全局配置文件
├── 📄 requirements.txt        # 依赖包列表
├── 📄 README.md              # 项目说明文档
│
├── 📁 assets/                # 静态资源
│   ├── 📁 images/            # 图片资源
│   │   ├── 113.png          # Logo
│   │   ├── 322.jpg          # 背景图
│   │   ├── front.gif        # 正视图
│   │   └── side.gif         # 侧视图
│   └── 📁 css/              # CSS样式
│       └── styles.py        # 统一样式定义
│
├── 📁 components/            # 可复用组件（预留）
│
├── 📁 pages/                 # 页面模块
│   ├── page_0.py            # 项目介绍页
│   ├── page_1.py            # 控制系统页
│   ├── page_2.py            # 数据分析页
│   └── page_3.py            # 智能助手页
│
└── 📁 utils/                 # 工具模块
    ├── helpers.py           # 通用工具函数
    ├── ai_models.py         # AI模型（LSTM/GAN）
    └── control_system.py    # 控制系统
```

## 🔧 配置说明

### 配置文件 (config.py)

```python
# 页面配置
PAGE_CONFIG = {
    "page_title": "数智化电磁驱动霍普金森杆测试系统",
    "page_icon": "⚡",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# 安全阈值配置
SAFETY_THRESHOLDS = {
    "voltage": 1000.0,        # 电压阈值 (V)
    "current": 50.0,          # 电流阈值 (A)
    "temperature": 85.0,      # 温度阈值 (°C)
    "capacitor_charge": 0.9,  # 电容充电阈值
}

# AI模型配置
LSTM_CONFIG = {
    "sequence_length": 50,
    "prediction_horizon": 10,
    "epochs": 100,
    "batch_size": 32
}
```

### 自定义样式

样式文件位于 `assets/css/styles.py`，包含：

- `BASE_STYLES`: 基础样式
- `GLASS_CARD_STYLES`: 玻璃拟态卡片
- `TEXT_STYLES`: 文字样式
- `COMPONENT_STYLES`: 组件样式
- `TAB_STYLES`: 标签页样式
- `ANIMATION_STYLES`: 动画效果
- `RESPONSIVE_STYLES`: 响应式设计

## 🎨 界面预览

### 项目介绍页
- 系统概览与技术参数
- 应用场景展示
- 3D模型可视化

### 控制系统页
- 实时波形监控
- LSTM预测分析
- GAN波形生成
- 安全监控面板

### 数据分析页
- 材料行为分析
- Johnson-Cook模型
- 小波变换分析
- 数据可视化

### 智能助手页
- AI对话交互
- 文本生成
- 数据分析

## 🛠️ 技术栈

### 前端
- **Streamlit**: Web应用框架
- **Plotly**: 交互式图表
- **CSS3**: 样式设计

### 后端
- **Python 3.8+**: 编程语言
- **TensorFlow/Keras**: 深度学习框架
- **NumPy**: 数值计算
- **Pandas**: 数据处理
- **SciPy**: 科学计算

### AI模型
- **LSTM**: 时序预测
- **GAN**: 波形生成
- **Johnson-Cook**: 本构模型

## 📊 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 波形控制精度 | ±2% | 加载精度提升40% |
| 信号信噪比 | >60dB | 提升60% |
| 预测准确率 | 95%+ | LSTM模型 |
| 系统响应时间 | <100ms | 实时监控 |

## 🔐 安全特性

- ✅ 电压/电流/温度实时监控
- ✅ 多级安全阈值设置
- ✅ 自动停机保护
- ✅ 紧急停机功能
- ✅ 安全历史记录

## 📝 使用指南

### 1. 项目介绍
- 浏览系统概述和技术架构
- 查看应用场景案例
- 观看3D模型展示

### 2. 控制系统
- 选择运行模式
- 配置安全阈值
- 启动实时监控
- 查看波形和预测结果

### 3. 数据分析
- 选择材料和加载条件
- 运行Johnson-Cook分析
- 执行小波变换去噪
- 上传CSV文件进行可视化

### 4. 智能助手
- 与AI对话获取帮助
- 使用文本生成功能
- 上传数据进行分析

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - Web应用框架
- [TensorFlow](https://tensorflow.org/) - 深度学习框架
- [Plotly](https://plotly.com/) - 图表库

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: example@example.com
- 🌐 Website: https://example.com

---

<p align="center">
  <strong>Powered by 数智化电磁驱动霍普金森杆多场耦合动态测试系统</strong><br>
  <span style="color: #666;">2025 AI技术展示平台</span>
</p>
