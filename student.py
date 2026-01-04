import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# 设置页面配置
st.set_page_config(
    page_title="学生成绩分析与预测系统",
    page_icon="📊",
    layout="wide"
)

# 生成模拟数据
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    n_students = 1000
    
    majors = ['大数据管理', '计算机科学', '信息系统', '软件工程', '数据科学', '人工智能', '电子商务']
    
    data = {
        '学号': [f'2023{str(i).zfill(6)}' for i in range(1, n_students+1)],
        '姓名': [f'学生{i}' for i in range(1, n_students+1)],
        '性别': np.random.choice(['男', '女'], n_students, p=[0.6, 0.4]),
        '专业': np.random.choice(majors, n_students, p=[0.25, 0.15, 0.15, 0.15, 0.10, 0.10, 0.10]),
        '平时成绩': np.random.normal(75, 10, n_students).clip(40, 100),
        '作业完成率': np.random.uniform(60, 100, n_students).round(1),
        '上课出勤率': np.random.uniform(70, 100, n_students).round(1),
        '每周学习时长': np.random.uniform(10, 40, n_students).round(1),
        '期中考试分数': np.random.normal(70, 15, n_students).clip(40, 100).round(1),
        '期末成绩': np.random.normal(70, 15, n_students).clip(40, 100).round(1)
    }
    
    df = pd.DataFrame(data)
    df['总评成绩'] = (df['平时成绩'] * 0.3 + df['期中考试分数'] * 0.3 + df['期末成绩'] * 0.4).round(1)
    
    return df

# 创建预测模型
@st.cache_resource
def create_prediction_model(df):
    le_gender = LabelEncoder()
    le_major = LabelEncoder()
    
    df['性别_编码'] = le_gender.fit_transform(df['性别'])
    df['专业_编码'] = le_major.fit_transform(df['专业'])
    
    features = ['平时成绩', '作业完成率', '上课出勤率', '每周学习时长', '期中考试分数', '性别_编码', '专业_编码']
    
    X = df[features]
    y = df['期末成绩']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, le_gender, le_major, features

# 创建成绩分段柱状图
def create_score_segment_bar_chart(major_df, major_name="大数据管理"):
    """创建成绩分段柱状图，展示各分数段人数分布"""
    
    # 定义分数段
    bins = [0, 60, 70, 80, 90, 100]
    labels = ['不及格(0-59)', '及格(60-69)', '中等(70-79)', '良好(80-89)', '优秀(90-100)']
    
    # 对成绩进行分段
    major_df['成绩段'] = pd.cut(major_df['期末成绩'], bins=bins, labels=labels, right=False)
    
    # 统计各分数段人数
    score_segments = major_df['成绩段'].value_counts().reindex(labels).fillna(0)
    
    # 计算百分比
    total_students = len(major_df)
    percentages = (score_segments / total_students * 100).round(1)
    
    # 创建柱状图
    fig = go.Figure()
    
    # 添加柱状图
    fig.add_trace(go.Bar(
        x=score_segments.index,
        y=score_segments.values,
        name='人数',
        marker_color='#4BC0C0',
        text=[f'{val}人 ({pct}%)' for val, pct in zip(score_segments.values, percentages.values)],
        textposition='outside',
        textfont=dict(color='white', size=12),
        hovertemplate='分数段: %{x}<br>人数: %{y}人<br>占比: %{customdata:.1f}%<extra></extra>',
        customdata=percentages.values
    ))
    
    # 更新布局
    fig.update_layout(
        title=f'{major_name}专业期末成绩分布',
        xaxis_title='成绩段',
        yaxis_title='人数',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        margin=dict(l=50, r=20, t=50, b=50)
    )
    
    # 更新X轴
    fig.update_xaxes(
        showgrid=False,
        tickangle=0
    )
    
    # 更新Y轴
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        title='人数'
    )
    
    return fig

