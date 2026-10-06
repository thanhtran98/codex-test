import json
import math
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"

def load_catalog():
    with open(DATA_DIR / "catalog.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_sources():
    with open(DATA_DIR / "sources.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_destination_by_id(dest_id, catalog=None):
    if catalog is None:
        catalog = load_catalog()
    for d in catalog["destinations"]:
        if d["id"] == dest_id:
            return d
    return None

def determine_transport(pax, catalog=None):
    if catalog is None:
        catalog = load_catalog()
    transports = catalog["transports"]
    if pax <= 2:
        return "motorbike", transports["motorbike"]
    elif pax <= 4:
        return "car_small", transports["car_small"]
    else:
        return "car_large", transports["car_large"]

def calculate_plan_budget(pax, days, selected_destinations, accommodation_id="hotel", transport_id=None, catalog=None):
    if catalog is None:
        catalog = load_catalog()
    
    pax = max(1, min(12, int(pax)))
    days = max(1, min(3, int(days)))
    
    # 1. Vé tham quan & hoạt động
    ticket_items = []
    total_tickets = 0
    for d_id in selected_destinations:
        d = get_destination_by_id(d_id, catalog)
        if not d:
            continue
        p = d.get("ticket_price", 0)
        item_cost = p * pax
        total_tickets += item_cost
        ticket_items.append({
            "name": d["name"],
            "unit_price": p,
            "pax": pax,
            "cost": item_cost,
            "is_free": p == 0
        })
    
    # 2. Ăn uống (mặc định mỗi ngày 1 sáng, 1 trưa, 1 tối)
    # Giá trung bình: Sáng 45k, Trưa 150k, Tối 160k = 355k/người/ngày
    meals_catalog = {m["id"]: m for m in catalog["meals"]}
    meal_items = []
    total_meals = 0
    
    # Chuẩn bị thực đơn tiêu chuẩn cho từng ngày
    sample_menus = [
        {"breakfast": "sang-bundo", "lunch": "trua-amthuc-bmt", "dinner": "toi-lau-calang"},
        {"breakfast": "sang-bundo", "lunch": "trua-comlam-ganuong", "dinner": "toi-com-nha-dai"},
        {"breakfast": "sang-bundo", "lunch": "trua-comlam-ganuong", "dinner": "toi-lau-calang"}
    ]
    
    for day_idx in range(days):
        menu = sample_menus[day_idx % len(sample_menus)]
        day_num = day_idx + 1
        for meal_time, meal_id in menu.items():
            meal_data = meals_catalog.get(meal_id, {
                "name": "Bữa ăn đặc sản địa phương",
                "price_per_person": 120000
            })
            cost = meal_data["price_per_person"] * pax
            total_meals += cost
            time_label = "Sáng" if meal_time == "breakfast" else ("Trưa" if meal_time == "lunch" else "Tối")
            meal_items.append({
                "day": day_num,
                "time_label": time_label,
                "name": meal_data["name"],
                "price_per_person": meal_data["price_per_person"],
                "pax": pax,
                "cost": cost
            })
            
    # 3. Lưu trú
    nights = max(0, days - 1)
    rooms = math.ceil(pax / 2.0)
    acc_data = catalog["accommodations"].get(accommodation_id, catalog["accommodations"]["hotel"])
    room_rate = acc_data["price_per_room_night"]
    total_accommodation = nights * rooms * room_rate
    accommodation_detail = {
        "id": acc_data["id"],
        "name": acc_data["name"],
        "nights": nights,
        "rooms": rooms,
        "price_per_room_night": room_rate,
        "cost": total_accommodation
    }
    
    # 4. Phương tiện di chuyển
    if not transport_id:
        transport_id, trans_data = determine_transport(pax, catalog)
    else:
        trans_data = catalog["transports"].get(transport_id, catalog["transports"]["car_small"])
        
    daily_transport_cost = trans_data["daily_rate"] + trans_data.get("fuel_per_day", 0)
    # Nếu là xe máy thì cần tính số lượng xe: ceil(pax / 2)
    if transport_id == "motorbike":
        num_bikes = math.ceil(pax / 2.0)
        daily_transport_cost = daily_transport_cost * num_bikes
    else:
        num_bikes = 1
        
    total_transport = days * daily_transport_cost
    transport_detail = {
        "id": trans_data["id"],
        "name": trans_data["name"],
        "days": days,
        "vehicles": num_bikes if transport_id == "motorbike" else 1,
        "daily_rate": daily_transport_cost,
        "cost": total_transport
    }
    
    # 5. Tổng & Dự phòng
    subtotal = total_tickets + total_meals + total_accommodation + total_transport
    contingency = int(round(subtotal * 0.08 / 1000.0) * 1000) # 8% dự phòng biến động giá
    total = subtotal + contingency
    per_pax = int(round((total / pax) / 1000.0) * 1000)
    
    return {
        "pax": pax,
        "days": days,
        "nights": nights,
        "breakdown": {
            "tickets": {"total": total_tickets, "items": ticket_items},
            "meals": {"total": total_meals, "items": meal_items},
            "accommodation": accommodation_detail,
            "transport": transport_detail,
            "subtotal": subtotal,
            "contingency": contingency,
            "total": total,
            "per_pax": per_pax
        },
        "not_included": [
            "Vé máy bay / xe khách khứ hồi liên tỉnh tới TP. Buôn Ma Thuột",
            "Chi phí đồ uống cá nhân ngoài thực đơn và quà đặc sản (cà phê, hạt Kơ nia)",
            "Tiền bồi dưỡng (tip) cho tài xế và hướng dẫn viên (tùy tâm)"
        ]
    }

def build_itinerary_timeline(pax, days, destination_ids, catalog=None):
    if catalog is None:
        catalog = load_catalog()
    
    dest_map = {d["id"]: d for d in catalog["destinations"]}
    meals_map = {m["id"]: m for m in catalog["meals"]}
    
    timeline = []
    
    # Chia điểm đến vào các ngày một cách hợp lý
    dests = [dest_map[did] for did in destination_ids if did in dest_map]
    
    if days == 1:
        # Ngày 1 duy nhất: Sáng 1-2 điểm, Chiều 1 điểm
        d1 = dests[:2]
        day1_schedule = []
        
        # Sáng
        day1_schedule.append({
            "slot": "07:30 - 08:30",
            "title": "Điểm tâm sáng & Cà phê Buôn Ma Thuột",
            "type": "meal",
            "desc": "Thưởng thức bún đỏ trứ danh và ly cà phê Robusta chuẩn vị phố núi.",
            "location": "Trung tâm TP. Buôn Ma Thuột"
        })
        if len(d1) > 0:
            day1_schedule.append({
                "slot": "08:30 - 11:30",
                "title": d1[0]["name"],
                "type": "visit",
                "desc": d1[0]["highlight"],
                "cultural_note": d1[0]["cultural_note"],
                "ticket": d1[0]["ticket_price"],
                "duration": f"{d1[0]['duration_hours']} giờ",
                "address": d1[0]["address"],
                "dest_id": d1[0]["id"]
            })
        # Trưa
        day1_schedule.append({
            "slot": "11:30 - 13:30",
            "title": "Bữa trưa đặc sản Tây Nguyên & Nghỉ trưa",
            "type": "meal",
            "desc": "Bánh ướt đĩa chồng Lê Thánh Tông hoặc cơm lam gà nướng than hoa.",
            "location": "TP. Buôn Ma Thuột"
        })
        # Chiều
        if len(d1) > 1:
            day1_schedule.append({
                "slot": "14:00 - 17:00",
                "title": d1[1]["name"],
                "type": "visit",
                "desc": d1[1]["highlight"],
                "cultural_note": d1[1]["cultural_note"],
                "ticket": d1[1]["ticket_price"],
                "duration": f"{d1[1]['duration_hours']} giờ",
                "address": d1[1]["address"],
                "dest_id": d1[1]["id"]
            })
        # Tối
        day1_schedule.append({
            "slot": "18:00 - 21:00",
            "title": "Lẩu cá lăng Sêrêpôk & Khám phá Chợ đêm BMT",
            "type": "meal",
            "desc": "Bữa tối ấm cúng với lẩu măng le cá lăng, tự do dạo ngã 6 Ban Mê và thưởng thức ẩm thực đêm.",
            "location": "Phố đi bộ Buôn Ma Thuột"
        })
        
        timeline.append({"day": 1, "theme": "Hương vị Phố núi & Dấu ấn Văn hóa", "schedule": day1_schedule})
        
    elif days == 2:
        # Ngày 1: TP Buôn Ma Thuột & Cà phê
        # Ngày 2: Thiên nhiên ngoại thành (Thác hoặc Yok Đôn/Lắk)
        d_day1 = dests[:2]
        d_day2 = dests[2:4] if len(dests) >= 4 else dests[2:]
        if not d_day2 and len(dests) > 1:
            d_day2 = [dests[1]]
            d_day1 = [dests[0]]
            
        # Schedule Day 1
        s1 = [
            {"slot": "07:30 - 08:30", "title": "Bún đỏ & Cà phê sáng", "type": "meal", "desc": "Khởi đầu năng lượng với ẩm thực địa phương đặc trưng."},
            {"slot": "08:30 - 11:30", "title": d_day1[0]["name"], "type": "visit", "desc": d_day1[0]["highlight"], "cultural_note": d_day1[0]["cultural_note"], "ticket": d_day1[0]["ticket_price"], "duration": f"{d_day1[0]['duration_hours']}h", "address": d_day1[0]["address"], "dest_id": d_day1[0]["id"]},
            {"slot": "11:30 - 13:30", "title": "Cơm trưa ẩm thực Tây Nguyên", "type": "meal", "desc": "Nghỉ ngơi và thưởng thức món gỏi cà đắng cá khô."},
        ]
        if len(d_day1) > 1:
            s1.append({"slot": "14:00 - 17:00", "title": d_day1[1]["name"], "type": "visit", "desc": d_day1[1]["highlight"], "cultural_note": d_day1[1]["cultural_note"], "ticket": d_day1[1]["ticket_price"], "duration": f"{d_day1[1]['duration_hours']}h", "address": d_day1[1]["address"], "dest_id": d_day1[1]["id"]})
        s1.append({"slot": "18:00 - 21:00", "title": "Bữa tối cá lăng & Không gian cồng chiêng", "type": "meal", "desc": "Thưởng thức lẩu cá lăng sông Sêrêpôk, ngắm thành phố về đêm."})
        timeline.append({"day": 1, "theme": "Huyền thoại Cà phê & Di sản Phố núi", "schedule": s1})
        
        # Schedule Day 2
        s2 = [
            {"slot": "07:00 - 08:00", "title": "Ăn sáng và xuất phát đi ngoại ô", "type": "meal", "desc": "Chuẩn bị trang phục dã ngoại thoải mái, mang nước uống cá nhân."},
        ]
        if len(d_day2) > 0:
            s2.append({"slot": "08:30 - 12:00", "title": d_day2[0]["name"], "type": "visit", "desc": d_day2[0]["highlight"], "cultural_note": d_day2[0]["cultural_note"], "ticket": d_day2[0]["ticket_price"], "duration": f"{d_day2[0]['duration_hours']}h", "address": d_day2[0]["address"], "dest_id": d_day2[0]["id"]})
        s2.append({"slot": "12:00 - 14:00", "title": "Cơm lam & Gà nướng than củi", "type": "meal", "desc": "Ẩm thực nướng ống tre đặc sắc của đồng bào bản địa ven suối."})
        if len(d_day2) > 1:
            s2.append({"slot": "14:00 - 16:30", "title": d_day2[1]["name"], "type": "visit", "desc": d_day2[1]["highlight"], "cultural_note": d_day2[1]["cultural_note"], "ticket": d_day2[1]["ticket_price"], "duration": f"{d_day2[1]['duration_hours']}h", "address": d_day2[1]["address"], "dest_id": d_day2[1]["id"]})
        s2.append({"slot": "17:00 - 18:30", "title": "Trở về trung tâm & Mua sắm đặc sản", "type": "visit", "desc": "Ghé hợp tác xã nông sản Đắk Lắk mua cà phê hạt rang mộc và hạt mắc-ca làm quà."})
        timeline.append({"day": 2, "theme": "Hùng vĩ Đại ngàn & Trải nghiệm Sinh thái", "schedule": s2})

    else:
        # Days == 3
        d1 = dests[0:2]
        d2 = dests[2:4] if len(dests) >= 4 else dests[1:3]
        d3 = dests[4:6] if len(dests) >= 6 else (dests[3:5] if len(dests) >= 5 else [dests[-1]])
        
        # Day 1: Buôn Ma Thuột
        s1 = [
            {"slot": "07:30 - 08:30", "title": "Bún đỏ & Cà phê sáng", "type": "meal", "desc": "Nạp năng lượng chuẩn bị hành trình."},
            {"slot": "08:30 - 11:30", "title": d1[0]["name"], "type": "visit", "desc": d1[0]["highlight"], "cultural_note": d1[0]["cultural_note"], "ticket": d1[0]["ticket_price"], "duration": f"{d1[0]['duration_hours']}h", "address": d1[0]["address"], "dest_id": d1[0]["id"]},
            {"slot": "11:30 - 13:30", "title": "Cơm trưa ẩm thực phố núi", "type": "meal", "desc": "Bánh ướt chồng đĩa hoặc cơm niêu truyền thống."},
            {"slot": "14:00 - 17:00", "title": d1[1]["name"] if len(d1) > 1 else "Bảo tàng Thế giới Cà phê", "type": "visit", "desc": "Khám phá kiến trúc nhà rông cách điệu.", "cultural_note": "Giữ gìn vệ sinh và trật tự chung.", "ticket": 150000, "duration": "2.0h", "address": "TP. BMT", "dest_id": d1[1]["id"] if len(d1) > 1 else "baotang-thegioicaphe"},
            {"slot": "18:00 - 21:00", "title": "Lẩu cá lăng Sêrêpôk măng chua", "type": "meal", "desc": "Món đặc sản sông lớn trứ danh Tây Nguyên."}
        ]
        timeline.append({"day": 1, "theme": "Trái tim Thủ phủ Cà phê & Di sản Tây Nguyên", "schedule": s1})
        
        # Day 2: Thiên nhiên Thác Dray Nur / Yok Đôn
        s2 = [
            {"slot": "07:00 - 08:00", "title": "Ăn sáng xuất phát đi Vùng Sinh thái", "type": "meal", "desc": "Di chuyển bằng ô tô tới điểm đến thiên nhiên."},
            {"slot": "08:30 - 12:00", "title": d2[0]["name"], "type": "visit", "desc": d2[0]["highlight"], "cultural_note": d2[0]["cultural_note"], "ticket": d2[0]["ticket_price"], "duration": f"{d2[0]['duration_hours']}h", "address": d2[0]["address"], "dest_id": d2[0]["id"]},
            {"slot": "12:00 - 13:30", "title": "Cơm lam gà sa lửa Bản Đôn", "type": "meal", "desc": "Gà đồi ướp muối é rừng nướng thơm giòn."},
            {"slot": "14:00 - 17:00", "title": d2[1]["name"] if len(d2) > 1 else "Cụm Thác Dray Nur", "type": "visit", "desc": "Chiêm ngưỡng dòng thác nước trắng xoá giữa đại ngàn.", "cultural_note": "Tuân thủ ranh giới an toàn của ban quản lý.", "ticket": 40000, "duration": "3h", "address": "Krông Ana", "dest_id": d2[1]["id"] if len(d2) > 1 else "thac-draynur"},
            {"slot": "18:30 - 21:00", "title": "Bữa tối buôn làng & Giao lưu văn hóa", "type": "meal", "desc": "Cơm nếp nương, canh cà đắng và thưởng thức cồng chiêng bên bếp lửa."}
        ]
        timeline.append({"day": 2, "theme": "Hùng vĩ Dòng Sêrêpôk & Rừng Khộp Nguyên sinh", "schedule": s2})
        
        # Day 3: Hồ Lắk hoặc Làng nghề
        s3 = [
            {"slot": "07:00 - 08:00", "title": "Điểm tâm sáng và trả phòng", "type": "meal", "desc": "Chuẩn bị hành trang cho ngày trải nghiệm văn hóa ven hồ."},
            {"slot": "08:30 - 12:00", "title": d3[0]["name"], "type": "visit", "desc": d3[0]["highlight"], "cultural_note": d3[0]["cultural_note"], "ticket": d3[0]["ticket_price"], "duration": f"{d3[0]['duration_hours']}h", "address": d3[0]["address"], "dest_id": d3[0]["id"]},
            {"slot": "12:00 - 13:30", "title": "Bữa trưa cá bống hồ Lắk kho tộ", "type": "meal", "desc": "Đặc sản dân dã đậm đà của đồng bào M'Nông Rlâm."},
            {"slot": "14:00 - 16:30", "title": "Ghé thăm Buôn AKô Dhông (Buôn Cô Thôn)", "type": "visit", "desc": "Buôn làng cổ đẹp nhất giữa lòng Buôn Ma Thuột với những ngôi nhà dài trăm tuổi.", "cultural_note": "Tôn trọng đời sống sinh hoạt của bà con.", "ticket": 0, "duration": "1.5h", "address": "P. Tân Lợi, TP. BMT", "dest_id": "chua-khaidoan"},
            {"slot": "16:30 - 18:00", "title": "Mua sắm nông sản OCOP Đắk Lắk & Ra sân bay/bến xe", "type": "visit", "desc": "Kết thúc chuyến đi ý nghĩa và trọn vẹn văn minh."}
        ]
        timeline.append({"day": 3, "theme": "Lắng đọng Hồ Lắk & Tạm biệt Đại ngàn", "schedule": s3})

    return timeline

def calculate_category_distribution(destination_ids, catalog=None):
    if catalog is None:
        catalog = load_catalog()
    dest_map = {d["id"]: d for d in catalog["destinations"]}
    counts = {"Văn hóa & Di sản": 0, "Thiên nhiên & Sinh thái": 0, "Cà phê & Lối sống": 0}
    total = 0
    for did in destination_ids:
        d = dest_map.get(did)
        if not d:
            continue
        cat = d.get("category", "")
        if cat == "van_hoa":
            counts["Văn hóa & Di sản"] += 1
        elif cat in ("thien_nhien", "sinh_thai"):
            counts["Thiên nhiên & Sinh thái"] += 1
        elif cat == "ca_phe":
            counts["Cà phê & Lối sống"] += 1
        total += 1
    if total == 0:
        return [{"label": k, "pct": 33} for k in counts]
    return [
        {"label": k, "count": v, "pct": round(v / total * 100)}
        for k, v in counts.items()
    ]

def generate_trip_plans(pax, days, user_budget, preference, cluster="bmt"):
    catalog = load_catalog()
    pax = max(1, min(12, int(pax)))
    days = max(1, min(3, int(days)))
    user_budget = float(user_budget) if user_budget else 5000000.0

    # Xây dựng 3 bộ điểm đến ứng viên cho 3 phong cách
    # Option 1: Plan A - Cân bằng & Trải nghiệm
    # Option 2: Plan B - Văn hóa & Di sản Cồng chiêng
    # Option 3: Plan C - Sinh thái & Thiên nhiên Hoang sơ
    
    if days == 1:
        opts_dests = {
            "A": ["baotang-daklak", "langcaphe-trungnguyen"],
            "B": ["baotang-daklak", "chua-khaidoan"],
            "C": ["thac-draynur", "langcaphe-trungnguyen"]
        }
    elif days == 2:
        opts_dests = {
            "A": ["baotang-daklak", "langcaphe-trungnguyen", "thac-draynur", "chua-khaidoan"],
            "B": ["baotang-daklak", "chua-khaidoan", "ho-lak-buon-jun", "langcaphe-trungnguyen"],
            "C": ["langcaphe-trungnguyen", "thac-draynur", "vqg-yokdon", "buondon-cautro"]
        }
    else: # 3 days
        opts_dests = {
            "A": ["baotang-daklak", "langcaphe-trungnguyen", "thac-draynur", "vqg-yokdon", "ho-lak-buon-jun"],
            "B": ["baotang-daklak", "chua-khaidoan", "ho-lak-buon-jun", "buondon-cautro", "langcaphe-trungnguyen"],
            "C": ["thac-draynur", "vqg-yokdon", "buondon-cautro", "ho-lak-buon-jun", "langcaphe-trungnguyen"]
        }

    plan_metadata = {
        "A": {
            "name": "Hành trình Trải nghiệm Cân bằng",
            "tagline": "Tối ưu thời gian, kết hợp hài hòa cà phê, di sản và thác nước hùng vĩ",
            "badge": "Lựa chọn Phổ biến",
            "acc_type": "hotel"
        },
        "B": {
            "name": "Hành trình Văn hóa & Di sản Cồng Chiêng",
            "tagline": "Đi sâu vào nếp sống nhà dài Êđê, buôn làng M'Nông và không gian di sản UNESCO",
            "badge": "Đậm đà Bản sắc",
            "acc_type": "homestay"
        },
        "C": {
            "name": "Hành trình Thiên nhiên & Sinh thái Voi Thân thiện",
            "tagline": "Chiêm ngưỡng kỳ quan thác ghềnh và trải nghiệm du lịch ngắm voi bảo tồn văn minh",
            "badge": "Du lịch Bền vững",
            "acc_type": "hotel"
        }
    }

    results = []
    for code, dest_list in opts_dests.items():
        meta = plan_metadata[code]
        budget_info = calculate_plan_budget(
            pax=pax,
            days=days,
            selected_destinations=dest_list,
            accommodation_id=meta["acc_type"],
            catalog=catalog
        )
        total_cost = budget_info["breakdown"]["total"]
        diff = user_budget - total_cost
        
        if diff >= 0:
            status = "fit"
            status_text = f"Nằm trọn trong ngân sách (Dư {int(diff):,}đ)"
        else:
            status = "exceeded"
            status_text = f"Vượt ngân sách {int(abs(diff)):,}đ"

        timeline = build_itinerary_timeline(pax, days, dest_list, catalog)
        distribution = calculate_category_distribution(dest_list, catalog)

        results.append({
            "code": code,
            "name": meta["name"],
            "tagline": meta["tagline"],
            "badge": meta["badge"],
            "accommodation_type": meta["acc_type"],
            "destinations": dest_list,
            "destination_details": [get_destination_by_id(d, catalog) for d in dest_list if get_destination_by_id(d, catalog)],
            "budget": budget_info,
            "timeline": timeline,
            "distribution": distribution,
            "budget_check": {
                "user_budget": int(user_budget),
                "total_cost": total_cost,
                "difference": int(diff),
                "status": status,
                "status_text": status_text
            }
        })

    # Đưa ra phương án mặc định theo quy tắc dựa trên preference
    default_code = "A"
    pref_lower = (preference or "").lower()
    if any(k in pref_lower for k in ["văn hóa", "cồng chiêng", "di sản", "lịch sử", "buôn"]):
        default_code = "B"
    elif any(k in pref_lower for k in ["thiên nhiên", "thác", "sinh thái", "voi", "rừng", "khám phá"]):
        default_code = "C"

    return {
        "user_input": {
            "pax": pax,
            "days": days,
            "budget": int(user_budget),
            "preference": preference,
            "cluster": cluster
        },
        "default_option": default_code,
        "options": results,
        "responsible_rules": catalog["responsible_rules"],
        "sources": load_sources()["sources"]
    }

def swap_destination_in_plan(current_destinations, old_dest_id, new_dest_id, pax, days, acc_type="hotel"):
    catalog = load_catalog()
    new_dests = []
    for d in current_destinations:
        if d == old_dest_id:
            new_dests.append(new_dest_id)
        else:
            new_dests.append(d)
            
    budget_info = calculate_plan_budget(pax, days, new_dests, accommodation_id=acc_type, catalog=catalog)
    timeline = build_itinerary_timeline(pax, days, new_dests, catalog)
    distribution = calculate_category_distribution(new_dests, catalog)
    
    return {
        "destinations": new_dests,
        "destination_details": [get_destination_by_id(d, catalog) for d in new_dests if get_destination_by_id(d, catalog)],
        "budget": budget_info,
        "timeline": timeline,
        "distribution": distribution
    }
