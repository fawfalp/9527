import streamlit as st
import os
import re

st.set_page_config(page_title="AI智能重命名", layout="wide")

st.title("🤖 AI智能文件重命名工具")
st.markdown("本地运行，保护隐私，不上传云端")

# 文件夹选择
folder_path = st.text_input("📁 输入文件夹路径（如：D:\\\\照片）", "")

if folder_path and os.path.exists(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    st.success(f"找到 {len(files)} 个文件")
    
    if files:
        # 显示原文件名
        with st.expander("查看原文件列表"):
            for i, f in enumerate(files[:10], 1):
                st.text(f"{i}. {f}")
            if len(files) > 10:
                st.text(f"... 还有 {len(files)-10} 个文件")
        
        # 重命名规则
        st.markdown("---")
        st.subheader("📝 命名规则")
        
        col1, col2 = st.columns(2)
        with col1:
            prefix = st.text_input("前缀（如：2025春节）", "新文件")
        with col2:
            start_num = st.number_input("起始序号", min_value=1, value=1, step=1)
        
        # 预览
        st.markdown("---")
        st.subheader("👁️ 预览新文件名")
        
        new_names = []
        for i, old_name in enumerate(files):
            ext = os.path.splitext(old_name)[1]  # 保留扩展名
            new_name = f"{prefix}_{start_num+i:03d}{ext}"
            new_names.append((old_name, new_name))
        
        # 显示预览表格
        preview_data = [{"原文件名": old, "新文件名": new} for old, new in new_names[:5]]
        st.table(preview_data)
        if len(new_names) > 5:
            st.text(f"... 还有 {len(new_names)-5} 个文件")
        
        # 执行按钮
        st.markdown("---")
        if st.button("🚀 确认重命名", type="primary"):
            success_count = 0
            error_count = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, (old_name, new_name) in enumerate(new_names):
                try:
                    old_path = os.path.join(folder_path, old_name)
                    new_path = os.path.join(folder_path, new_name)
                    os.rename(old_path, new_path)
                    success_count += 1
                    status_text.text(f"处理中：{new_name}")
                except Exception as e:
                    error_count += 1
                    st.error(f"重命名失败 {old_name}: {e}")
                
                progress_bar.progress((i + 1) / len(new_names))
            
            st.success(f"✅ 完成！成功 {success_count} 个，失败 {error_count} 个")
            
            # 显示结果
            final_files = os.listdir(folder_path)
            st.markdown("---")
            st.subheader("📋 重命名后文件列表")
            for f in sorted(final_files)[:10]:
                st.text(f)
else:
    if folder_path:
        st.error("❌ 路径不存在，请检查")
    
    # 示例说明
    st.info("""
    💡 **使用示例**：
    1. 在文件夹路径输入：`D:\\\\我的照片`
    2. 前缀输入：`2025春节`
    3. 起始序号：`1`
    4. 预览确认后，点击"确认重命名"
    
    结果：`2025春节_001.jpg`, `2025春节_002.jpg` ...
    """)

# 底部信息
st.markdown("---")
st.caption("🔒 纯本地运行 | 数据不上传 | 由 AI 驱动")