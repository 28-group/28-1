import streamlit as st
from PIL import Image
import io

# 页面配置 - 使用宽屏布局
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS - 简化设计，确保所有元素可见
st.markdown(
    """
    <style>
    /* 全局样式重置 */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* 确保页面占满整个屏幕 */
    html, body {
        height: 100vh;
        width: 100vw;
        overflow: hidden;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 主容器样式 */
    .stApp {
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        position: relative;
    }
    
    /* 修复Streamlit默认容器样式 */
    .main .block-container {
        padding: 2rem !important;
        margin: 0 auto !important;
        max-width: 100% !important;
    }
    
    /* 层面0：灰色背景层 */
    .layer-0 {
        background-color: #808080;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
    /* 层面1：白色工作区 */
    .layer-1 {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        z-index: 2;
        padding: 2%;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
        width: 100%;
    }
    
    .main-title {
        font-size: 24px;
        font-weight: bold;
        color: #ff69b4; /* 粉红色 */
        margin: 0;
    }
    
    /* 图片框容器 */
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        width: 100%;
        flex: 1;
        padding: 2%;
    }
    
    /* 单个图片框样式 */
    .image-box {
        width: 28%;
        aspect-ratio: 3/2;
        border: 2px dashed #4CAF50; /* 绿色边框 */
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9; /* 浅绿色背景 */
        transition: all 0.3s ease;
        padding: 10px;
    }
    
    .image-box:hover {
        border-color: #388E3C; /* 深绿色边框 */
        background-color: #dcedc8; /* 深一点的绿色背景 */
    }
    
    .box-text {
        color: #2E7D32; /* 绿色文字 */
        font-size: 16px;
        text-align: center;
        margin-top: 8px;
    }
    
    /* 加号样式 */
    .operator {
        font-size: 24px;
        color: #6b7280;
        font-weight: 300;
    }
    
    /* 按钮容器 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 1%;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
        width: 100%;
    }
    
    .generate-button {
        background-color: #3b82f6; /* 蓝色按钮 */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 30px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .generate-button:hover {
        background-color: #2563eb; /* 深蓝色按钮 */
        transform: translateY(-2px);
    }
    
    /* 底部信息 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 14px;
        margin-top: 1%;
        width: 100%;
    }
    
    /* 图标样式 */
    .icon {
        font-size: 36px;
        color: #4CAF50;
        margin-bottom: 8px;
    }
    
    /* 文件上传按钮样式 */
    .upload-btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: 14px;
        cursor: pointer;
        margin-top: 10px;
    }
    
    .upload-btn:hover {
        background-color: #388E3C;
    }
    
    /* 隐藏默认文件上传控件 */
    input[type="file"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 创建层面0：灰色背景
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 创建层面1：白色工作区
st.markdown('<div class="layer-1">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 内容图片框
st.markdown('''
<div class="image-box">
    <div class="icon">📷</div>
    <div class="box-text">内容图片</div>
    <button class="upload-btn" onclick="document.getElementById('content-upload').click()">上传图片</button>
    <input type="file" id="content-upload" accept="image/*" style="display: none;">
</div>
''', unsafe_allow_html=True)

# 加号1
st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

# 风格图片框
st.markdown('''
<div class="image-box">
    <div class="icon">🎨</div>
    <div class="box-text">风格图片</div>
    <button class="upload-btn" onclick="document.getElementById('style-upload').click()">上传图片</button>
    <input type="file" id="style-upload" accept="image/*" style="display: none;">
</div>
''', unsafe_allow_html=True)

# 加号2
st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
st.markdown('''
<div class="image-box">
    <div class="icon">✨</div>
    <div class="box-text">融合结果</div>
    <div id="result-image" style="margin-top: 10px; display: none;">
        <img src="" alt="融合结果" style="max-width: 100%; max-height: 100px;">
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭图片框容器

# 生成按钮
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("一键生成", key="generate_btn", use_container_width=False):
    st.success("风格融合完成！")
    # 在实际应用中，这里会显示生成的图片
    st.markdown('''
    <script>
        document.getElementById('result-image').style.display = 'block';
        document.getElementById('result-image').querySelector('img').src = 'https://via.placeholder.com/200x150/4CAF50/FFFFFF?text=融合结果';
    </script>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown('''
<div class="footer">
    使用说明：上传内容图和风格图，点击一键生成按钮即可获得融合风格图
</div>
''', unsafe_allow_html=True)

# 关闭层面1
st.markdown('</div>', unsafe_allow_html=True)

# 添加JavaScript处理文件上传预览
st.markdown('''
<script>
    // 内容图片上传预览
    document.getElementById('content-upload').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageBox = document.querySelector('.image-container > div:first-child');
                imageBox.innerHTML = `<img src="${e.target.result}" alt="内容图片" style="max-width: 100%; max-height: 100%;">`;
            }
            reader.readAsDataURL(file);
        }
    });
    
    // 风格图片上传预览
    document.getElementById('style-upload').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imageBox = document.querySelector('.image-container > div:nth-child(3)');
                imageBox.innerHTML = `<img src="${e.target.result}" alt="风格图片" style="max-width: 100%; max-height: 100%;">`;
            }
            reader.readAsDataURL(file);
        }
    });
</script>
''', unsafe_allow_html=True)




