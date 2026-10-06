const places=[
  {id:"buon-don",name:"Buôn Đôn",category:"Văn hóa · cộng đồng",filter:"culture",tags:["culture","food","slow"],image:"./images/buon-don.jpg",alt:"Cảnh quan khu du lịch Buôn Đôn",description:"Cầu treo, nhà sàn cổ và câu chuyện vùng đất bên dòng Sêrêpôk.",distance:"Khoảng 40 km từ Buôn Ma Thuột",fee:40000,feeLabel:"Cầu treo từ 40.000đ/người*",source:"https://vietnamtourism.vn/index.php/tourism/items/1686/",sourceLabel:"Cục Du lịch Quốc gia",near:false,route:"buon-don"},
  {id:"troh-bu",name:"Vườn Troh Bư",category:"Thiên nhiên · vườn sinh thái",filter:"nature",tags:["nature","slow"],image:"./images/troh-bu.jpg",alt:"Khu vườn xanh tại Troh Bư",imageSource:"https://vietnamtourism.vn/index.php/news/items/10114",imageCredit:"Cục Du lịch Quốc gia Việt Nam",description:"Không gian dã ngoại và tìm hiểu cây rừng, lan rừng được bài giới thiệu.",distance:"Khoảng 10 km từ Buôn Ma Thuột",fee:35000,feeLabel:"Vé người lớn tham khảo 35.000đ*",source:"https://vietnamtourism.vn/index.php/news/items/10114",sourceLabel:"Cục Du lịch Quốc gia",near:true,route:"buon-don"},
  {id:"hoc-ca-sau",name:"Hộc Cá Sấu",category:"Thiên nhiên · hồ đá",filter:"nature",tags:["nature"],image:"./images/hoc-ca-sau.jpg",alt:"Hồ đá Hộc Cá Sấu",description:"Hồ đá xanh nằm trong khu vực thủy điện Sêrêpôk 3.",distance:"Khoảng 80 km từ Buôn Ma Thuột",fee:0,feeLabel:"Không thu phí tham quan*",source:"https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html",sourceLabel:"VnExpress Du lịch",near:false,route:"remote",caution:"Bài nguồn khuyên không tắm và không leo đá cao; cần xác minh quyền tiếp cận."},
  {id:"da-voi",name:"Đá Voi Yang Tao",category:"Thiên nhiên · địa chất",filter:"nature",tags:["nature","slow"],image:"./images/da-voi-yang-tao.jpg",alt:"Khối đá lớn ở Yang Tao",description:"Cặp đá tự nhiên Đá Voi Mẹ và Đá Voi Cha giữa cảnh đồng, núi.",distance:"Khoảng 40 km từ Buôn Ma Thuột",fee:0,feeLabel:"Không thu phí tham quan*",source:"https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html",sourceLabel:"VnExpress Du lịch",near:false,route:"lak"},
  {id:"ho-lak",name:"Hồ Lắk",category:"Thiên nhiên · trải nghiệm",filter:"nature",tags:["nature","culture","slow"],image:"./images/ho-lak.jpg",alt:"Mặt nước và cảnh quan hồ Lắk",description:"Ngắm cảnh hồ, ghé buôn Jun hoặc tìm hiểu trải nghiệm thuyền độc mộc.",distance:"Khoảng 52–60 km từ Buôn Ma Thuột",fee:null,feeLabel:"Thuyền từ 80.000đ/thuyền*",source:"https://vnexpress.net/cuoi-voi-cheo-thuyen-doc-moc-tren-ho-nuoc-ngot-lon-nhat-tay-nguyen-3802326.html",sourceLabel:"VnExpress Du lịch",near:false,route:"lak"},
  {id:"lang-gom",name:"Làng gốm Yang Tao",category:"Văn hóa · nghề thủ công",filter:"culture",tags:["culture","slow"],image:"./images/lang-gom-yang-tao.jpg",alt:"Nghề gốm thủ công Yang Tao",description:"Tìm hiểu nghề gốm thủ công của người M’nông Rlăm.",distance:"Khoảng 50–60 km từ Buôn Ma Thuột",fee:null,feeLabel:"Chưa có giá trải nghiệm công khai",source:"https://vnexpress.net/cuoi-voi-cheo-thuyen-doc-moc-tren-ho-nuoc-ngot-lon-nhat-tay-nguyen-3802326.html",sourceLabel:"VnExpress Du lịch",near:false,route:"lak"},
  {id:"dray-nur",name:"Thác Dray Nur",category:"Thiên nhiên · thác nước",filter:"nature",tags:["nature"],image:"./images/thac-dray-nur.jpg",alt:"Thác Dray Nur",description:"Một điểm dừng trên cụm thác Sêrêpôk; kiểm tra điều kiện đường và thời tiết.",distance:"Khoảng 25–30 km từ Buôn Ma Thuột",fee:30000,feeLabel:"Vé tham khảo 30.000đ/người*",source:"https://daktip.vn/tin-trong-tinh/cam-nang-du-lich-dak-lak-2.html",sourceLabel:"Trung tâm Xúc tiến Du lịch Đắk Lắk",near:true,route:"serepok"},
  {id:"gia-long",name:"Thác Gia Long",category:"Thiên nhiên · thác nước",filter:"nature",tags:["nature","slow"],image:"./images/gia-long.jpg",alt:"Dòng nước thác Gia Long giữa rừng",imageSource:"https://vietnamtourism.vn/index.php/tourism/items/1287",imageCredit:"Cục Du lịch Quốc gia Việt Nam",description:"Còn gọi là Dray Sáp Thượng; bài nêu lối đi bộ khoảng 2 km từ Dray Nur.",distance:"Khoảng 27–32 km từ Buôn Ma Thuột",fee:null,feeLabel:"Combo Dray Nur – Gia Long 50.000đ*",source:"https://daktip.vn/tin-trong-tinh/cam-nang-du-lich-dak-lak-2.html",sourceLabel:"Trung tâm Xúc tiến Du lịch Đắk Lắk",near:false,route:"serepok"},
  {id:"dray-sap",name:"Thác Dray Sáp",category:"Thiên nhiên · thác nước",filter:"nature",tags:["nature"],image:"./images/dray-sap.jpg",alt:"Toàn cảnh thác Dray Sáp",imageSource:"https://www.vamvo.com/Photos/tabid/334/AlbumID/311/selectedmoduleid/1024/Default.aspx",imageCredit:"Vamvo",description:"Bài cẩm nang ghi điểm này thuộc Đắk Nông tại thời điểm viết; cần rà soát lại địa giới và lối đi.",distance:"Khoảng 37–42 km từ Buôn Ma Thuột",fee:null,feeLabel:"Chưa có giá vé công khai",source:"https://daktip.vn/tin-trong-tinh/cam-nang-du-lich-dak-lak-2.html",sourceLabel:"Trung tâm Xúc tiến Du lịch Đắk Lắk",near:false,route:"serepok"},
  {id:"chu-yang-sin",name:"Vườn quốc gia Chư Yang Sin",category:"Thiên nhiên · trekking",filter:"nature",tags:["nature","slow"],image:"./images/vuon-quoc-gia-chu-yang-sin.jpg",alt:"Rừng và vách đá tại Vườn quốc gia Chư Yang Sin",imageSource:"https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html",imageCredit:"Đỗ Tuấn Hưng · VnExpress",description:"Bài nêu hành trình chinh phục đỉnh ít nhất 3 ngày 2 đêm; không áp dụng thời lượng này cho chuyến tham quan ngắn.",distance:"Khoảng 60 km từ Buôn Ma Thuột",fee:null,feeLabel:"Tuyến và giá cần hỏi ban quản lý",source:"https://vietnamtourism.vn/index.php/tourism/items/2869",sourceLabel:"Cục Du lịch Quốc gia",near:false,route:"park",caution:"Cần xác nhận tuyến, giấy phép, hướng dẫn và thời tiết."},
  {id:"yok-don",name:"Vườn quốc gia Yok Don",category:"Thiên nhiên · rừng khộp",filter:"nature",tags:["nature","culture","slow"],image:"./images/yok-don.jpg",alt:"Rừng khộp Yok Đôn vào mùa thay lá",imageSource:"https://nhandan.vn/anh-say-dam-rung-khop-mua-thay-la-post940867.html",imageCredit:"Báo Nhân Dân",description:"Rừng khộp và các trải nghiệm tự nhiên, văn hóa; kiểm tra dịch vụ với đơn vị quản lý.",distance:"Khoảng 38 km từ Buôn Ma Thuột",fee:null,feeLabel:"Tour nửa ngày từ 450.000đ/2 người*",source:"https://tour.yokdonnationalpark.vn/yokdon-national-park.html",sourceLabel:"Vườn quốc gia Yok Don",near:false,route:"park",caution:"Chỉ lên lịch sau khi xác nhận tour và mức dịch vụ."},
  {id:"yang-praong",name:"Tháp Yang Praong",category:"Văn hóa · di tích",filter:"culture",tags:["culture","slow"],image:"./images/yang-praong.jpg",alt:"Tháp Chăm Yang Praong giữa rừng",imageSource:"https://vietnamtourism.vn/index.php/tourism/items/1562/2",imageCredit:"Cục Du lịch Quốc gia Việt Nam",description:"Tháp Chăm nằm giữa không gian rừng theo mô tả trong bài cẩm nang.",distance:"Gần 100 km từ Buôn Ma Thuột",fee:null,feeLabel:"Chưa có giá vé công khai",source:"https://vietnamtourism.vn/index.php/tourism/items/1562/2",sourceLabel:"Cục Du lịch Quốc gia",near:false,route:"remote"},
  {id:"dien-gio",name:"Điện gió Dlieyang",category:"Cảnh quan · công trình",filter:"nature",tags:["nature"],image:"./images/dien-gio-dlieyang.jpg",alt:"Tuabin gió tại Dlieyang",description:"Cánh đồng điện gió ở Dlieyang; ảnh minh họa không đồng nghĩa khu nhà máy mở cửa.",distance:"Khoảng 70–80 km từ Buôn Ma Thuột",fee:null,feeLabel:"Quyền tiếp cận và phí chưa xác minh",source:"https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html",sourceLabel:"VnExpress Du lịch",near:false,route:"remote",caution:"Không mặc định khách được vào khu vực nhà máy."},
  {id:"museum-coffee",name:"Bảo tàng Thế giới Cà phê",category:"Văn hóa · bảo tàng",filter:"culture",tags:["culture","slow"],image:"./images/museum-coffee.jpg",alt:"Kiến trúc Bảo tàng Thế giới Cà phê",imageSource:"https://baotangthegioicaphe.com/bao-tang-the-gioi-ca-phe-khi-du-lich-la-ket-tinh-cua-van-hoa-va-cam-hung",imageCredit:"Bảo tàng Thế giới Cà phê",description:"Điểm tham quan trong trung tâm Buôn Ma Thuột được bài cẩm nang gợi ý.",distance:"Trong nội đô, dưới 5 km từ trung tâm",fee:150000,feeLabel:"Vé người lớn 150.000đ/người*",source:"https://baotangthegioicaphe.com/hoi-dap",sourceLabel:"Website chính thức của bảo tàng",near:true,route:"city"},
  {id:"museum-daklak",name:"Bảo tàng Đắk Lắk",category:"Văn hóa · bảo tàng",filter:"culture",tags:["culture","slow"],image:"./images/museum-daklak.jpg",alt:"Kiến trúc Bảo tàng Đắk Lắk",imageSource:"https://www.tapchikientruc.com.vn/tac-gia-tac-pham/bao-tang-dak-lak.html",imageCredit:"Tạp chí Kiến trúc",description:"Một lựa chọn tìm hiểu văn hóa, lịch sử trong khu vực trung tâm.",distance:"Trong nội đô, dưới 3 km từ trung tâm",fee:30000,feeLabel:"Vé người lớn tham khảo 30.000đ*",source:"https://baotangdaklak.vn/",sourceLabel:"Bảo tàng Đắk Lắk",near:true,route:"city"},
  {id:"prison",name:"Nhà đày Buôn Ma Thuột",category:"Văn hóa · di tích lịch sử",filter:"culture",tags:["culture","slow"],image:"./images/prison.jpg",alt:"Toàn cảnh di tích Nhà đày Buôn Ma Thuột",imageSource:"https://tienphong.vn/ben-trong-di-tich-quoc-gia-dac-biet-nha-day-buon-ma-thuot-post1553721.tpo",imageCredit:"Báo Tiền Phong",description:"Di tích lịch sử trong trung tâm Buôn Ma Thuột; kiểm tra lịch đón khách trước khi đi.",distance:"Trong nội đô, dưới 3 km từ trung tâm",fee:null,feeLabel:"Chưa có giá vé công khai",source:"https://tienphong.vn/ben-trong-di-tich-quoc-gia-dac-biet-nha-day-buon-ma-thuot-post1553721.tpo",sourceLabel:"Báo Tiền Phong",near:true,route:"city"}
];
const foods=[
  {
    "id": "bun-do",
    "name": "Bún đỏ",
    "image": "./images/mon-bun-do.jpg",
    "alt": "Bún đỏ được giới thiệu trên VnExpress",
    "desc": "Sợi bún to nhuộm màu dầu điều, ăn cùng riêu cua, chả viên và trứng cút. Một món quen thuộc cho buổi chiều ở phố núi.",
    "credit": "VnExpress · Tâm Linh",
    "source": "https://vnexpress.net/nhung-mon-nen-thu-o-buon-ma-thuot-4247663.html",
    "imageSource": "https://i1-dulich.vnecdn.net/2022/01/04/VnExpress-BMT-1-6562-161554021-8355-1622-1641272065.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=xlPOAMVFoQiRuQSMhzO8gw",
    "note":""
  },
  {
    "id": "banh-uot",
    "name": "Bánh ướt chồng đĩa",
    "image": "./images/mon-banh-uot.jpg",
    "alt": "Bánh ướt chồng đĩa được giới thiệu trên VnExpress",
    "desc": "Từng đĩa bánh mỏng được dọn riêng để bạn tự cuốn thịt nướng, chả lụa, xoài và dưa chua; chấm mắm nêm hoặc nước mắm.",
    "credit": "nganha86/Instagram · qua VnExpress",
    "source": "https://vnexpress.net/nhung-mon-nen-thu-o-buon-ma-thuot-4247663.html",
    "imageSource": "https://i1-dulich.vnecdn.net/2022/01/04/VnExpress-BMT-9-6742-161554021-6691-4702-1641272066.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=NjW8giI3Rl4lw4IOzX_ldA",
    "note":""
  },
  {
    "id": "lau-ca-lang",
    "name": "Lẩu cá lăng",
    "image": "./images/mon-lau-ca-lang.jpg",
    "alt": "Lẩu cá lăng được giới thiệu trên VnExpress",
    "desc": "Cá lăng thịt chắc nấu trong nước lẩu chua cay, ăn cùng măng chua và rau rừng. Hợp cho một bữa quây quần bên nồi lẩu nóng.",
    "credit": "Du Lịch Tây Nguyên · qua VnExpress",
    "source": "https://vnexpress.net/mon-lau-ca-dam-chat-tay-nguyen-dai-ngan-4326393.html",
    "imageSource": "https://i1-dulich.vnecdn.net/2022/01/07/calang1-3441-1626606695-4534-1641543074.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Ea6RQEyBkTvhzh32PyAsjw",
    "note":""
  },
  {
    "id": "ca-dang",
    "name": "Cà đắng trộn cá khô",
    "image": "./images/mon-ca-dang.jpg",
    "alt": "Cà đắng trộn cá khô được giới thiệu trên VnExpress",
    "desc": "Cà đắng thái mỏng trộn cá khô và nước mắm chua ngọt, thêm rau thơm. Vị đắng nhẹ và hậu ngọt tạo nét riêng của bữa cơm Tây Nguyên.",
    "credit": "Ngôi Sao · qua VnExpress",
    "source": "https://vnexpress.net/nhung-mon-ngon-doc-quyen-cua-buon-ma-thuot-3516878.html",
    "imageSource": "https://i1-ngoisao.vnecdn.net/2022/04/22/IMG-0795-JPG-8439-1482224774-4177-1650594047.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=U-ruoFI2pJQ3pegl3dFCPw",
    "note":""
  }
];
const grid=document.querySelector("#destination-grid");
const foodGrid=document.querySelector("#food-grid");
const filterResult=document.querySelector("#filter-result");
const destinationPagination=document.querySelector("#destination-pagination");
const heroSlides = [...document.querySelectorAll(".hero-slide")];
const heroCounter = document.querySelector("#hero-counter");
const heroLocation = document.querySelector("#hero-location");
let heroIndex = 0;

