# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from io import BytesIO
from streamlit.components.v1 import html
from datetime import datetime

def update_database_from_latest(latest_file, db_file):
    """
    读取最新读数文件，匹配ID并追加到数据库对应工作表中。
    返回更新后的数据库字典和最新读数DataFrame。
    """
    # 读取最新读数文件
    latest_df = pd.read_excel(latest_file, sheet_name=0)
    # 确保列名正确（根据示例文件，列名为uploadTime, ID, SensorTotalLength, SensorCurrentLength）
    # 如果文件可能有多行，这里直接使用全部数据
    
    # 读取数据库所有工作表
    xls = pd.ExcelFile(db_file)
    db_dict = pd.read_excel(xls, sheet_name=None)

    return db_dict, latest_df

def get_latest_sensor_status(db_dict):
    """
    从数据库字典中提取每个传感器的最新一条记录，用于状态显示。
    返回DataFrame，列：sensorName, latestTime, totalLength, actualLength
    """
    results = []
    for sheet_name, df in db_dict.items():
        if df.empty:
            results.append({
                'sensorName': sheet_name,
                'latestTime': None,
                'totalLength': None,
                'actualLength': None
            })
        else:
            last_row = df.iloc[-1]
            results.append({
                'sensorName': sheet_name,
                'latestTime': last_row['SensorScanTime'],  # 使用传感器扫描时间作为最新时间
                'totalLength': last_row['InitialThickness'],
                'actualLength': last_row['CurrentThickness']
            })
    return pd.DataFrame(results)

def plot_sensor_data_from_dict(db_dict):
    """
    基于数据库字典绘制每个传感器的CurrentThickness随时间变化曲线，
    并添加水平线标注InitialThickness。
    """
    fig = go.Figure()
    
    for sheet_name, df in db_dict.items():
        if df.empty:
            continue
        # 转换时间列
        df['SensorScanTime'] = pd.to_datetime(df['SensorScanTime'])
        # 按时间排序
        df = df.sort_values('SensorScanTime')
        # 添加当前厚度曲线
        fig.add_trace(go.Scatter(
            x=df['SensorScanTime'],
            y=df['CurrentThickness'],
            mode='lines+markers',
            name=f"{sheet_name} (Current)"
        ))
        # 添加初始厚度水平线（取第一行的InitialThickness，假设恒定）
        init_val = df['InitialThickness'].iloc[0]
        fig.add_hline(y=init_val, line_dash="dash", 
                      annotation_text=f"{sheet_name} Init: {init_val}mm",
                      annotation_position="top left")
    
    fig.update_yaxes(title_text="Thickness (mm)")
    fig.update_xaxes(title_text="Sensor Scan Time")
    fig.update_layout(
        margin=dict(l=1, r=1, t=30, b=1),
        template="seaborn",
        legend=dict(orientation="h", yanchor="bottom", y=0.9, xanchor="right", x=1)
    )
    return fig

def downloadData(file_path):
    # 定义新的列名
    NEW_COLUMNS = [
        "ServerUpdateTime", 
        "SensorScanTime", 
        "InitialThickness", 
        "CurrentThickness", 
        "Wear"
    ]

    try:
        # 读取所有工作表（返回字典格式：{sheet_name: DataFrame}）
        with pd.ExcelFile(file_path) as excel_file:
            # 创建内存缓冲区
            output = BytesIO()
            
            # 使用ExcelWriter将处理后的数据写入内存
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # 遍历每个工作表
                for sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    
                    # 检查列数是否匹配
                    if len(df.columns) != len(NEW_COLUMNS):
                        raise ValueError(f"工作表 '{sheet_name}' 列数不匹配："
                                        f"需要 {len(NEW_COLUMNS)} 列，实际 {len(df.columns)} 列")
                    
                    # 重命名列
                    df.columns = NEW_COLUMNS
                    
                    # 写入新的Excel文件
                    df.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )
            
            # 创建下载按钮
            st.download_button(
                label=":material/Download:  Download Database",
                data=output.getvalue(),
                file_name=file_path,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width = True
            )
            
            st.success("Sensor database available. Please click button to download!!!")    

    except FileNotFoundError:
        st.error(f"File not found : {file_path}")
        st.info("Please confirm file path and permission!")
    except Exception as e:
        st.error(f"Error: {str(e)}")





