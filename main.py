import requests
import re
import traceback
import json
from bs4 import BeautifulSoup


def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


# 获取首页常见食物分类
def get_food_class_list(gpl, main_url):
    html = get_html_text(main_url)
    soup = BeautifulSoup(html, 'html.parser')  #煮汤
    a = soup.find_all('a')  # 寻找其中所有a标签的数据
    flag = 0
    gp_dist = {}
    for i in a:
        try:
            href = i.attrs['href']  # 获取a标签的href里的信息
            gp_url = re.findall(r"/food/group/\d+", href)[0]
            if href == gp_url:
                if i.find_all('img'):
                    gp_dist.update({'imgUrl': i.find_all('img')[0].attrs['src']})  # 加入字典
                    flag = flag + 1
                else:
                    gp_dist.update({'gpName': i.text.split()[0]})
                    flag = flag + 1
            if gp_url not in snl:
                if flag == 2:
                    gp_dist.update({'gpUrl': 'http://www.boohee.com' + gp_url})
                    gpl.append(gp_dist)  # 使用正则将所需数据抽取出来给snl数组
                    flag = 0
                    gp_dist = {}
            # 到这里获得首页的对应数据
            return json.dumps(gpl)
        except:
            return ''
            continue


def search_food_list(origin_url, list):
    html = get_html_text(origin_url)
    soup = BeautifulSoup(html, 'html.parser')  # 煮汤
    food_list = soup.find_all('ul', attrs={'class': 'food-list'})[0]
    food_item = food_list.find_all('li', attrs={'class': 'item'})

    for i in range(len(food_item)):
        item_dist = {}
        img = food_item[i].find_all('div', attrs={'class': 'img-box'})[0].find('img').attrs['src']
        text_part = food_item[i].find_all('div', attrs={'class': 'text-box'})[0]
        heat_part = food_item[i].find('p').text
        title = text_part.find('a').attrs['title']
        id = text_part.find('a').attrs['href'].replace('/shiwu/', '')
        item_dist.update({
            'heat': heat_part,
            'img': img,
            'title': title,
            'id': id
        })
        list.append(item_dist)
    return json.dumps(list)


# 仅针对从列表进入的
def get_food_detail(flag):
    detail_dist = {}
    detail_url = 'http://www.boohee.com/shiwu/' + flag;
    html = get_html_text(detail_url)
    soup = BeautifulSoup(html, 'html.parser')  # 煮汤
    main_content = soup.find_all(attrs={'class': 'container'})[0]
    img_part = main_content.find_all('a', attrs={'class': 'lightbox'})[0]
    big_img = img_part.attrs['href']
    mid_img = img_part.img.attrs['src']
    food_name = img_part.img.attrs['alt']
    basic_info = main_content.find_all('div', attrs={'class': 'widget-food-detail'})[0]
    calories = basic_info.find(id='food-calory').span.text
    evaluate = basic_info.p.text.replace('评价：', '')
    nutr = main_content.find_all('div', attrs={'class': 'nutr-tag'})[0]
    nutr_list = {}
    nutr_data = nutr.find_all('dd')

    for i in nutr_data:
        nutr_list[i.find("span", attrs={"class": "dt"}).text] = \
            i.find("span", attrs={"class": "dd"}).text

    detail_dist.update({
        "big_img": big_img,
        "mid_img": mid_img,
        "food_name": food_name,
        "calories": calories,
        "evaluate": evaluate,
        "nutr_list": nutr_list
    })
    return json.dumps(detail_dist)


def main():
    depth = 2  # 可用于设置抓取的深度
    main_url = 'http://www.boohee.com/food/'
    gp_list = []
    get_food_class_list(gp_list, main_url)
    search_list = []
    search_food_list("http://www.boohee.com/food/group/1", search_list)


main()