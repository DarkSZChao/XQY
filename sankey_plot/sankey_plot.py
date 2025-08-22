import glob
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


def generate_sankey_from_csv(csv_path, output_dir="sankey_output"):
    """
    从单个CSV文件生成交互式桑基图并保存为HTML

    参数:
        csv_path (str): 输入的CSV文件路径
        output_dir (str): 输出HTML的目录（默认"sankey_output"）
    """
    # 读取数据
    df = pd.read_csv(csv_path)

    # 检查必要列是否存在
    required_columns = {'source', 'target', 'value'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        print(f"跳过文件 {csv_path} - 缺少必要列: {missing}")
        return

    # 提取所有唯一节点并按字母顺序排序
    all_nodes = pd.concat([df['source'], df['target']]).unique()
    all_nodes_sorted = sorted(all_nodes)
    num_nodes = len(all_nodes_sorted)

    # 动态计算高度（基础高度+每个节点的额外空间）
    base_height = 400  # 基础高度
    node_height = 20  # 每个节点占用的高度
    dynamic_height = base_height + num_nodes * node_height

    # 动态计算节点厚度（基于数据量）
    max_value = df['value'].max()
    min_thickness = 10
    max_thickness = 20
    node_thickness = min(max_thickness, max(min_thickness, max_value / 5))

    # 字体大小配置
    title_font_size = 18  # 标题字体
    label_font_size = 14  # 节点标签字体
    hover_font_size = 12  # 悬停信息字体

    # 创建桑基图
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=15,  # 增大的节点间距
            thickness=node_thickness,  # 增大的节点厚度
            line=dict(color="black", width=1),  # 加粗的边框
            label=all_nodes_sorted,
            hoverlabel=dict(font=dict(size=hover_font_size)),  # 修正的悬停字体设置
        ),
        link=dict(
            source=[all_nodes_sorted.index(s) for s in df['source']],
            target=[all_nodes_sorted.index(t) for t in df['target']],
            value=df['value'],
            hoverinfo="all",
            hoverlabel=dict(font=dict(size=hover_font_size))  # 修正的悬停字体设置
        )
    ))

    # 设置布局
    filename = Path(csv_path).stem
    fig.update_layout(
        title_text=f"Sankey Diagram - {filename}",
        title_font=dict(size=title_font_size),
        font=dict(size=label_font_size),  # 全局字体大小
        height=dynamic_height,
        margin=dict(l=80, r=80, b=120, t=120, pad=15),  # 增大的边距
        hoverlabel=dict(
            font_size=hover_font_size,
            bgcolor="white"  # 白色悬停背景提高可读性
        )
    )

    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 保存HTML（与CSV同文件名）
    output_path = Path(output_dir) / f"{filename}.html"
    fig.write_html(output_path)
    print(f"成功生成: {output_path} (高度: {dynamic_height}px, 节点: {num_nodes}个)")


# 使用示例
if __name__ == "__main__":
    input_path = "./*.csv"
    csv_files = glob.glob(input_path)

    if not csv_files:
        print(f"没有找到匹配 {input_path} 的CSV文件")

    print(f"找到 {len(csv_files)} 个CSV文件，开始处理...")

    for csv_file in csv_files:
        generate_sankey_from_csv(csv_file, './')

    print("批量处理完成！")