# 创建成绩对比柱状图
def create_score_comparison_chart(major_df, major_name="大数据管理"):
    """创建成绩对比柱状图，展示各指标对比"""
    
    # 计算各指标的平均值
    avg_scores = {
        '平时成绩': major_df['平时成绩'].mean().round(1),
        '期中考试': major_df['期中考试分数'].mean().round(1),
        '期末考试': major_df['期末成绩'].mean().round(1),
        '总评成绩': major_df['总评成绩'].mean().round(1)
    }
    
    # 创建柱状图
    fig = go.Figure()
    
    # 添加柱状图
    fig.add_trace(go.Bar(
        x=list(avg_scores.keys()),
        y=list(avg_scores.values()),
        name='平均分',
        marker_color=['#FF6B6B', '#4ECDC4', '#4BC0C0', '#FFD93D'],
        text=[f'{val}分' for val in avg_scores.values()],
        textposition='outside',
        textfont=dict(color='white', size=12),
        hovertemplate='指标: %{x}<br>平均分: %{y:.1f}分<extra></extra>'
    ))
    
    # 更新布局
    fig.update_layout(
        title=f'{major_name}专业各项成绩对比',
        xaxis_title='成绩类型',
        yaxis_title='平均分',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        margin=dict(l=50, r=20, t=50, b=50)
    )
    
    # 更新X轴
    fig.update_xaxes(
        showgrid=False
    )
    
    # 更新Y轴
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        range=[0, 100]
    )
    
    return fig

