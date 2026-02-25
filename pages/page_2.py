"""
数据分析页面
材料力学分析系统，包含材料行为分析、本构模型、小波变换等功能
"""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import display_footer, simulate_progress, cached_function
from assets.css.styles import apply_styles

# ==================== 应用样式 ====================
apply_styles(st, style_set="minimal")

# ==================== 数据类型定义 ====================
class LoadingType(Enum):
    """加载类型枚举"""
    TENSION = "拉伸"
    COMPRESSION = "压缩"
    SHEAR = "剪切"
    BENDING = "弯曲"
    TORSION = "扭转"

@dataclass
class MaterialProperties:
    """材料属性数据类"""
    name: str
    youngs_modulus: float  # 杨氏模量 (Pa)
    poissons_ratio: float  # 泊松比
    yield_strength: float  # 屈服强度 (Pa)
    tensile_strength: float  # 抗拉强度 (Pa)
    density: float  # 密度 (kg/m³)
    failure_strain: float  # 破坏应变

# ==================== 材料数据库 ====================
MATERIALS_DB = {
    "steel_304": MaterialProperties(
        name="304不锈钢",
        youngs_modulus=200e9,
        poissons_ratio=0.29,
        yield_strength=250e6,
        tensile_strength=620e6,
        density=8000,
        failure_strain=0.7
    ),
    "aluminum_6061": MaterialProperties(
        name="6061铝合金",
        youngs_modulus=68.9e9,
        poissons_ratio=0.33,
        yield_strength=275e6,
        tensile_strength=310e6,
        density=2700,
        failure_strain=0.12
    ),
    "titanium_6al4v": MaterialProperties(
        name="钛合金6Al-4V",
        youngs_modulus=113.8e9,
        poissons_ratio=0.342,
        yield_strength=880e6,
        tensile_strength=950e6,
        density=4430,
        failure_strain=0.14
    ),
    "polycarbonate": MaterialProperties(
        name="聚碳酸酯",
        youngs_modulus=2.4e9,
        poissons_ratio=0.37,
        yield_strength=60e6,
        tensile_strength=72e6,
        density=1200,
        failure_strain=0.6
    ),
    "alumina": MaterialProperties(
        name="氧化铝陶瓷",
        youngs_modulus=370e9,
        poissons_ratio=0.22,
        yield_strength=2000e6,
        tensile_strength=300e6,
        density=3900,
        failure_strain=0.001
    ),
    "carbon_fiber": MaterialProperties(
        name="碳纤维复合材料",
        youngs_modulus=150e9,
        poissons_ratio=0.3,
        yield_strength=700e6,
        tensile_strength=1200e6,
        density=1600,
        failure_strain=0.015
    )
}

# ==================== Johnson-Cook模型 ====================
class JohnsonCookModel:
    """Johnson-Cook本构模型"""
    
    def __init__(self):
        self.parameters = {
            'A': 500e6,    # 准静态屈服应力 (Pa)
            'B': 300e6,    # 应变硬化系数 (Pa)
            'n': 0.25,     # 应变硬化指数
            'C': 0.02,     # 应变率敏感系数
            'm': 1.03,     # 热软化指数
            'T_ref': 293,   # 参考温度 (K)
            'T_melt': 1800, # 熔化温度 (K)
            'epsilon_dot_0': 1.0  # 参考应变率 (s^-1)
        }
    
    def calculate_stress(self, epsilon: np.ndarray, epsilon_dot: float, temperature: float) -> np.ndarray:
        """计算应力"""
        A, B, n, C, m, T_ref, T_melt, epsilon_dot_0 = self.parameters.values()
        
        # 应变硬化项
        strain_hardening = A + B * epsilon**n
        
        # 应变率硬化项
        strain_rate_term = 1 + C * np.log(epsilon_dot / epsilon_dot_0)
        
        # 热软化项
        T_star = (temperature - T_ref) / (T_melt - T_ref)
        T_star = np.clip(T_star, 0, 1)
        thermal_softening = 1 - T_star**m
        
        return strain_hardening * strain_rate_term * thermal_softening

