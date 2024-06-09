import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from wordcloud import WordCloud
from PySide6 import QtWidgets
from app.interface import common

matplotlib.use('QtAgg')
plt.rcParams["font.sans-serif"] = ["SimHei"]


class Canvas1(FigureCanvas):
    """
    将隔个数量的总和对比各个总和的总数量的饼状体
    分成三个饼状图在一张布上面
    """

    def __init__(self, parent=None, width=5, height=4, dpi=common.canvas_dpi):
        self.fig, self.ax = plt.subplots(1, 3, figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(common.canvas1_config['fig_facecolor'])
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self):
        view_sum = 0
        dianzhan_sum = 0
        pinglun_sum = 0
        zhuanfa_sum = 0
        for value in common.rank_data:
            view_sum += value[1]
            dianzhan_sum += value[2]
            pinglun_sum += value[6]
            zhuanfa_sum += value[7]
        # print(view_sum, dianzhan_sum, pinglun_sum, zhuanfa_sum)
        data = [dianzhan_sum, pinglun_sum, zhuanfa_sum]
        labels = common.canvas1_config['labels']
        self.wedges = []
        for i in range(3):
            wedges, texts, autotexts = self.ax[i].pie(
                [view_sum, data[i]],
                labels=[labels[0], labels[i + 1]],
                autopct=common.canvas1_config['autopct'],
                shadow=common.canvas1_config['shadow'],
                startangle=common.canvas1_config['startangle'],
                colors=common.canvas1_config['colors'],
                wedgeprops=common.canvas1_config['wedgeprops'],
                pctdistance=common.canvas1_config['pctdistance'],
                explode=common.canvas1_config['explode'],
                labeldistance=common.canvas1_config['labeldistance']
            )
            self.ax[i].axis('equal')
            self.ax[i].set_facecolor(common.canvas1_config['ax_facecolor'])
            self.wedges.extend(wedges)
            # 美化标签
            for text in texts:
                text.set_color(common.canvas1_config['label_color'])
                text.set_fontsize(common.canvas1_config['label_fontsize'])
            for autotext in autotexts:
                autotext.set_color(common.canvas1_config['autotext_color'])
                autotext.set_fontsize(common.canvas1_config['autotext_fontsize'])
                autotext.set_fontweight(common.canvas1_config['autotext_fontweight'])

        self.draw()
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def on_hover(self, event):
        for wedge in self.wedges:
            if wedge.contains(event)[0]:
                wedge.set_edgecolor('grey')
                wedge.set_linewidth(2)
            else:
                wedge.set_edgecolor('none')
                wedge.set_linewidth(0)
        self.draw()


class Canvas2(FigureCanvas):
    """
    播放量柱状图统计
    """

    def __init__(self, parent=None, width=5, height=4, dpi=common.canvas_dpi):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(common.canvas2_config['fig_facecolor'])
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.set_facecolor(common.canvas2_config['ax_facecolor'])

    def plot(self):
        keys = []
        values = []
        for value in common.rank_data:
            keys.append(value[0])
            values.append(value[1] / 10000)

        self.ax.clear()  # 清除之前的图表
        bars = self.ax.bar(keys, values,
                           color=common.canvas2_config['bar_color'],
                           width=common.canvas2_config['bar_width'],
                           edgecolor=common.canvas2_config['edge_color'],
                           linewidth=common.canvas2_config['edge_width'])

        self.ax.set_xlabel(common.canvas2_config['xlabel'], fontsize=common.canvas2_config['xlabel_fontsize'])
        self.ax.set_ylabel(common.canvas2_config['ylabel'], fontsize=common.canvas2_config['ylabel_fontsize'])
        self.ax.set_title(common.canvas2_config['title'], fontsize=common.canvas2_config['title_fontsize'])

        if common.canvas2_config['grid']:
            self.ax.grid(True, color=common.canvas2_config['grid_color'],
                         linestyle=common.canvas2_config['grid_linestyle'],
                         linewidth=common.canvas2_config['grid_linewidth'])

        # 添加交互功能
        self.annotation = self.ax.annotate("", xy=(0, 0), xytext=(20, 20),
                                           textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
                                           arrowprops=dict(arrowstyle="->"))
        self.annotation.set_visible(False)
        self.bars = bars
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)
        self.draw()

    def on_hover(self, event):
        vis = self.annotation.get_visible()
        if event.inaxes == self.ax:
            for bar in self.bars:
                cont, _ = bar.contains(event)
                if cont:
                    self.update_annotation(bar)
                    self.annotation.set_visible(True)
                    self.draw()
                    return
        if vis:
            self.annotation.set_visible(False)
            self.draw()

    def update_annotation(self, bar):
        x = int(bar.get_x() + bar.get_width() / 2)
        y = bar.get_height()
        self.annotation.xy = (x, y)
        text = f"{x}: {y:.2f} 万"
        self.annotation.set_text(text)


