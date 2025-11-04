import streamlit as st
from PIL import Image
import io

# 页面配置 - 使用宽屏布局
st.set_page_config(
    page_title="AI画家 - 图片风格融合",  # 设置浏览器标签页标题
    page_icon="🎨",                      # 设置浏览器标签页图标
    layout="wide",                       # 使用宽屏布局模式
    initial_sidebar_state="collapsed"    # 初始状态下侧边栏为折叠状态
)

# 自定义CSS - 明确三个层级
st.markdown(
    """
    <style>
    /* 彻底禁止页面滑动 - 确保页面固定不滚动 */
    html, body, #root, [data-testid="stAppViewContainer"] {
        height: 100vh !important;        /* 高度为视口的100% */
        width: 100vw !important;         /* 宽度为视口的100% */
        overflow: hidden !important;     /* 隐藏溢出内容，禁止滚动 */
        position: fixed !important;      /* 固定定位 */
        top: 0 !important;               /* 顶部对齐 */
        left: 0 !important;              /* 左侧对齐 */
        margin: 0 !important;            /* 清除外边距 */
        padding: 0 !important;           /* 清除内边距 */
    }
    
    /* Streamlit应用主容器样式 */
    .stApp {
        height: 100vh !important;        /* 高度为视口的100% */
        width: 100vw !important;         /* 宽度为视口的100% */
        overflow: hidden !important;     /* 隐藏溢出内容 */
        position: fixed !important;      /* 固定定位 */
        top: 0 !important;               /* 顶部对齐 */
        left: 0 !important;              /* 左侧对齐 */
        margin: 0 !important;            /* 清除外边距 */
        padding: 0 !important;           /* 清除内边距 */
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}      /* 隐藏主菜单 */
    footer {visibility: hidden;}         /* 隐藏页脚 */
    header {visibility: hidden;}         /* 隐藏页眉 */
    
    /* 第1层级：灰色背景层 - 最底层 */
    .layer-0 {
        background-color: #808080;       /* 灰色背景 */
        position: fixed;                 /* 固定定位 */
        top: 0;                         /* 顶部对齐 */
        left: 0;                        /* 左侧对齐 */
        width: 100vw;                   /* 宽度为视口的100% */
        height: 100vh;                  /* 高度为视口的100% */
        z-index: 1;                     /* 层级为1（最底层） */
    }
    
    /* 第2层级：白色工作区 - 中间层 */
    .layer-1 {
        background-color: white;         /* 白色背景 */
        border-radius: 15px;             /* 圆角边框 */
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);  /* 阴影效果 */
        position: fixed;                 /* 固定定位 */
        top: 50%;                       /* 垂直居中 */
        left: 50%;                      /* 水平居中 */
        transform: translate(-50%, -50%); /* 精确居中定位 */
        width: 70%;                     /* 宽度为视口的70% */
        height: 70%;                    /* 高度为视口的70% */
        z-index: 2;                     /* 层级为2（中间层） */
        padding: 2%;                    /* 内边距 */
        display: flex;                  /* 弹性布局 */
        flex-direction: column;         /* 垂直方向排列 */
    }
    
    /* 第3层级：透明组件容器 - 最上层，用于放置交互组件 */
    .layer-2 {
        position: fixed;                 /* 固定定位 */
        top: 50%;                       /* 垂直居中 */
        left: 50%;                      /* 水平居中 */
        transform: translate(-50%, -50%); /* 精确居中定位 */
        width: 70%;                     /* 宽度与第2层级一致 */
        height: 70%;                    /* 高度与第2层级一致 */
        z-index: 3;                     /* 层级为3（最上层） */
        padding: 2%;                    /* 内边距 */
        display: flex;                  /* 弹性布局 */
        flex-direction: column;         /* 垂直方向排列 */
        background-color: transparent;  /* 完全透明背景 */
        pointer-events: auto;           /* 确保可以接收鼠标事件 */
    }
    
    /* 标题区域样式 - 位于第3层级 */
    .title-section {
        text-align: center;              /* 文字居中 */
        margin-bottom: 2%;              /* 底部外边距 */
        padding-bottom: 1%;             /* 底部内边距 */
        border-bottom: 1px solid #f0f0f0; /* 底部边框线 */
    }
    
    /* 主标题样式 */
    .main-title {
        font-size: 1.8vw;               /* 响应式字体大小 */
        font-weight: bold;              /* 粗体 */
        color: #ff69b4;                 /* 粉红色 */
        margin: 0;                      /* 清除外边距 */
    }
    
    /* 图片框容器样式 - 位于第3层级 */
    .image-container {
        flex: 1;                        /* 占据剩余空间 */
        display: flex;                  /* 弹性布局 */
        justify-content: center;        /* 水平居中 */
        align-items: center;            /* 垂直居中 */
        gap: 2%;                       /* 元素间距 */
        padding: 2%;                   /* 内边距 */
    }
    
    /* 单个图片框样式 */
    .image-box {
        width: 35%;                     /* 宽度为容器的40% */
        aspect-ratio: 2/3;              /* 宽高比2:3 */
        border: 2px dashed #4CAF50;     /* 绿色虚线边框 */
        border-radius: 10px;            /* 圆角 */
        display: flex;                  /* 弹性布局 */
        flex-direction: column;         /* 垂直方向排列 */
        align-items: center;            /* 水平居中 */
        justify-content: center;        /* 垂直居中 */
        background-color: #f1f8e9;      /* 浅绿色背景 */
        transition: all 0.3s ease;      /* 过渡动画效果 */
        padding: 1%;                   /* 内边距 */
        position: relative;             /* 相对定位 */
        overflow: hidden;               /* 新增：隐藏溢出内容 */
    }
    
    /* 图片框悬停效果 */
    .image-box:hover {
        border-color: #388E3C;          /* 悬停时边框颜色变深 */
        background-color: #dcedc8;      /* 悬停时背景颜色变深 */
    }
    
    /* 图片框内文字样式 */
    .box-text {
        color: #2E7D32;                 /* 深绿色文字 */
        font-size: 1vw;                 /* 响应式字体大小 */
        text-align: center;             /* 文字居中 */
        margin-top: 8px;                /* 顶部外边距 */
    }
    
    /* 加号运算符样式 */
    .operator {
        font-size: 4vw;                 /* 响应式字体大小 */
        color: #6b7280;                 /* 灰色 */
        font-weight: 400;               /* 细字体 */
    }
    
    /* 按钮容器样式 */
    .button-container {
        display: flex;                  /* 弹性布局 */
        justify-content: center;        /* 水平居中 */
        margin-top: 1%;                /* 顶部外边距 */
        padding-top: 1%;               /* 顶部内边距 */
        border-top: 1px solid #f0f0f0;  /* 顶部边框线 */
    }
    
    
    
    /* 生成按钮悬停效果 */
    .generate-button:hover {
        background-color: #2563eb;      /* 悬停时背景色变深 */
        transform: translateY(-2px);    /* 悬停时向上移动2像素 */
    }
    
    /* 底部信息样式 */
    .footer {
        text-align: center;              /* 文字居中 */
        color: #6b7280;                 /* 灰色文字 */
        font-size: 0.8vw;               /* 响应式小字体 */
        margin-top: 2%;                 /* 顶部外边距 */
    }
    
    /* 强制所有Streamlit组件在第3层级显示 */
    .stFileUploader, .stButton, .stImage, .stSpinner, .stSuccess, .stWarning {
        position: relative !important;   /* 相对定位 */
        z-index: 3 !important;          /* 层级为3 */
    }
    
    /* 隐藏文件上传器的标签 */
    .stFileUploader label {
        display: none !important;       /* 不显示标签 */
    }
    
    /* 文件上传器内部div样式 */
    .stFileUploader div {
        border: none !important;        /* 无边框 */
        background-color: transparent !important;  /* 透明背景 */
        padding: 0 !important;          /* 无内边距 */
        width: 75% !important;         /* 修改：宽度75% */
        height: 75% !important;        /* 修改：高度75% */
        display: flex !important;       /* 新增：弹性布局 */
        justify-content: center !important;  /* 新增：水平居中 */
        align-items: center !important; /* 新增：垂直居中 */
    }
    
    /* 确保所有列和块都在第3层级 */
    .stColumn, [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        position: relative !important;   /* 相对定位 */
        z-index: 3 !important;          /* 层级为3 */
    }
    
    /* 图片通用样式 - 修改为限制在图片框内 */
    .image-box img {
        max-width: 90% !important;      /* 修改：最大宽度90% */
        max-height: 90% !important;     /* 修改：最大高度90% */
        object-fit: contain !important; /* 保持图片比例完整显示 */
        border-radius: 8px;             /* 新增：圆角 */
    }
    
    /* 新增：文件上传器按钮样式 */
    .stFileUploader button {
        width: 100% !important;         /* 宽度100% */
        height: 100% !important;        /* 高度100% */
        border: none !important;        /* 无边框 */
        background: transparent !important;  /* 透明背景 */
    }
    
    /* 新增：文件上传器按钮内的文字样式 */
    .stFileUploader button p {
        font-size: 0.9vw !important;    /* 响应式字体大小 */
        color: #2E7D32 !important;      /* 深绿色 */
    }
    
    /* 新增：限制Streamlit图片组件在图片框内 */
    .stImage {
        max-width: 100% !important;     /* 最大宽度100% */
        max-height: 100% !important;    /* 最大高度100% */
        display: flex !important;       /* 弹性布局 */
        justify-content: center !important;  /* 水平居中 */
        align-items: center !important; /* 垂直居中 */
    }
    
    /* 新增：图片框内部容器样式 */
    .image-inner-container {
        width: 100% !important;         /* 宽度100% */
        height: 100% !important;        /* 高度100% */
        display: flex !important;       /* 弹性布局 */
        flex-direction: column !important;  /* 垂直排列 */
        justify-content: center !important;  /* 垂直居中 */
        align-items: center !important; /* 水平居中 */
        overflow: hidden !important;    /* 隐藏溢出 */
    }
    </style>
    """,
    unsafe_allow_html=True  # 允许使用HTML，注意安全风险
)