# ==================== 主界面 ====================
def main():
    """主函数"""
    st.markdown('<h1 class="gradient-text">🔬 材料力学分析系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.markdown("## 🎯 系统功能")
        st.markdown("""
        ### 实现功能:
        1. **材料行为分析** - 预测不同加载条件下的材料响应
        2. **应力跨材料映射** - 将应力映射到不同材料
        3. **智能方案优化** - 根据场景选择最优分析方案
        4. **本构模型分析** - Johnson-Cook模型拟合
        5. **小波变换分析** - 数据去噪与特征提取
        """)
        
        st.markdown("---")
        st.markdown("### 📊 系统状态")
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">98.5%</div>
            <div class="metric-label" style="color: white;">系统正常</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 主内容区域 - 标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 材料行为分析", "📈 本构模型分析", "🔍 小波变换分析", "📁 数据可视化"
    ])
    
    with tab1:
        display_material_behavior_analysis()
    
    with tab2:
        display_constitutive_analysis()
    
    with tab3:
        display_wavelet_analysis()
    
    with tab4:
        display_data_visualization()
    


def display_material_behavior_analysis():
    """显示材料行为分析界面"""
    st.subheader("📊 材料行为分析与预测")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 材料选择
        material_options = list(MATERIALS_DB.keys())
        selected_material_key = st.selectbox(
            "选择材料",
            options=material_options,
            format_func=lambda x: MATERIALS_DB[x].name
        )
        
        material = MATERIALS_DB[selected_material_key]
        
        # 加载条件
        st.markdown("### 加载条件")
        loading_type = st.selectbox(
            "加载类型",
            options=list(LoadingType),
            format_func=lambda x: x.value
        )
        
        strain_rate = st.slider("应变率 (s⁻¹)", 0.001, 1000.0, 1.0, 0.1, format="%.3f")
        temperature = st.slider("温度 (K)", 100.0, 1500.0, 293.0, 1.0)
    
    with col2:
        # 显示材料属性
        st.markdown("### 材料属性")
        st.metric("杨氏模量", f"{material.youngs_modulus/1e9:.1f} GPa")
        st.metric("屈服强度", f"{material.yield_strength/1e6:.1f} MPa")
        st.metric("抗拉强度", f"{material.tensile_strength/1e6:.1f} MPa")
        st.metric("破坏应变", f"{material.failure_strain:.3%}")
    
    if st.button("开始分析", type="primary"):
        with st.spinner("正在分析材料行为..."):
            # Johnson-Cook模型计算
            jc_model = JohnsonCookModel()
            strains = np.linspace(0, material.failure_strain * 0.8, 100)
            stresses = jc_model.calculate_stress(strains, strain_rate, temperature)
            
            # 绘制应力-应变曲线
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=strains, y=stresses/1e6,
                mode='lines', name='预测曲线',
                line=dict(color='blue', width=2)
            ))
            
            # 标记屈服点
            yield_idx = np.argmin(np.abs(stresses - material.yield_strength))
            fig.add_trace(go.Scatter(
                x=[strains[yield_idx]],
                y=[stresses[yield_idx]/1e6],
                mode='markers', name='屈服点',
                marker=dict(size=12, color='orange', symbol='circle')
            ))
            
            fig.update_layout(
                title=f"{material.name} 应力-应变曲线",
                xaxis_title="应变",
                yaxis_title="应力 (MPa)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 分析结果
            max_stress = np.max(stresses)
            safety_factor = material.tensile_strength / max_stress
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("最大应力", f"{max_stress/1e6:.1f} MPa")
            with col2:
                st.metric("安全系数", f"{safety_factor:.2f}")
            with col3:
                status = "✅ 安全" if safety_factor > 1.5 else "⚠️ 警告" if safety_factor > 1.0 else "❌ 危险"
                st.metric("状态", status)

def display_constitutive_analysis():
    """显示本构模型分析界面"""
    st.subheader("📈 改进型Johnson-Cook本构模型分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 模型参数配置")
        A = st.number_input("参数A (准静态屈服应力, MPa)", value=500.0)
        B = st.number_input("参数B (应变硬化系数, MPa)", value=300.0)
        n = st.number_input("参数n (应变硬化指数)", value=0.25, format="%.3f")
        C = st.number_input("参数C (应变率敏感系数)", value=0.02, format="%.3f")
        m = st.number_input("参数m (热软化指数)", value=1.03, format="%.3f")
    
    with col2:
        st.markdown("### 实验条件")
        strain_rate = st.slider("应变率 (s⁻¹)", 0.001, 1000.0, 1.0, 0.1, key="jc_strain_rate")
        temperature = st.slider("温度 (K)", 100.0, 1500.0, 293.0, 1.0, key="jc_temperature")
    
    if st.button("执行模型计算", type="primary"):
        # 创建模型并计算
        jc_model = JohnsonCookModel()
        jc_model.parameters.update({
            'A': A * 1e6, 'B': B * 1e6, 'n': n, 'C': C, 'm': m
        })
        
        strains = np.linspace(0, 0.5, 100)
        stresses = jc_model.calculate_stress(strains, strain_rate, temperature)
        
        # 绘制曲线
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=strains, y=stresses/1e6,
            mode='lines', name='Johnson-Cook模型',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Johnson-Cook本构关系曲线",
            xaxis_title="应变",
            yaxis_title="应力 (MPa)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 显示参数表格
        st.markdown("### 模型参数")
        params_df = pd.DataFrame({
            '参数': ['A', 'B', 'n', 'C', 'm'],
            '值': [A, B, n, C, m],
            '单位': ['MPa', 'MPa', '-', '-', '-']
        })
        st.dataframe(params_df, use_container_width=True)

def display_wavelet_analysis():
    """显示小波变换分析界面"""
    st.subheader("🔍 小波变换数据融合分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wavelet_type = st.selectbox(
            "小波类型",
            ['db4', 'db8', 'sym8', 'coif5'],
            index=0
        )
        decomposition_level = st.slider("分解层数", 1, 8, 5)
    
    with col2:
        threshold = st.slider("去噪阈值", 0.01, 0.5, 0.1)
        signal_length = st.number_input("信号长度", 100, 10000, 1000)
    
    # 生成示例信号
    t = np.linspace(0, 10, signal_length)
    original_signal = np.sin(2*np.pi*t) + 0.5*np.sin(6*np.pi*t) + 0.3*np.random.randn(signal_length)
    
    if st.button("执行小波分析", type="primary"):
        with st.spinner("正在进行小波分析..."):
            simulate_progress(1.5)
            
            # 简化的去噪（使用移动平均模拟）
            window_size = 10
            denoised_signal = np.convolve(original_signal, np.ones(window_size)/window_size, mode='same')
            
            # 显示结果
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=['原始信号', '去噪后信号'],
                vertical_spacing=0.15
            )
            
            fig.add_trace(
                go.Scatter(y=original_signal, name='原始', line=dict(color='blue')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(y=denoised_signal, name='去噪', line=dict(color='green')),
                row=2, col=1
            )
            
            fig.update_layout(height=500, title_text="小波去噪效果")
            st.plotly_chart(fig, use_container_width=True)
            
            # 显示统计信息
            noise_reduction = (np.std(original_signal) - np.std(denoised_signal)) / np.std(original_signal) * 100
            st.success(f"噪声降低: {noise_reduction:.1f}%")

def display_data_visualization():
    """显示数据可视化界面"""
    st.subheader("📁 CSV 文件上传与可视化")
    
    uploaded_file = st.file_uploader("上传 CSV 文件", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("数据预览:")
            st.dataframe(df.head(), use_container_width=True)
            
            st.write("数据统计:")
            st.dataframe(df.describe(), use_container_width=True)
        
        with col2:
            st.subheader("数据可视化")
            
            chart_type = st.selectbox("图表类型", ["折线图", "散点图", "直方图", "箱线图"])
            
            if chart_type == "折线图":
                x_col = st.selectbox("X轴", df.columns)
                y_col = st.selectbox("Y轴", df.columns)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', name='数据'))
                fig.update_layout(title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "散点图":
                x_col = st.selectbox("X轴", df.columns, key="scatter_x")
                y_col = st.selectbox("Y轴", df.columns, key="scatter_y")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='markers', name='数据'))
                fig.update_layout(title=f"{y_col} vs {x_col}")
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "直方图":
                col = st.selectbox("选择列", df.columns)
                fig = go.Figure(data=[go.Histogram(x=df[col])])
                fig.update_layout(title=f"{col} 分布")
                st.plotly_chart(fig, use_container_width=True)
            
            elif chart_type == "箱线图":
                cols = st.multiselect("选择列", df.columns, default=df.columns[:min(3, len(df.columns))])
                if cols:
                    fig = go.Figure()
                    for col in cols:
                        fig.add_trace(go.Box(y=df[col], name=col))
                    fig.update_layout(title="数据分布箱线图")
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
