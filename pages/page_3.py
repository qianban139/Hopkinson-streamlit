"""
智能助手页面
AI聊天机器人界面，提供对话、文本生成和数据分析功能
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import display_footer, simulate_progress
from assets.css.styles import apply_styles

# ==================== 应用样式 ====================
apply_styles(st, style_set="all")

# ==================== 页面标题 ====================
st.markdown(
    '<h1 class="gradient-text animate__animated animate__fadeInDown" '
    'style="text-align: center; width: 100%; display: block;">'
    '🤖 智能助手</h1>', 
    unsafe_allow_html=True
)

st.write("---")

# ==================== 侧边栏参数设置 ====================
with st.sidebar:
    st.markdown("### ⚙️ 参数设置")
    
    temperature = st.slider(
        "创意温度 (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="值越高，输出越随机"
    )
    
    max_tokens = st.slider(
        "最大输出长度",
        min_value=100,
        max_value=8000,
        value=2000,
        step=100,
        help="生成的最大token数量"
    )
    
    st.markdown("---")
    st.markdown("### 📊 系统信息")
    st.info("""
    **模型**: GPT-4o-mini
    **状态**: ✅ 在线
    **响应时间**: < 1s
    """)

# ==================== 主内容区域 ====================
st.markdown('<div class="glass-card" style="margin-top: 32px;">', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">💬 与我对话吧</h2>', unsafe_allow_html=True)

# 创建标签页
tab1, tab2, tab3 = st.tabs(["💬 智能对话", "📝 文本生成", "📊 数据分析"])

# ==================== 标签页1: 智能对话 ====================
with tab1:
    st.markdown("### 与AI助手对话")
    st.info("💡 提示: 您可以询问关于霍普金森杆测试、材料力学、数据分析等相关问题")
    
    # 初始化对话历史
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "您好！我是您的智能助手，专门为数智化电磁驱动霍普金森杆测试系统提供支持。请问有什么可以帮助您的？"}
        ]
    
    # 显示对话历史
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 聊天输入
    if prompt := st.chat_input("输入您的问题..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 模拟AI响应
        with st.chat_message("assistant"):
            # 根据问题类型生成不同的响应
            responses = {
                "霍普金森": "霍普金森杆（Hopkinson Bar）是一种用于测量材料在高应变率下动态力学性能的实验装置。我们的数智化系统通过电磁驱动和AI技术，实现了更精准的波形控制和数据采集。",
                "材料": "我们的系统可以测试多种材料，包括金属、合金、聚合物、陶瓷和复合材料。通过Johnson-Cook本构模型，可以准确描述材料在不同应变率和温度下的力学行为。",
                "安全": "系统配备了完善的安全监控机制，包括电压、电流、温度实时监测，以及自动停机保护功能。当检测到异常时，系统会自动触发安全保护措施。",
                "数据": "系统提供强大的数据分析功能，包括小波变换去噪、Johnson-Cook模型拟合、跨材料应力映射等。您可以上传CSV文件进行可视化分析。",
                "波形": "我们的AI驱动波形自适应调控技术，利用LSTM神经网络进行预测，GAN生成满足特定要求的波形，实现精准控制。"
            }
            
            # 匹配关键词
            response = f"已收到您的问题：'{prompt}'\n\n"
            matched = False
            for keyword, reply in responses.items():
                if keyword in prompt:
                    response += reply
                    matched = True
                    break
            
            if not matched:
                response += f"基于当前配置（温度参数：{temperature}），我正在为您分析问题...\n\n这是一个关于数智化电磁驱动霍普金森杆测试系统的专业问题。我们的系统集成了电磁驱动、数字孪生和人工智能技术，能够实现热-力-电多场耦合动态加载、智能波形调控和全链条数据融合。如需更详细的解答，请提供更具体的问题描述。"
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 清空对话按钮
    if st.button("🗑️ 清空对话", type="secondary"):
        st.session_state.messages = [
            {"role": "assistant", "content": "您好！我是您的智能助手，专门为数智化电磁驱动霍普金森杆测试系统提供支持。请问有什么可以帮助您的？"}
        ]
        st.rerun()

# ==================== 标签页2: 文本生成 ====================
with tab2:
    st.markdown("### 📝 智能文本生成")
    st.info("💡 提示: 输入主题，AI将为您生成相关文本内容")
    
    prompt = st.text_area(
        "输入主题或要求",
        "请写一篇关于基于数智化电磁驱动霍普金森杆测试系统的应用介绍...",
        height=100
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("✨ 生成文本", type="primary"):
            with st.spinner("正在生成文本..."):
                simulate_progress(2.0)
                
                generated_text = """
                **数智化电磁驱动霍普金森杆测试系统：材料动态力学性能测试的新篇章**
                
                随着现代工程技术的发展，材料在极端载荷条件下的动态力学性能研究日益重要。
                数智化电磁驱动霍普金森杆测试系统应运而生，它通过电磁驱动-数字孪生-人工智能的深度融合，
                实现了热-力-电多场耦合动态加载、智能波形调控、全链条数据融合三大核心突破。
                
                **核心技术优势：**
                
                1. **AI驱动的波形自适应调控**：利用LSTM神经网络进行时序预测，GAN生成满足特定规格的波形，
                   实现精准控制，加载精度提升40%以上。
                
                2. **多场耦合智能同步加载**：实现真三轴六向应力脉冲纳秒级同步加载，
                   可模拟复杂工况下的材料响应。
                
                3. **高保真信号采集**：采用自适应滤波算法和小波变换技术，
                   有效抑制电磁干扰，信号信噪比提升60%。
                
                **应用前景：**
                
                该系统在土木工程、矿业工程、安全科学、航空航天等领域具有广阔的应用前景，
                可为重大工程提供可靠的材料动态性能数据支撑，推动动态力学测试技术向更高层次发展。
                """
                
                st.markdown("""
                <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; margin-top: 20px;">
                """, unsafe_allow_html=True)
                st.markdown(generated_text)
                st.markdown("</div>", unsafe_allow_html=True)

# ==================== 标签页3: 数据分析 ====================
with tab3:
    st.markdown("### 📊 AI数据分析")
    st.info("💡 提示: 上传CSV文件，AI将自动分析并生成可视化图表")
    
    uploaded_file = st.file_uploader("上传 CSV 文件", type="csv", key="ai_data_uploader")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.write("数据预览:")
        st.dataframe(df.head(), use_container_width=True)
        
        # 数据分析选项
        analysis_type = st.selectbox(
            "选择分析类型",
            ["数据概览", "趋势分析", "相关性分析", "异常检测"]
        )
        
        if st.button("🔍 开始分析", type="primary"):
            with st.spinner("AI正在分析数据..."):
                simulate_progress(2.0)
                
                if analysis_type == "数据概览":
                    st.subheader("📈 数据概览")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("数据行数", len(df))
                    with col2:
                        st.metric("数据列数", len(df.columns))
                    with col3:
                        st.metric("缺失值比例", f"{df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100:.2f}%")
                    
                    st.write("数据统计:")
                    st.dataframe(df.describe(), use_container_width=True)
                
                elif analysis_type == "趋势分析":
                    st.subheader("📈 趋势分析")
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    
                    if len(numeric_cols) >= 2:
                        x_col = st.selectbox("X轴", numeric_cols)
                        y_col = st.selectbox("Y轴", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df[x_col], y=df[y_col],
                            mode='lines+markers',
                            name=f'{y_col} vs {x_col}'
                        ))
                        fig.update_layout(
                            title=f"{y_col} 趋势图",
                            xaxis_title=x_col,
                            yaxis_title=y_col
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("数据需要至少两列数值型数据才能进行趋势分析")
                
                elif analysis_type == "相关性分析":
                    st.subheader("🔗 相关性分析")
                    numeric_df = df.select_dtypes(include=[np.number])
                    
                    if len(numeric_df.columns) >= 2:
                        corr_matrix = numeric_df.corr()
                        
                        fig = go.Figure(data=go.Heatmap(
                            z=corr_matrix.values,
                            x=corr_matrix.columns,
                            y=corr_matrix.columns,
                            colorscale='RdBu',
                            zmin=-1, zmax=1
                        ))
                        fig.update_layout(title="相关性热力图")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("数据需要至少两列数值型数据才能进行相关性分析")
                
                elif analysis_type == "异常检测":
                    st.subheader("🔍 异常检测")
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    
                    if numeric_cols:
                        selected_col = st.selectbox("选择列", numeric_cols)
                        
                        # 使用IQR方法检测异常值
                        Q1 = df[selected_col].quantile(0.25)
                        Q3 = df[selected_col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        
                        outliers = df[(df[selected_col] < lower_bound) | (df[selected_col] > upper_bound)]
                        
                        fig = go.Figure()
                        fig.add_trace(go.Box(y=df[selected_col], name=selected_col))
                        fig.update_layout(title=f"{selected_col} 箱线图")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        st.info(f"检测到 {len(outliers)} 个异常值 ({len(outliers)/len(df)*100:.2f}%)")
                        if len(outliers) > 0:
                            st.write("异常值预览:")
                            st.dataframe(outliers.head(), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


