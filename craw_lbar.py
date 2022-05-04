# Website: https://www.lbar.com/agents
# Lấy dữ liệu gồm: ảnh, tên, địa chỉ, số điện thoại, email của các nhân viên


import requests
from bs4 import BeautifulSoup
import re


link_base = "https://www.lbar.com/index.php?src=directory&view=rets_flex_active_agents&srctype=rets_flex_active_agents_lister& \
    xsearch_id=rets_flex_active_agents_alpha&xsearch=dummy&query=name.starts."
link_domain = "https://www.lbar.com/"

link_list=[]
for one in range(97,123):
    # thêm vào link kí tự a -> z bằng hàm chr()
    item = link_base + chr(one) + "&pos=0,1000,1000&xsearch_id=rets_flex_active_agents_alpha&xsearch=dummy"
    link_list.append(item)

f = open("data_lbar.csv", "a") # ghi thông tin vào file 

# phan tich cu phap, boc tach 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
for i in range(0,len(link_list)):
    print("counter: ",i)
    link = link_list[i]
    r = requests.get(link, headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    tb_data = soup.find_all('table')

    t_tr = soup.find_all('tr')

#lay thong tin tung nguoi
    for row in t_tr[1:]:

        td_list = row.find_all('td')
        # lay thong tin profile
        link_profile = link_domain + td_list[0].find_all('a')[0].get('href')
        # dung text lay ten
        name = td_list[1].get_text().split('\n')
        name.pop(0)
        name1 = name[0].strip()
        name2 = name[1].strip()
        # dug text lay dia chi
        address = td_list[2].get_text().strip().replace("   ","") 
        address = address.replace("\n","").replace(",","-")          # thay dấu , trong địa chỉ để tránh việc tách dữ liệu 
        
        # xử lí các trường hợp không có địa chỉ
        try:

            email = td_list[3].find_all('a')[0].get_text().strip()
        except:
            email = ''

        phone = td_list[3].get_text()
        
        # xử lí các trường hợp không có điện thoại
        try:

            p = re.compile(r"\([0-9]{3}\)\s+[0-9]{3}\-[0-9]{4}")
            x = p.search(phone)
            phone_number = x.group(0)
        except:
            phone_number=""


        str = f"{link_profile},{name1},{name2},{address},{email},{phone_number},\n"
        f.write(str)
        
f.write("Now the file has more content!")
        


