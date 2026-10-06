const places=[
  {id:"buon-don",name:"Buôn Đôn",category:"Văn hóa · cộng đồng",filter:"culture",tags:["culture","food","slow"],image:"./images/buon-don.jpg",alt:"Cảnh quan khu du lịch Buôn Đôn",description:"Cầu treo, nhà sàn cổ và câu chuyện vùng đất bên dòng Sêrêpôk.",distance:"Hơn 50 km từ Buôn Ma Thuột",fee:40000,feeLabel:"Cầu treo từ 40.000đ/người*",near:false,route:"buon-don"},
  {id:"troh-bu",name:"Vườn Troh Bư",category:"Thiên nhiên · vườn sinh thái",filter:"nature",tags:["nature","slow"],image:"./images/troh-bu.jpg",alt:"Khu vườn xanh tại Troh Bư",imageSource:"https://vietnamtourism.vn/index.php/news/items/10114",imageCredit:"Cục Du lịch Quốc gia Việt Nam",description:"Không gian dã ngoại và tìm hiểu cây rừng, lan rừng được bài giới thiệu.",distance:"Trong cụm Buôn Đôn; cự ly chưa nêu",fee:35000,feeLabel:"Vé người lớn tham khảo 35.000đ*",near:false,route:"buon-don"},
  {id:"hoc-ca-sau",name:"Hộc Cá Sấu",category:"Thiên nhiên · hồ đá",filter:"nature",tags:["nature"],image:"./images/hoc-ca-sau.jpg",alt:"Hồ đá Hộc Cá Sấu",description:"Hồ đá xanh nằm trong khu vực thủy điện Sêrêpôk 3.",distance:"Cách Buôn Đôn khoảng 40 km",fee:null,feeLabel:"Chưa có giá vé",near:false,route:"remote",caution:"Bài nguồn khuyên không tắm và không leo đá cao; cần xác minh quyền tiếp cận."},
  {id:"da-voi",name:"Đá Voi Yang Tao",category:"Thiên nhiên · địa chất",filter:"nature",tags:["nature","slow"],image:"./images/da-voi-yang-tao.jpg",alt:"Khối đá lớn ở Yang Tao",description:"Cặp đá tự nhiên Đá Voi Mẹ và Đá Voi Cha giữa cảnh đồng, núi.",distance:"Đá Voi Mẹ khoảng 40 km từ trung tâm",fee:0,feeLabel:"Không thu phí tham quan*",near:false,route:"lak"},
  {id:"ho-lak",name:"Hồ Lắk",category:"Thiên nhiên · trải nghiệm",filter:"nature",tags:["nature","culture","slow"],image:"./images/ho-lak.jpg",alt:"Mặt nước và cảnh quan hồ Lắk",description:"Ngắm cảnh hồ, ghé buôn Jun hoặc tìm hiểu trải nghiệm thuyền độc mộc.",distance:"Bài nguồn không nêu cự ly",fee:null,feeLabel:"Thuyền từ 80.000đ/thuyền*",near:false,route:"lak"},
  {id:"lang-gom",name:"Làng gốm Yang Tao",category:"Văn hóa · nghề thủ công",filter:"culture",tags:["culture","slow"],image:"./images/lang-gom-yang-tao.jpg",alt:"Nghề gốm thủ công Yang Tao",description:"Tìm hiểu nghề gốm thủ công của người M’nông Rlăm.",distance:"Cách hồ Lắk chưa đầy 10 km",fee:null,feeLabel:"Giá trải nghiệm chưa rõ",near:false,route:"lak"},
  {id:"dray-nur",name:"Thác Dray Nur",category:"Thiên nhiên · thác nước",filter:"nature",tags:["nature"],image:"./images/thac-dray-nur.jpg",alt:"Thác Dray Nur",description:"Một điểm dừng trên cụm thác Sêrêpôk; kiểm tra điều kiện đường và thời tiết.",distance:"Gần 30 km từ Buôn Ma Thuột",fee:30000,feeLabel:"Vé tham khảo 30.000đ/người*",near:true,route:"serepok"},
  {id:"gia-long",name:"Thác Gia Long",category:"Thiên nhiên · thác nước",filter:"nature",tags:["nature","slow"],image:"./images/gia-long.jpg",alt:"Dòng nước thác Gia Long giữa rừng",imageSource:"https://vietnamtourism.vn/index.php/tourism/items/1287",imageCredit:"Cục Du lịch Quốc gia Việt Nam",description:"Còn gọi là Dray Sáp Thượng; bài nêu lối đi bộ khoảng 2 km từ Dray Nur.",distance:"Cách Dray Nur khoảng 2 km đi bộ",fee:null,feeLabel:"Giá riêng chưa được nêu",near:false,route:"serepok"},
  {id:"dray-sap",name:"Thác Dray Sáp",category:"Thiên nhiên · thác nước",filter:"nature",tags:["nature"],image:"./images/dray-sap.jpg",alt:"Toàn cảnh thác Dray Sáp",imageSource:"https://www.vamvo.com/Photos/tabid/334/AlbumID/311/selectedmoduleid/1024/Default.aspx",imageCredit:"Vamvo",description:"Bài cẩm nang ghi điểm này thuộc Đắk Nông tại thời điểm viết; cần rà soát lại địa giới và lối đi.",distance:"Cách Dray Nur khoảng 12 km đường bộ",fee:null,feeLabel:"Giá vé chưa xác minh",near:false,route:"serepok"},
  {id:"chu-yang-sin",name:"Vườn quốc gia Chư Yang Sin",category:"Thiên nhiên · trekking",filter:"nature",tags:["nature","slow"],image:"./images/vuon-quoc-gia-chu-yang-sin.jpg",alt:"Rừng và vách đá tại Vườn quốc gia Chư Yang Sin",imageSource:"https://vnexpress.net/cam-nang-du-lich-dak-lak-4453797.html",imageCredit:"Đỗ Tuấn Hưng · VnExpress",description:"Bài nêu hành trình chinh phục đỉnh ít nhất 3 ngày 2 đêm; không áp dụng thời lượng này cho chuyến tham quan ngắn.",distance:"Cách trung tâm hơn 60 km; tuyến vào cần xác minh",fee:null,feeLabel:"Tuyến và giá cần hỏi ban quản lý",near:false,route:"park",caution:"Cần xác nhận tuyến, giấy phép, hướng dẫn và thời tiết."},
  {id:"yok-don",name:"Vườn quốc gia Yok Don",category:"Thiên nhiên · rừng khộp",filter:"nature",tags:["nature","culture","slow"],image:"./images/yok-don.jpg",alt:"Rừng khộp Yok Đôn vào mùa thay lá",imageSource:"https://nhandan.vn/anh-say-dam-rung-khop-mua-thay-la-post940867.html",imageCredit:"Báo Nhân Dân",description:"Rừng khộp và các trải nghiệm tự nhiên, văn hóa; kiểm tra dịch vụ với đơn vị quản lý.",distance:"Bài không nêu khoảng cách",fee:null,feeLabel:"Xem bảng giá dịch vụ của vườn",near:false,route:"park",caution:"Chỉ lên lịch sau khi xác nhận tour và mức dịch vụ."},
  {id:"yang-praong",name:"Tháp Yang Praong",category:"Văn hóa · di tích",filter:"culture",tags:["culture","slow"],image:"./images/yang-praong.jpg",alt:"Tháp Chăm Yang Praong giữa rừng",imageSource:"https://vietnamtourism.vn/index.php/tourism/items/1562/2",imageCredit:"Cục Du lịch Quốc gia Việt Nam",description:"Tháp Chăm nằm giữa không gian rừng theo mô tả trong bài cẩm nang.",distance:"Bài không nêu khoảng cách",fee:null,feeLabel:"Phí và tuyến chưa xác minh",near:false,route:"remote"},
  {id:"dien-gio",name:"Điện gió Dlieyang",category:"Cảnh quan · công trình",filter:"nature",tags:["nature"],image:"./images/dien-gio-dlieyang.jpg",alt:"Tuabin gió tại Dlieyang",description:"Cánh đồng điện gió ở Dlieyang; ảnh minh họa không đồng nghĩa khu nhà máy mở cửa.",distance:"Dlieyang, Ea H’leo",fee:null,feeLabel:"Quyền tiếp cận cần xác minh",near:false,route:"remote",caution:"Không mặc định khách được vào khu vực nhà máy."},
  {id:"buon-trap",name:"Thủy điện Buôn Trấp",category:"Cảnh quan · công trình",filter:"nature",tags:["nature"],image:null,alt:"",description:"Cảnh quan sông, cầu và hồ được bài mô tả; cần xác minh khu vực được phép tham quan.",distance:"Bài không nêu khoảng cách",fee:null,feeLabel:"Quyền tiếp cận và phí chưa rõ",near:false,route:"remote"},
  {id:"museum-coffee",name:"Bảo tàng Thế giới Cà phê",category:"Văn hóa · bảo tàng",filter:"culture",tags:["culture","slow"],image:"./images/museum-coffee.jpg",alt:"Kiến trúc Bảo tàng Thế giới Cà phê",imageSource:"https://baotangthegioicaphe.com/bao-tang-the-gioi-ca-phe-khi-du-lich-la-ket-tinh-cua-van-hoa-va-cam-hung",imageCredit:"Bảo tàng Thế giới Cà phê",description:"Điểm tham quan trong trung tâm Buôn Ma Thuột được bài cẩm nang gợi ý.",distance:"Trong khu vực trung tâm",fee:null,feeLabel:"Giá vé và giờ mở cửa cần xác minh",near:true,route:"city"},
  {id:"museum-daklak",name:"Bảo tàng Đắk Lắk",category:"Văn hóa · bảo tàng",filter:"culture",tags:["culture","slow"],image:"./images/museum-daklak.jpg",alt:"Kiến trúc Bảo tàng Đắk Lắk",imageSource:"https://www.tapchikientruc.com.vn/tac-gia-tac-pham/bao-tang-dak-lak.html",imageCredit:"Tạp chí Kiến trúc",description:"Một lựa chọn tìm hiểu văn hóa, lịch sử trong khu vực trung tâm.",distance:"Trong khu vực trung tâm",fee:null,feeLabel:"Giá vé và giờ mở cửa cần xác minh",near:true,route:"city"},
  {id:"prison",name:"Nhà đày Buôn Ma Thuột",category:"Văn hóa · di tích lịch sử",filter:"culture",tags:["culture","slow"],image:"./images/prison.jpg",alt:"Toàn cảnh di tích Nhà đày Buôn Ma Thuột",imageSource:"https://tienphong.vn/ben-trong-di-tich-quoc-gia-dac-biet-nha-day-buon-ma-thuot-post1553721.tpo",imageCredit:"Báo Tiền Phong",description:"Di tích lịch sử trong trung tâm Buôn Ma Thuột; kiểm tra lịch đón khách trước khi đi.",distance:"Trong khu vực trung tâm",fee:null,feeLabel:"Giá vé và giờ mở cửa cần xác minh",near:true,route:"city"}
];
const foods=[
  {icon:"◉",name:"Cơm lam, gà nướng",desc:"Món được bài gợi ý tại các buôn làng du lịch như Buôn Đôn, Buôn Jun.",note:"Giá tùy quán · chưa xác minh"},
  {icon:"◌",name:"Bún đỏ",desc:"Món ăn bình dân được giới thiệu ở khu vực trung tâm Buôn Ma Thuột.",note:"Bài nguồn nêu quán tham khảo · nên kiểm tra trước"},
  {icon:"⌁",name:"Bánh ướt thịt nướng",desc:"Bài cẩm nang gợi ý món ăn tại một địa chỉ ở Buôn Ma Thuột.",note:"Giá tùy quán · chưa xác minh"},
  {icon:"✳",name:"Cá lăng, lẩu lá",desc:"Một vài hương vị địa phương được cẩm nang nhắc đến; hỏi quán về món theo mùa.",note:"Giá tùy quán · chưa xác minh"}
];
const grid=document.querySelector("#destination-grid");
const foodGrid=document.querySelector("#food-grid");
const filterResult=document.querySelector("#filter-result");
function escapeHtml(value){return String(value).replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[char]));}
function renderPlaces(filter="all"){
 const chosen=places.filter(place=>filter==="all"||place.filter===filter||(filter==="near"&&place.near));
 grid.innerHTML=chosen.map((place,index)=>`<article class="destination-card"><div class="destination-image${place.image?"":" is-placeholder"}">${place.image?`<img src="${place.image}" alt="${escapeHtml(place.alt)}" loading="lazy"/>`:`<div class="image-placeholder" aria-label="Chưa có ảnh đã xác minh đúng địa điểm"><span>CHƯA CÓ ẢNH<br/>ĐÃ XÁC MINH</span><i aria-hidden="true">✳</i></div>`}<span class="image-index">ĐIỂM ${String(index+1).padStart(2,"0")}</span></div><div class="card-body">${place.imageSource?`<a class="photo-credit" href="${escapeHtml(place.imageSource)}" target="_blank" rel="noopener noreferrer" aria-label="Nguồn ảnh ${escapeHtml(place.name)}">Ảnh: ${escapeHtml(place.imageCredit)} ↗</a>`:""}<div class="card-meta"><span>${escapeHtml(place.category)}</span><span>↗</span></div><h3>${escapeHtml(place.name)}</h3><p>${escapeHtml(place.description)}</p><div class="card-foot"><span class="card-cost">${escapeHtml(place.feeLabel)}<small>${escapeHtml(place.distance)}</small></span><span class="card-more" aria-hidden="true">↗</span></div></div></article>`).join("");
 filterResult.textContent=filter==="all"?`${chosen.length} điểm từ bộ dữ liệu`:`${chosen.length} điểm phù hợp bộ lọc`;
}
function renderFoods(){foodGrid.innerHTML=foods.map(food=>`<article class="food-card"><span class="food-icon" aria-hidden="true">${food.icon}</span><h3>${escapeHtml(food.name)}</h3><p>${escapeHtml(food.desc)}</p><small>${escapeHtml(food.note)}</small></article>`).join("");}
renderPlaces();renderFoods();
document.querySelectorAll(".filter-chip").forEach(button=>button.addEventListener("click",()=>{document.querySelectorAll(".filter-chip").forEach(item=>item.classList.toggle("active",item===button));renderPlaces(button.dataset.filter);}));
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