function updateHeroSlide(nextIndex = 0){
  if (!heroSlides.length) return;
  heroIndex = (nextIndex + heroSlides.length) % heroSlides.length;
  heroSlides.forEach((slide, index) => {
    const isActive = index === heroIndex;
    slide.classList.toggle("is-active", isActive);
    slide.setAttribute("aria-hidden", String(!isActive));
  });

  if (heroCounter) heroCounter.textContent = `${String(heroIndex + 1).padStart(2, "0")} / ${String(heroSlides.length).padStart(2, "0")}`;
  if (heroLocation) heroLocation.textContent = heroSlides[heroIndex]?.dataset.name || "HỒ LẮK · ẢNH TƯ LIỆU";
}

setInterval(() => updateHeroSlide(heroIndex + 1), 5000);

function escapeHtml(value){return String(value).replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));}
let placeFilter="all";
let placePage=1;
function getPlacePageSize(){return window.innerWidth<=600?2:(window.innerWidth<=1000?4:8);}
function renderPlaces(filter=placeFilter){
 placeFilter=filter;
 const chosen=places.filter(place=>filter==="all"||place.filter===filter||(filter==="near"&&place.near));
 const pageSize=getPlacePageSize();
 const pageCount=Math.max(1,Math.ceil(chosen.length/pageSize));
 placePage=Math.min(placePage,pageCount);
 const start=(placePage-1)*pageSize;
 const visible=chosen.slice(start,start+pageSize);
 grid.innerHTML=visible.map((place,index)=>`<article class="destination-card"><div class="destination-image${place.image?"":" is-placeholder"}">${place.image?`<img src="${place.image}" alt="${escapeHtml(place.alt)}" loading="lazy"/>`:`<div class="image-placeholder" aria-label="Chưa có ảnh đã xác minh đúng địa điểm"><span>CHƯA CÓ ẢNH<br/>ĐÃ XÁC MINH</span><i aria-hidden="true">✳</i></div>`}<span class="image-index">ĐIỂM ${String(start+index+1).padStart(2,"0")}</span></div><div class="card-body"><div class="card-meta"><span>${escapeHtml(place.category)}</span></div><h3>${escapeHtml(place.name)}</h3><a class="place-source" href="${escapeHtml(place.source)}" target="_blank" rel="noopener noreferrer" aria-label="Đọc nguồn giới thiệu ${escapeHtml(place.name)}">Đọc giới thiệu · ${escapeHtml(place.sourceLabel)} </a><div class="card-foot"><span class="card-cost">${escapeHtml(place.feeLabel)}<small>${escapeHtml(place.distance)}</small></span></div></div></article>`).join("");
 filterResult.textContent=`${chosen.length} điểm · Trang ${placePage}/${pageCount}`;
 destinationPagination.innerHTML=pageCount>1?`<button type="button" data-page="prev" ${placePage===1?"disabled":""}>← Trang trước</button><span>Trang ${placePage} / ${pageCount}</span><button type="button" data-page="next" ${placePage===pageCount?"disabled":""}>Trang sau →</button>`:"";
}
function renderFoods(){
 foodGrid.innerHTML=foods.map(food=>`<article class="food-card"><img class="food-image" src="${escapeHtml(food.image)}" alt="${escapeHtml(food.alt)}" loading="lazy" width="1000" height="750"/><div class="food-body"><h3>${escapeHtml(food.name)}</h3><p>${escapeHtml(food.desc)}</p><small>${escapeHtml(food.note)}</small><a class="food-source" href="${escapeHtml(food.source)}" target="_blank" rel="noopener noreferrer" aria-label="Đọc bài VnExpress về ${escapeHtml(food.name)}">Đọc bài </a></div></article>`).join("");
}
renderPlaces();renderFoods();
document.querySelectorAll(".filter-chip").forEach(button=>button.addEventListener("click",()=>{document.querySelectorAll(".filter-chip").forEach(item=>item.classList.toggle("active",item===button));placePage=1;renderPlaces(button.dataset.filter);}));
destinationPagination.addEventListener("click",event=>{const button=event.target.closest("button[data-page]");if(!button||button.disabled)return;placePage+=button.dataset.page==="next"?1:-1;renderPlaces();document.querySelector("#diem-den").scrollIntoView({behavior:"smooth",block:"start"});});
window.addEventListener("resize",()=>renderPlaces());
document.querySelector(".menu-toggle").addEventListener("click",event=>{const nav=document.querySelector(".main-nav");const isOpen=nav.classList.toggle("open");event.currentTarget.setAttribute("aria-expanded",String(isOpen));});
document.querySelectorAll(".main-nav a").forEach(link=>link.addEventListener("click",()=>{document.querySelector(".main-nav").classList.remove("open");document.querySelector(".menu-toggle").setAttribute("aria-expanded","false");}));

