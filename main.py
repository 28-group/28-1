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

# 自定义CSS - 重新规划组件大小和位置
st.markdown(
    """
    <style>
    /* ==================== 基础布局设置 ==================== */
    /* 彻底禁止页面滑动 - 确保整个应用固定不滚动 */
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
    
    /* ==================== 三层级布局系统 ==================== */
    
    /* 
    第1层级：灰色背景层 
    作用：作为整个应用的底层背景，相当于"桌子"
    特性：固定定位，覆盖整个视口，最低层级(z-index: 1)
    */
    .layer-0 {
        background-color: #808080;        /* 灰色背景 */
        position: fixed;                  /* 固定定位，不随页面滚动 */
        top: 0;
        left: 0;
        width: 100vw;                     /* 覆盖整个视口宽度 */
        height: 100vh;                    /* 覆盖整个视口高度 */
        z-index: 1;                       /* 最低层级，作为背景 */
    }
    
    /* 
    第2层级：白色工作区 
    作用：作为主要内容容器，相当于"桌布"
    特性：居中显示，白色背景，带阴影和圆角，中间层级(z-index: 2)
    */
    .layer-1 {
        background-color: white;          /* 白色背景 */
        border-radius: 15px;              /* 圆角设计 */
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);  /* 阴影效果增加层次感 */
        position: fixed;
        top: 50%;                         /* 垂直居中 */
        left: 50%;                        /* 水平居中 */
        transform: translate(-50%, -50%); /* 精确居中定位 */
        width: 70%;                       /* 占据视口宽度的70% */
        height: 70%;                      /* 占据视口高度的70% */
        z-index: 2;                       /* 中间层级，在灰色背景之上 */
    }
    
    /* 
    第3层级：透明组件容器 
    作用：承载所有交互组件的透明层，相当于"菜肴摆放区"
    特性：与第2层级完全重合但透明，承载所有UI组件，最高层级(z-index: 3)
    */
    .layer-2 {
        position: fixed;
        top: 50%;                         /* 与第2层级相同的垂直位置 */
        left: 50%;                        /* 与第2层级相同的水平位置 */
        transform: translate(-50%, -50%); /* 与第2层级相同的居中方式 */
        width: 70%;                       /* 与第2层级相同的宽度 */
        height: 70%;                      /* 与第2层级相同的高度 */
        z-index: 3;                       /* 最高层级，在所有内容之上 */
        padding: 3%;                      /* 内边距，为内部组件提供呼吸空间 */
        display: flex;
        flex-direction: column;           /* 垂直弹性布局，便于组件排列 */
        background-color: transparent;    /* 完全透明，不遮挡下层内容 */
        pointer-events: auto;             /* 确保可以接收鼠标事件 */
        box-sizing: border-box;           /* 盒模型：padding包含在总尺寸内 */
    }
    
    /* ==================== 第3层级内部组件样式 ==================== */
    
    /* 标题区域 - 位于第3层级顶部 */
    .title-section {
        text-align: center;
        margin-bottom: 3%;                /* 与下方内容的间距 */
        padding-bottom: 2%;               /* 底部内边距 */
        border-bottom: 1px solid #f0f0f0; /* 底部边框线，视觉分隔 */
        width: 100%;                      /* 占据容器全宽 */
        height: 8%;                       /* 固定高度，占容器高度的8% */
    }
    
    .main-title {
        font-size: 2.2vw;                 /* 响应式字体大小，基于视口宽度 */
        font-weight: bold;
        color: #ff69b4;                   /* 粉红色标题 */
        margin: 0;
    }
    
    /* 图片框容器 - 三个图片框的水平排列容器 */
    .image-container {
        flex: 1;                          /* 弹性填充剩余空间 */
        display: flex;
        justify-content: space-between;   /* 三个框均匀分布 */
        align-items: center;
        gap: 3%;                         /* 框之间的间距 */
        padding: 0 2%;                   /* 左右内边距 */
        width: 100%;                     /* 占据容器全宽 */
        box-sizing: border-box;
        height: 60%;                     /* 固定高度，占容器高度的60% */
    }
    
    /* 单个图片框样式 - 三个框的统一样式 */
    .image-box {
        width: 26%;                      /* 宽度占容器的26% */
        height: 80%;                     /* 高度占图片容器高度的80% */
        border: 2px dashed #4CAF50;      /* 绿色虚线边框 */
        border-radius: 12px;             /* 圆角设计 */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #f1f8e9;       /* 浅绿色背景 */
        transition: all 0.3s ease;       /* 悬停动画效果 */
        padding: 3%;                     /* 内边距 */
        position: relative;
        box-sizing: border-box;          /* 确保padding不增加总尺寸 */
    }
    
    .image-box:hover {
        border-color: #388E3C;           /* 悬停时边框颜色加深 */
        background-color: #dcedc8;       /* 悬停时背景色加深 */
        transform: translateY(-3px);     /* 悬停时上浮效果 */
    }
    
    .box-text {
        color: #2E7D32;                  /* 深绿色文字 */
        font-size: 1.2vw;                /* 响应式字体大小 */
        text-align: center;
        margin-top: 10px;                /* 与上方内容的间距 */
    }
    
    /* 运算符样式 - 加号和等号 */
    .operator {
        font-size: 2.5vw;                /* 较大的运算符字体 */
        color: #6b7280;                  /* 灰色运算符 */
        font-weight: 300;                /* 细体字重 */
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;                    /* 占据容器全高 */
    }
    
    /* 按钮容器 - 位于第三个框下方 */
    .button-container {
        display: flex;
        justify-content: center;          /* 按钮水平居中 */
        margin-top: 2%;                  /* 与上方内容的间距 */
        padding-top: 2%;                 /* 顶部内边距 */
        width: 100%;                     /* 占据容器全宽 */
        box-sizing: border-box;
        height: 15%;                     /* 固定高度，占容器高度的15% */
        border-top: none;                /* 移除顶部边框线 */
    }
    
    .generate-button {
        background-color: #3b82f6;       /* 蓝色按钮 */
        color: white;
        border: none;
        border-radius: 10px;             /* 圆角按钮 */
        padding: 12px 30px;
        font-size: 1.3vw;                /* 响应式字体大小 */
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;       /* 悬停动画 */
        width: 35%;                      /* 按钮宽度占容器的35% */
        max-width: 220px;                /* 最大宽度限制 */
        height: 60%;                     /* 高度占按钮容器的60% */
        box-sizing: border-box;
    }
    
    .generate-button:hover {
        background-color: #2563eb;       /* 悬停时蓝色加深 */
        transform: translateY(-3px);     /* 悬停时上浮效果 */
        box-shadow: 0 5px 15px rgba(37, 99, 235, 0.3);  /* 悬停阴影 */
    }
    
    /* 底部信息区域 */
    .footer {
        text-align: center;
        color: #6b7280;                  /* 灰色文字 */
        font-size: 0.9vw;                /* 较小的响应式字体 */
        margin-top: 1%;                  /* 与上方内容的间距 */
        width: 100%;                     /* 占据容器全宽 */
        box-sizing: border-box;
        height: 5%;                      /* 固定高度，占容器高度的5% */
    }
    
    /* ==================== Streamlit组件样式覆盖 ==================== */
    
    /* 强制所有Streamlit组件在第3层级显示 */
    .stFileUploader, .stButton, .stImage, .stSpinner, .stSuccess, .stWarning {
        position: relative !important;
        z-index: 3 !important;           /* 确保在第3层级内 */
        box-sizing: border-box !important;
    }
    
    /* 文件上传器样式定制 */
    .stFileUploader label {
        display: none !important;         /* 隐藏默认标签 */
    }
    
    .stFileUploader div {
        border: none !important;          /* 移除默认边框 */
        background-color: transparent !important;  /* 透明背景 */
        padding: 0 !important;
        width: 100%;
        height: 100%;
        box-sizing: border-box !important;
    }
    
    /* 【修改】自定义文件上传按钮文字为中文 */
    .stFileUploader button {
        font-family: inherit !important;
    }
    
    .stFileUploader button::after {
        content: "上传" !important;       /* 将按钮文字改为中文"上传" */
    }
    
    /* 确保所有Streamlit布局组件在第3层级 */
    .stColumn, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        position: relative !important;
        z-index: 3 !important;
        box-sizing: border-box !important;
    }
    
    /* 图片显示样式 */
    img {
        max-width: 90%;                  /* 最大宽度限制 */
        max-height: 90%;                 /* 最大高度限制 */
        object-fit: contain;             /* 保持图片比例 */
        border-radius: 8px;              /* 图片圆角 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== HTML结构 - 三层级实现 ====================

# 第1层级：灰色背景 - 最底层
# 作用：提供整个应用的背景色，不包含任何交互元素
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 第2层级：白色工作区 - 中间层  
# 作用：提供视觉容器，有背景色和阴影，但不包含具体内容
st.markdown('<div class="layer-1"></div>', unsafe_allow_html=True)

# 第3层级：透明组件容器 - 最上层
# 作用：承载所有交互组件，透明背景，与第2层级完全重合
st.markdown('<div class="layer-2">', unsafe_allow_html=True)

# 标题区域 - 在第3层级内
st.markdown('''
<div class="title-section">
    <div class="main-title">AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器 - 在第3层级内，包含三个横向排列的图片框
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 使用Streamlit的columns创建精确的横向布局
# 比例说明：[26, 3, 26, 3, 26] 表示：
# - 26%：内容图片框宽度
# - 3%：运算符间距
# - 26%：风格图片框宽度  
# - 3%：运算符间距
# - 26%：结果图片框宽度
col1, col2, col3, col4, col5 = st.columns([26, 3, 26, 3, 26])

# 内容图片框 - 第一个框
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    content_image = st.file_uploader(
        "上传内容图片",  # 【修改】改为中文提示
        type=['png', 'jpg', 'jpeg'],
        key="content",
        label_visibility="collapsed"  # 隐藏默认标签
    )
    if content_image:
        image = Image.open(content_image)
        st.image(image)
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div class="box-text">内容图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 加号运算符 - 第一个和第二个框之间
with col2:
    st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

# 风格图片框 - 第二个框
with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    style_image = st.file_uploader(
        "上传风格图片",  # 【修改】改为中文提示
        type=['png', 'jpg', 'jpeg'],
        key="style",
        label_visibility="collapsed"  # 隐藏默认标签
    )
    if style_image:
        image = Image.open(style_image)
        st.image(image)
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div class="box-text">风格图片</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 等号运算符 - 第二个和第三个框之间
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框 - 第三个框
with col5:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    if 'result_image' in st.session_state and st.session_state.result_image:
        st.image(st.session_state.result_image, caption="融合结果")
    else:
        st.markdown('''
        <div style="text-align: center; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <div class="box-text">融合结果</div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 关闭图片框容器
st.markdown('</div>', unsafe_allow_html=True)

# 生成按钮容器 - 在第3层级内，位于三个图片框下方
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("一键生成风格融合", key="generate_btn", use_container_width=False):
    if content_image and style_image:
        # 模拟生成过程
        with st.spinner("正在生成融合图片..."):
            # 这里添加实际的风格融合代码
            # 暂时使用占位图
            st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
            st.success("风格融合完成！")
            st.rerun()
    else:
        st.warning("请先上传内容图片和风格图片")
st.markdown('</div>', unsafe_allow_html=True)

# 底部信息 - 在第3层级内，最底部
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

# 关闭第3层级容器
st.markdown('</div>', unsafe_allow_html=True)

# 初始化session state - 用于存储生成结果
if 'result_image' not in st.session_state:
    st.session_state.result_image = None