const state = { plans: null, selectedCode: "A", ai: null, requestId: 0 };

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
  result.hidden = false;
  document.querySelector("#result-empty").hidden = true;
  result.innerHTML = `<div class="result-empty"><span class="result-sparkle">✳</span><p class="eyebrow">ĐANG LẬP HÀNH TRÌNH</p><h3>${escapeHtml(msg)}</h3></div>`;
}

function renderPlans(){
  if(!state.plans) return;
  const opts = state.plans.options || [];
  const selected = opts.find(o=>o.code===state.selectedCode) || opts[0];
  const b = selected.budget.breakdown;
  const check = selected.budget_check;
  const result = document.querySelector("#result-content");
  const optionCards = opts.map(o=>{
    const ob = o.budget.breakdown;
    const oc = o.budget_check;
    return `<div class="result-option ${o.code===state.selectedCode?"selected":""}" data-code="${o.code}">
      <div class="result-option-top"><b>${o.code} · ${escapeHtml(o.name)}</b><span>${escapeHtml(o.badge||"")}</span></div>
      <div class="result-option-total">${formatMoney(ob.total)}</div>
      <div class="result-option-sub">${o.budget.pax} người · ${o.budget.days} ngày · bình quân ${formatMoney(ob.per_pax)}/người</div>
      <div class="result-option-badge ${oc.status==="fit"?"budget-fit":"budget-exceeded"}">${escapeHtml(oc.status_text)}</div>
    </div>`;
  }).join("");

  const daysHtml = selected.timeline.map(day=>{
    const items = day.schedule.map(item=>`<div class="result-day"><div class="result-day-top"><b>${escapeHtml(item.slot)}</b><span>${escapeHtml(item.type==="visit"?"THAM QUAN":"BỮA ĂN / NGHỈ")}</span></div><h4>${escapeHtml(item.title)}</h4><p>${escapeHtml(item.desc||"")}</p>${item.ticket!==undefined?`<p>${item.ticket===0?"Miễn phí":`Vé ${formatMoney(item.ticket)}/người`}</p>`:""}</div>`).join("");
    return `<div class="result-day-block"><div class="result-day-top"><b>Ngày ${day.day}</b><span>${escapeHtml(day.theme||"")}</span></div>${items}</div>`;
  }).join("");

  const swapRow = selected.destinations.map(id=>{
    const d = selected.destination_details.find(x=>x.id===id);
    return `<button type="button" data-swap="${id}">⇄ ${escapeHtml(d?d.name:id)}</button>`;
  }).join("");

  const aiHtml = state.ai ? `<div class="ai-note"><b>${state.ai.is_fallback?"Gợi ý theo quy tắc":"Gợi ý từ AI qua gateway BTC"}</b><p>${escapeHtml(state.ai.reasoning||"")}</p><p>Mẹo: ${escapeHtml(state.ai.practical_tip||"—")} · Ứng xử: ${escapeHtml(state.ai.responsible_reminder||"—")}</p></div>` : "";

  result.innerHTML = `<div class="result-head"><div><p class="eyebrow">BẢN NHÁP HÀNH TRÌNH</p><h3>${selected.days} ngày · ${selected.pax} người</h3></div><span class="result-badge">XẾP HẠNG THEO QUY TẮC</span></div>
  <div class="result-summary"><span>Ưu tiên: ${escapeHtml(state.plans.user_input?.preference||"")}</span><span>Ngân sách nhóm: ${formatMoney(selected.budget_check.user_budget)}</span></div>
  <div class="result-options">${optionCards}</div>
  <div class="result-days">${daysHtml}</div>
  <div class="cost-panel"><div class="cost-panel-top"><b>Tổng dự kiến cho cả nhóm*</b><strong>${formatMoney(b.total)}</strong></div><small>*Đã gồm vé, ăn, ở, di chuyển và dự phòng 8%. Chưa gồm chi phí đến/rời vùng và mua sắm.</small></div>
  <div class="cost-warning">${escapeHtml(check.status_text)}. ${check.status==="exceeded"?"Chọn ngân sách cao hơn hoặc đổi điểm để giảm chi phí.":"Các khoản được tính theo dữ liệu tham khảo, cần xác nhận với đơn vị cung cấp."}</div>
  <div class="result-swap-row">${swapRow}</div>
  ${aiHtml}
  <div class="result-actions"><button type="button" id="print-plan">In / lưu PDF</button><button type="button" id="change-plan">Đổi sở thích</button></div>`;

  document.querySelector("#result-empty").hidden = true;
  result.hidden = false;
  result.querySelectorAll(".result-option").forEach(el=>el.addEventListener("click",()=>{state.selectedCode=el.dataset.code;renderPlans();}));
  result.querySelectorAll("[data-swap]").forEach(el=>el.addEventListener("click",()=>swapDestination(el.dataset.swap)));
  result.querySelector("#print-plan").addEventListener("click",()=>window.print());
  result.querySelector("#change-plan").addEventListener("click",()=>document.querySelector("#planner-form").scrollIntoView({behavior:"smooth",block:"center"}));
}

