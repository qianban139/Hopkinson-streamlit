"""
数智化电磁驱动霍普金森杆测试系统 - 主程序
============================================
这是一个基于Streamlit的Web应用，用于展示数智化电磁驱动霍普金森杆测试系统。
系统包含项目介绍、控制系统、数据分析和智能助手四大模块。

作者: AI Assistant
版本: 2.0.0
日期: 2025-02-21
"""

import streamlit as st
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入配置
from config import PAGE_CONFIG, PAGES, LOGO_PATH, BACKGROUND_PATH, check_assets

# 导入工具函数
from utils.helpers import (
    add_logo_to_sidebar, 
    set_background_image,
    create_gradient_header,
    display_footer
)

# 导入样式
from assets.css.styles import apply_styles

# ==================== 页面配置 ====================
st.set_page_config(**PAGE_CONFIG)

# ==================== 应用样式 ====================
apply_styles(st, style_set="all")

# ==================== 隐藏默认元素 ====================
st.markdown("""
<style>
    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stApp > header { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ==================== 检查资源文件 ====================
asset_status = check_assets()
missing_assets = [k for k, v in asset_status.items() if not v]
if missing_assets:
    st.warning(f"⚠️ 以下资源文件缺失: {', '.join(missing_assets)}")

# ==================== 侧边栏Logo ====================
if asset_status.get('logo'):
    add_logo_to_sidebar(LOGO_PATH, width=180)

# ==================== 页面标题 ====================
st.markdown(create_gradient_header(
    "数智化电磁驱动霍普金森杆测试系统",
    "数智化测试平台 | AI驱动 | 多场耦合"
), unsafe_allow_html=True)

# ==================== 设置背景 ====================
if asset_status.get('background'):
    set_background_image(BACKGROUND_PATH, opacity=0.85)

# ==================== 页面路由 ====================
page_intro = st.Page("pages/page_0.py", title=PAGES['intro']['title'], icon=PAGES['intro']['icon'])
page_control = st.Page("pages/page_1.py", title=PAGES['control']['title'], icon=PAGES['control']['icon'])
page_analysis = st.Page("pages/page_2.py", title=PAGES['analysis']['title'], icon=PAGES['analysis']['icon'])
page_ai = st.Page("pages/page_3.py", title=PAGES['ai']['title'], icon=PAGES['ai']['icon'])

# ==================== 导航菜单 ====================
pg = st.navigation([page_intro, page_control, page_analysis, page_ai])
pg.run()

# ==================== 页脚 ====================
display_footer()