const routeInfo={
 "buon-don":{title:"Cụm Buôn Đôn",description:"Buôn Đôn là điểm neo; Vườn Troh Bư có thể cân nhắc ghép nếu xác minh khoảng cách và giờ mở cửa. Chưa có giờ lái xe giữa các điểm."},
 lak:{title:"Cụm hồ Lắk – Yang Tao",description:"Bài gợi tuyến qua Đá Voi Yang Tao trước khi đến hồ Lắk; làng gốm Yang Tao cách hồ chưa đầy 10 km. Chưa có giờ lái xe/giờ tham quan."},
 serepok:{title:"Cụm thác Sêrêpôk",description:"Có thể xem Dray Nur và Gia Long theo combo tham khảo; xác nhận lối đi, địa giới, giá và giờ mở cửa trước khi ghép Dray Sáp."},
 city:{title:"Cụm trung tâm Buôn Ma Thuột",description:"Bài nhắc các bảo tàng và Nhà đày trong trung tâm; giá, giờ mở cửa và thời lượng tham quan chưa được nguồn này cung cấp."},
 remote:{title:"Điểm xa cần kiểm tra riêng",description:"Thông tin đường vào và quyền tiếp cận còn thiếu; trợ lý không xếp vào lịch tự động để tránh gợi ý chuyến đi thiếu căn cứ."},
 park:{title:"Vườn quốc gia · cần đơn vị hướng dẫn",description:"Cần xác nhận tuyến, giấy phép, thời tiết, giá dịch vụ và thời lượng với ban quản lý trước khi lên lịch."}
};
function formatMoney(value){return new Intl.NumberFormat("vi-VN").format(value)+" ₫";}
function formatMoney(value){return new Intl.NumberFormat("vi-VN").format(value)+" ₫";}

