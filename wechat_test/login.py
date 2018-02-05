#-*- coding:utf-8 -*-

import itchat
import re
import jieba

def echart_pie(friends):
    total = len(friends) - 1
    male = female = other = 0

    for friend in friends[1:]:#统计男女比例
        sex = friend["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1

    #可视化
    from echarts import Echart, Legend, Pie
    chart = Echart('%s的微信好友性别比例' % (friends[0]['NickName']), 'from WeChat')
    chart.use(Pie('WeChat',
                  [{'value': male, 'name': '男性 %.2f%%' % (float(male) / total * 100)},
                   {'value': female, 'name': '女性 %.2f%%' % (float(female) / total * 100)},
                   {'value': other, 'name': '其他 %.2f%%' % (float(other) / total * 100)}],
                   radius=["50%", "70%"]))
    chart.use(Legend(["male", "female", "other"]))
    del chart.json["xAxis"]
    del chart.json["yAxis"]
    chart.plot()


def word_cloud(friends):
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud, ImageColorGenerator
    import PIL.Image as Image
    import os
    import numpy as np  #多维运算，矢量运算

    d = os.path.dirname(__file__)   #相对路径
    my_coloring = np.array(Image.open(os.path.join(d, "2.png")))#图片的矩阵
    signature_list = []
    for friend in friends:
        signature = friend["Signature"].strip()
        signature = re.sub("<span.*>", "", signature)
        signature_list.append(signature)
    raw_signature_string = ''.join(signature_list)
    text = jieba.cut(raw_signature_string, cut_all=True)#分词
    target_signatur_string = ' '.join(text)

    my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=my_coloring, max_font_size=40, random_state=42,font_path=r"/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf").generate(target_signatur_string)
    image_colors = ImageColorGenerator(my_coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()
    # 保存图片 并发送到手机
    my_wordcloud.to_file(os.path.join(d, "wechat_cloud.png"))
    #itchat.send_image("wechat_cloud.png", 'filehelper')

itchat.auto_login(hotReload=True)
itchat.dump_login_status()
 #登陆之后并保持登陆状态一段时间
     
friends = itchat.get_friends(update=True)[:]#获取好友列表,列表里第一个是自己

#echat_pie(friends)

word_cloud(friends)
