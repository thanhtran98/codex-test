import requests, json, ast, io
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
root=Path('chung-khao/app');work=Path('out/work/anh-dia-diem')
def source(n,contains):
 for l in (work/n).read_text().splitlines():
  if l.startswith('('):
   a=ast.literal_eval(l)
   if contains in a[0]:return a[0]
rows=[
['troh-bu','Vườn Troh Bư','https://vietnamtourism.vn/imguploads/news/vn/2013/16_vuondaklak.jpg','https://vietnamtourism.vn/index.php/news/items/10114','Cục Du lịch Quốc gia Việt Nam','Khu vườn xanh tại Troh Bư'],
['gia-long','Thác Gia Long','https://dulich.daknong.gov.vn/DataFiles/2022/03/Files/20220303-151131-RnurRCo4.webp','https://dulich.daknong.gov.vn/vi/gallery/details/thac-gia-long-4','Du lịch Đắk Nông','Dòng nước thác Gia Long giữa rừng'],
['dray-sap','Thác Dray Sáp','https://www.vamvo.com/Portals/0/hinhb/vietnam-travel/dak-lak/dray-sap/thac-dray-sap-11.jpg','https://www.vamvo.com/Photos/tabid/334/AlbumID/311/selectedmoduleid/1024/Default.aspx','Vamvo','Toàn cảnh thác Dray Sáp'],
['yok-don','Vườn quốc gia Yok Đôn','https://upload.wikimedia.org/wikipedia/commons/3/36/Yokdon8.JPG','https://commons.wikimedia.org/wiki/File:Yokdon8.JPG','Đỗ Tuấn Hưng · CC BY-SA 3.0','Rừng khộp Yok Đôn trong mùa khô'],
['yang-praong','Tháp Yang Praong','https://upload.wikimedia.org/wikipedia/commons/e/eb/Th%C3%A1p_Yang_Prong.jpg','https://commons.wikimedia.org/wiki/File:Th%C3%A1p_Yang_Prong.jpg','Shansov.net · CC BY 3.0','Tháp Yang Praong giữa những tán cây'],
['museum-coffee','Bảo tàng Thế giới Cà phê','https://baotangthegioicaphe.com/Data/Sites/1/media/content/bao-tang-the-gioi-ca-phe-1.jpg','https://baotangthegioicaphe.com/bao-tang-the-gioi-ca-phe-khi-du-lich-la-ket-tinh-cua-van-hoa-va-cam-hung','Bảo tàng Thế giới Cà phê','Kiến trúc Bảo tàng Thế giới Cà phê'],
['museum-daklak','Bảo tàng Đắk Lắk','https://hn.ss.bfcplatform.vn/tckt/2021/08/21A07057-3.jpg','https://www.tapchikientruc.com.vn/tac-gia-tac-pham/bao-tang-dak-lak.html','Tạp chí Kiến trúc','Kiến trúc Bảo tàng Đắk Lắk'],
['prison','Nhà đày Buôn Ma Thuột',source('nguon-7.txt','33-7702'),'https://tienphong.vn/ben-trong-di-tich-quoc-gia-dac-biet-nha-day-buon-ma-thuot-post1553721.tpo','Báo Tiền Phong','Toàn cảnh di tích Nhà đày Buôn Ma Thuột'],
]
def download(row):
 ident,name,url,page,credit,alt=row
 try:
  r=requests.get(url,timeout=30);r.raise_for_status(); im=Image.open(io.BytesIO(r.content));im.load()
  im=im.convert('RGB');im.thumbnail((1200,1000));p=root/'images'/f'{ident}.jpg';im.save(p,quality=87,optimize=True)
  return dict(id=ident,name=name,image=f'./images/{ident}.jpg',alt=alt,sourceUrl=page,imageUrl=url,credit=credit,width=im.width,height=im.height,change='Thu nhỏ và nén JPEG; khung hiển thị cắt bằng CSS.',license='CC BY-SA 3.0' if ident=='yok-don' else 'CC BY 3.0' if ident=='yang-praong' else 'Chưa xác minh giấy phép tái sử dụng; ghi nhận nguồn công khai.')
 except Exception as e:return dict(id=ident,error=type(e).__name__+': '+str(e)[:180])
with ThreadPoolExecutor(max_workers=5) as pool:result=list(pool.map(download,rows))
result.append(dict(id='chu-yang-sin',name='Vườn quốc gia Chư Yang Sin',image='./images/vuon-quoc-gia-chu-yang-sin.jpg',alt='Rừng và vách đá tại Vườn quốc gia Chư Yang Sin',sourceUrl='https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html',credit='Đỗ Tuấn Hưng · VnExpress',change='Dùng ảnh sẵn có trong dự án.',license='Chưa xác minh giấy phép tái sử dụng; ghi nhận nguồn công khai.'))
(work/'anh-da-chon.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
for r in result:print(r['id'],r.get('error',str((r.get('width'),r.get('height')))))