def app():
    st.subheader("Newmont Boddington Wear Sensor Trial - Linerless Tray", divider='rainbow')
    
    # 文件路径
    latest_file = "pwsReadingsLatest.xlsx"
    db_file = "Boddington_pwsTray_Database_update.xlsx"
    
    # 1. 更新数据库并获取最新数据字典
    db_dict, latest_df = update_database_from_latest(latest_file, db_file)
    
    # 2. 获取传感器最新状态
    sensor_status_df = get_latest_sensor_status(db_dict)
    
    # ------------------ 界面显示 ------------------
    st.markdown("1. Wear Sensor Installation Details")
    Tray1, Tray2 = st.tabs(["LinerLess Tray w/ Passive Wear Sensor", "Future Trials"])
    
    with Tray1:
        st.image("pwsTray.png", caption="Linerless Tray Passive Wear Sensor Install Locations", use_container_width=True)
    
    # 您之前设计的HTML代码（已包含所有样式和动画）
    html_code = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Coming Soon Block</title>
                <style>
                    * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    }

                    .coming-soon-block {
                    min-height: 400px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
                    border-radius: 16px;
                    padding: 40px;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
                    }

                    .coming-soon-block::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: radial-gradient(circle, rgba(255, 255, 255, 0.4) 0%, transparent 70%);
                    animation: shimmer 3s ease-in-out infinite;
                    }

                    @keyframes shimmer {
                    0%, 100% {
                        transform: translate(0, 0) rotate(0deg);
                    }
                    50% {
                        transform: translate(10%, 10%) rotate(5deg);
                    }
                    }

                    .content-wrapper {
                    position: relative;
                    z-index: 1;
                    }

                    .main-text {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #2d3748;
                    margin-bottom: 20px;
                    opacity: 0;
                    transform: translateY(30px);
                    animation: fadeInUp 0.8s ease-out forwards;
                    animation-delay: 0.3s;
                    }

                    @keyframes fadeInUp {
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                    }

                    .sub-text {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    font-size: 1.1rem;
                    color: #718096;
                    opacity: 0;
                    transform: translateY(20px);
                    animation: fadeInUp 0.8s ease-out forwards;
                    animation-delay: 0.6s;
                    }

                    .decorative-line {
                    width: 80px;
                    height: 4px;
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    border-radius: 2px;
                    margin: 25px auto;
                    opacity: 0;
                    transform: scaleX(0);
                    animation: expandLine 0.6s ease-out forwards;
                    animation-delay: 0.9s;
                    }

                    @keyframes expandLine {
                    to {
                        opacity: 1;
                        transform: scaleX(1);
                    }
                    }

                    .icon-container {
                    margin-bottom: 20px;
                    opacity: 0;
                    animation: bounceIn 0.8s ease-out forwards;
                    animation-delay: 0.1s;
                    }

                    @keyframes bounceIn {
                    0% {
                        opacity: 0;
                        transform: scale(0.3);
                    }
                    50% {
                        transform: scale(1.05);
                    }
                    70% {
                        transform: scale(0.9);
                    }
                    100% {
                        opacity: 1;
                        transform: scale(1);
                    }
                    }

                    .rocket-icon {
                    width: 60px;
                    height: 60px;
                    fill: #667eea;
                    animation: float 3s ease-in-out infinite;
                    }

                    @keyframes float {
                    0%, 100% {
                        transform: translateY(0);
                    }
                    50% {
                        transform: translateY(-10px);
                    }
                    }

                    .particles {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                    pointer-events: none;
                    overflow: hidden;
                    }

                    .particle {
                    position: absolute;
                    width: 8px;
                    height: 8px;
                    background: rgba(102, 126, 234, 0.3);
                    border-radius: 50%;
                    animation: particleFloat 4s ease-in-out infinite;
                    }

                    .particle:nth-child(1) {
                    top: 20%;
                    left: 10%;
                    animation-delay: 0s;
                    }

                    .particle:nth-child(2) {
                    top: 40%;
                    left: 80%;
                    animation-delay: 1s;
                    }

                    .particle:nth-child(3) {
                    top: 70%;
                    left: 30%;
                    animation-delay: 2s;
                    }

                    .particle:nth-child(4) {
                    top: 60%;
                    left: 70%;
                    animation-delay: 1.5s;
                    }

                    .particle:nth-child(5) {
                    top: 30%;
                    left: 50%;
                    animation-delay: 0.5s;
                    }

                    @keyframes particleFloat {
                    0%, 100% {
                        transform: translateY(0) scale(1);
                        opacity: 0.3;
                    }
                    50% {
                        transform: translateY(-20px) scale(1.2);
                        opacity: 0.6;
                    }
                    }

                    @media (max-width: 768px) {
                    .main-text {
                        font-size: 1.8rem;
                    }

                    .sub-text {
                        font-size: 1rem;
                    }

                    .coming-soon-block {
                        padding: 30px 20px;
                    }
                    }
                </style>
                </head>
                <body>
                <div class="coming-soon-block">
                    <div class="particles">
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    <div class="particle"></div>
                    </div>
                    
                    <div class="content-wrapper">
                    <div class="icon-container">
                        <svg class="rocket-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2.5s-4 5-4 9c0 2.5 1.5 4.5 4 6.5 2.5-2 4-4 4-6.5 0-4-4-9-4-9zm0 12c-1.5 0-2.5-1-2.5-2.5S10.5 9.5 12 9.5s2.5 1 2.5 2.5-1 2.5-2.5 2.5z"/>
                        <path d="M12 22c-1.5 0-3-1-3-2.5h6c0 1.5-1.5 2.5-3 2.5z"/>
                        <path d="M8 14.5c-2 1-4 2-4 4h16c0-2-2-3-4-4"/>
                        </svg>
                    </div>
                    
                    <h1 class="main-text">Something Great is on the Way!</h1>
                    
                    <div class="decorative-line"></div>
                    
                    <p class="sub-text">Stay tuned for something amazing</p>
                    </div>
                </div>
                </body>
                </html>
        """


    with Tray2:
        #st.markdown("Coming Soon: Future Trials with Linerless Tray and Active Wear Sensor")
        # 在Streamlit应用中渲染该HTML组件
        html(html_code, height=300)
    
    st.markdown("###")
    
    st.markdown("2. Wear Sensor Live Status")
    Tray1_sensor, Tray2_sensor = st.tabs(["LinerLess Tray w/ Passive Wear Sensor", "Debug & Data Table"])
    
    with Tray1_sensor:
        # 显示传感器状态指标
        for row in sensor_status_df.itertuples():
            sensor_name = row.sensorName
            latest_time = row.latestTime
            total_len = row.totalLength
            actual_len = row.actualLength

            # 显示metric
            if pd.notna(total_len):
                st.caption(f"Latest Reading at: {latest_time}")
                delta_val = actual_len - total_len
                st.metric(
                    label=f":material/Sensors: {sensor_name} Sensor Reading",
                    value=f"{actual_len}mm",
                    delta=delta_val,
                    border=True
                )
            else:
                st.metric(
                    label=f":material/Sensors: {sensor_name} Sensor Reading",
                    value="No Wear Data Received",
                    border=True
                )
                continue  # 无数据时跳过后续判断

            # 根据CurrentThickness进行条件判断
            if actual_len is not None and pd.notna(actual_len):
                # 获取该传感器的历史CurrentThickness列（去重排序）
                sheet_df = db_dict.get(sensor_name)
                thickness_vals = []
                if sheet_df is not None and not sheet_df.empty:
                    thickness_vals = sheet_df['CurrentThickness'].drop_duplicates().sort_values(ascending=False).tolist()

                # 条件分支
                if actual_len > 18:
                    st.info("Acceptable thickness, use as normal!")
                    # 若当前厚度不等于初始厚度，显示区间信息
                    if actual_len != total_len:
                        if thickness_vals and actual_len in thickness_vals:
                            idx = thickness_vals.index(actual_len)
                            if idx > 0:  # 存在更大的值
                                next_larger = thickness_vals[idx - 1]
                                st.info(f"Actual thickness is between {actual_len} and {next_larger}")
                elif actual_len == 18:
                    st.info("Please order trays!")
                elif 10 < actual_len < 18:
                    st.warning("Wearing thin, inspections required!")
                elif actual_len == 10:
                    st.error("Replace!")
        
        
        
        # 绘制传感器曲线
        st.markdown("###")
        st.markdown("3. Wear Sensor Plots")
        fig = plot_sensor_data_from_dict(db_dict)
        st.plotly_chart(fig, use_container_width=True)
        
        # 下载数据库按钮（需调整downloadData以适配新列名，此处暂不调用）
        # data download function
        st.markdown("###")
        downloadData(db_file)
    
    with Tray2_sensor:
        # 显示最新读数文件内容表格
        st.markdown("Latest Readings from pwsReadingsLatest.xlsx")
        st.dataframe(latest_df, use_container_width=True)
    
    st.markdown("###")