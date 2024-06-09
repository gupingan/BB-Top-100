from PySide6 import QtCore

# 应用基本信息
# ///////////////////////////////////////////////////////////
app_name = '哔哩哔哩 - 数据分析'  # 应用名称
header_center_context = ''  # 标题头中部内容

app_icon_path = './assets/images/app.png'  # app 图标的路径
app_logs_path = './logs'  # 日志所在目录的路径
rank_data_path = './data/bilibili.xlsx'  # 排行榜表格的存储路径
comments_of_first_path = './data/comments_of_first.xml'  # 排行榜第一名视频弹幕的存储路径

rank_data = []  # 存储所需的排行榜数据
comments_of_first = []  # 存储弹幕内容
jieba_comments = []  # 利用NLP分词后的列表

canvas_dpi = 100  # 绘制分析图的 DPI
background_color = '#FFFFFF'  # 背景颜色 默认白色

left_button_texts = ['弹幕云图', '总和饼图', '播放量柱图', '行为折线图', '行为饼图']

wordcloud_config = {
    'width': 800,
    'height': 600,
    'background_color': background_color,  # 背景颜色
    'max_words': 2000,  # 最大词数
    'max_font_size': 100,  # 最大字体
    'min_font_size': 16,  # 最小字体
    'font_path': './assets/fonts/msyh.ttc',  # 字体文件路径，确保支持中文
}

canvas1_config = {
    'fig_facecolor': background_color,  # 整个图表的背景颜色
    'ax_facecolor': background_color,  # 子图的背景颜色
    'labels': ['观看', '点赞', '转发', '评论'],
    'colors': ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],  # 每个楔形的颜色
    'autopct': '%.2f%%',  # 百分比标签格式
    'shadow': False,  # 是否显示阴影
    'startangle': 140,  # 起始角度
    'wedgeprops': {'width': 0.3, 'edgecolor': 'w'},  # 楔形的属性
    'pctdistance': 0.85,  # 百分比标签离饼图的距离
    'explode': (0.1, 0),  # 分离效果
    'labeldistance': 1.1,  # 标签距离
    'label_color': 'grey',  # 标签颜色
    'label_fontsize': 12,  # 标签字体大小
    'autotext_color': 'black',  # 百分比标签颜色
    'autotext_fontsize': 11,  # 百分比标签字体大小
    'autotext_fontweight': 'bold'  # 百分比标签字体粗细
}

canvas2_config = {
    'fig_facecolor': background_color,  # 整个图表的背景颜色
    'ax_facecolor': background_color,  # 子图的背景颜色
    'xlabel': '排名',  # x轴标签
    'ylabel': '播放量(万)',  # y轴标签
    'title': '播放量柱状图统计',  # 图表标题
    'grid': True,  # 是否显示网格
    'grid_color': '#cccccc',  # 网格颜色
    'grid_linestyle': '--',  # 网格线型
    'grid_linewidth': 0.5,  # 网格线宽
    'xlabel_fontsize': 12,  # x轴标签字体大小
    'ylabel_fontsize': 12,  # y轴标签字体大小
    'title_fontsize': 14,  # 标题字体大小
    'bar_width': 0.8,  # 柱状图宽度
    'bar_color': '#8A8AFF',  # 柱状图颜色
    'edge_color': '#0000FF',  # 柱状图边框颜色
    'edge_width': 0.5  # 柱状图边框宽度
}

canvas3_config = {
    'fig_facecolor': background_color,  # 整个图表的背景颜色
    'ax_facecolor': background_color,  # 子图的背景颜色
    'line1_color': 'blue',  # 第一条折线（点赞）的颜色
    'line2_color': 'red',  # 第二条折线（收藏）的颜色
    'line3_color': 'green',  # 第三条折线（转发）的颜色
    'marker': 'o',  # 数据点的标记样式
    'marker_size': 30,  # 数据点的标记大小
    'label_interval': 20,  # 数据点标签的间隔
    'title': '点赞、收藏、转发折线图',  # 图表的标题
    'title_fontsize': 14,  # 图表标题的字体大小
    'xlabel': '时间',  # X轴的标签
    'xlabel_fontsize': 12,  # X轴标签的字体大小
    'ylabel': '数量',  # Y轴的标签
    'ylabel_fontsize': 12,  # Y轴标签的字体大小
    'grid': True,  # 是否显示网格
    'grid_color': 'gray',  # 网格线的颜色
    'grid_linestyle': '--',  # 网格线的样式
    'grid_linewidth': 0.5  # 网格线的宽度
}

