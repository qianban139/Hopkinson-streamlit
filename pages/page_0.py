"""
项目介绍页面
展示数智化电磁驱动霍普金森杆测试系统的整体介绍和应用场景
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import FRONT_GIF_PATH, SIDE_GIF_PATH
from utils.helpers import (
    create_feature_tags, 
    create_metric_card,
    display_footer,
    cached_function
)
from assets.css.styles import apply_styles

# ==================== 应用样式 ====================
apply_styles(st, style_set="minimal")

# ==================== 缓存内容加载 ====================
@cached_function
def load_home_content() -> dict:
    """加载主页内容"""
    return {
        "title": "项目介绍界面",
        "icon": "💎",
        "main_title": "🤖 项目介绍",
        "overview": """
        **数智化电磁驱动霍普金森杆多场耦合动态测试系统**是通过电磁驱动-数字孪生-人工智能的深度融合，
        实现热-力-电多场耦合动态加载、智能波形调控、全链条数据融合三大核心突破，
        构建从"材料特性感知—动态加载控制—本构关系提取"的全流程数智化测试平台。
        
        该系统将显著提升电磁驱动霍普金森杆在材料适应性、信号可靠性、加载复杂性方面的核心性能，
        推动动态力学测试技术向更高层次发展。
        """,
        "core_tech": [
            "AI驱动的波形自适应调控技术",
            "多场耦合环境下的智能同步加载技术", 
            "电磁干扰智能抑制与高保真信号采集技术"
        ],
        "features": ["💬 智能对话", "📝 文本生成", "🔍 知识问答", "🌐 安全评估", "📊 数据分析"],
        "tech_specs": {
            "architecture": "Maxwell-Simplorer-Simulink",
            "physical_layer": "电磁驱动霍普金森杆主体",
            "digital_twin": "高保真多物理场耦合模型",
            "control_layer": "LSTM时序预测+GAN波形",
            "analysis_layer": "改进型Johnson-Cook模型"
        }
    }

@cached_function
def load_scenarios() -> dict:
    """加载应用场景内容"""
    return {
        "civil_engineering": {
            "title": "🎓 土木工程领域",
            "subtitle": "岩土路基动态稳定性评估与抗震设计",
            "content": {
                "background": "高速公路/铁路路基岩土易因列车动力载荷产生<span class='highlight'>松软变形、裂纹扩展</span>，需评估其动态力学特性以优化加固方案。",
                "solution": """采用<span class='tech-term'>电磁驱动霍普金森杆（E-Hopkinson杆）</span>结合<span class='tech-term'>XTDIC三维全场应变测量系统</span>，
                对岩土试样进行<span class='highlight'>高应变率（10²-10⁴/s）动态压缩/拉伸测试</span>。
                通过<span class='tech-term'>多级RLC链式电路</span>调控半正弦波至梯形波，匹配路基材料<span class='highlight'>恒应变率加载需求</span>；
                利用高速相机捕捉试样表面裂纹演化路径，结合<span class='tech-term'>动态本构方程（如Johnson-Cook模型）</span>提取应力-应变曲线。""",
                "highlight": "实现<span class='highlight'>'波形自适应调控-裂纹实时追踪-本构关系提取'全链条测试</span>，解决传统静态测试无法反映动态载荷下材料应变率效应的难题。",
                "effect": "为<span class='tech-term'>川藏铁路等重大工程</span>提供岩土路基动力稳定性评价数据，指导<span class='highlight'>路基厚度优化与土体加固措施</span>，降低地震/列车冲击导致的路基沉降风险。",
                "innovation": "本方案将电磁驱动技术与数字图像相关法结合，实现了岩土材料在高应变率下的精准力学表征。"
            }
        },
        "mining_engineering": {
            "title": "🏢 矿业工程领域",
            "subtitle": "深部岩石动态破碎与三轴应力耦合实验",
            "content": {
                "background": "深部矿产开采中岩石常面临<span class='highlight'>高应力、爆破冲击</span>等复杂动力学环境，需精准评估其裂纹扩展规律与破碎效率。",
                "solution": """依托<span class='tech-term'>动态三轴电磁霍普金森杆试验系统</span>，实现岩石试样在三维应力状态下的动态响应测试，
                结合<span class='tech-term'>数字孪生技术</span>和<span class='tech-term'>AI算法</span>优化爆破参数。
                通过电磁驱动产生可调<span class='tech-term'>幅值（0-600MPa）</span>、<span class='tech-term'>脉宽（300-800μs）</span>的应力波，
                结合<span class='highlight'>高速DIC视觉传感器阵列</span>实时监测岩石裂纹网络演化。""",
                "highlight": "实现<span class='highlight'>'真三轴六向应力脉冲纳秒级同步加载'</span>，解决深部岩石动态破碎机理不明、安全评估依据不足的难题。",
                "effect": "在深部矿山开采中成功预测围岩稳定性，<span class='highlight'>显著降低岩爆事故率</span>，提升开采安全性与效率。",
                "innovation": "突破传统单轴测试局限，为深部矿产资源安全高效开采提供关键技术支撑。"
            }
        },
        "safety_engineering": {
            "title": "🎮 安全科学与工程领域",
            "subtitle": "防火材料抗爆炸冲击性能评估",
            "content": {
                "background": "化工爆炸、火灾等事故中，防火材料需在<span class='highlight'>极端高温-冲击耦合环境</span>下保持结构完整性，传统静态测试无法反映其动态失效机制。",
                "solution": """利用<span class='tech-term'>电磁驱动霍普金森杆</span>进行防火材料的<span class='highlight'>高应变率热-力耦合测试</span>，
                结合<span class='tech-term'>自适应滤波算法</span>和<span class='tech-term'>小波变换</span>提取能量吸收特性。
                通过<span class='tech-term'>红外热像仪</span>与<span class='tech-term'>半导体应变片</span>同步监测试样温度场与应力场演化，
                基于<span class='highlight'>动态本构方程</span>提取材料在爆炸冲击下的能量吸收特性与失效阈值。""",
                "highlight": "实现<span class='highlight'>'热-力-电多场耦合动态加载-智能信号处理-本构关系高置信度提取'</span>全链条测试方案。",
                "effect": "在<span class='tech-term'>1000℃高温+50kA冲击电流</span>极端条件下验证材料性能，显著提升化工装置安全防护能力。",
                "innovation": "建立防火材料在爆炸冲击环境下的动态性能评估体系，为化工安全防护提供科学依据。"
            }
        }
    }

# ==================== 主内容区域 ====================
def main():
    """主函数"""
    # 加载内容
    home_content = load_home_content()
    scenarios = load_scenarios()
    
    # 主标题
    st.markdown(f'<h1 class="gradient-text">{home_content["main_title"]}</h1>', unsafe_allow_html=True)
    
    # 主要内容区域 - 两列布局
    col1, col2 = st.columns([2, 1])
    
    # 左侧主列 - 项目概览
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="subtitle">📋 项目概览</h2>', unsafe_allow_html=True)
        st.markdown(home_content["overview"])
        
        # 核心技术
        st.markdown("### 🔬 核心技术")
        for tech in home_content["core_tech"]:
            st.markdown(f"- {tech}")
        
        # 功能标签
        st.markdown("### 🔥 核心功能")
        st.markdown(create_feature_tags(home_content["features"]), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 右列 - 技术参数
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="subtitle">⚡ 技术参数</h3>', unsafe_allow_html=True)
        
        specs = home_content["tech_specs"]
        st.markdown(f"""
        <div style="margin-top: 20px;">
            <div style="margin-bottom: 16px;">
                <strong>架构类型:</strong><br>
                <span style="color: #00dbde;">{specs['architecture']}</span>
            </div>
            <div style="margin-bottom: 16px;">
                <strong>物理层:</strong><br>
                <span style="color: #00dbde;">{specs['physical_layer']}</span>
            </div>
            <div style="margin-bottom: 16px;">
                <strong>数字孪生层:</strong><br>
                <span style="color: #00dbde;">{specs['digital_twin']}</span>
            </div>
            <div style="margin-bottom: 16px;">
                <strong>智能控制层:</strong><br>
                <span style="color: #00dbde;">{specs['control_layer']}</span>
            </div>
            <div style="margin-bottom: 16px;">
                <strong>数据分析层:</strong><br>
                <span style="color: #00dbde;">{specs['analysis_layer']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 产品展示区域
    st.markdown('<div class="glass-card" style="margin-top: 32px;">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">🚀 产品展示</h2>', unsafe_allow_html=True)
    
    # 3D模型展示
    col1, col2 = st.columns(2)
    with col1:
        if FRONT_GIF_PATH.exists():
            st.image(str(FRONT_GIF_PATH), caption="正视图", use_container_width=True)
        else:
            st.info("正视图资源缺失")
    with col2:
        if SIDE_GIF_PATH.exists():
            st.image(str(SIDE_GIF_PATH), caption="侧视图", use_container_width=True)
        else:
            st.info("侧视图资源缺失")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 应用场景区域
    st.markdown('<div class="glass-card" style="margin-top: 32px;">', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">🚀 应用场景</h2>', unsafe_allow_html=True)
    
    # 创建标签页
    tab1, tab2, tab3 = st.tabs([
        scenarios["civil_engineering"]["title"], 
        scenarios["mining_engineering"]["title"], 
        scenarios["safety_engineering"]["title"]
    ])
    
    # 土木工程
    with tab1:
        civ = scenarios["civil_engineering"]
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin: 10px 0;">
            <h4 style="color: #00dbde;">{civ['title']}</h4>
            <p style="font-size: 16px;">{civ['subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="tech-card animate-content">
            <div class="section-title">🔬 问题背景</div>
            <p>{civ['content']['background']}</p>
            <div class="section-title">💡 解决方案</div>
            <p>{civ['content']['solution']}</p>
            <div class="section-title">✨ 技术亮点</div>
            <p>{civ['content']['highlight']}</p>
            <div class="section-title">📈 应用效果</div>
            <p>{civ['content']['effect']}</p>
            <div class="quote-box">
                <strong>创新价值：</strong>{civ['content']['innovation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 矿业工程
    with tab2:
        mine = scenarios["mining_engineering"]
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin: 10px 0;">
            <h4 style="color: #00dbde;">{mine['title']}</h4>
            <p style="font-size: 16px;">{mine['subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="tech-card animate-content">
            <div class="section-title">⛏️ 问题背景</div>
            <p>{mine['content']['background']}</p>
            <div class="section-title">🔧 解决方案</div>
            <p>{mine['content']['solution']}</p>
            <div class="section-title">💎 技术亮点</div>
            <p>{mine['content']['highlight']}</p>
            <div class="section-title">📊 应用效果</div>
            <p>{mine['content']['effect']}</p>
            <div class="quote-box">
                <strong>创新价值：</strong>{mine['content']['innovation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 安全工程
    with tab3:
        safe = scenarios["safety_engineering"]
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin: 10px 0;">
            <h4 style="color: #00dbde;">{safe['title']}</h4>
            <p style="font-size: 16px;">{safe['subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="tech-card animate-content">
            <div class="section-title">🔥 问题背景</div>
            <p>{safe['content']['background']}</p>
            <div class="section-title">🔬 解决方案</div>
            <p>{safe['content']['solution']}</p>
            <div class="section-title">💡 技术亮点</div>
            <p>{safe['content']['highlight']}</p>
            <div class="section-title">📈 应用效果</div>
            <p>{safe['content']['effect']}</p>
            <div class="quote-box">
                <strong>创新价值：</strong>{safe['content']['innovation']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    


if __name__ == "__main__":
    main()