class Canvas3(FigureCanvas):
    """
    点赞、收藏、投币折线图，设置节点上的数字
    """

    def __init__(self, parent=None, width=8, height=6, dpi=common.canvas_dpi):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(common.canvas3_config['fig_facecolor'])
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.set_facecolor(common.canvas3_config['ax_facecolor'])

    def plot(self):
        dianzhan = []
        shoucang = []
        zhuanfa = []
        for value in common.rank_data:
            dianzhan.append(value[2])
            shoucang.append(value[4])
            zhuanfa.append(value[7])

        self.ax.clear()  # 清除之前的图表

        # 绘制折线图
        self.ax.plot(dianzhan, label='点赞', color=common.canvas3_config['line1_color'])
        self.ax.plot(shoucang, label='收藏', color=common.canvas3_config['line2_color'])
        self.ax.plot(zhuanfa, label='转发', color=common.canvas3_config['line3_color'])

        # 设置节点上的数字和标记
        for i in range(0, len(dianzhan), common.canvas3_config['label_interval']):
            self.ax.text(i, dianzhan[i], dianzhan[i], ha='center', va='bottom',
                         color=common.canvas3_config['line1_color'])
            self.ax.text(i, shoucang[i], shoucang[i], ha='center', va='bottom',
                         color=common.canvas3_config['line2_color'])
            self.ax.text(i, zhuanfa[i], zhuanfa[i], ha='center', va='bottom',
                         color=common.canvas3_config['line3_color'])
            self.ax.scatter(i, dianzhan[i], color=common.canvas3_config['line1_color'],
                            marker=common.canvas3_config['marker'], s=common.canvas3_config['marker_size'])
            self.ax.scatter(i, shoucang[i], color=common.canvas3_config['line2_color'],
                            marker=common.canvas3_config['marker'], s=common.canvas3_config['marker_size'])
            self.ax.scatter(i, zhuanfa[i], color=common.canvas3_config['line3_color'],
                            marker=common.canvas3_config['marker'], s=common.canvas3_config['marker_size'])

        # 设置图例
        self.ax.legend()

        # 设置标题和标签
        self.ax.set_title(common.canvas3_config['title'], fontsize=common.canvas3_config['title_fontsize'])
        self.ax.set_xlabel(common.canvas3_config['xlabel'], fontsize=common.canvas3_config['xlabel_fontsize'])
        self.ax.set_ylabel(common.canvas3_config['ylabel'], fontsize=common.canvas3_config['ylabel_fontsize'])

        # 设置网格
        if common.canvas3_config['grid']:
            self.ax.grid(True, color=common.canvas3_config['grid_color'],
                         linestyle=common.canvas3_config['grid_linestyle'],
                         linewidth=common.canvas3_config['grid_linewidth'])

        # 添加交互功能
        self.annotation = self.ax.annotate(
            "", xy=(0, 0), xytext=(10, 10),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        self.annotation.set_visible(False)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_hover)

        self.draw()

    def on_hover(self, event):
        vis = self.annotation.get_visible()
        if event.inaxes == self.ax:
            for line in self.ax.get_lines():
                cont, ind = line.contains(event)
                if cont:
                    x, y = line.get_data()
                    self.update_annotation(x[ind["ind"][0]], y[ind["ind"][0]])
                    self.annotation.set_visible(True)
                    self.draw()
                    return
        if vis:
            self.annotation.set_visible(False)
            self.draw()

    def update_annotation(self, x, y):
        self.annotation.xy = (x, y)
        text = f"{x:.0f}: {y:.0f}"
        self.annotation.set_text(text)


