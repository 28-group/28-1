import streamlit as st
from PIL import Image
import io
import base64

# 页面配置 - 使用宽屏布局
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS
st.markdown(
    """
    <style>
    /* 彻底禁止页面滑动 */
    html, body, #root, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .stApp {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 层级样式 */
    .layer-0 {
        background-color: #808080;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    
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
    }
    
    .layer-2 {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70%;
        height: 70%;
        z-index: 3;
        padding: 2%;
        display: flex;
        flex-direction: column;
        background-color: transparent;
        pointer-events: auto;
    }
    
    /* 标题区域 */
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
        position: relative;
        z-index: 4;
    }
    
    .main-title {
        font-size: 1.8vw;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
        line-height: 1.5;
    }
    
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5% !important;
        padding: 0.2% !important;
        position: relative;
        z-index: 3;
    }
    
    .image-box {
        width: 35%;
        aspect-ratio: 2/3;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;
        transition: all 0.3s ease;
        padding: 1%;
        position: relative;
        overflow: hidden;  /* 关键：防止内容溢出 */
    }
    
    .image-box:hover {
        border-color: #388E3C;
        background-color: #dcedc8;
    }
    
    .box-text {
        color: #2E7D32;
        font-size: 1vw;
        text-align: center;
        margin-top: 8px;
    }
    
    .operator {
        font-size: 3vw;
        color: #6b7280;
        font-weight: 400;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: 1%;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
        position: relative;
        z-index: 3;
    }
    
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8% 2%;
        font-size: 1.1vw;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 25%;
        max-width: 100px;
    }
    
    .generate-button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
    }
    
    /* 底部说明 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 1%;
        padding-top: 1%;
        position: relative;
        z-index: 4;
        border-top: 1px solid #f0f0f0;
    }
    
    /* 自定义上传容器样式 */
    .custom-upload-container {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        position: absolute;  /* 绝对定位，确保在图片框内部 */
        top: 0;
        left: 0;
        z-index: 5;
    }
    
    .upload-icon {
        font-size: 4vw;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    
    .upload-text {
        color: #2E7D32;
        font-size: 1.2vw;
        text-align: center;
    }
    
    .upload-hint {
        color: #6b7280;
        font-size: 0.8vw;
        margin-top: 8px;
        text-align: center;
    }
    
    /* 图片预览样式 - 确保在图片框内部 */
    .image-preview-container {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: absolute;  /* 绝对定位 */
        top: 0;
        left: 0;
        z-index: 6;  /* 比上传界面更高 */
        background-color: #f1f8e9;  /* 与图片框背景一致 */
        border-radius: 10px;  /* 与图片框圆角一致 */
    }
    
    .preview-image {
        max-width: 90% !important;  /* 限制最大宽度 */
        max-height: 70% !important; /* 限制最大高度 */
        object-fit: contain !important;
        border-radius: 8px;
    }
    
    .reupload-btn {
        background-color: #6b7280;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 0.9vw;
        cursor: pointer;
        margin-top: 10px;
        transition: all 0.3s ease;
        z-index: 7;
    }
    
    .reupload-btn:hover {
        background-color: #4b5563;
    }
    
    /* 隐藏默认的文件上传器 */
    .stFileUploader {
        display: none !important;
    }
    
    /* 确保图片在图片框内部 */
    .stImage {
        max-width: 90% !important;
        max-height: 80% !important;
        object-fit: contain !important;
        position: relative !important;
        z-index: 6 !important;
    }
    
    /* 图片框内部容器 */
    .image-box-inner {
        width: 100%;
        height: 100%;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 自定义文件上传组件
def custom_image_uploader(key, label):
    """完全自定义的图片上传组件，确保图片在框内显示"""
    
    # 初始化session state
    if f'uploaded_image_{key}' not in st.session_state:
        st.session_state[f'uploaded_image_{key}'] = None
    
    # 创建图片框内部容器
    st.markdown('<div class="image-box-inner">', unsafe_allow_html=True)
    
    # 如果已经上传了图片，显示预览
    if st.session_state[f'uploaded_image_{key}'] is not None:
        # 显示图片预览（在图片框内部）
        st.markdown(f'''
        <div class="image-preview-container">
            <img class="preview-image" src="data:image/png;base64,{st.session_state[f'uploaded_image_{key}']}" alt="{label}">
            <button class="reupload-btn" onclick="window.parent.document.getElementById('reupload_{key}').click()">重新上传</button>
        </div>
        ''', unsafe_allow_html=True)
        
        # 重新上传按钮（隐藏的Streamlit按钮）
        if st.button("重新上传", key=f"reupload_{key}", help="点击重新上传图片"):
            st.session_state[f'uploaded_image_{key}'] = None
            st.rerun()
            
    # 显示自定义上传界面
    else:
        st.markdown(f'''
        <div class="custom-upload-container" onclick="window.parent.document.getElementById('upload_trigger_{key}').click()">
            <div class="upload-icon">📁</div>
            <div class="upload-text">{label}</div>
            <div class="upload-hint">点击上传图片</div>
            <div class="upload-hint">支持 PNG, JPG, JPEG 格式</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # 隐藏的文件上传触发器
        uploaded_file = st.file_uploader(
            f"上传{label}",
            type=['png', 'jpg', 'jpeg'],
            key=f"upload_trigger_{key}",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # 将图片转换为base64存储在session state中
            try:
                image = Image.open(uploaded_file)
                # 调整图片大小以适应图片框
                max_size = (300, 400)  # 根据图片框大小调整
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                st.session_state[f'uploaded_image_{key}'] = img_str
                st.rerun()
            except Exception as e:
                st.error(f"图片处理错误: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)  # 关闭image-box-inner
    
    # 返回PIL Image对象
    if st.session_state[f'uploaded_image_{key}'] is not None:
        try:
            img_data = base64.b64decode(st.session_state[f'uploaded_image_{key}'])
            return Image.open(io.BytesIO(img_data))
        except:
            return None
    else:
        return None

# 层级结构
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)
st.markdown('<div class="layer-1"></div>', unsafe_allow_html=True)
st.markdown('<div class="layer-2">', unsafe_allow_html=True)

# 标题区域
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 横向布局
col1, col2, col3, col4, col5 = st.columns([1, 0.04, 1, 0.04, 1])

# 内容图片框
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    content_image = custom_image_uploader("content", "内容图片")
    st.markdown('</div>', unsafe_allow_html=True)

# 加号
with col2:
    st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

# 风格图片框
with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    style_image = custom_image_uploader("style", "风格图片")
    st.markdown('</div>', unsafe_allow_html=True)

# 等号
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框
with col5:
    with st.container():
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        if 'result_image' in st.session_state and st.session_state.result_image:
            # 使用相同的内部容器确保一致性
            st.markdown('<div class="image-box-inner">', unsafe_allow_html=True)
            st.image(st.session_state.result_image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('''
            <div class="image-box-inner">
                <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 3vw; color: #4CAF50;"></div>
                    <div class="box-text">融合结果</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("✨ 一键生成", key="generate_btn", use_container_width=True):
                if content_image is not None and style_image is not None:
                    with st.spinner("正在生成融合图片..."):
                        # 这里添加实际的风格融合代码
                        # 暂时使用占位图模拟生成结果
                        st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
                        st.success("风格融合完成！")
                        st.rerun()
                else:
                    st.warning("请先上传内容图片和风格图片")

st.markdown('</div>', unsafe_allow_html=True)  # 关闭image-container

# 底部使用说明
st.markdown('''
<div class="footer">
    使用说明：点击图片框上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2

# 初始化session state
if 'result_image' not in st.session_state:
    st.session_state.result_image = None