canvas4_config = {
    'fig_facecolor': background_color,  # 整个图表的背景颜色
    'ax_facecolor': background_color,  # 子图的背景颜色
    'labels': ['点赞', '投币', '收藏', '白嫖'],
    'colors': ['#89CFF0', '#0000FF', '#00008B', '#191970'],  # 饼图的颜色列表
    'shadow': False,  # 是否显示阴影
    'startangle': 140,  # 起始角度
    'label_color': 'white',  # 饼图标签的颜色
    'label_fontsize': 8,  # 饼图标签的字体大小
    'labeldistance': 0.5,  # 标签距离
    'explode': (0.1, 0.1, 0.1, 0.1),  # 分离效果
    'autopct': '%.2f%%',  # 百分比标签格式
    'pctdistance': 1.4,  # 百分比标签离饼图的距离
    'autotext_fontsize': 12,  # 饼图百分比文字的字体大小
    'autotext_color': 'black',  # 饼图百分比文字的颜色
    'autotext_fontweight': 'bold'  # 百分比标签字体粗细
}

is_debug = False  # 调试模式开关
settings = QtCore.QSettings('gupingan', 'display_bilibili_data')
threads = []  # 线程存储列表

# 以下为请求携带信息
# ///////////////////////////////////////////////////////////
# Cookies 值
cookies = {
    'LIVE_BUVID': 'AUTO9316483489499086',
    'CURRENT_FNVAL': '4048',
    'header_theme_version': 'CLOSE',
    'buvid4': 'D99D9D06-9716-972D-13C4-C9B760A51D9F42321-022032710-SV44yNkYjlH6%2Fl37PHzku7Wf%2Foz%2BE8kE%2FEYIdsPt4bBpGHtMsNABEg%3D%3D',
    'PVID': '1',
    'DedeUserID': '2130323544',
    'DedeUserID__ckMd5': 'c68f26c0b07ccfb4',
    'enable_web_push': 'DISABLE',
    'buvid3': '48D1B548-6EF5-577E-C95D-8E84DDCAA22E78014infoc',
    'b_nut': '100',
    '_uuid': '982F3A12-10D9C-4338-4842-10E7B55ECF61280218infoc',
    'FEED_LIVE_VERSION': 'V8',
    'rpdid': "|(um~JlmlR~Y0J'u~ukRmkY~R",
    'buvid_fp': 'e442bb8d30363cc926ed67f3b1294179',
    'home_feed_column': '5',
    'bp_t_offset_2130323544': '932829672215937030',
    'browser_resolution': '1528-716',
    'b_lsid': '28DBEB62_18FE68C0833',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTc4MTkwODgsImlhdCI6MTcxNzU1OTgyOCwicGx0IjotMX0.THfHLyg--5oyVOL-FXQqpKWpGGrDkAvcUbLnIRK3PI0',
    'bili_ticket_expires': '1717819028',
    'SESSDATA': '0f492d14%2C1733111889%2C12a29%2A61CjDdC3ur5z91LiqVXiJ-dvgOMADcfw-iBI3iEAV4e1B_4S4-UuYeMGlL93j63AVcO5ASVlZzT3cwSUJqdTFyNXpCdC11VGQzcDgxWlRNY1p5c1JaOW8weWpObmtsVWd5T0ZYZmhrWHR5QTdfWG5HYTZxd1NTNlJmODBCNVhKU2xJUFRaTndjSk5BIIEC',
    'bili_jct': '996bff7e6e8bb2181f9f4f6cce04c689',
    'sid': '8u4w9zoo',
}

# 请求头信息
headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'origin': 'https://www.bilibili.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/v/popular/rank/all/',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
}
