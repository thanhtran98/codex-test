import requests,json,io,ast,subprocess
from pathlib import Path
from PIL import Image
p=Path('out/work/anh-dia-diem/anh-da-chon.json');rows=json.loads(p.read_text())
fix={
'yok-don':('https://cdn.nhandan.vn/images/PtqBLtqtAh8ZpvFp0owaHBqRBJR2Zk0PhOjQWB79Z_Mp1OC7tQSat1c2U7NwpRX4SSBIBkv6SyHSz4YOj8Oyhw/ndo_tl_img-1639-1383.jpg.avif','https://nhandan.vn/anh-say-dam-rung-khop-mua-thay-la-post940867.html','Báo Nhân Dân','Vườn quốc gia Yok Đôn','Rừng khộp Yok Đôn vào mùa thay lá'),
'yang-praong':('https://vietnamtourism.vn/imguploads/tourist/16ThapChamYangProng01.jpg','https://vietnamtourism.vn/index.php/tourism/items/1562/2','Cục Du lịch Quốc gia Việt Nam','Tháp Yang Praong','Tháp Chăm Yang Praong giữa rừng'),
}
for l in Path('out/work/anh-dia-diem/nguon-7.txt').read_text().splitlines():
 if l.startswith('(') and '33-7702' in l:
  fix['prison']=(ast.literal_eval(l)[0],'https://tienphong.vn/ben-trong-di-tich-quoc-gia-dac-biet-nha-day-buon-ma-thuot-post1553721.tpo','Báo Tiền Phong','Nhà đày Buôn Ma Thuột','Toàn cảnh di tích Nhà đày Buôn Ma Thuột');break
for ident,(url,page,credit,name,alt) in fix.items():
 r=requests.get(url,timeout=30);r.raise_for_status()
 if url.endswith('.avif'):
  tmp=Path('out/work/anh-dia-diem')/(ident+'.avif');tmp.write_bytes(r.content)
  jpg=tmp.with_suffix('.jpg');subprocess.run(['sips','-s','format','jpeg',str(tmp),'--out',str(jpg)],check=True,capture_output=True);im=Image.open(jpg)
 else:im=Image.open(io.BytesIO(r.content))
 im=im.convert('RGB');im.thumbnail((1200,1000));im.save('chung-khao/app/images/'+ident+'.jpg',quality=87,optimize=True)
 rows=[x for x in rows if x['id']!=ident]
 rows.append(dict(id=ident,name=name,image='./images/'+ident+'.jpg',alt=alt,sourceUrl=page,imageUrl=url,credit=credit,width=im.width,height=im.height,change='Thu nhỏ và nén JPEG; khung hiển thị cắt bằng CSS.',license='Chưa xác minh giấy phép tái sử dụng; ghi nhận nguồn công khai.'))
 print(ident,im.size)
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2))
