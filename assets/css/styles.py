"""
统一的CSS样式管理模块
集中管理所有页面的CSS样式，便于维护和复用
"""

# ==================== 基础样式 ====================
BASE_STYLES = """
<style>
    /* 引入外部字体和动画库 */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap');

    /* 全局基础样式 */
    body {
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e0e0e0;
        margin: 0;
        padding: 0;
    }

    /* 主容器背景 */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    /* 隐藏Streamlit默认元素 */
    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stApp > header { display: none !important; }
</style>
"""

# ==================== 玻璃拟态卡片样式 ====================
GLASS_CARD_STYLES = """
<style>
    /* 毛玻璃效果卡片 - 基础样式 */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }

    /* 卡片悬停效果 */
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        background: rgba(255, 255, 255, 0.12);
    }

    /* 技术卡片 - 带流光效果 */
    .tech-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.25);
        padding: 32px;
        margin: 24px 0;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }

    .tech-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.6s;
    }

    .tech-card:hover::before {
        left: 100%;
    }

    .tech-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 60px rgba(31, 38, 135, 0.4);
        background: rgba(255, 255, 255, 0.12);
    }
</style>
"""

# ==================== 文字样式 ====================
TEXT_STYLES = """
<style>
    /* 渐变主标题 - 动态效果 */
    .gradient-text {
        background: linear-gradient(45deg, #00dbde, #fc00ff, #00dbde, #fc00ff);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-fill-color: transparent;
        animation: gradientShift 4s ease infinite;
        font-weight: 800;
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 32px;
        letter-spacing: -1px;
        font-family: 'Montserrat', sans-serif;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 副标题渐变样式 */
    .subtitle {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 50%, #00F260 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 24px 0 16px 0;
        font-family: 'Montserrat', sans-serif;
    }

    /* 章节标题样式 */
    .section-title {
        background: linear-gradient(90deg, #00dbde, #00F260);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(0, 219, 222, 0.3);
        display: inline-block;
        font-family: 'Montserrat', sans-serif;
    }

    /* 重点高亮文本 */
    .highlight {
        background: linear-gradient(120deg, rgba(0, 219, 222, 0.2) 0%, rgba(252, 0, 255, 0.2) 100%);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        color: #ffffff;
        border-left: 3px solid #00dbde;
    }

    /* 技术术语样式 */
    .tech-term {
        color: #00F260;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 242, 96, 0.3);
    }

    /* 引用框样式 */
    .quote-box {
        background: rgba(0, 219, 222, 0.1);
        border-left: 4px solid #00dbde;
        padding: 16px 20px;
        margin: 20px 0;
        border-radius: 0 12px 12px 0;
        font-style: italic;
    }
</style>
"""

# ==================== 组件样式 ====================
COMPONENT_STYLES = """
<style>
    /* 功能标签样式 */
    .feature-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 6px 16px;
        margin: 6px;
        font-size: 0.9rem;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.2s ease;
    }

    .feature-tag:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: scale(1.05);
    }

    /* 指标卡片容器 */
    .metric-card {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: scale(1.03);
    }

    /* 指标数值样式 */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #00dbde, #fc00ff);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-fill-color: transparent;
        font-family: 'Montserrat', sans-serif;
    }

    /* 指标标签样式 */
    .metric-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 8px;
        font-family: 'Montserrat', sans-serif;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(45deg, #1e9fff, #0062cc);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(31, 38, 135, 0.4);
    }

    /* 链接样式 */
    a {
        color: #00dbde;
        text-decoration: none;
        transition: color 0.2s ease;
    }

    a:hover {
        color: #fc00ff;
    }

    /* 输入框样式增强 */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
        color: white !important;
        font-family: 'Montserrat', sans-serif;
    }

    /* 进度条样式 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00dbde, #fc00ff) !important;
    }
</style>
"""

# ==================== 标签页样式 ====================
TAB_STYLES = """
<style>
    /* 标签页样式 */
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-size: 16px !important;
        font-weight: 600;
        padding: 10px 20px;
        color: rgba(255, 255, 255, 0.7);
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px 8px 0 0;
        margin-right: 4px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #00dbde;
        background: rgba(255, 255, 255, 0.1);
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(45deg, #00dbde, #fc00ff) !important;
        font-weight: 700;
    }
</style>
"""

# ==================== 动画样式 ====================
ANIMATION_STYLES = """
<style>
    /* 淡入上移动画 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animate-content {
        animation: fadeInUp 0.8s ease-out;
    }

    /* 脉冲动画 */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    .pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }

    /* 旋转动画 */
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .spin {
        animation: spin 1s linear infinite;
    }
</style>
"""

# ==================== 响应式设计 ====================
RESPONSIVE_STYLES = """
<style>
    /* 移动端适配 */
    @media (max-width: 768px) {
        .gradient-text {
            font-size: 2.5rem;
        }
        .subtitle {
            font-size: 1.5rem;
        }
        .tech-card {
            padding: 24px 20px;
            margin: 20px 0;
        }
        .section-title {
            font-size: 1.5rem;
        }
    }

    /* 大屏幕优化 */
    @media (min-width: 1200px) {
        .gradient-text {
            font-size: 4rem;
        }
        .glass-card {
            padding: 32px;
        }
    }
</style>
"""

# ==================== 安全监控样式 ====================
SAFETY_STYLES = """
<style>
    /* 安全状态指示器 */
    .safety-indicator {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        text-align: center;
        font-weight: bold;
    }

    .safety-normal { 
        background-color: rgba(0, 255, 0, 0.2); 
        border: 1px solid #00ff00; 
    }
    .safety-warning { 
        background-color: rgba(255, 255, 0, 0.2); 
        border: 1px solid #ffff00; 
    }
    .safety-danger { 
        background-color: rgba(255, 0, 0, 0.2); 
        border: 1px solid #ff0000; 
    }
    .safety-critical { 
        background-color: rgba(255, 0, 0, 0.4); 
        border: 2px solid #ff0000; 
    }
</style>
"""

# ==================== 页脚样式 ====================
FOOTER_STYLES = """
<style>
    /* 页脚样式 */
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: rgba(255, 255, 255, 0.6);
        background: rgba(0, 0, 0, 0.2);
        border-radius: 16px;
        margin-top: 40px;
    }

    .footer p {
        margin: 8px 0;
    }

    .footer a {
        color: #00dbde;
        text-decoration: none;
    }

    .footer a:hover {
        color: #fc00ff;
    }
</style>
"""

# ==================== 组合样式 ====================
def get_all_styles() -> str:
    """获取所有样式的组合"""
    return (
        BASE_STYLES + 
        GLASS_CARD_STYLES + 
        TEXT_STYLES + 
        COMPONENT_STYLES + 
        TAB_STYLES + 
        ANIMATION_STYLES + 
        RESPONSIVE_STYLES + 
        SAFETY_STYLES + 
        FOOTER_STYLES
    )

def get_minimal_styles() -> str:
    """获取最小化样式组合（用于简单页面）"""
    return BASE_STYLES + GLASS_CARD_STYLES + TEXT_STYLES + COMPONENT_STYLES

def apply_styles(st, style_set: str = "all"):
    """应用样式到Streamlit页面
    
    Args:
        st: Streamlit对象
        style_set: 样式集合类型 ("all" | "minimal" | "base")
    """
    if style_set == "all":
        st.markdown(get_all_styles(), unsafe_allow_html=True)
    elif style_set == "minimal":
        st.markdown(get_minimal_styles(), unsafe_allow_html=True)
    elif style_set == "base":
        st.markdown(BASE_STYLES, unsafe_allow_html=True)
