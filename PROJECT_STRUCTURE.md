# 项目结构文档

## 概述

本文档详细描述了数智化电磁驱动霍普金森杆测试系统的项目结构和文件组织方式。

## 目录结构

```
optimized_project/
├── 📄 main.py                      # 主程序入口
├── 📄 config.py                    # 全局配置文件
├── 📄 requirements.txt             # 依赖包列表
├── 📄 README.md                    # 项目说明文档
├── 📄 PROJECT_STRUCTURE.md         # 项目结构文档（本文件）
├── 📄 __init__.py                  # 包初始化文件
│
├── 📁 assets/                      # 静态资源目录
│   ├── 📁 images/                  # 图片资源
│   │   ├── 113.png                # 系统Logo
│   │   ├── 322.jpg                # 背景图片
│   │   ├── front.gif              # 霍普金森杆正视图
│   │   ├── side.gif               # 霍普金森杆侧视图
│   │   ├── tu_biao.png            # 图标
│   │   └── 河南理工大学-logo-2048px.png  # 校徽
│   │
│   └── 📁 css/                    # CSS样式模块
│       ├── __init__.py            # 模块初始化
│       └── styles.py              # 统一样式定义
│
├── 📁 components/                  # 可复用组件目录（预留扩展）
│   └── __init__.py                # 模块初始化
│
├── 📁 pages/                       # 页面模块目录
│   ├── __init__.py                # 模块初始化
│   ├── page_0.py                  # 项目介绍页面
│   ├── page_1.py                  # 控制系统页面
│   ├── page_2.py                  # 数据分析页面
│   └── page_3.py                  # 智能助手页面
│
└── 📁 utils/                       # 工具模块目录
    ├── __init__.py                # 模块初始化
    ├── helpers.py                 # 通用工具函数
    ├── ai_models.py               # AI模型（LSTM/GAN）
    └── control_system.py          # 控制系统
```

## 文件详细说明

### 根目录文件

#### main.py
- **类型**: 主程序入口
- **功能**: 
  - 设置页面配置
  - 应用全局样式
  - 配置页面路由
  - 加载资源文件
- **依赖**: config, utils.helpers, assets.css.styles

#### config.py
- **类型**: 配置文件
- **功能**:
  - 定义项目路径
  - 配置页面参数
  - 设置安全阈值
  - 配置AI模型参数
  - 定义分析场景
- **关键配置**:
  - PAGE_CONFIG: 页面基础配置
  - SAFETY_THRESHOLDS: 安全监控阈值
  - LSTM_CONFIG: LSTM模型参数
  - GAN_CONFIG: GAN模型参数

#### requirements.txt
- **类型**: 依赖列表
- **包含**: streamlit, tensorflow, numpy, pandas, plotly等

#### README.md
- **类型**: 项目说明文档
- **内容**: 项目简介、安装指南、使用说明、API文档

### assets目录

#### images/
存放所有图片资源文件，包括Logo、背景图、模型展示图等。

#### css/styles.py
- **类型**: CSS样式模块
- **功能**:
  - 定义基础样式
  - 玻璃拟态卡片样式
  - 文字渐变效果
  - 组件样式
  - 动画效果
  - 响应式设计
- **主要样式类**:
  - `glass-card`: 毛玻璃效果卡片
  - `gradient-text`: 渐变文字
  - `tech-card`: 技术卡片
  - `feature-tag`: 功能标签
  - `metric-card`: 指标卡片

### pages目录

#### page_0.py (项目介绍)
- **功能**: 展示系统概述、技术参数、应用场景
- **组件**:
  - 项目概览卡片
  - 技术参数面板
  - 产品展示区
  - 应用场景标签页
- **特色**: 使用缓存优化内容加载

#### page_1.py (控制系统)
- **功能**: 高压控制系统监控
- **组件**:
  - 实时波形监控
  - LSTM预测分析
  - GAN波形生成
  - 系统性能分析
  - 安全监控面板
- **特色**: 集成安全监控和预警功能

#### page_2.py (数据分析)
- **功能**: 材料力学分析
- **组件**:
  - 材料行为分析
  - Johnson-Cook本构模型
  - 小波变换分析
  - CSV数据可视化
- **特色**: 内置材料数据库，支持多种分析类型

#### page_3.py (智能助手)
- **功能**: AI对话和数据分析
- **组件**:
  - 智能对话
  - 文本生成
  - 数据分析
- **特色**: 支持上下文对话和数据自动分析

### utils目录

#### helpers.py
- **类型**: 通用工具函数
- **功能**:
  - 图片处理（base64转换）
  - UI组件创建
  - 缓存管理
  - 数据格式化
  - 错误处理
- **关键函数**:
  - `get_image_base64()`: 图片转base64
  - `add_logo_to_sidebar()`: 添加侧边栏Logo
  - `create_gradient_header()`: 创建渐变标题
  - `DataCache`: 缓存装饰器类

#### ai_models.py
- **类型**: AI模型模块
- **功能**:
  - LSTM时序预测模型
  - GAN波形生成模型
  - 模型管理器
- **关键类**:
  - `LSTMPredictor`: LSTM预测器
  - `WaveformGAN`: GAN波形生成器
  - `ModelManager`: 模型管理器

#### control_system.py
- **类型**: 控制系统模块
- **功能**:
  - 安全监控
  - 传感器模拟
  - 中央控制系统
- **关键类**:
  - `SafetyLevel`: 安全等级枚举
  - `SafetyMonitor`: 安全监控器
  - `SensorSimulator`: 传感器模拟器
  - `CentralControlSystem`: 中央控制系统

## 模块依赖关系

```
main.py
├── config.py
├── utils/
│   ├── helpers.py
│   ├── ai_models.py
│   └── control_system.py
├── assets/css/styles.py
└── pages/
    ├── page_0.py
    ├── page_1.py
    ├── page_2.py
    └── page_3.py
```

## 设计原则

### 1. 单一职责原则
- 每个模块只负责一个功能领域
- 页面组件与业务逻辑分离

### 2. 配置与代码分离
- 所有配置集中在config.py
- 便于维护和修改

### 3. 样式统一管理
- CSS样式集中管理
- 支持主题切换和复用

### 4. 缓存优化
- 使用装饰器实现函数级缓存
- 提升页面加载性能

### 5. 错误处理
- 统一的错误处理机制
- 友好的用户提示

## 扩展指南

### 添加新页面
1. 在pages目录创建page_X.py
2. 在config.py的PAGES中添加配置
3. 在main.py中添加页面路由

### 添加新样式
1. 在styles.py中添加样式定义
2. 使用apply_styles()应用样式

### 添加新工具函数
1. 在helpers.py中添加函数
2. 更新__init__.py的导出列表

### 添加新AI模型
1. 在ai_models.py中添加模型类
2. 在ModelManager中注册模型

## 性能优化

### 缓存策略
- 页面内容使用@cached_function装饰器
- 模型实例使用@st.cache_resource
- 静态资源使用base64编码缓存

### 懒加载
- 图片资源按需加载
- 图表数据分页显示

### 代码优化
- 避免重复计算
- 使用向量化操作
- 减少不必要的重渲染

## 安全考虑

### 输入验证
- 所有用户输入进行验证
- 防止SQL注入和XSS攻击

### 资源保护
- 敏感配置不暴露在前端
- 文件上传类型限制

### 错误处理
- 不暴露系统内部错误
- 统一的错误提示

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 2.0.0 | 2025-02-21 | 重构项目结构，优化代码组织 |
| 1.0.0 | 2025-01-01 | 初始版本 |

---

**文档维护**: AI Assistant  
**最后更新**: 2025-02-21