const state = { plans: null, selectedCode: "A", activeDay: 1, ai: null, requestId: 0 };

function mapPreference(interests){
  if(!interests.length) return "Tổng hòa văn hóa và thiên nhiên";
  const names = { nature:"thiên nhiên", culture:"văn hóa", food:"ẩm thực", slow:"nhịp thong thả" };
  return interests.map(i=>names[i]||i).join(", ");
}

function collectInputs(){
  return {
    pax: Math.max(1, Math.min(8, Number(document.querySelector("#people").value) || 1)),
    days: Math.max(1, Math.min(3, Number(document.querySelector("#days").value) || 1)),
    budget: Math.max(0, Number(document.querySelector("#budget").value) || 0),
    preference: mapPreference([...document.querySelectorAll("input[name='interest']:checked")].map(i=>i.value)),
    cluster: "bmt"
  };
}

function setLoading(msg){
  const result = document.querySelector("#result-content");
  document.querySelector("#plan-options-panel").hidden = true;
  result.hidden = false;
  document.querySelector("#result-empty").hidden = true;
  result.innerHTML = `<div class="result-empty"><p class="eyebrow">ĐANG LẬP HÀNH TRÌNH</p><h3>${escapeHtml(msg)}</h3></div>`;
}

function renderPlans(){
  if(!state.plans) return;
  const opts = state.plans.options || [];
  const selected = opts.find(o=>o.code===state.selectedCode) || opts[0];
  const b = selected.budget.breakdown;
  const check = selected.budget_check;
  const accommodationBase = Number(b.accommodation?.cost||0);
  const accommodationLow = accommodationBase ? Math.round(accommodationBase*.85/10000)*10000 : 0;
  const accommodationHigh = accommodationBase ? Math.round(accommodationBase*1.2/10000)*10000 : 0;
  const result = document.querySelector("#result-content");
  const optionCards = opts.map(o=>{
    const ob = o.budget.breakdown;
    const oc = o.budget_check;
    return `<button class="result-option ${o.code===state.selectedCode?"selected":""}" type="button" data-code="${o.code}">
      <span class="result-option-top"><b>${o.code} · ${escapeHtml(o.name)}</b><span>${escapeHtml(o.badge||"")}</span></span>
      <span class="result-option-total">${formatMoney(ob.total)}</span>
      <span class="result-option-sub">${o.budget.pax} người · ${o.budget.days} ngày · bình quân ${formatMoney(ob.per_pax)}/người</span>
      <span class="result-option-badge ${oc.status==="fit"?"budget-fit":"budget-exceeded"}">${escapeHtml(oc.status_text)}</span>
    </button>`;
  }).join("");

  const availableDays = selected.timeline.map(day=>Number(day.day));
  if(!availableDays.includes(state.activeDay)) state.activeDay = availableDays[0] || 1;
  const dayTabs = selected.timeline.map(day=>`<button class="day-tab${Number(day.day)===state.activeDay?" active":""}" type="button" role="tab" aria-selected="${Number(day.day)===state.activeDay}" data-day="${day.day}" onclick="selectPlanDay(${Number(day.day)})">Ngày ${day.day}</button>`).join("");
  const daysHtml = selected.timeline.map(day=>{
    const mealsForDay = (b.meals?.items||[]).filter(meal=>Number(meal.day)===Number(day.day));
    let mealIndex = 0;
    const items = day.schedule.map(item=>{
      const meal = item.type==="meal" ? mealsForDay[mealIndex++] : null;
      const estimatedCost = item.type==="meal" ? Number(meal?.cost||0) : Number(item.ticket||0) * Number(selected.budget.pax||1);
      const estimateNote = `<span class="item-estimate">Ước tính cho nhóm: <b>${formatMoney(estimatedCost)}</b></span>`;
      const mapLink = item.type==="visit" ? `<a class="map-link" href="https://www.google.com/maps/search/?api=1&amp;query=${encodeURIComponent(`${item.title}, ${item.address||"Đắk Lắk"}, Việt Nam`)}" target="_blank" rel="noopener noreferrer" aria-label="Mở ${escapeHtml(item.title)} trên Google Maps">Mở Google Maps <span aria-hidden="true"></span></a>` : "";
      return `<div class="result-day"><div class="result-day-top"><b>${escapeHtml(item.slot)}</b><span>${escapeHtml(item.type==="visit"?"THAM QUAN":"BỮA ĂN / NGHỈ")}</span></div><h4>${escapeHtml(item.title)}</h4><p>${escapeHtml(item.desc||"")}</p><div class="result-day-meta">${estimateNote}${mapLink}</div></div>`;
    }).join("");
    return `<section class="result-day-panel" role="tabpanel" data-day-panel="${day.day}"${Number(day.day)===state.activeDay?"":" hidden"}><div class="day-theme"><b>Ngày ${day.day}</b><span>${escapeHtml(day.theme||"")}</span></div>${items}</section>`;
  }).join("");

  const swapRow = selected.destinations.map(id=>{
    const d = selected.destination_details.find(x=>x.id===id);
    return `<button type="button" data-swap="${id}">⇄ ${escapeHtml(d?d.name:id)}</button>`;
  }).join("");

  const aiHtml = state.ai ? `<div class="ai-note"><b>${state.ai.is_fallback?"Gợi ý theo quy tắc":"Gợi ý từ AI qua gateway BTC"}</b><p>${escapeHtml(state.ai.reasoning||"")}</p><p>Mẹo: ${escapeHtml(state.ai.practical_tip||"—")} · Ứng xử: ${escapeHtml(state.ai.responsible_reminder||"—")}</p></div>` : "";

  const optionsPanel = document.querySelector("#plan-options-panel");
  optionsPanel.innerHTML = `<p class="options-label">Chọn phương án hành trình</p><div class="result-options">${optionCards}</div>`;
  optionsPanel.hidden = false;

  result.innerHTML = `<div class="result-summary"><span>Ưu tiên: ${escapeHtml(state.plans.user_input?.preference||"")}</span><span>Ngân sách nhóm: ${formatMoney(selected.budget_check.user_budget)}</span></div>
  <div class="day-tabs" role="tablist" aria-label="Chọn ngày trong hành trình">${dayTabs}</div>
  <div class="result-days">${daysHtml}</div>
  <div class="cost-panel">
    <div class="cost-line"><span>Vé tham quan và ăn uống</span><b>${formatMoney(Number(b.tickets?.total||0)+Number(b.meals?.total||0))}</b></div>
    <div class="cost-line cost-hotel"><span>Khách sạn (${Number(selected.budget?.days||0)} ngày · ${Number(b.accommodation?.nights||0)} đêm theo lộ trình)</span><span><b>${accommodationBase?`${formatMoney(accommodationLow)} – ${formatMoney(accommodationHigh)}`:"Không phát sinh"}</b><a href="https://www.traveloka.com/" target="_blank" rel="noopener noreferrer" aria-label="Tìm khách sạn trên Traveloka">Xem khách sạn </a></span></div>
    <div class="cost-line"><span>Di chuyển giữa các điểm</span><b>${formatMoney(b.transport?.cost||0)}</b></div>
    <div class="cost-line"><span>Dự phòng 8%</span><b>${formatMoney(b.contingency||0)}</b></div>
    <div class="cost-panel-top"><b>Tổng dự kiến cho cả nhóm*</b><strong>${formatMoney(b.total)}</strong></div>
    <small>*Tổng sử dụng mức khách sạn tham khảo trong dữ liệu. Khoảng giá phòng có thể thay đổi theo ngày lưu trú; chưa gồm chi phí đến/rời vùng và mua sắm.</small>
  </div>
  <div class="cost-warning">${escapeHtml(check.status_text)}. ${check.status==="exceeded"?"Chọn ngân sách cao hơn hoặc đổi điểm để giảm chi phí.":"Các khoản được tính theo dữ liệu tham khảo, cần xác nhận với đơn vị cung cấp."}</div>
  <div class="result-swap-row">${swapRow}</div>
  ${aiHtml}
  <div class="result-actions"><button type="button" id="print-plan">In / lưu PDF</button><button type="button" id="change-plan">Đổi sở thích</button></div>
  <a class="flight-booking result-flight-booking" href="https://www.vietjetair.com/vi/ve-may-bay" target="_blank" rel="noopener noreferrer" aria-label="Đặt vé máy bay trên website chính thức của Vietjet Air">Đặt vé máy bay <span aria-hidden="true"></span></a>`;

  document.querySelector("#result-empty").hidden = true;
  result.hidden = false;
  optionsPanel.querySelectorAll(".result-option").forEach(el=>el.addEventListener("click",()=>{state.selectedCode=el.dataset.code;state.activeDay=1;renderPlans();}));
  result.querySelectorAll("[data-swap]").forEach(el=>el.addEventListener("click",()=>swapDestination(el.dataset.swap)));
  result.querySelector("#print-plan").addEventListener("click",()=>window.print());
  result.querySelector("#change-plan").addEventListener("click",()=>document.querySelector("#planner-form").scrollIntoView({behavior:"smooth",block:"center"}));
}

