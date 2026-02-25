"""
通用工具函数模块
提供项目中常用的辅助函数
"""
import base64
import streamlit as st
from pathlib import Path
from typing import Optional, Union
import time
import hashlib
import json
from functools import wraps

# ==================== 图片处理函数 ====================
def get_image_base64(image_path: Union[str, Path]) -> Optional[str]:
    """将图片文件转换为base64编码
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        base64编码的字符串，如果失败返回None
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"图片文件未找到: {image_path}")
        return None
    except Exception as e:
        st.error(f"加载图片时出错: {e}")
        return None

def add_logo_to_sidebar(logo_path: Union[str, Path], width: int = 120) -> bool:
    """在侧边栏顶部添加Logo
    
    Args:
        logo_path: Logo图片路径
        width: 图片宽度
        
    Returns:
        是否成功添加
    """
    logo_base64 = get_image_base64(logo_path)
    if logo_base64:
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin: 20px 0;">
                <img src="data:image/png;base64,{logo_base64}" width="{width}">
            </div>
            """,
            unsafe_allow_html=True
        )
        return True
    return False

def set_background_image(image_path: Union[str, Path], opacity: float = 0.7) -> bool:
    """设置页面背景图片
    
    Args:
        image_path: 背景图片路径
        opacity: 遮罩透明度
        
    Returns:
        是否成功设置
    """
    image_base64 = get_image_base64(image_path)
    if image_base64:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{image_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, {opacity});
                z-index: -1;
            }}
            
            .main .block-container {{
                background: rgba(255, 255, 255, 0.85);
                border-radius: 10px;
                padding: 2rem;
                margin: 1rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        return True
    return False

# ==================== 缓存装饰器 ====================
class DataCache:
    """数据缓存装饰器类"""
    
    def __init__(self, max_size: int = 128, ttl: int = 3600):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存数量
            ttl: 缓存生存时间(秒)
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache = {}
        self._timestamps = {}
        
    def __call__(self, func):
        """装饰器实现"""
        @wraps(func)
        def wrapped(*args, **kwargs):
            cache_key = self._generate_key(func.__name__, args, kwargs)
            
            if cache_key in self._cache:
                timestamp = self._timestamps.get(cache_key, 0)
                if time.time() - timestamp < self.ttl:
                    return self._cache[cache_key]
            
            result = func(*args, **kwargs)
            self._cache[cache_key] = result
            self._timestamps[cache_key] = time.time()
            self._cleanup()
            
            return result
            
        return wrapped
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """生成缓存键"""
        args_str = str(args)[:100]
        kwargs_str = json.dumps(kwargs, sort_keys=True)[:100]
        key_str = f"{func_name}:{args_str}:{kwargs_str}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _cleanup(self):
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = [
            k for k, t in self._timestamps.items()
            if current_time - t > self.ttl
        ]
        
        for k in expired_keys:
            self._cache.pop(k, None)
            self._timestamps.pop(k, None)
        
        if len(self._cache) > self.max_size:
            oldest_key = min(self._timestamps.items(), key=lambda x: x[1])[0]
            self._cache.pop(oldest_key, None)
            self._timestamps.pop(oldest_key, None)
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self._timestamps.clear()
    
    def get_stats(self) -> dict:
        """获取缓存统计信息"""
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "ttl": self.ttl,
            "usage_percent": len(self._cache) / self.max_size * 100
        }

# 全局缓存实例
cache_manager = DataCache(max_size=256, ttl=1800)

def cached_function(func):
    """缓存装饰器快捷方式"""
    return cache_manager(func)

# ==================== UI组件函数 ====================
def create_gradient_header(title: str, subtitle: str = "") -> str:
    """创建渐变标题HTML
    
    Args:
        title: 主标题
        subtitle: 副标题
        
    Returns:
        HTML字符串
    """
    html = f"""
    <div style="text-align: center; padding: 30px 0;">
        <h1 class="gradient-text">{title}</h1>
        {f'<p style="color: rgba(255,255,255,0.7); font-size: 1.2rem;">{subtitle}</p>' if subtitle else ''}
        <div style="
            background: linear-gradient(90deg, transparent, #00c6ff, transparent);
            height: 3px;
            width: 400px;
            margin: 20px auto;
            border-radius: 2px;
        "></div>
    </div>
    """
    return html

def create_feature_tags(features: list) -> str:
    """创建功能标签HTML
    
    Args:
        features: 功能列表
        
    Returns:
        HTML字符串
    """
    tags_html = "".join([f'<span class="feature-tag">{f}</span>' for f in features])
    return f"<div style='margin: 16px 0;'>{tags_html}</div>"

def create_metric_card(value: str, label: str, delta: str = "") -> str:
    """创建指标卡片HTML
    
    Args:
        value: 数值
        label: 标签
        delta: 变化值
        
    Returns:
        HTML字符串
    """
    delta_html = f"<div style='color: #00F260; font-size: 0.9rem;'>{delta}</div>" if delta else ""
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """

def create_footer() -> str:
    """创建页脚HTML
    
    Returns:
        HTML字符串
    """
    return """
    <div class="footer">
        <p>Powered by <a href="#" target="_blank">数智化电磁驱动霍普金森杆多场耦合动态测试系统</a> | 2025 AI技术展示平台</p>
        <p style="margin-top: 10px; font-size: 0.9rem;">
            <span style="margin: 0 10px;">🚀 高性能</span> | 
            <span style="margin: 0 10px;">🔒 安全可信</span> | 
            <span style="margin: 0 10px;">🌍 数智化测试</span>
        </p>
    </div>
    """

def display_footer():
    """显示页脚"""
    st.markdown("---")
    st.markdown(create_footer(), unsafe_allow_html=True)

# ==================== 数据处理函数 ====================
def format_number(value: float, precision: int = 2, unit: str = "") -> str:
    """格式化数字显示
    
    Args:
        value: 数值
        precision: 小数位数
        unit: 单位
        
    Returns:
        格式化后的字符串
    """
    if abs(value) >= 1e9:
        return f"{value/1e9:.{precision}f} G{unit}"
    elif abs(value) >= 1e6:
        return f"{value/1e6:.{precision}f} M{unit}"
    elif abs(value) >= 1e3:
        return f"{value/1e3:.{precision}f} k{unit}"
    else:
        return f"{value:.{precision}f} {unit}"

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """安全除法
    
    Args:
        numerator: 分子
        denominator: 分母
        default: 默认值
        
    Returns:
        除法结果或默认值
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except:
        return default

# ==================== 错误处理函数 ====================
def handle_error(func):
    """错误处理装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ 操作失败: {str(e)}")
            return None
    return wrapper

def show_success_message(message: str):
    """显示成功消息"""
    st.success(f"✅ {message}")

def show_warning_message(message: str):
    """显示警告消息"""
    st.warning(f"⚠️ {message}")

def show_info_message(message: str):
    """显示信息消息"""
    st.info(f"ℹ️ {message}")

# ==================== 进度显示函数 ====================
def show_progress_bar(progress: float, text: str = ""):
    """显示进度条
    
    Args:
        progress: 进度值 (0-1)
        text: 进度文本
    """
    progress_bar = st.progress(0)
    progress_bar.progress(min(progress, 1.0))
    if text:
        st.text(text)

def simulate_progress(duration: float = 2.0, steps: int = 100):
    """模拟进度动画
    
    Args:
        duration: 总时长(秒)
        steps: 步数
    """
    progress_bar = st.progress(0)
    for i in range(steps):
        time.sleep(duration / steps)
        progress_bar.progress((i + 1) / steps)
    progress_bar.empty()