class Canvas4(FigureCanvas):
    """
    每个的白嫖、点赞、投币、收藏的饼图
    """

    def __init__(self, parent=None, width=8, height=6, dpi=common.canvas_dpi):
        self.fig, self.ax = plt.subplots(2, 5, figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(common.canvas4_config['fig_facecolor'])
        super().__init__(self.fig)
        self.setParent(parent)

    def plot(self):
        datas = []
        for value in common.rank_data:
            dianzhan = value[2]
            toubi = value[3]
            shoucang = value[4]
            baipiao = value[1] - dianzhan - toubi - shoucang
            datas.append([dianzhan, toubi, shoucang, baipiao])
        self.wedges = []
        for i in range(2):
            for j in range(5):
                wedges, texts, autotexts = self.ax[i, j].pie(
                    datas[i],
                    labels=common.canvas4_config['labels'],
                    colors=common.canvas4_config['colors'],
                    autopct=common.canvas4_config['autopct'],
                    explode=common.canvas4_config['explode'],
                    shadow=common.canvas4_config['shadow'],
                    startangle=common.canvas4_config['startangle'],
                    labeldistance=common.canvas4_config['labeldistance'],
                    pctdistance=common.canvas4_config['pctdistance'],
                )
                self.ax[i, j].axis('equal')
                self.ax[i, j].set_facecolor(common.canvas4_config['ax_facecolor'])

                self.wedges.extend(wedges)
                # 美化标签
                for text in texts:
                    text.set_color(common.canvas4_config['label_color'])
                    text.set_fontsize(common.canvas4_config['label_fontsize'])
                for autotext in autotexts:
                    autotext.set_color(common.canvas4_config['autotext_color'])
                    autotext.set_fontsize(common.canvas4_config['autotext_fontsize'])
                    autotext.set_fontweight(common.canvas4_config['autotext_fontweight'])
        self.draw()

        self.fig.canvas.mpl_connect('motion_notify_event', self.on_hover)

    def on_hover(self, event):
        for wedge in self.wedges:
            if wedge.contains(event)[0]:
                wedge.set_edgecolor('grey')
                wedge.set_linewidth(2)
            else:
                wedge.set_edgecolor('none')
                wedge.set_linewidth(0)
        self.draw()


class WordCloudWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.switch = QtWidgets.QCheckBox('启用分词效果', self)
        self.switch.stateChanged.connect(self.update_wordcloud)
        self.switch.setChecked(False)
        switch_layout = QtWidgets.QHBoxLayout(self)
        switch_layout.addStretch()
        switch_layout.addWidget(self.switch)

        self.canvas = FigureCanvas(plt.Figure())

        self.layout.addLayout(switch_layout)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
        self.update_wordcloud()

    def update_wordcloud(self):
        if self.parent().width() > common.wordcloud_config['width']:
            common.wordcloud_config['width'] = self.parent().width()
        if self.parent().height() > common.wordcloud_config['height']:
            common.wordcloud_config['height'] = self.parent().height()

        if self.switch.isChecked():
            text = ' '.join(common.jieba_comments)
        else:
            text = ' '.join(common.comments_of_first)

        wordcloud = WordCloud(**common.wordcloud_config).generate(text)

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')

        self.canvas.figure.set_facecolor(common.wordcloud_config['background_color'])
        self.canvas.draw()