# 第1层级：灰色背景 - 创建最底层的背景
st.markdown('<div class="layer-0"></div>', unsafe_allow_html=True)

# 第2层级：白色工作区 - 创建中间层的白色面板
st.markdown('<div class="layer-1"></div>', unsafe_allow_html=True)

# 第3层级：透明组件容器 - 创建最上层的透明容器，所有交互组件放在这里
st.markdown('<div class="layer-2">', unsafe_allow_html=True)

# 标题区域 - 显示应用主标题
st.markdown('''
<div class="title-section">
    <div class="main-title">🎨 AI图片风格融合工具</div>
</div>
''', unsafe_allow_html=True)

# 图片框容器 - 包含三个图片框和运算符
st.markdown('<div class="image-container">', unsafe_allow_html=True)

# 使用Streamlit的columns创建横向布局
# 比例分配：内容图片框(1) | 加号(0.05) | 风格图片框(1) | 等号(0.05) | 结果图片框(1)
col1, col2, col3, col4, col5 = st.columns([1, 0.05, 1, 0.05, 1])

# 辅助函数：创建图片显示容器
def create_image_display(image, default_text):
    """创建图片显示容器"""
    if image:
        # 如果已上传图片，打开并显示图片
        pil_image = Image.open(image)
        return st.image(pil_image, use_column_width=True)
    else:
        # 如果未上传图片，显示占位内容
        return st.markdown(f'''
        <div class="image-inner-container">
            <div style="font-size: 3vw; color: #4CAF50;"></div>
            <div class="box-text">{default_text}</div>
        </div>
        ''', unsafe_allow_html=True)

