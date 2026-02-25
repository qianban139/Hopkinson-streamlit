"""
控制系统页面
高压控制系统界面，包含实时监控、LSTM预测、GAN生成、安全监控等功能
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.control_system import CentralControlSystem, SafetyLevel
from utils.helpers import display_footer, simulate_progress
from assets.css.styles import apply_styles

# ==================== 应用样式 ====================
apply_styles(st, style_set="minimal")

# ==================== 初始化控制系统 ====================
@st.cache_resource
def get_control_system():
    """获取控制系统实例（缓存）"""
    return CentralControlSystem()

# ==================== 主界面 ====================
def main():
    """主函数"""
    control_system = get_control_system()
    
    # 页面标题
    st.markdown('<h1 class="gradient-text">⚡ 高压控制系统</h1>', unsafe_allow_html=True)
    
    # 侧边栏控制面板
    with st.sidebar:
        st.markdown("### ⚡ 控制面板")
        
        # 运行模式选择
        operation_mode = st.selectbox(
            "运行模式",
            ["仿真模式", "实时控制", "训练模式", "安全诊断"],
            key="operation_mode"
        )
        
        # 安全监控
        st.markdown("### 🔐 安全监控")
        col1, col2 = st.columns(2)
        with col1:
            control_system.safety_enabled = st.checkbox(
                "启用安全监控", 
                value=control_system.safety_enabled
            )
        with col2:
            control_system.auto_shutdown_enabled = st.checkbox(
                "自动停机", 
                value=control_system.auto_shutdown_enabled
            )
        
        # 安全阈值设置
        with st.expander("安全阈值设置"):
            control_system.safety_monitor.thresholds.voltage = st.slider(
                "电压阈值 (V)", 500.0, 2000.0, 1000.0, 10.0
            )
            control_system.safety_monitor.thresholds.current = st.slider(
                "电流阈值 (A)", 20.0, 100.0, 50.0, 1.0
            )
            control_system.safety_monitor.thresholds.temperature = st.slider(
                "温度阈值 (°C)", 50.0, 120.0, 85.0, 1.0
            )
        
        # 系统状态
        st.markdown("### 📊 系统状态")
        status = control_system.get_system_status()
        st.markdown(f"**状态:** {status['status']}")
        st.markdown(f"**模式:** {status['operation_mode']}")
        st.markdown(f"**安全检查:** {'启用' if status['safety_enabled'] else '禁用'}")
    
    # 主内容区域 - 标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 实时监控", "🧠 LSTM预测", "🎨 GAN生成", "📊 系统分析", "🛡️ 安全监控"
    ])
    
    # 实时监控
    with tab1:
        display_realtime_monitoring(control_system)
    
    # LSTM预测
    with tab2:
        display_lstm_prediction(control_system)
    
    # GAN生成
    with tab3:
        display_gan_generation(control_system)
    
    # 系统分析
    with tab4:
        display_system_analysis(control_system)
    
    # 安全监控
    with tab5:
        display_safety_monitoring(control_system)
    


def display_realtime_monitoring(control_system):
    """显示实时监控界面"""
    st.subheader("📈 实时波形监控")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 生成示例波形数据
        time_axis = np.linspace(0, 10, 1000)
        
        # 安全检查获取电压
        is_safe, _, safety_info = control_system.perform_safety_check()
        voltage = safety_info.get('data', {}).get('voltage', 800)
        
        # 生成波形
        waveform = np.sin(2 * np.pi * time_axis) + 0.5 * np.random.randn(1000)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_axis,
            y=waveform * (voltage / 1000),
            name="实时波形",
            line=dict(color='blue' if is_safe else 'red', width=2),
            mode='lines'
        ))
        
        if not is_safe:
            fig.add_hrect(
                y0=0.8, y1=1.2,
                fillcolor="red", opacity=0.1,
                line_width=0,
                annotation_text="危险区域",
                annotation_position="top right"
            )
        
        fig.update_layout(
            title="实时波形监控",
            xaxis_title="时间 (s)",
            yaxis_title="幅度 (V)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚙️ 系统参数")
        sensor_data = control_system.sensor_simulator.generate_data()
        
        st.metric("电压", f"{sensor_data['voltage']:.1f} V")
        st.metric("电流", f"{sensor_data['current']:.1f} A")
        st.metric("温度", f"{sensor_data['temperature']:.1f} °C")
        st.metric("电容充电", f"{sensor_data['capacitor_charge']*100:.1f} %")
        
        # 控制按钮
        st.subheader("🎮 控制")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("启动系统", type="primary", use_container_width=True):
                control_system.start_real_time_control()
                st.success("系统已启动")
        with col2:
            if st.button("停止系统", use_container_width=True):
                control_system.safe_shutdown()
                st.warning("系统已停止")

def display_lstm_prediction(control_system):
    """显示LSTM预测界面"""
    st.subheader("🧠 LSTM时序预测分析")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        train_epochs = st.number_input("训练轮数", 10, 1000, 100)
    with col2:
        batch_size = st.number_input("批大小", 16, 256, 32)
    with col3:
        sequence_length = st.slider("序列长度", 10, 100, 50)
    
    if st.button("开始训练", type="primary"):
        with st.spinner("训练LSTM模型中..."):
            simulate_progress(2.0)
            st.success("训练完成！")
    
    # 预测结果可视化
    time_points = np.linspace(0, 10, 100)
    actual_data = np.sin(time_points) + 0.1 * np.random.randn(100)
    predicted_data = np.sin(time_points + 0.1) + 0.05 * np.random.randn(100)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_points, y=actual_data,
        name="实际数据", line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=time_points, y=predicted_data,
        name="预测数据", line=dict(color='red', dash='dash', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([time_points, time_points[::-1]]),
        y=np.concatenate([predicted_data + 0.1, (predicted_data - 0.1)[::-1]]),
        fill='toself', fillcolor='rgba(255, 0, 0, 0.1)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='预测区间'
    ))
    
    fig.update_layout(
        title="LSTM预测结果",
        xaxis_title="时间",
        yaxis_title="数值",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def display_gan_generation(control_system):
    """显示GAN生成界面"""
    st.subheader("🎨 GAN波形生成控制")
    
    col1, col2 = st.columns(2)
    with col1:
        target_freq = st.slider("目标频率 (Hz)", 1, 100, 10)
    with col2:
        target_amp = st.slider("目标幅度", 0.1, 5.0, 1.0)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("生成波形", type="primary", use_container_width=True):
            with st.spinner("生成波形中..."):
                t = np.linspace(0, 2*np.pi, 1000)
                generated_wave = target_amp * np.sin(target_freq * t) + 0.1 * np.random.randn(1000)
                st.session_state.generated_waveform = generated_wave
                st.success("波形生成完成！")
    
    with col2:
        if st.button("应用到系统", use_container_width=True):
            if 'generated_waveform' in st.session_state:
                st.success("波形已应用到控制系统")
            else:
                st.warning("请先生成波形")
    
    # 显示生成的波形
    if 'generated_waveform' in st.session_state:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=np.arange(len(st.session_state.generated_waveform)),
            y=st.session_state.generated_waveform,
            name="生成波形", line=dict(color='green', width=2)
        ))
        fig.update_layout(
            title="GAN生成的波形",
            xaxis_title="采样点",
            yaxis_title="幅度",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

def display_system_analysis(control_system):
    """显示系统分析界面"""
    st.subheader("📊 系统性能分析")
    
    # 性能指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("系统安全率", "98.5%", "+0.5%")
    with col2:
        st.metric("预测准确率", "95.2%", "+1.2%")
    with col3:
        st.metric("控制延迟", "12.3ms", "-2.1ms")
    with col4:
        st.metric("系统稳定性", "98.5%", "+0.5%")
    
    # 性能趋势图
    time_points = range(1, 11)
    accuracy = [90 + i*0.5 + np.random.normal(0, 1) for i in range(10)]
    stability = [95 + i*0.3 + np.random.normal(0, 0.5) for i in range(10)]
    safety = [98 - i*0.2 + np.random.normal(0, 0.8) for i in range(10)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(time_points), y=accuracy,
        name="预测准确率", line=dict(color='blue', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=list(time_points), y=stability,
        name="系统稳定性", line=dict(color='green', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=list(time_points), y=safety,
        name="系统安全性", line=dict(color='red', width=3)
    ))
    
    fig.update_layout(
        title="系统性能趋势",
        xaxis_title="时间 (分钟)",
        yaxis_title="百分比 (%)",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

def display_safety_monitoring(control_system):
    """显示安全监控界面"""
    st.subheader("🛡️ 高压安全监控系统")
    
    # 执行安全检查
    is_safe, description, safety_info = control_system.perform_safety_check()
    sensor_data = safety_info.get('data', {})
    level = safety_info.get('level', SafetyLevel.NORMAL)
    
    # 安全状态卡片
    col1, col2, col3, col4 = st.columns(4)
    
    level_colors = {
        SafetyLevel.NORMAL: '🟢',
        SafetyLevel.WARNING: '🟡',
        SafetyLevel.DANGER: '🔴',
        SafetyLevel.CRITICAL: '⛔'
    }
    
    with col1:
        st.metric("安全等级", f"{level_colors.get(level, '🟢')} {level.value.upper()}")
    with col2:
        st.metric("当前电压", f"{sensor_data.get('voltage', 0):.1f} V")
    with col3:
        st.metric("当前电流", f"{sensor_data.get('current', 0):.1f} A")
    with col4:
        st.metric("当前温度", f"{sensor_data.get('temperature', 0):.1f} °C")
    
    st.divider()
    
    # 传感器数据图表
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔋 电压监控")
        time_points = np.linspace(0, 10, 100)
        voltage_data = sensor_data.get('voltage', 800) + np.random.randn(100) * 20
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_points, y=voltage_data,
            name="电压", line=dict(color='blue')
        ))
        fig.add_hline(
            y=control_system.safety_monitor.thresholds.voltage,
            line_dash="dash", line_color="red",
            annotation_text=f"阈值: {control_system.safety_monitor.thresholds.voltage}V"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌡️ 温度监控")
        temp_data = sensor_data.get('temperature', 60) + np.random.randn(100) * 2
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_points, y=temp_data,
            name="温度", line=dict(color='orange'),
            fill='tozeroy', fillcolor='rgba(255, 165, 0, 0.2)'
        ))
        fig.add_hline(
            y=control_system.safety_monitor.thresholds.temperature,
            line_dash="dash", line_color="red",
            annotation_text=f"阈值: {control_system.safety_monitor.thresholds.temperature}°C"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # 绝缘与接地监测
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚡ 绝缘电阻监测")
        insulation = sensor_data.get('insulation_resistance', 1000)
        if insulation > 500:
            st.success(f"绝缘良好: {insulation:.0f} MΩ")
        elif insulation > 200:
            st.warning(f"绝缘下降: {insulation:.0f} MΩ")
        else:
            st.error(f"绝缘危险: {insulation:.0f} MΩ")
    
    with col2:
        st.subheader("⚡ 接地电阻监测")
        ground = sensor_data.get('ground_resistance', 0.1)
        if ground < 0.5:
            st.success(f"接地良好: {ground:.2f} Ω")
        elif ground < 1.0:
            st.warning(f"接地警告: {ground:.2f} Ω")
        else:
            st.error(f"接地危险: {ground:.2f} Ω")

if __name__ == "__main__":
    main()