async function makePlan(event){
  event.preventDefault();
  const inputs = collectInputs();
  const reqId = ++state.requestId;
  state.ai = null;
  const aiBtn = document.querySelector("#ai-button");
  aiBtn.disabled = true;
  setLoading("Đang ghép cụm điểm và tính dự toán…");
  try{
    const res = await fetch("/api/lap-lich", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(inputs) });
    const data = await res.json().catch(()=>({}));
    if(reqId !== state.requestId) return;
    if(!res.ok || !data.ok) throw new Error(data.error || "Không lập được hành trình.");
    state.plans = data;
    state.selectedCode = data.default_option || "A";
    renderPlans();
    aiBtn.disabled = false;
  }catch(e){
    if(reqId === state.requestId){
      setLoading(e.message || "Không kết nối được máy chủ.");
    }
  }
}

async function askAI(){
  if(!state.plans) return;
  const inputs = collectInputs();
  const reqId = ++state.requestId;
  const btn = document.querySelector("#ai-button");
  btn.disabled = true;
  btn.textContent = "AI đang chọn…";
  setLoading("Đang gọi AI qua gateway BTC để chọn phương án…");
  try{
    const res = await fetch("/api/tu-van", { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(inputs) });
    const data = await res.json().catch(()=>({}));
    if(reqId !== state.requestId) return;
    if(!res.ok || !data.ok) throw new Error(data.error || "Không lấy được gợi ý AI.");
    state.ai = data.ai;
    state.plans.options = data.options;
    state.plans.responsible_rules = data.responsible_rules;
    state.selectedCode = data.ai.selected_code || state.selectedCode;
    renderPlans();
  }catch(e){
    if(reqId === state.requestId){
      state.ai = { is_fallback:true, reasoning:"AI tạm thời chưa khả dụng. Bạn vẫn có thể xem và chỉnh phương án theo quy tắc.", practical_tip:"—", responsible_reminder:"—" };
      renderPlans();
    }
  }finally{
    btn.disabled = false;
    btn.textContent = "Lấy gợi ý AI ✳";
  }
}

async function swapDestination(oldId){
  if(!state.plans) return;
  const opt = state.plans.options.find(o=>o.code===state.selectedCode);
  if(!opt) return;
  const candidates = [...new Set(state.plans.options.flatMap(o=>o.destinations))].filter(id=>id!==oldId);
  const nameOf = id => { const d = opt.destination_details.find(x=>x.id===id); return d?d.name:id; };
  const choice = window.prompt("Đổi điểm " + nameOf(oldId) + " thành:\n\n" + candidates.map((id,i)=>`${i+1}. ${nameOf(id)}`).join("\n") + "\n\nNhập số (0 để hủy):", "1");
  if(choice === null || choice === "") return;
  const idx = Number.parseInt(choice, 10);
  if(!Number.isFinite(idx) || idx === 0) return;
  const newId = candidates[idx-1];
  if(!newId) return;
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
  }
}

document.querySelector("#planner-form").addEventListener("submit", makePlan);
document.querySelector("#ai-button").addEventListener("click", askAI);
