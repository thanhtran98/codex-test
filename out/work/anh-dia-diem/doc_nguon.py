import requests, concurrent.futures
from bs4 import BeautifulSoup
urls=[
'https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html',
'https://dulich.daknong.gov.vn/vi/gallery/details/thac-gia-long-4',
'https://www.vamvo.com/Photos/tabid/334/AlbumID/311/selectedmoduleid/1024/Default.aspx',
'https://commons.wikimedia.org/wiki/File:Yokdon8.JPG',
'https://commons.wikimedia.org/wiki/Category:Thap_Yang_Prong',
'https://baotangthegioicaphe.com/chinh-thuc-khai-truong-bao-tang-the-gioi-ca-phe-diem-den-moi-cua-viet-nam',
'https://www.tapchikientruc.com.vn/tac-gia-tac-pham/bao-tang-dak-lak.html',
'https://tienphong.vn/ben-trong-di-tich-quoc-gia-dac-biet-nha-day-buon-ma-thuot-post1553721.tpo']
def read(u):
 try:
  r=requests.get(u,timeout=25);s=BeautifulSoup(r.content,'html.parser'); lines=[u,str(r.status_code)]
  if 'vnexpress' in u:
   a=s.select_one('article'); lines += [str(a)[max(0,str(a).find(t)-200):str(a).find(t)+1700] for t in ['Troh Bư','quoc-gia-dak-lak','Thủy điện Buôn Trấp']]
  else:
   for i in s.select('img'):
    src=i.get('data-src') or i.get('src','')
    if any(t in src.lower() for t in ['logo','icon','banner','avatar']):continue
    lines.append(str((src,i.get('alt',''),i.parent.get_text(' ',strip=True)[:100])))
  return '\n'.join(lines)
 except Exception as e:return u+' '+type(e).__name__
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for i,result in enumerate(pool.map(read,urls)):
  open(f'out/work/anh-dia-diem/nguon-{i}.txt','w').write(result)
  print(result[:10000])