# 内容图片框 - 第一个图片上传区域
with col1:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)  # 开始图片框
    
    # 创建内部容器来限制内容
    with st.container():
        content_image = st.file_uploader(
            "内容图片",                    # 上传器标签（被隐藏）
            type=['png', 'jpg', 'jpeg'],   # 允许的文件类型
            key="content",                 # 唯一标识符
            label_visibility="collapsed"   # 隐藏标签显示
        )
        create_image_display(content_image, "内容图片")
    
    st.markdown('</div>', unsafe_allow_html=True)  # 结束图片框

# 加号运算符 - 第一个运算符
with col2:
    st.markdown('<div class="operator">+</div>', unsafe_allow_html=True)

# 风格图片框 - 第二个图片上传区域
with col3:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)  # 开始图片框
    
    # 创建内部容器来限制内容
    with st.container():
        style_image = st.file_uploader(
            "风格图片",                    # 上传器标签（被隐藏）
            type=['png', 'jpg', 'jpeg'],   # 允许的文件类型
            key="style",                   # 唯一标识符
            label_visibility="collapsed"   # 隐藏标签显示
        )
        create_image_display(style_image, "风格图片")
    
    st.markdown('</div>', unsafe_allow_html=True)  # 结束图片框

# 等号运算符 - 第二个运算符
with col4:
    st.markdown('<div class="operator">=</div>', unsafe_allow_html=True)

# 结果图片框 - 显示融合结果的区域
with col5:
    # 创建一个垂直容器来放置图片框和按钮
    with st.container():
        # 结果图片框
        st.markdown('<div class="image-box">', unsafe_allow_html=True)  # 开始图片框
        
        # 创建内部容器来限制内容
        with st.container():
            if 'result_image' in st.session_state and st.session_state.result_image:
                # 如果已生成结果图片，显示图片
                st.image(st.session_state.result_image, use_column_width=True)
            else:
                # 如果未生成结果，显示占位内容
                st.markdown('''
                <div class="image-inner-container">
                    <div style="font-size: 3vw; color: #4CAF50;"></div>
                    <div class="box-text">融合结果</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # 结束图片框
        
        # 在图片框下方添加一些垂直间距
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        
        # 使用固定宽度的按钮布局
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])  # 左右留空，中间放按钮
        with col_btn2:
            # 生成按钮
            if st.button("一键生成", key="generate_btn", use_container_width=True):
                if content_image and style_image:
                    # 如果已上传内容图片和风格图片，开始生成过程
                    with st.spinner("正在生成融合图片..."):
                        # 这里添加实际的风格融合代码
                        # 暂时使用占位图模拟生成结果
                        st.session_state.result_image = "https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果"
                        st.success("风格融合完成！")  # 显示成功消息
                        st.rerun()  # 重新运行应用以更新界面
                else:
                    # 如果未上传图片，显示警告消息
                    st.warning("请先上传内容图片和风格图片")

# 底部信息 - 显示使用说明
st.markdown('''
<div class="footer">
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
</div>
''', unsafe_allow_html=True)

# 关闭第3层级 - 结束透明组件容器
st.markdown('</div>', unsafe_allow_html=True)  # 关闭layer-2（第3层级）

# 初始化session state - 用于存储应用状态
if 'result_image' not in st.session_state:
    st.session_state.result_image = None  # 初始化结果图片状态为None