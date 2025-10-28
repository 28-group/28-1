# app.py
import streamlit as st
from PIL import Image
# ---------- 页面级配置 ----------
import io
#test wu hao ming lai le
# 页面配置
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- 全局样式 ----------
st.markdown(
    """
    <style>
    /* 1. 强制全屏不可滑动 */
    html, body, #root, [data-testid="stAppViewContainer"] {
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
        margin: 0;
        padding: 0;
    }
    .stApp { height: 100vh; width: 100vw; overflow: hidden; }

    /* 2. 隐藏官方头尾 */
    #MainMenu, footer, header { visibility: hidden; }

    /* 3. 灰色背景层 */
    .gray-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #808080;
        z-index: 1;
    }

    /* 4. 白色工作区 */
    .white-panel {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 70vw;
        height: 70vh;
        background: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0,0,0,.2);
        z-index: 2;
        display: flex;
        flex-direction: column;
        padding: 2%;
        overflow: hidden;
    }

    /* 5. 标题 + 底部说明 */
    .title-section, .footer {
        flex: 0 0 auto;
        text-align: center;
        position: relative;
        z-index: 100;
    }
    .main-title { font-size: 1.8vw; color: #ff69b4; font-weight: bold; }
    .footer { font-size: .8vw; color: #6b7280; margin-top: 1%; }

    /* 6. 图片栅格区域 */
    .grid {
        flex: 1 1 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2%;
        min-height: 0;
    }
    .cell {
        width: 28%;
        height: 100%;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .image-box {
        width: 100%;
        height: 100%;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        background: #f1f8e9;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    .operator {
        font-size: 2vw;
        color: #6b7280;
        user-select: none;
    }

    /* 7. 上传组件完全铺满白框 */
    .stFileUploader {
        position: absolute !important;
        inset: 0;
        width: 100% !important;
        height: 100% !important;
        z-index: 5;
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
    .stFileUploader label {
        display: block !important;
        font-size: .9vw;
        color: #2E7D32;
        margin-bottom: 4px;
    }

    /* 8. 生成按钮 */
    .button-box {
        flex: 0 0 auto;
        text-align: center;
        padding-top: 1%;
        border-top: 1px solid #f0f0f0;
    }
    .generate-button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: .8% 2%;
        font-size: 1.1vw;
        font-weight: 600;
        cursor: pointer;
        width: 25%;
        max-width: 180px;
    }
    .generate-button:hover { background: #2563eb; }

    /* 9. 图片展示 */
    img { max-width: 90%; max-height: 90%; object-fit: contain; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- 布局 ----------
st.markdown('<div class="gray-bg"></div>', unsafe_allow_html=True)
st.markdown('<div class="white-panel">', unsafe_allow_html=True)

# 标题
st.markdown(
    '<div class="title-section"><div class="main-title">AI 图片风格融合工具</div></div>',
    unsafe_allow_html=True
)

# 图片栅格
grid = st.container()
with grid:
    c1, op1, c2, op2, c3 = st.columns([1, .05, 1, .05, 1])
    # 内容框
    with c1:
        box1 = st.container()
        with box1:
            st.markdown('<div class="image-box" id="content-box">', unsafe_allow_html=True)
            content_file = st.file_uploader("上传内容图片", type=['png', 'jpg', 'jpeg'], key="content")
            if content_file:
                st.image(Image.open(content_file), use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    # 运算符
    with op1: st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)
    # 风格框
    with c2:
        box2 = st.container()
        with box2:
            st.markdown('<div class="image-box" id="style-box">', unsafe_allow_html=True)
            style_file = st.file_uploader("上传风格图片", type=['png', 'jpg', 'jpeg'], key="style")
            if style_file:
                st.image(Image.open(style_file), use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    # 运算符
    with op2: st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)
    # 结果框
    with c3:
        box3 = st.container()
        with box3:
            st.markdown('<div class="image-box" id="result-box">', unsafe_allow_html=True)
           