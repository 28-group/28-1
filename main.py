您说得对！之前的方案确实经常出现组件不固定的问题。让我分析一下当前设计的固定性：

## 当前设计的固定性分析：

### ✅ **真正固定的部分：**
- 页面整体容器 (`stApp`) - 完全固定，禁止滚动
- 灰色背景 - 固定全屏
- 白色工作区 (`.main-workspace`) - 绝对定位居中固定

### ⚠️ **可能不固定的风险点：**
Streamlit组件本身有自带的布局行为，可能会破坏固定效果。

## 更彻底的固定方案：

```python
import streamlit as st
from PIL import Image
import io

# 页面配置
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 更严格的固定CSS
st.markdown(
    """
    <style>
    /* 彻底锁定整个页面 */
    html, body, #root, [data-testid="stAppViewContainer"], .stApp {
        height: 100vh !important;
        width: 100vw !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        background-color: #808080 !important;
    }
    
    /* 隐藏所有可能破坏布局的元素 */
    #MainMenu {visibility: hidden !important; height: 0 !important;}
    footer {visibility: hidden !important; height: 0 !important;}
    header {visibility: hidden !important; height: 0 !important;}
    .stDeployButton {display: none !important;}
    
    /* 主工作区 - 绝对固定 */
    .main-workspace {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 85vw;
        height: 85vh;
        z-index: 1000;
        padding: 2%;
        display: flex;
        flex-direction: column;
        /* 防止内部内容溢出 */
        overflow: hidden !important;
    }
    
    /* 锁定内部布局结构 */
    .workspace-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        height: 100%;
        overflow: hidden;
    }
    
    .title-section {
        text-align: center;
        margin-bottom: 2%;
        padding-bottom: 1%;
        border-bottom: 1px solid #f0f0f0;
        flex-shrink: 0;
    }
    
    .main-title {
        font-size: 2rem;
        font-weight: bold;
        color: #ff69b4;
        margin: 0;
    }
    
    /* 图片区域 - 固定高度 */
    .image-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2%;
        padding: 2%;
        min-height: 0;
        height: 60vh; /* 固定高度 */
        overflow: hidden;
    }
    
    .image-box {
        width: 28%;
        height: 100%;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;
        position: relative;
        overflow: hidden;
        flex-shrink: 0;
    }
    
    /* 强制Streamlit组件遵守固定布局 */
    [data-testid="stAppViewContainer"] > div {
        position: fixed !important;
        width: 100vw !important;
        height: 100vh !important;
    }
    
    /* 列布局锁定 */
    .stColumn {
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* 文件上传器完全锁定在图片框内 */
    .stFileUploader {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        z-index: 1002 !important;
    }
    
    .stFileUploader > section {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
    }
    
    .stFileUploader > section > div {
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 按钮区域固定 */
    .button-container {
        display: flex;
        justify-content: center;
        margin-top: auto;
        padding-top: 2%;
        border-top: 1px solid #f0f0f0;
        flex-shrink: 0;
        position: relative;
        z-index: 1002;
    }
    
    .generate-button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        min-width: 150px;
    }
    
    /* 彻底禁用任何滚动条 */
    ::-webkit-scrollbar {
        display: none !important;
    }
    
    /* 响应式锁定 - 确保在小屏幕上也固定 */
    @media (max-height: 600px) {
        .main-workspace {
            height: 95vh !important;
            width: 95vw !important;
        }
        .image-container {
            height: 50vh !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 创建完全固定的布局
st.markdown('<div class="main-workspace">', unsafe_allow_html=True)
st.markdown('<div class="workspace-content">', unsafe_allow_html=True)

# 标题
st.markdown('''
<div class="title-section">
    <div class="main-title">AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片区域 - 使用固定布局
st.markdown('<div class="image-container">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns([1, 0.1, 1, 0.1, 1])

with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    content_image = st.file_uploader("内容图片", type=['png', 'jpg', 'jpeg'], key="content", label_visibility="collapsed")
    if content_image:
        image = Image.open(content_image)
        st.image(image, use_column_width=True)
    else:
        st.markdown('<div class="box-text">内容图片</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    style_image = st.file_uploader("风格图片", type=['png', 'jpg', 'jpeg'], key="style", label_visibility="collapsed")
    if style_image:
        image = Image.open(style_image)
        st.image(image, use_column_width=True)
    else:
        st.markdown('<div class="box-text">风格图片</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    if 'result_image' in st.session_state and st.session_state.result_image:
        st.image(st.session_state.result_image, use_column_width=True)
    else:
        st.markdown('<div class="box-text">融合结果</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭图片容器

# 按钮区域
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("🎨 一键生成", key="generate_btn", use_container_width=True):
    if content_image and style_image:
        with st.spinner("AI正在创作中..."):
            import time
            time.sleep(2)
            st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
            st.success("风格融合完成！")
            st.rerun()
    else:
        st.warning("请先上传内容图片和风格图片")
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown('''
<div class="footer">
    💡 上传内容图片和风格图片，点击生成按钮获得融合结果
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # 关闭workspace-content
st.markdown('</div>', unsafe_allow_html=True)  # 关闭main-workspace

# 初始化
if 'result_image' not in st.session_state:
    st.session_state.result_image = None




