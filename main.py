import streamlit as st
from PIL import Image
import io

# 页面配置 - 使用宽屏布局适配笔记本
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="wide"  # 改为宽屏布局
)

# 自定义CSS - 重点修改层面比例和布局
st.markdown(
    """
    <style>
    /* 层面0：全屏灰色背景 */
    .layer-0 {
        background-color: #808080;  /* 纯灰色 */
        min-height: 100vh;
        width: 100vw;
        margin: 0;
        padding: 2rem;
        position: relative;
    }
    
    /* 层面1：白色工作区 - 调整为层面0的2/3大小 */
    .layer-1 {
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        width: 66.67%; /* 层面0宽度的2/3 */
        height: 66.67vh; /* 层面0高度的2/3 */
        margin: 0 auto;
        padding: 2.5rem;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        position: relative;
    }
    
    /* 主标题样式 */
    .main-title {
        text-align: center;
        margin-bottom: 2rem;
        color: #1f2937;
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* 三个图片框容器 - 放置在层面1中间 */
    .three-boxes-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem; /* 保持一致的间隔 */
        margin: 1rem auto;
        width: 90%;
    }
    
    /* 图片输入框样式 */
    .image-input-box {
        aspect-ratio: 3/2; /* 保持3:2长宽比 */
        border: 2px dashed #d1d5db;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        background-color: #f8f9fa;
        flex: 1;
        min-height: 200px;
    }
    
    .image-input-box:hover {
        border-color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
    }
    
    /* 输入框文字样式 */
    .input-box-text {
        color: #6b7280;
        font-size: 1rem;
        text-align: center;
        font-weight: 500;
    }
    
    /* 加号样式 */
    .plus-sign {
        font-size: 2rem;
        color: #6b7280;
        font-weight: 300;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 0.5rem;
    }
    
    /* 生成按钮容器 - 放置在生成框正下方 */
    .generate-btn-container {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        width: 100%;
    }
    
    /* 生成按钮样式 - 缩小为1/3，扁平蓝色长方形 */
    .generate-btn {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        border: none;
        width: 33.33%; /* 缩小为1/3宽度 */
        height: 50px; /* 扁平长方形 */
        margin: 0 auto;
    }
    
    .generate-btn:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* 加载动画 */
    .loading-overlay {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }
    
    .spinner {
        border: 3px solid rgba(59, 130, 246, 0.1);
        border-radius: 50%;
        border-top: 3px solid #3b82f6;
        width: 24px;
        height: 24px;
        animation: spin 1s linear infinite;
        margin-bottom: 0.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* 隐藏Streamlit默认的标题 */
    .main .block-container {
        padding-top: 1rem;
    }
    
    /* 结果图片样式 */
    .result-image {
        border-radius: 8px;
        object-fit: cover;
        width: 100%;
        height: 100%;
    }
    
    /* 响应式调整 */
    @media (max-width: 1200px) {
        .layer-1 {
            width: 80%;
            height: 70vh;
        }
        
        .three-boxes-container {
            gap: 1.5rem;
        }
    }
    
    @media (max-width: 768px) {
        .layer-1 {
            width: 95%;
            height: 75vh;
            padding: 1.5rem;
        }
        
        .three-boxes-container {
            flex-direction: column;
            gap: 1rem;
        }
        
        .generate-btn {
            width: 50%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 隐藏Streamlit默认的标题和菜单
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 层面0：全屏灰色背景
st.markdown('<div class="layer-0">', unsafe_allow_html=True)

# 层面1：白色工作区
st.markdown('<div class="layer-1">', unsafe_allow_html=True)

# 主标题
st.markdown('<div class="main-title">🎨 AI图片风格融合工具</div>', unsafe_allow_html=True)

# 三个图片框容器
st.markdown('<div class="three-boxes-container">', unsafe_allow_html=True)

# 内容图片输入框
st.markdown('<div class="image-input-box" id="content-image-box">', unsafe_allow_html=True)
content_image = st.file_uploader(
    "内容图片",
    type=['png', 'jpg', 'jpeg'],
    key="content",
    label_visibility="collapsed"
)

if content_image:
    image = Image.open(content_image)
    st.image(image, use_column_width=True, caption="内容图片")
else:
    st.markdown('<div class="input-box-text">📷 内容图片</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 加号1
st.markdown('<div class="plus-sign">+</div>', unsafe_allow_html=True)

# 风格图片输入框
st.markdown('<div class="image-input-box" id="style-image-box">', unsafe_allow_html=True)
style_image = st.file_uploader(
    "风格图片", 
    type=['png', 'jpg', 'jpeg'],
    key="style",
    label_visibility="collapsed"
)

if style_image:
    image = Image.open(style_image)
    st.image(image, use_column_width=True, caption="风格图片")
else:
    st.markdown('<div class="input-box-text">🎨 风格图片</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 加号2
st.markdown('<div class="plus-sign">=</div>', unsafe_allow_html=True)

# 结果图片显示框
st.markdown('<div class="image-input-box" id="result-image-box">', unsafe_allow_html=True)

# 检查是否有生成结果
if 'result_image' in st.session_state:
    st.image(st.session_state.result_image, use_column_width=True, caption="融合结果")
else:
    st.markdown('<div class="input-box-text">✨ 融合结果</div>', unsafe_allow_html=True)

# 加载动画（默认隐藏）
st.markdown('<div class="loading-overlay" id="loading-overlay" style="display: none;">', unsafe_allow_html=True)
st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
st.markdown('<div>生成中...</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 关闭三个图片框容器
st.markdown('</div>', unsafe_allow_html=True)

# 生成按钮容器 - 放置在生成框正下方
st.markdown('<div class="generate-btn-container">', unsafe_allow_html=True)

# 生成按钮
if st.button("🚀 一键生成风格融合图片", key="generate_btn"):
    if content_image and style_image:
        # 显示加载动画
        st.markdown(
            """
            <script>
            document.getElementById('loading-overlay').style.display = 'flex';
            </script>
            """,
            unsafe_allow_html=True
        )
        
        # 这里添加实际的风格融合代码
        # 暂时模拟生成过程
        st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
        st.success("风格融合完成！")
        
        # 隐藏加载动画
        st.markdown(
            """
            <script>
            setTimeout(function() {
                document.getElementById('loading-overlay').style.display = 'none';
            }, 1000);
            </script>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("请先上传内容图片和风格图片")

st.markdown('</div>', unsafe_allow_html=True)

# 关闭层面1
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown(
    """
    <div style='text-align: center; color: #d1d5db; font-size: 0.9rem; margin-top: 2rem;'>
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
    </div>
    """,
    unsafe_allow_html=True
)

# 关闭层面0
st.markdown('</div>', unsafe_allow_html=True)

# 初始化session state
if 'content_img' not in st.session_state:
    st.session_state.content_img = None
if 'style_img' not in st.session_state:
    st.session_state.style_img = None
if 'result_image' not in st.session_state:
    st.session_state.result_image = None