# 主应用
def main():
    # 加载数据
    df = generate_sample_data()
    model, le_gender, le_major, features = create_prediction_model(df)
    
    # 侧边栏导航 - 改为选择菜单栏格式
    with st.sidebar:
        st.title("导航菜单")
        st.markdown("---")
        
        # 创建导航选项
        nav_options = ["项目介绍", "专业数据分析", "成绩预测"]
        
        # 使用单选按钮作为菜单
        selected_page = st.radio(
            "选择页面",
            nav_options,
            index=0
        )
    
    # 根据选择的页面显示内容
    if selected_page == "项目介绍":
        # 项目概述
        st.title("学生成绩分析与预测系统")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("项目概述")
            st.write("""
            本项目是一个基于Streamlit的学生成绩分析平台，通过数据可视化和机器学习技术，
            帮助教育工作者和学生深入了解学业表现，并预测期末考试成绩。
            """)
            
            st.subheader("主要特点:")
            st.write("- **数据可视化**: 多维度展示学生学业数据")
            st.write("- **专业分析**: 按专业分类的详细统计分析")
            st.write("- **智能预测**: 基于机器学习模型的成绩预测")
            st.write("- **学习建议**: 根据预测结果提供个性化反馈")
        
        with col2:
            # 专业分布图
            major_counts = df['专业'].value_counts()
            fig = go.Figure(data=[go.Bar(
                x=major_counts.index,
                y=major_counts.values,
                marker_color='rgb(55, 83, 109)'
            )])
            
            fig.update_layout(
                title='各专业学生人数分布',
                xaxis_title='专业',
                yaxis_title='学生人数',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 项目目标
        st.header("项目目标")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("目标一")
            st.write("**分析影响因素**")
            st.write("- 识别关键学习指标")
            st.write("- 探索成绩相关因素")
            st.write("- 提供数据支持决策")
        
        with col2:
            st.subheader("目标二")
            st.write("**可视化展示**")
            st.write("- 专业对比分析")
            st.write("- 性别差异研究")
            st.write("- 学习模式识别")
        
        with col3:
            st.subheader("目标三")
            st.write("**成绩预测**")
            st.write("- 机器学习模型")
            st.write("- 个性化预测")
            st.write("- 及时干预预警")
        
        # 技术架构
        st.header("技术架构")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**前端框架**")
            st.markdown("Streamlit")
        
        with col2:
            st.markdown("**数据处理**")
            st.markdown("Pandas")
            st.markdown("NumPy")
        
        with col3:
            st.markdown("**可视化**")
            st.markdown("Plotly")
            st.markdown("Matplotlib")
        
        with col4:
            st.markdown("**机器学习**")
            st.markdown("Scikit-learn")
    
    elif selected_page == "专业数据分析":
        st.title("📈 专业数据分析")
        
        # 1. 各专业男女性别比例
        st.header("1. 各专业男女性别比例")
        
        gender_by_major = pd.crosstab(df['专业'], df['性别'])
        gender_by_major = gender_by_major.sort_index()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 水平分组条形图 - 根据图片调整
            fig = go.Figure()
            
            colors = ['#1f77b4', '#ff7f0e']  # 为男女分配不同颜色
            
            for i, gender in enumerate(['男', '女']):
                fig.add_trace(go.Bar(
                    y=gender_by_major.index,
                    x=gender_by_major[gender],
                    name=gender,
                    orientation='h',
                    text=gender_by_major[gender],
                    textposition='inside',
                    marker_color=colors[i],
                    hovertemplate='%{y}: %{x}人<extra></extra>'
                ))
            
            fig.update_layout(
                barmode='group',
                title='各专业男女性别比例',
                yaxis_title='专业',
                xaxis_title='人数',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                margin=dict(l=50, r=20, t=50, b=50)
            )
            
            fig.update_xaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.3)'
            )
            
            fig.update_yaxes(
                showgrid=False,
                tickfont=dict(size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("性别比例数据")
            
            # 计算比例
            gender_by_major_pct = pd.crosstab(df['专业'], df['性别'], normalize='index') * 100
            
            # 创建格式化数据表格
            display_df = pd.DataFrame({
                '专业': gender_by_major_pct.index,
                '男生比例 (%)': gender_by_major_pct['男'].round(1),
                '女生比例 (%)': gender_by_major_pct['女'].round(1),
                '男生人数': gender_by_major['男'],
                '女生人数': gender_by_major['女'],
                '总人数': gender_by_major.sum(axis=1)
            })
            
            # 设置索引
            display_df = display_df.set_index('专业')
            
            # 添加样式
            st.dataframe(
                display_df,
                column_config={
                    "男生比例 (%)": st.column_config.NumberColumn(format="%.1f %%"),
                    "女生比例 (%)": st.column_config.NumberColumn(format="%.1f %%"),
                    "男生人数": st.column_config.NumberColumn(format="%d"),
                    "女生人数": st.column_config.NumberColumn(format="%d"),
                    "总人数": st.column_config.NumberColumn(format="%d")
                },
                use_container_width=True
            )
        
        # 2. 各专业学习指标对比
        st.header("2. 各专业学习指标对比")
        
        # 添加选择框
        col1, col2 = st.columns([1, 1])
        with col1:
            metric = st.selectbox(
                "选择学习指标",
                ['平时成绩', '期中考试分数', '期末成绩', '总评成绩', '作业完成率', '上课出勤率', '每周学习时长']
            )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 改进的组合图表
            major_avg = df.groupby('专业')[metric].mean()
            major_std = df.groupby('专业')[metric].std()
            
            fig = go.Figure()
            
            # 添加平均值柱状图
            fig.add_trace(go.Bar(
                x=major_avg.index,
                y=major_avg.values,
                name='平均值',
                marker_color='rgba(55, 83, 109, 0.8)',
                text=[f'{val:.1f}' for val in major_avg.values],
                textposition='outside'
            ))
            
            # 添加误差线
            fig.add_trace(go.Scatter(
                x=major_avg.index,
                y=major_avg.values,
                mode='markers',
                name='误差范围',
                error_y=dict(
                    type='data',
                    array=major_std.values,
                    visible=True,
                    color='rgba(255, 69, 0, 0.8)',
                    thickness=2
                ),
                marker=dict(
                    color='rgba(255, 69, 0, 0.8)',
                    size=8,
                    symbol='diamond'
                )
            ))
            
            fig.update_layout(
                title=f'各专业{metric}对比',
                xaxis_title='专业',
                yaxis_title=metric,
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                barmode='overlay',
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig.update_xaxes(
                tickangle=45,
                showgrid=False,
                gridcolor='rgba(255,255,255,0.1)'
            )
            
            fig.update_yaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("详细数据")
            
            # 创建统计表格
            stats_df = df.groupby('专业')[metric].agg(['mean', 'std', 'min', 'max']).round(1)
            stats_df.columns = ['平均值', '标准差', '最小值', '最大值']
            stats_df = stats_df.sort_values('平均值', ascending=False)
            
            # 添加排名
            stats_df['排名'] = range(1, len(stats_df) + 1)
            stats_df = stats_df[['排名', '平均值', '标准差', '最小值', '最大值']]
            
            st.dataframe(
                stats_df,
                column_config={
                    "排名": st.column_config.NumberColumn(format="%d"),
                    "平均值": st.column_config.NumberColumn(format="%.1f"),
                    "标准差": st.column_config.NumberColumn(format="%.1f"),
                    "最小值": st.column_config.NumberColumn(format="%.1f"),
                    "最大值": st.column_config.NumberColumn(format="%.1f")
                },
                use_container_width=True
            )
        
        # 3. 各专业出勤率分析
        st.header("3. 各专业出勤率分析")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 改进的矩形色块图
            attendance_by_major = df.groupby('专业')['上课出勤率'].mean().sort_values()
            
            # 使用渐变色
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']
            fig = go.Figure()
            
            for i, (major, attendance) in enumerate(attendance_by_major.items()):
                fig.add_trace(go.Bar(
                    x=[major],
                    y=[attendance],
                    name=major,
                    marker_color=colors[i % len(colors)],
                    text=f"{attendance:.1f}%",
                    textposition='outside',
                    width=0.6
                ))
            
            fig.update_layout(
                title='各专业平均出勤率',
                yaxis_title='出勤率 (%)',
                xaxis_title='专业',
                height=350,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(l=50, r=20, t=50, b=50)
            )
            
            fig.update_xaxes(
                tickangle=45,
                showgrid=False
            )
            
            fig.update_yaxes(
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                range=[attendance_by_major.min() - 5, attendance_by_major.max() + 5]
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("出勤率排名")
            
            attendance_rank = df.groupby('专业')['上课出勤率'].mean().sort_values(ascending=False).round(1)
            attendance_df = pd.DataFrame({
                '专业': attendance_rank.index,
                '平均出勤率': attendance_rank.values,
                '排名': range(1, len(attendance_rank) + 1)
            })
            
            attendance_df = attendance_df.set_index('排名')
            
            st.dataframe(
                attendance_df,
                column_config={
                    "专业": st.column_config.TextColumn(),
                    "平均出勤率": st.column_config.NumberColumn(format="%.1f %%")
                },
                use_container_width=True
            )
        
        # 4. 专项分析 - 根据图片调整为"大数据管理专业专项分析"
        st.header("4. 大数据管理专业专项分析")
        
        # 设置默认选择为大数据管理专业
        selected_major = "大数据管理"
        
        major_df = df[df['专业'] == selected_major]
        
        # 添加挂科率计算
        major_df['是否挂科'] = major_df['期末成绩'] < 60
        major_df['是否优良'] = major_df['期末成绩'] >= 80
        
        # 指标卡片 - 使用更醒目的样式
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pass_rate = (1 - major_df['是否挂科'].mean()) * 100
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
            ">
                <h3 style="margin: 0;">及格率</h3>
                <h1 style="margin: 10px 0; font-size: 36px;">{pass_rate:.1f}%</h1>
                <p style="margin: 0; opacity: 0.8;">{(len(major_df) - major_df['是否挂科'].sum())}/{len(major_df)}人</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_score = major_df['期末成绩'].mean()
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
            ">
                <h3 style="margin: 0;">平均分</h3>
                <h1 style="margin: 10px 0; font-size: 36px;">{avg_score:.1f}分</h1>
                <p style="margin: 0; opacity: 0.8;">标准差: {major_df['期末成绩'].std():.1f}分</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            excellent_rate = major_df['是否优良'].mean() * 100
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
            ">
                <h3 style="margin: 0;">优良率</h3>
                <h1 style="margin: 10px 0; font-size: 36px;">{excellent_rate:.1f}%</h1>
                <p style="margin: 0; opacity: 0.8;">{major_df['是否优良'].sum()}/{len(major_df)}人</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_study_hours = major_df['每周学习时长'].mean()
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: white;
            ">
                <h3 style="margin: 0;">平均学习时长</h3>
                <h1 style="margin: 10px 0; font-size: 36px;">{avg_study_hours:.1f}小时</h1>
                <p style="margin: 0; opacity: 0.8;">每周</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 成绩分布分析
        st.subheader(f"{selected_major}专业成绩分布")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 改进的成绩分布直方图
            fig = px.histogram(
                major_df,
                x='期末成绩',
                nbins=20,
                title='期末成绩分布直方图',
                color_discrete_sequence=['#36A2EB'],
                opacity=0.8,
                labels={'期末成绩': '成绩'},
                marginal=None
            )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False,
                margin=dict(l=50, r=20, t=50, b=50)
            )
            
            fig.update_xaxes(
                title='期末成绩 (分)',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)'
            )
            
            fig.update_yaxes(
                title='人数',
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)'
            )
            
            # 添加平均线
            fig.add_vline(
                x=avg_score,
                line_dash="dash",
                line_color="red",
                annotation_text=f"平均: {avg_score:.1f}分",
                annotation_position="top right"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 将箱线图改为柱状图 - 使用成绩分段柱状图
            fig = create_score_segment_bar_chart(major_df, selected_major)
            st.plotly_chart(fig, use_container_width=True)
    
    elif selected_page == "成绩预测":
        st.title("期末成绩预测")
        
        st.markdown("#### 请输入学生的学习信息，系统将预测其期末成绩并提供学习建议")
        
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("学号", value="1234567890")
            student_name = st.text_input("姓名", value="张三")
            gender = st.selectbox("性别", ["男", "女"])
            major = st.selectbox("专业", ["计算机科学", "信息系统", "软件工程", "数据科学", "人工智能", "电子商务"])
        
        with col2:
            usual_score = st.slider("平时成绩", 0.0, 100.0, 80.0, 0.5)
            study_hours = st.slider("每周学习时长(小时)", 0.0, 40.0, 20.0, 0.5)
            attendance = st.slider("上课出勤率(%)", 0.0, 100.0, 85.0, 0.5)
            midterm_score = st.slider("期中考试分数", 0.0, 100.0, 75.0, 0.5)
            homework_rate = st.slider("作业完成率(%)", 0.0, 100.0, 80.0, 0.5)
        
        # 显示当前输入
        st.subheader("当前输入信息")
        input_cols = st.columns(4)
        
        with input_cols[0]:
            st.metric("平时成绩", f"{usual_score}分")
        with input_cols[1]:
            st.metric("期中考试", f"{midterm_score}分")
        with input_cols[2]:
            st.metric("出勤率", f"{attendance}%")
        with input_cols[3]:
            st.metric("作业完成率", f"{homework_rate}%")
        
        # 预测按钮
        if st.button("预测期末成绩", type="primary"):
            # 准备输入数据
            input_data = pd.DataFrame({
                '平时成绩': [usual_score],
                '作业完成率': [homework_rate],
                '上课出勤率': [attendance],
                '每周学习时长': [study_hours],
                '期中考试分数': [midterm_score],
                '性别_编码': [le_gender.transform([gender])[0]],
                '专业_编码': [le_major.transform([major])[0]]
            })
            
            # 预测成绩
            prediction = model.predict(input_data)[0]
            predicted_score = round(prediction, 1)
            
            # 显示预测结果
            st.subheader("预测结果")
            
            # 创建突出显示区域
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 30px;
                border-radius: 10px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 20px 0;
                color: white;
            ">
                <h2 style="color: white; margin-bottom: 10px;">🎉 Congratulations!</h2>
                <h1 style="color: white; font-size: 72px; margin: 20px 0;">{predicted_score}</h1>
                <h3 style="color: white;">预测期末成绩</h3>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
