def occupancy_rate(list_apartment):
    occupancy_map = {}
    total_records = 0
    total_rooms = 0
    total_available_rooms = 0

    for apartment in list_apartment:
        name = apartment['name']
        rooms_total = apartment['roomsNumber']
        available_rooms = apartment['availableRoom']
        rooms_index = rooms_total - available_rooms
        total_rooms += rooms_total
        total_available_rooms += rooms_index
        total_records += 1

        occupancy_index = (rooms_index / rooms_total * 100.0) if rooms_total > 0 else 0.0

        list_value = [str(rooms_total), str(rooms_index), f"{occupancy_index:.2f}%"]
        occupancy_map[name] = list_value

    total_list = [str(total_rooms), str(total_available_rooms)]
    total_list.append(f"{(total_available_rooms / total_rooms * 100.0):.2f}%" if total_rooms > 0 else "0.00%")
    occupancy_map["Total"] = total_list

    return occupancy_map

def revenue(list_apartments):
    total_revenue = 0
    total_records = 0
    total_rent_price = 0
    total_available_rooms = 0
    revenue_map = {}

    for apartment in list_apartments:
        name = apartment['name']
        rooms_total = apartment['roomsNumber']
        available_rooms = apartment['availableRoom']
        rent_price = apartment['rentPrice']
        rooms_index = rooms_total - available_rooms
        revenue = rooms_index * rent_price

        list_value = [str(rooms_index), str(rent_price), str(revenue)]
        revenue_map[name] = list_value

        total_revenue += revenue
        total_rent_price += rent_price
        total_available_rooms += rooms_index
        total_records += 1

    total_revenue_list = [str(total_available_rooms), str(total_rent_price), str(total_revenue)]
    revenue_map["Total"] = total_revenue_list

    return revenue_map
