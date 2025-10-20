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

# 创建层面1的容器 - 3:2比例的主要工作区
with st.container():
    # 使用columns创建3:2比例的布局
    col1, col2, col3 = st.columns([3, 2, 3])  # 左右留白，中间是3:2区域
    
    with col2:  # 这是中间的3:2比例区域
        st.markdown(
            """
            <style>
            .main-container {
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                background-color: #f8f9fa;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # 层面1的内容
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        st.subheader("📁 上传图片进行风格融合")
        
        # 创建三个并排的输入框/图片显示区域
        col_left, col_plus, col_right = st.columns([1, 0.2, 1])
        
        with col_left:
            st.markdown("**内容图片**")
            content_image = st.file_uploader(
                "上传内容图",
                type=['png', 'jpg', 'jpeg'],
                key="content",
                label_visibility="collapsed"
            )
            if content_image:
                image = Image.open(content_image)
                st.image(image, use_column_width=True, caption="内容图片")
            else:
                st.info("请上传内容图片")
        
        with col_plus:
            st.markdown("<br><br><br><h2>+</h2>", unsafe_allow_html=True)
        
        with col_right:
            st.markdown("**风格图片**")
            style_image = st.file_uploader(
                "上传风格图", 
                type=['png', 'jpg', 'jpeg'],
                key="style",
                label_visibility="collapsed"
            )
            if style_image:
                image = Image.open(style_image)
                st.image(image, use_column_width=True, caption="风格图片")
            else:
                st.info("请上传风格图片")
        
        # 生成按钮
        st.markdown("---")
        generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])
        with generate_col2:
            if st.button("🚀 生成风格融合图片", use_container_width=True):
                if content_image and style_image:
                    st.success("开始生成融合图片...")
                    # 这里后面添加实际的风格融合代码
                    # 暂时显示一个占位图
                    st.image("https://via.placeholder.com/400x300/4CAF50/FFFFFF?text=融合结果预览", 
                            caption="风格融合结果")
                else:
                    st.warning("请先上传内容和风格图片")
        
        st.markdown('</div>', unsafe_allow_html=True)

# 底部信息
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    使用说明：上传内容图片和风格图片，点击生成按钮即可获得风格融合后的图片
    </div>
    """,
    unsafe_allow_html=True
)

# 初始化session state
if 'content_img' not in st.session_state:
    st.session_state.content_img = None
if 'style_img' not in st.session_state:
    st.session_state.style_img = None
