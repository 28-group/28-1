import streamlit as st
from PIL import Image
import io

# 页面配置
st.set_page_config(
    page_title="AI画家 - 图片风格融合",
    page_icon="🎨",
    layout="centered"  # 使用居中布局
)

# 应用标题
st.title("🎨 AI图片风格融合工具")
st.markdown("---")

# 自定义CSS
st.markdown(
    """
    <style>
    /* 层面0：背景层 */
    .layer-0 {
        background-color: #1f2937;
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* 层面1：主要工作区 */
    .layer-1 {
        background-color: #f3f4f6;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        width: 66.666%; /* 2/3 宽度 */
        aspect-ratio: 1/2; /* 1:2 长宽比 */
        margin: 0 auto;
        padding: 2rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* 图片输入框样式 */
    .image-input-box {
        aspect-ratio: 3/2; /* 3:2 长宽比 */
        border: 2px dashed #d1d5db;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        transition: all 0.3s ease;
        position: relative;
        background-color: white;
    }
    
    .image-input-box:hover {
        border-color: #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
    }
    
    /* 输入框文字样式 */
    .input-box-text {
        color: #6b7280;
        font-size: 0.9rem;
        text-align: center;
    }
    
    /* 生成按钮样式 */
    .generate-btn {
        aspect-ratio: 3/1; /* 3:1 长宽比 */
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
        width: 100%;
        max-width: 300px;
        margin: 1.5rem auto 0;
    }
    
    .generate-btn:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* 加号样式 */
    .plus-sign {
        font-size: 1.5rem;
        color: #6b7280;
        font-weight: 300;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 加载动画 */
    .loading-overlay {
        background-color: rgba(255, 255, 255, 0.8);
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
    
    /* 调整字体大小 */
    .css-10trblm {
        font-size: 0.9rem;
    }
    
    .css-16huue1 {
        font-size: 1.2rem;
    }
    
    .css-1v0mbdj {
        font-size: 0.85rem;
    }
    
    /* 结果图片样式 */
    .result-image {
        border-radius: 8px;
        object-fit: cover;
        width: 100%;
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 层面0：背景层
st.markdown('<div class="layer-0">', unsafe_allow_html=True)

# 层面1：主要工作区
st.markdown('<div class="layer-1">', unsafe_allow_html=True)

# 标题
st.markdown('<h2 style="text-align: center; margin-bottom: 1.5rem;">上传图片进行风格融合</h2>', unsafe_allow_html=True)

# 创建三个并排的输入框/图片显示区域
col_left, col_plus1, col_middle, col_plus2, col_right = st.columns([1, 0.1, 1, 0.1, 1])

# 内容图片输入框
with col_left:
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
        st.markdown('<div class="input-box-text"><i class="fa fa-cloud-upload" style="font-size: 1.5rem; margin-bottom: 0.5rem;"></i><br>内容图片</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 加号1
with col_plus1:
    st.markdown('<div class="plus-sign">+</div>', unsafe_allow_html=True)

# 风格图片输入框
with col_middle:
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
        st.markdown('<div class="input-box-text"><i class="fa fa-cloud-upload" style="font-size: 1.5rem; margin-bottom: 0.5rem;"></i><br>风格图片</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 加号2
with col_plus2:
    st.markdown('<div class="plus-sign">=</div>', unsafe_allow_html=True)

# 结果图片显示框
with col_right:
    st.markdown('<div class="image-input-box" id="result-image-box">', unsafe_allow_html=True)
    
    # 检查是否有生成结果
    if 'result_image' in st.session_state:
        st.image(st.session_state.result_image, use_column_width=True, caption="融合结果")
    else:
        st.markdown('<div class="input-box-text"><i class="fa fa-image" style="font-size: 1.5rem; margin-bottom: 0.5rem;"></i><br>融合结果</div>', unsafe_allow_html=True)
    
    # 加载动画（默认隐藏）
    st.markdown('<div class="loading-overlay" id="loading-overlay" style="display: none;">', unsafe_allow_html=True)
    st.markdown('<div class="spinner"></div>', unsafe_allow_html=True)
    st.markdown('<div>生成中...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 一键生成按钮
st.markdown('<button class="generate-btn" id="generate-btn">一键生成</button>', unsafe_allow_html=True)

# 关闭层面1
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #d1d5db; font-size: 0.85rem;'>
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

# JavaScript 代码
st.markdown(
    """
    <script>
    // 获取DOM元素
    const contentImageBox = document.getElementById('content-image-box');
    const styleImageBox = document.getElementById('style-image-box');
    const resultImageBox = document.getElementById('result-image-box');
    const generateBtn = document.getElementById('generate-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // 检查是否可以生成
    function checkGenerateStatus() {
        const contentImageSelected = contentImageBox.querySelector('img') !== null;
        const styleImageSelected = styleImageBox.querySelector('img') !== null;
        
        if (contentImageSelected && styleImageSelected) {
            generateBtn.disabled = false;
            generateBtn.style.opacity = '1';
            generateBtn.style.cursor = 'pointer';
        } else {
            generateBtn.disabled = true;
            generateBtn.style.opacity = '0.7';
            generateBtn.style.cursor = 'not-allowed';
        }
    }
    
    // 监听图片上传变化
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                checkGenerateStatus();
            }
        });
    });
    
    // 观察内容图片和风格图片区域的变化
    observer.observe(contentImageBox, { childList: true, subtree: true });
    observer.observe(styleImageBox, { childList: true, subtree: true });
    
    // 初始化检查
    checkGenerateStatus();
    
    // 生成按钮点击事件
    generateBtn.addEventListener('click', function() {
        // 显示加载动画
        loadingOverlay.style.display = 'flex';
        
        // 模拟生成过程（实际应用中这里会调用AI模型）
        setTimeout(function() {
            // 隐藏加载动画
            loadingOverlay.style.display = 'none';
            
            // 在实际应用中，这里会显示生成的图片
            // 这里只是模拟，实际需要后端处理
        }, 2000);
    });
    </script>
    """,
    unsafe_allow_html=True
)