function selectPlanDay(day){
  state.activeDay = Number(day);
  renderPlans();
}

async function makePlan(event){
  event.preventDefault();
  const inputs = collectInputs();
  const reqId = ++state.requestId;
  state.ai = null;
  setLoading("Đang ghép cụm điểm và tính dự toán…");
  try{
    const res = await fetch("/api/lap-lich", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(inputs) });
    const data = await res.json().catch(()=>({}));
    if(reqId !== state.requestId) return;
    if(!res.ok || !data.ok) throw new Error(data.error || "Không lập được hành trình.");
    state.plans = data;
    state.selectedCode = data.default_option || "A";
    state.activeDay = 1;
    renderPlans();
  }catch(e){
    if(reqId === state.requestId){
      setLoading(e.message || "Không kết nối được máy chủ.");
    }
  }
}

async function swapDestination(oldId){
  if(!state.plans) return;
  const opt = state.plans.options.find(o=>o.code===state.selectedCode);
  if(!opt) return;
  const allDetails = state.plans.options.flatMap(o=>o.destination_details||[]);
  const nameOf = id => allDetails.find(x=>x.id===id)?.name || id;
  const candidates = [...new Set(state.plans.options.flatMap(o=>o.destinations))]
    .filter(id=>id!==oldId && !opt.destinations.includes(id));
  const newId = candidates[0];
  if(!newId){
    window.alert("Chưa có điểm thay thế phù hợp trong danh mục hiện tại.");
    return;
  }
  const button = document.querySelector(`[data-swap="${oldId}"]`);
  const originalLabel = button?.textContent;
  if(button){
    button.disabled = true;
    button.textContent = "Đang đổi điểm…";
  }
  try{
    const res = await fetch("/api/doi-diem", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({ pax:opt.budget.pax, days:opt.budget.days, destinations:opt.destinations, old_id:oldId, new_id:newId, acc_type:opt.accommodation_type||"hotel" }) });
    const data = await res.json().catch(()=>({}));
    if(!res.ok || !data.ok) throw new Error(data.error || "Không đổi được điểm.");
    opt.destinations = data.destinations;
    opt.destination_details = data.destination_details;
    opt.budget = data.budget;
    opt.timeline = data.timeline;
    opt.distribution = data.distribution;
    opt.budget_check = {
      user_budget: opt.budget_check.user_budget,
      total_cost: data.budget.breakdown.total,
      difference: opt.budget_check.user_budget - data.budget.breakdown.total,
      status: opt.budget_check.user_budget >= data.budget.breakdown.total ? "fit" : "exceeded",
      status_text: opt.budget_check.user_budget >= data.budget.breakdown.total ? `Nằm trọn trong ngân sách (Dư ${formatMoney(opt.budget_check.user_budget - data.budget.breakdown.total)})` : `Vượt ngân sách ${formatMoney(data.budget.breakdown.total - opt.budget_check.user_budget)}`
    };
    renderPlans();
  }catch(e){
    window.alert(e.message || e);
    if(button){
      button.disabled = false;
      button.textContent = originalLabel;
    }
  }
}

document.querySelector("#planner-form").addEventListener("submit", makePlan);
