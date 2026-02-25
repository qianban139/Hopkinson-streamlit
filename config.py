"""
项目配置文件
统一管理所有配置参数和路径设置
"""
import os
from pathlib import Path

# ==================== 项目路径配置 ====================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
CSS_DIR = ASSETS_DIR / "css"
COMPONENTS_DIR = BASE_DIR / "components"
UTILS_DIR = BASE_DIR / "utils"
PAGES_DIR = BASE_DIR / "pages"

# ==================== 图片资源路径 ====================
LOGO_PATH = IMAGES_DIR / "113.png"
BACKGROUND_PATH = IMAGES_DIR / "322.jpg"
FRONT_GIF_PATH = IMAGES_DIR / "front.gif"
SIDE_GIF_PATH = IMAGES_DIR / "side.gif"
ICON_PATH = IMAGES_DIR / "tu_biao.png"
UNIVERSITY_LOGO_PATH = IMAGES_DIR / "河南理工大学-logo-2048px.png"

# ==================== 页面配置 ====================
PAGE_CONFIG = {
    "page_title": "数智化电磁驱动霍普金森杆测试系统",
    "page_icon": "⚡",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ==================== 页面路由配置 ====================
PAGES = {
    "intro": {
        "file": "page_0.py",
        "title": "项目介绍",
        "icon": "🏠"
    },
    "control": {
        "file": "page_1.py",
        "title": "控制系统",
        "icon": "⚡"
    },
    "analysis": {
        "file": "page_2.py",
        "title": "数据分析",
        "icon": "📊"
    },
    "ai": {
        "file": "page_3.py",
        "title": "智能助手",
        "icon": "🤖"
    }
}

# ==================== 安全监控配置 ====================
SAFETY_THRESHOLDS = {
    "voltage": 1000.0,        # 电压阈值 (V)
    "current": 50.0,          # 电流阈值 (A)
    "temperature": 85.0,      # 温度阈值 (°C)
    "capacitor_charge": 0.9,  # 电容充电阈值
    "discharge_rate": 5.0,    # 放电速率阈值
}

SAFETY_LEVELS = {
    "normal": "🟢 正常",
    "warning": "🟡 警告",
    "danger": "🔴 危险",
    "critical": "⛔ 紧急"
}

# ==================== AI模型配置 ====================
LSTM_CONFIG = {
    "sequence_length": 50,
    "prediction_horizon": 10,
    "epochs": 100,
    "batch_size": 32,
    "learning_rate": 0.001
}

GAN_CONFIG = {
    "waveform_length": 100,
    "latent_dim": 100,
    "epochs": 10000,
    "batch_size": 32
}

# ==================== 材料数据库配置 ====================
MATERIALS_CONFIG = {
    "default_similarity_threshold": 0.7,
    "max_similar_materials": 5,
    "strain_rate_range": (0.001, 1000.0),
    "temperature_range": (100.0, 1500.0)
}

# ==================== 小波变换配置 ====================
WAVELET_CONFIG = {
    "default_wavelet": "db4",
    "default_level": 5,
    "default_threshold": 0.1
}

# ==================== 缓存配置 ====================
CACHE_CONFIG = {
    "max_size": 256,
    "ttl": 1800,  # 30分钟
    "enabled": True
}

# ==================== UI主题配置 ====================
THEME_CONFIG = {
    "primary_color": "#00dbde",
    "secondary_color": "#fc00ff",
    "accent_color": "#00F260",
    "background_gradient": "linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)",
    "card_background": "rgba(255, 255, 255, 0.08)",
    "text_color": "#e0e0e0",
    "border_color": "rgba(255, 255, 255, 0.18)"
}

# ==================== 分析场景配置 ====================
ANALYSIS_SCENARIOS = {
    "high_precision": {
        "description": "高精度模式",
        "wavelet_level": 8,
        "jc_iterations": 10000,
        "use_advanced_features": True,
        "cache_enabled": True,
        "suitable_for": ["small_data", "high_accuracy_required"]
    },
    "fast_processing": {
        "description": "快速处理模式",
        "wavelet_level": 3,
        "jc_iterations": 1000,
        "use_advanced_features": False,
        "cache_enabled": True,
        "suitable_for": ["large_data", "real_time"]
    },
    "balanced": {
        "description": "平衡模式",
        "wavelet_level": 5,
        "jc_iterations": 5000,
        "use_advanced_features": True,
        "cache_enabled": True,
        "suitable_for": ["medium_data", "general_purpose"]
    },
    "memory_efficient": {
        "description": "内存优化模式",
        "wavelet_level": 2,
        "jc_iterations": 500,
        "use_advanced_features": False,
        "cache_enabled": False,
        "suitable_for": ["very_large_data", "limited_memory"]
    }
}

# ==================== 辅助函数 ====================
def get_image_path(filename: str) -> Path:
    """获取图片文件的完整路径"""
    return IMAGES_DIR / filename

def check_assets() -> dict:
    """检查所有资源文件是否存在"""
    return {
        "logo": LOGO_PATH.exists(),
        "background": BACKGROUND_PATH.exists(),
        "front_gif": FRONT_GIF_PATH.exists(),
        "side_gif": SIDE_GIF_PATH.exists(),
        "icon": ICON_PATH.exists(),
        "university_logo": UNIVERSITY_LOGO_PATH.exists()
    }

def validate_config() -> bool:
    """验证配置是否完整"""
    required_paths = [ASSETS_DIR, IMAGES_DIR, COMPONENTS_DIR, UTILS_DIR, PAGES_DIR]
    return all(path.exists() for path in required_paths)
