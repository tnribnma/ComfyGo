import json
from datetime import date, datetime, timezone, timedelta
from random import choice, randint, uniform

from .database import Database
from .models import (
    Hotel, Room, Customer, Review, TourPackage, PackageBooking,
    Activity, ActivityBooking, Restaurant, Flight, Promotion, LocalTransport,
)

def _imgs(*urls):
    return json.dumps(list(urls))

def _list(*items):
    return json.dumps(list(items))

def _gen_rooms(hotel_ids):
    """Generate 2-3 room types per hotel."""
    room_types = [
        ("Standard Room", "A comfortable room with all the essentials.", "2 adults", "1 Queen Bed", 22, 0.7),
        ("Deluxe Room", "Spacious room with premium amenities and city views.", "2 adults", "1 King Bed", 30, 1.0),
        ("Ocean View Suite", "Luxury suite with stunning ocean panorama.", "2 adults", "1 King Bed + Sofa", 45, 1.4),
        ("Family Room", "Perfect for families with extra space and beds.", "4 adults + 2 children", "2 Queen Beds", 38, 1.1),
    ]
    base_amenities = ["Wi-Fi", "Air Conditioning", "TV", "Mini Bar"]
    extra_amenities = ["Balcony", "Sea View", "Coffee Machine", "Bathtub", "Room Service"]

    rooms = []
    for hid in hotel_ids:
        for rt in room_types:
            name, desc, cap, beds, size, price_mult = rt
            ams = base_amenities + [choice(extra_amenities) for _ in range(randint(1, 3))]
            if price_mult > 1.0:
                ams.append("Balcony")
            breakfast = price_mult >= 1.0
            rooms.append(dict(
                hotel_id=hid,
                room_type=name,
                room_name=f"{name} - {choice(['City', 'Garden', 'Pool', 'Mountain'])} View",
                room_description=desc,
                room_capacity=cap,
                room_beds=beds,
                room_size_sqm=size + randint(-3, 5),
                price_per_night=round(randint(45, 180) * price_mult, 2),
                available_rooms=randint(2, 15),
                amenities=_list(*ams),
                breakfast_included=breakfast,
                images=_imgs(
                    "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=800&q=85",
                    "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=800&q=85",
                ),
            ))
    return rooms


REVIEW_TEMPLATES = [
    (5, "Absolutely magical!", "This place exceeded all my expectations. The views were breathtaking, the staff were incredibly warm, and every detail was thoughtfully curated. I'll definitely be coming back."),
    (5, "A perfect getaway", "From the moment we arrived, everything was seamless. The room was stunning, the food was divine, and the atmosphere was pure relaxation. Worth every penny."),
    (5, "Best travel experience ever", "I've travelled extensively and this ranks among my top experiences. The attention to detail, the genuine hospitality, and the unique character of this place make it truly special."),
    (4, "Great experience overall", "Really enjoyed our stay. The location was perfect and the room was comfortable. Only minor issue was the WiFi speed, but everything else was excellent."),
    (4, "Beautiful and well-maintained", "The property is gorgeous and clearly well cared for. Staff were friendly and helpful. Breakfast could have more variety, but the quality was great."),
    (4, "Would recommend to friends", "Solid choice for a holiday. Clean rooms, nice pool area, and the restaurant serves excellent local food. The only reason it's not 5 stars is the noise from the street at night."),
    (3, "Decent but room for improvement", "The location is unbeatable and the views are spectacular. However, some facilities felt dated and the service was inconsistent. Still, I had a good time."),
    (3, "Good value for money", "For the price, this is a solid option. Rooms are clean and functional, breakfast is included, and the staff try their best. Don't expect luxury, but you won't be disappointed."),
    (5, "A hidden gem", "Stumbled upon this place and was blown away. The authenticity, the warmth of the hosts, and the stunning surroundings made this a trip to remember. Highly recommended!"),
    (4, "Perfect for couples", "Romantic setting, beautiful sunsets, and excellent food. We celebrated our anniversary here and it was absolutely magical. The spa treatments were divine."),
    (5, "Outstanding hospitality", "The hosts went above and beyond to make our stay special. From restaurant recommendations to arranging a surprise birthday cake, everything was perfect."),
    (4, "Lovely property with character", "This isn't a cookie-cutter hotel — it has real soul. The architecture, the art on the walls, the handcrafted furniture — everything tells a story."),
    (3, "Nice but overpriced", "Beautiful property and great location, but for the price I expected more. The room was smaller than advertised and some amenities listed weren't available."),
    (5, "Will return!", "This was our third visit and it gets better every time. The new pool area is fantastic and the evening entertainment is a wonderful touch."),
    (4, "Solid choice in the area", "Compared to other options in the area, this is one of the best. Clean, well-located, and the staff speak excellent English."),
    (5, "Trip of a lifetime", "This package exceeded every expectation. The itinerary was perfectly paced, the guide was knowledgeable and fun, and the accommodations were top-notch."),
    (4, "Well-organized tour", "Everything was well planned and executed. The only suggestion would be to add more free time, but overall a fantastic experience."),
    (5, "Delicious food, great ambiance", "The chef clearly loves what they do. Every dish was a masterpiece. The seafood platter was the best I've ever had. Beautiful setting too!"),
    (4, "Fresh and flavorful", "Great local cuisine with a modern twist. The chef uses locally sourced ingredients and you can taste the difference. Highly recommend the fish curry."),
    (3, "Good food, slow service", "The food quality is excellent but the service can be painfully slow during peak hours. Come early or be prepared to wait."),
    (5, "Incredible adventure!", "This activity was the highlight of our trip. Professional guides, stunning scenery, and an adrenaline rush like no other. Safety was well managed too."),
    (4, "Fun and well-run", "Great activity for all skill levels. The guide was patient with beginners and made sure everyone had a great time. Thoroughly enjoyed it."),
    (5, "Unforgettable flight!", "Smooth flight with stunning aerial views. The airline crew were professional and the in-flight service was excellent for the price."),
    (4, "Comfortable and on time", "Reliable service with good legroom. The flight was on time and the baggage allowance was generous. Would fly again."),
]


RESTAURANT_REVIEW_TEMPLATES = [
    (5, "Best meal of the trip!", "Absolutely incredible food. The flavours were authentic and the portions generous. The grilled seafood platter was outstanding. Will definitely return!"),
    (4, "Really good local food", "Great atmosphere and friendly staff. The food was fresh and well-prepared. Service was a bit slow during peak hours but worth the wait."),
    (5, "A must-visit for food lovers", "This restaurant is a hidden gem. The chef clearly knows what they are doing. Every dish was beautifully presented and bursting with flavour."),
    (4, "Great value for money", "Excellent quality food at very reasonable prices. The local specialties were authentic and delicious. The outdoor seating area has lovely views."),
    (3, "Decent but not spectacular", "The food was fine but nothing extraordinary. Service was friendly and the ambiance was nice. Good option if you are in the area."),
    (5, "Outstanding dining experience", "From the moment we walked in, we were treated like family. The food was phenomenal - fresh ingredients, bold flavours, and generous portions. A highlight of our trip!"),
    (4, "Perfect for a casual meal", "Lovely spot for a relaxed dinner. The outdoor seating is wonderful and the menu has great variety. Vegetarian options were impressive."),
    (5, "Authentic local cuisine at its best", "If you want to taste the real flavours of this region, this is the place. The chef uses traditional recipes and you can taste the difference. Highly recommended!"),
]


def _gen_reviews(hotel_ids, customer_ids, spot_ids, package_ids, restaurant_ids=None):
    reviews = []
    used = set()
    for hid in hotel_ids:
        for _ in range(randint(2, 4)):
            cid = choice(customer_ids)
            key = (cid, "hotel", hid)
            if key in used:
                continue
            used.add(key)
            tpl = choice(REVIEW_TEMPLATES)
            reviews.append(dict(
                customer_id=cid,
                entity_type="hotel",
                entity_id=hid,
                rating=tpl[0],
                title=tpl[1],
                comment=tpl[2],
                helpful_count=randint(0, 50),
                verified_visit=choice([True, True, False]),
                photos=_imgs("https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=400&q=85") if choice([True, False]) else None,
            ))

    for sid in (spot_ids or [])[:10]:
        for _ in range(randint(1, 3)):
            cid = choice(customer_ids)
            key = (cid, "destination", sid)
            if key in used:
                continue
            used.add(key)
            tpl = choice(REVIEW_TEMPLATES)
            reviews.append(dict(
                customer_id=cid,
                entity_type="destination",
                entity_id=sid,
                rating=tpl[0],
                title=tpl[1],
                comment=tpl[2],
                helpful_count=randint(0, 30),
                verified_visit=choice([True, False]),
                photos=None,
            ))

    for pid in (package_ids or [])[:8]:
        for _ in range(randint(1, 2)):
            cid = choice(customer_ids)
            key = (cid, "package", pid)
            if key in used:
                continue
            used.add(key)
            tpl = choice(REVIEW_TEMPLATES)
            reviews.append(dict(
                customer_id=cid,
                entity_type="package",
                entity_id=pid,
                rating=tpl[0],
                title=tpl[1],
                comment=tpl[2],
                helpful_count=randint(0, 20),
                verified_visit=True,
                photos=None,
            ))

    for rid in (restaurant_ids or []):
        for _ in range(randint(2, 5)):
            cid = choice(customer_ids)
            key = (cid, "restaurant", rid)
            if key in used:
                continue
            used.add(key)
            tpl = choice(RESTAURANT_REVIEW_TEMPLATES)
            reviews.append(dict(
                customer_id=cid,
                entity_type="restaurant",
                entity_id=rid,
                rating=tpl[0],
                title=tpl[1],
                comment=tpl[2],
                helpful_count=randint(0, 30),
                verified_visit=choice([True, True, False]),
                photos=_imgs("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=85") if choice([True, False]) else None,
            ))

    return reviews


PACKAGES = [
    dict(
        package_name="Cox's Bazar Coastal Escape",
        destination="Cox's Bazar", country="Bangladesh",
        duration_days=4, duration_nights=3, price_per_person=220, original_price=280,
        description="Escape to the world's longest natural sandy beach. Enjoy sunset walks, visit Himchari National Park, indulge in fresh seafood, and experience the vibrant night market. Perfect for beach lovers and adventure seekers.",
        included_services=_list("3-star hotel accommodation", "Airport transfer", "Daily breakfast", "Guided beach tour", "Himchari day trip", "Local transportation"),
        excluded_services=_list("Flights", "Personal expenses", "Lunch and dinner", "Travel insurance"),
        itinerary=_list(
            {"day":1,"title":"Arrival & Beach Sunset","description":"Arrive at Cox's Bazar, hotel check-in, Laboni Beach sunset walk, seafood dinner at Ocean Breeze Restaurant."},
            {"day":2,"title":"Himchari Adventure","description":"Himchari National Park hike, waterfall visit, afternoon at Inani Beach with coral exploration."},
            {"day":3,"title":"Island Exploration","description":"St. Martin Island day trip or Cox's Bazar sightseeing, night market shopping for souvenirs."},
            {"day":4,"title":"Departure","description":"Morning beach walk, last-minute souvenir shopping, departure transfer."},
        ),
        hotel_name="Coastline Villa", hotel_rating="4 star", transportation="AC minibus", meals="Breakfast included",
        tour_guide_included=True, tour_guide_name="Rahim Ahmed",
        difficulty="Easy", group_size_min=2, group_size_max=12, max_group_size=24, booked_count=8,
        available_dates=_list("2026-09-15", "2026-10-01", "2026-10-15", "2026-11-01", "2026-11-15"),
        cancellation_policy="Free cancellation up to 7 days before departure. 50% fee for cancellations within 7 days.",
        rating=4.7, review_count=23, is_active=True,
        highlights=_list("World's longest natural sandy beach", "Himchari waterfall trek", "St. Martin Island snorkelling", "Fresh seafood experience", "Night market shopping"),
        what_to_bring=_list("Sunscreen SPF 50+", "Comfortable walking shoes", "Swimwear", "Camera", "Light jacket for evening")
        , languages="English, Bengali",
        image="https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=1200&q=85",
        gallery_images=_imgs("https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=85"),
    ),
    dict(
        package_name="Bandarban Hill Trek Adventure",
        destination="Bandarban", country="Bangladesh",
        duration_days=5, duration_nights=4, price_per_person=350, original_price=420,
        description="Trek through the pristine Chittagong Hill Tracts. Visit Nilgiri Hills, Boga Lake, and indigenous tribal villages. Experience authentic hill culture and breathtaking mountain panoramas.",
        included_services=_list("Eco-lodge accommodation", "All meals", "Expert local guide", "Trekking permits", "4x4 transport", "Camping equipment"),
        excluded_services=_list("Flights", "Personal gear", "Tips", "Travel insurance"),
        itinerary=_list(
            {"day":1,"title":"Arrival & Village Walk","description":"Arrive Bandarban, transfer to eco-lodge, evening walk through indigenous Marma village."},
            {"day":2,"title":"Nilgiri Hills Trek","description":"Full day trek to Nilgiri Hills (3,200 ft), sunrise viewpoint, Marma village cultural visit."},
            {"day":3,"title":"Boga Lake Expedition","description":"Full day trek to the stunning Boga Lake at 1,200 ft, camp overnight with mountain views."},
            {"day":4,"title":"Waterfall & Return","description":"Morning at Boga Lake, return trek via Thanchi Waterfall, evening bonfire at eco-lodge."},
            {"day":5,"title":"Departure","description":"Morning at leisure, photos, departure transfer."},
        ),
        hotel_name="Sylvan Retreat", hotel_rating="3 star eco-lodge", transportation="4x4 Jeep", meals="All meals included",
        tour_guide_included=True, tour_guide_name="Marma Guide Team",
        difficulty="Moderate", group_size_min=4, group_size_max=10, max_group_size=20, booked_count=6,
        available_dates=_list("2026-10-01", "2026-10-15", "2026-11-01", "2026-11-15"),
        cancellation_policy="Free cancellation up to 14 days before departure. No refund within 14 days.",
        rating=4.9, review_count=18, is_active=True,
        highlights=_list("Nilgiri Hills sunrise trek", "Boga Lake overnight camping", "Indigenous Marma village culture", "Thanchi Waterfall", "Mountain panorama views"),
        what_to_bring=_list("Trekking boots", "Warm layers", "Rain gear", "Headlamp", "First-aid kit", "Water bottle 2L"),
        languages="English, Bengali, Marma",
        image="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85",
        gallery_images=_imgs("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=85"),
    ),
    dict(
        package_name="Galle Heritage & Beach Holiday",
        destination="Galle", country="Sri Lanka",
        duration_days=5, duration_nights=4, price_per_person=380, original_price=450,
        description="Explore the UNESCO World Heritage Galle Fort, relax on pristine beaches, visit local spice gardens, and enjoy authentic Sri Lankan cuisine. A perfect blend of culture and relaxation.",
        included_services=_list("Boutique hotel", "Daily breakfast", "Airport transfers", "Galle Fort walking tour", "Spice garden visit", "Tuk-tuk day trip", "Snorkelling gear"),
        excluded_services=_list("Flights", "Lunch and dinner", "Personal expenses", "Travel insurance"),
        itinerary=_list(
            {"day":1,"title":"Arrival & Fort Sunset","description":"Arrive Galle, hotel check-in at The Ceylon House, Galle Fort sunset walk along ramparts."},
            {"day":2,"title":"Galle Fort Deep Dive","description":"Guided tour of Galle Fort, Maritime Museum, lighthouse visit, lunch at Fort Kitchen."},
            {"day":3,"title":"Beach Day","description":"Unawatuna Beach full day, snorkelling at coral reef, beachside seafood dinner."},
            {"day":4,"title":"Spice & Culture","description":"Spice garden visit with guided tour, traditional Sri Lankan cooking class, farewell dinner."},
            {"day":5,"title":"Departure","description":"Morning at leisure, last shopping at Fort boutiques, departure transfer."},
        ),
        hotel_name="The Ceylon House", hotel_rating="4 star boutique", transportation="Tuk-tuk & private car", meals="Breakfast included",
        tour_guide_included=True, tour_guide_name="Nimal Perera",
        difficulty="Easy", group_size_min=2, group_size_max=8, max_group_size=16, booked_count=4,
        available_dates=_list("2026-09-01", "2026-09-15", "2026-10-01", "2026-10-15", "2026-11-01"),
        cancellation_policy="Free cancellation up to 10 days before departure. 30% fee within 10 days.",
        rating=4.8, review_count=31, is_active=True,
        highlights=_list("UNESCO Galle Fort guided tour", "Unawatuna snorkelling", "Spice garden & cooking class", "Tuk-tuk adventure", "Colonial boutique hotel"),
        what_to_bring=_list("Sun hat & sunscreen", "Comfortable shoes for fort walks", "Swimwear", "Camera", "Light shawl for temples")
        , languages="English, Sinhala",
        image="https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=1200&q=85",
        gallery_images=_imgs("https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=800&q=85"),
    ),
    dict(
        package_name="Kathmandu Valley Explorer",
        destination="Kathmandu", country="Nepal",
        duration_days=6, duration_nights=5, price_per_person=420, original_price=520,
        description="Discover the mystical Kathmandu Valley — from ancient temples to vibrant markets. Visit Swayambhunath, Boudhanath, Bhaktapur, and enjoy a day trip to Nagarkot for Himalayan views.",
        included_services=_list("Heritage hotel", "Daily breakfast and lunch", "All temple entries", "Expert cultural guide", "Airport transfers", "Nagarkot excursion", "Cooking class"),
        excluded_services=_list("Flights", "Dinner", "Personal expenses", "Travel insurance"),
        itinerary=_list(
            {"day":1,"title":"Arrival & Thamel","description":"Arrive Kathmandu, hotel check-in, evening exploration of vibrant Thamel district."},
            {"day":2,"title":"Sacred Temples","description":"Swayambhunath (Monkey Temple) morning climb, Pashupatinath temple afternoon, river views."},
            {"day":3,"title":"Bhaktapur Heritage","description":"Full day Bhaktapur trip, pottery and weaving workshops, Durbar Square, local lunch."},
            {"day":4,"title":"Boudhanath & Patan","description":"Boudhanath Stupa morning visit, Patan Durbar Square, Tibetan dinner experience."},
            {"day":5,"title":"Nagarkot Sunrise","description":"4AM departure for Nagarkot sunrise over Himalayas, Changu Narayan temple visit."},
            {"day":6,"title":"Departure","description":"Free morning for shopping, departure transfer."},
        ),
        hotel_name="Himalayan Heritage Inn", hotel_rating="4 star heritage", transportation="Private vehicle", meals="Breakfast and lunch included",
        tour_guide_included=True, tour_guide_name="Dawa Sherpa",
        difficulty="Easy", group_size_min=2, group_size_max=15, max_group_size=30, booked_count=12,
        available_dates=_list("2026-09-01", "2026-10-01", "2026-10-15", "2026-11-01"),
        cancellation_policy="Free cancellation up to 14 days before departure. 40% fee within 14 days.",
        rating=4.8, review_count=42, is_active=True,
        highlights=_list("Nagarkot Himalayan sunrise", "Swayambhunath Monkey Temple", "Bhaktapur pottery workshop", "Boudhanath Stupa", "Patan Durbar Square"),
        what_to_bring=_list("Comfortable walking shoes", "Warm layers for Nagarkot", "Camera", "Cash for tips & souvenirs", "Respectful clothing for temples"),
        languages="English, Nepali",
        image="https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=85",
        gallery_images=_imgs("https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=85"),
    ),
    dict(
        package_name="Chiang Mai Cultural Immersion",
        destination="Chiang Mai", country="Thailand",
        duration_days=5, duration_nights=4, price_per_person=310, original_price=380,
        description="Immerse yourself in Lanna culture — visit golden temples, learn Thai cooking, explore the night bazaar, and spend a day with rescued elephants at the Elephant Nature Park.",
        included_services=_list("Lanna-style resort", "Daily breakfast", "Cooking class", "Doi Suthep temple trip", "Night bazaar tour", "Elephant Nature Park full-day"),
        excluded_services=_list("Flights", "Lunch and dinner", "Personal expenses", "Travel insurance"),
        itinerary=_list(
            {"day":1,"title":"Old City Temples","description":"Arrive Chiang Mai, resort check-in, evening Old City temple walk, night market dinner."},
            {"day":2,"title":"Cooking & Doi Suthep","description":"Morning Thai cooking class at local farm, afternoon Doi Suthep temple with panoramic views."},
            {"day":3,"title":"Elephant Day","description":"Elephant Nature Park full-day ethical elephant experience, feeding, bathing, and learning."},
            {"day":4,"title":"Free Day & Night Bazaar","description":"Free morning for spa or shopping, evening Night Bazaar food tour and shopping."},
            {"day":5,"title":"Departure","description":"Morning meditation at a local temple, departure transfer."},
        ),
        hotel_name="Lanna Lotus Resort", hotel_rating="4 star Lanna-style", transportation="Songthaew & minivan", meals="Breakfast included",
        tour_guide_included=True, tour_guide_name="Nong Bai",
        difficulty="Easy", group_size_min=2, group_size_max=12, max_group_size=24, booked_count=10,
        available_dates=_list("2026-09-15", "2026-10-01", "2026-10-15", "2026-11-01", "2026-11-15"),
        cancellation_policy="Free cancellation up to 7 days before departure. 50% fee within 7 days.",
        rating=4.9, review_count=56, is_active=True,
        highlights=_list("Elephant Nature Park ethical visit", "Thai cooking class with market tour", "Doi Suthep golden temple", "Night Bazaar food adventure", "Lanna temple meditation"),
        what_to_bring=_list("Comfortable sandals", "Light breathable clothing", "Sunscreen", "Camera", "Reusable water bottle"),
        languages="English, Thai",
        image="https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1200&q=85",
        gallery_images=_imgs("https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=800&q=85"),
    ),
    dict(
        package_name="Darjeeling Tea & Himalayas",
        destination="Darjeeling", country="India",
        duration_days=4, duration_nights=3, price_per_person=280, original_price=340,
        description="Wake to Tiger Hill sunrise, ride the heritage Toy Train, walk through emerald tea plantations, and sip the world-famous Darjeeling tea. A journey for the senses.",
        included_services=_list("Heritage homestay", "Daily breakfast", "Tiger Hill sunrise trip", "Toy Train ride", "Tea garden tour & tasting", "Airport transfers", "Monastery visit"),
        excluded_services=_list("Flights", "Lunch and dinner", "Personal expenses", "Travel insurance"),
        itinerary=_list(
            {"day":1,"title":"Arrival & Mall Road","description":"Arrive Darjeeling, check-in at Misty Peaks Homestay, evening Mall Road walk with tea."},
            {"day":2,"title":"Tiger Hill Sunrise","description":"4AM departure for Tiger Hill sunrise over Kanchenjunga, Ghoom Monastery, Batasia Loop."},
            {"day":3,"title":"Toy Train & Tea","description":"Darjeeling Himalayan Railway Toy Train ride, Makaibari Tea Estate tour and tasting."},
            {"day":4,"title":"Departure","description":"Free morning for shopping, departure transfer."},
        ),
        hotel_name="Misty Peaks Homestay", hotel_rating="3 star heritage", transportation="Jeep & Toy Train", meals="Breakfast included",
        tour_guide_included=True, tour_guide_name="Anil Rai",
        difficulty="Easy", group_size_min=2, group_size_max=10, max_group_size=20, booked_count=5,
        available_dates=_list("2026-10-01", "2026-10-15", "2026-11-01", "2026-11-15"),
        cancellation_policy="Free cancellation up to 7 days before departure. No refund within 7 days.",
        rating=4.7, review_count=15, is_active=True,
        highlights=_list("Tiger Hill Kanchenjunga sunrise", "Heritage Toy Train ride", "Makaibari Tea Estate tour", "Ghoom Monastery", "Mall Road evening stroll"),
        what_to_bring=_list("Warm jacket for sunrise", "Comfortable walking shoes", "Camera", "Binoculars for mountain views", "Light layers"),
        languages="English, Hindi, Bengali",
        image="https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=85",
        gallery_images=_imgs("https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85"),
    ),
]

ACTIVITIES = [
    dict(activity_name="Surfing Lesson", destination="Cox's Bazar", country="Bangladesh", description="Learn to ride the waves at the world's longest beach. Professional instructors, all equipment provided. Perfect for beginners who want to catch their first wave.", duration="2 hours", price=25, difficulty="Beginner", min_age=12, max_participants=8, booked_count=3, rating=4.6, review_count=12, category="Water", included=_list("Surfboard", "Wetsuit", "Instructor", "Insurance"), excluded=_list("Towel", "Sunscreen", "Transport to beach"), highlights=_list("World's longest beach", "Professional instructors", "All equipment included", "Small group sizes"), schedule="Daily, 7:00 AM & 4:00 PM", available_dates=_list("2026-09-15","2026-10-01","2026-10-15","2026-11-01"), cancellation_policy="Free cancellation up to 24 hours before.", is_active=True, what_to_bring=_list("Swimwear","Sunscreen","Towel","Water bottle"), instructor_guide="Kamal Rahman", languages="English, Bengali", location_details="Inani Beach, Cox's Bazar", safety_info="Basic swimming recommended. Life jackets provided.", fitness_level="Beginner"),
    dict(activity_name="Snorkelling at Unawatuna", destination="Galle", country="Sri Lanka", description="Explore vibrant coral reefs teeming with tropical fish. Crystal-clear waters with 15+ metre visibility. Equipment and boat ride included.", duration="3 hours", price=35, difficulty="Beginner", min_age=8, max_participants=10, booked_count=4, rating=4.7, review_count=18, category="Water", included=_list("Snorkel gear", "Boat ride", "Guide", "Fruit snack"), excluded=_list("Underwater camera","Transport"), highlights=_list("Coral reef exploration","15m+ visibility","Tropical fish species","Boat ride included"), schedule="Daily, 8:00 AM", available_dates=_list("2026-09-01","2026-09-15","2026-10-01","2026-10-15"), cancellation_policy="Free cancellation up to 48 hours before.", is_active=True, what_to_bring=_list("Swimwear","Sunscreen","Underwater camera"), instructor_guide="Nimal Perera", languages="English, Sinhala", location_details="Unawatuna Beach, Galle", safety_info="Must be comfortable in water. Snorkelling vests available.", fitness_level="Beginner"),
    dict(activity_name="Himchari Hiking", destination="Cox's Bazar", country="Bangladesh", description="Trek through lush tropical forest to stunning waterfalls cascading into the ocean. A moderate hike with breathtaking coastal views.", duration="5 hours", price=20, difficulty="Moderate", min_age=12, max_participants=15, booked_count=6, rating=4.5, review_count=9, category="Land", included=_list("Guide", "Water", "Packed lunch"), excluded=_list("Transport","Trekking gear"), highlights=_list("Tropical waterfall","Ocean panorama views","Dense jungle trek","Wildlife spotting"), schedule="Daily, 6:00 AM", available_dates=_list("2026-09-15","2026-10-01","2026-10-15","2026-11-01"), cancellation_policy="Free cancellation up to 48 hours before.", is_active=True, what_to_bring=_list("Trekking shoes","Water bottle","Hat","Insect repellent"), instructor_guide="Rahim Ahmed", languages="English, Bengali", location_details="Himchari National Park entrance, Cox's Bazar", safety_info="Moderate fitness required. Steep sections. Stay on marked trails.", fitness_level="Moderate"),
    dict(activity_name="Whale Watching at Mirissa", destination="Galle", country="Sri Lanka", description="Spot blue whales, sperm whales, and dolphins in their natural habitat. A once-in-a-lifetime marine encounter. Season runs November to April.", duration="4 hours", price=55, difficulty="Easy", min_age=5, max_participants=30, booked_count=14, rating=4.8, review_count=32, category="Water", included=_list("Boat trip", "Breakfast", "Guide", "Life jacket"), excluded=_list("Transport","Seasickness medication"), highlights=_list("Blue whale sightings","Dolphin pods","Expert marine guide","Breakfast on board"), schedule="Nov–Apr, 6:30 AM", available_dates=_list("2026-11-01","2026-11-15","2026-12-01","2027-01-15"), cancellation_policy="Free cancellation up to 48 hours before. Weather-dependent.", is_active=True, what_to_bring=_list("Sunscreen","Hat","Camera","Seasickness pills"), instructor_guide="Dilanka Silva", languages="English, Sinhala", location_details="Mirissa Fishery Harbour", safety_info="Life jackets mandatory. Not recommended for pregnant women.", fitness_level="Beginner"),
    dict(activity_name="Thai Cooking Class", destination="Chiang Mai", country="Thailand", description="Learn to prepare 4 authentic Thai dishes from scratch using fresh market ingredients. Includes a morning market tour and recipe book to take home.", duration="4 hours", price=40, difficulty="Beginner", min_age=10, max_participants=12, booked_count=7, rating=4.9, review_count=45, category="Cultural", included=_list("Market tour", "All ingredients", "Recipe book", "Lunch"), excluded=_list("Transport","Dinner"), highlights=_list("Market tour with chef","4 dishes to cook","Recipe book included","Eat what you cook"), schedule="Daily, 8:30 AM", available_dates=_list("2026-09-15","2026-10-01","2026-10-15","2026-11-01","2026-11-15"), cancellation_policy="Free cancellation up to 24 hours before.", is_active=True, what_to_bring=_list("Comfortable shoes","Camera","Appetite!"), instructor_guide="Nong Bai", languages="English, Thai", location_details="Nimmanhaemin Road, Chiang Mai", safety_info="Allergies: please inform us in advance.", fitness_level="Beginner"),
    dict(activity_name="Doi Suthep Temple Trek", destination="Chiang Mai", country="Thailand", description="Hike through forest trails to the sacred golden temple. Panoramic views of Chiang Mai valley from the summit. Visit the stunning Wat Phra That.", duration="5 hours", price=30, difficulty="Moderate", min_age=10, max_participants=15, booked_count=5, rating=4.7, review_count=22, category="Land", included=_list("Guide", "Water", "Temple entry"), excluded=_list("Transport","Meals"), highlights=_list("Sacred golden temple","Panoramic valley views","Forest trail trek","Cultural learning"), schedule="Daily, 7:00 AM", available_dates=_list("2026-09-15","2026-10-01","2026-10-15","2026-11-01"), cancellation_policy="Free cancellation up to 24 hours before.", is_active=True, what_to_bring=_list("Comfortable shoes","Water bottle","Hat","Respectful clothing for temple"), instructor_guide="Somchai", languages="English, Thai", location_details="Doi Suthep-Pui National Park base", safety_info="Moderate fitness required. Steep 300+ steps at the end.", fitness_level="Moderate"),
    dict(activity_name="Swayambhunath Temple Tour", destination="Kathmandu", country="Nepal", description="Climb the ancient 365 steps to the Monkey Temple. Learn about Buddhist and Hindu traditions. Stunning panoramic views of the Kathmandu Valley.", duration="3 hours", price=15, difficulty="Easy", min_age=5, max_participants=20, booked_count=8, rating=4.8, review_count=28, category="Cultural", included=_list("Expert guide", "Entry fee", "Water"), excluded=_list("Transport","Tips"), highlights=_list("365 ancient steps","Monkey encounters","Buddhist & Hindu history","Valley panorama"), schedule="Daily, 9:00 AM", available_dates=_list("2026-09-01","2026-10-01","2026-10-15","2026-11-01"), cancellation_policy="Free cancellation up to 24 hours before.", is_active=True, what_to_bring=_list("Comfortable shoes","Camera","Water","Respectful clothing"), instructor_guide="Dawa Sherpa", languages="English, Nepali", location_details="Swayambhunath, Kathmandu", safety_info="Watch for monkeys — don't show food openly.", fitness_level="Beginner"),
    dict(activity_name="Tiger Hill Sunrise Trip", destination="Darjeeling", country="India", description="Wake before dawn for a legendary sunrise over Kanchenjunga. The third-highest mountain glows pink and gold. An unforgettable experience.", duration="6 hours", price=20, difficulty="Easy", min_age=5, max_participants=15, booked_count=9, rating=4.9, review_count=35, category="Land", included=_list("Jeep transport", "Guide", "Hot tea"), excluded=_list("Breakfast","Tips"), highlights=_list("Kanchenjunga sunrise","Mountain panorama","Heritage jeep ride","Hot tea at summit"), schedule="Daily, 3:30 AM", available_dates=_list("2026-10-01","2026-10-15","2026-11-01","2026-11-15"), cancellation_policy="Free cancellation up to 24 hours before. Weather-dependent.", is_active=True, what_to_bring=_list("Warm jacket","Camera","Binoculars","Blanket"), instructor_guide="Anil Rai", languages="English, Hindi, Bengali", location_details="Tiger Hill, Darjeeling", safety_info="Very early start. Bring warm clothing — it's cold at dawn.", fitness_level="Beginner"),
    dict(activity_name="Tea Garden Walk & Tasting", destination="Darjeeling", country="India", description="Walk through emerald plantations, learn the tea-making process, and taste 5 varieties of fresh Darjeeling tea. A sensory journey.", duration="3 hours", price=15, difficulty="Easy", min_age=8, max_participants=20, booked_count=6, rating=4.6, review_count=14, category="Cultural", included=_list("Estate tour", "5 teas tasting", "Guide"), excluded=_list("Transport","Meals"), highlights=_list("5 tea varieties tasting","Plantation walk","Tea processing tour","Scenic views"), schedule="Daily, 10:00 AM", available_dates=_list("2026-10-01","2026-10-15","2026-11-01"), cancellation_policy="Free cancellation up to 24 hours before.", is_active=True, what_to_bring=_list("Comfortable shoes","Camera","Light jacket"), instructor_guide="Tenzing Dorji", languages="English, Hindi, Bengali", location_details="Makaibari Tea Estate, Kurseong", safety_info="Easy walk on estate paths. Some uneven ground.", fitness_level="Beginner"),
    dict(activity_name="Inani Beach Coral Walk", destination="Cox's Bazar", country="Bangladesh", description="Explore unique coral formations and tide pools at low tide. A natural aquarium experience. Best during low tide season.", duration="2 hours", price=10, difficulty="Easy", min_age=5, max_participants=20, booked_count=4, rating=4.3, review_count=7, category="Land", included=_list("Guide", "Reef shoes"), excluded=_list("Transport","Snacks"), highlights=_list("Natural coral formations","Tide pool exploration","Unique marine life","Guided nature walk"), schedule="Check tide schedule", available_dates=_list("2026-09-15","2026-10-01","2026-10-15"), cancellation_policy="Free cancellation up to 12 hours before.", is_active=True, what_to_bring=_list("Sunscreen","Hat","Water bottle","Camera"), instructor_guide="Rahim Ahmed", languages="English, Bengali", location_details="Inani Beach, Cox's Bazar", safety_info="Watch your footing on rocks. Don't remove coral.", fitness_level="Beginner"),
    dict(activity_name="Scuba Diving at Rumassala", destination="Galle", country="Sri Lanka", description="Dive into crystal-clear waters with colourful coral reefs and marine life. PADI-certified instructors. No experience needed for introductory dive.", duration="4 hours", price=80, difficulty="Intermediate", min_age=16, max_participants=6, booked_count=3, rating=4.8, review_count=20, category="Water", included=_list("Full equipment", "Boat dive", "Instructor", "Certificate"), excluded=_list("Underwater camera","Transport"), highlights=_list("PADI-certified instruction","Coral reef diving","Marine life encounters","Certificate included"), schedule="Daily, 8:00 AM", available_dates=_list("2026-09-01","2026-09-15","2026-10-01","2026-10-15"), cancellation_policy="Free cancellation up to 48 hours before.", is_active=True, what_to_bring=_list("Swimwear","Medical certificate","ID proof"), instructor_guide="Dilanka Silva", languages="English, Sinhala", location_details="Rumassala, Unawatuna, Galle", safety_info="Medical certificate required. Not for those with heart/lung conditions.", fitness_level="Intermediate"),
    dict(activity_name="Night Bazaar Food Tour", destination="Chiang Mai", country="Thailand", description="Taste your way through 20+ street food stalls with a local food expert. Pad Thai, mango sticky rice, northern sausage, and more.", duration="3 hours", price=35, difficulty="Easy", min_age=12, max_participants=10, booked_count=6, rating=4.9, review_count=38, category="Cultural", included=_list("10 tastings", "Guide", "Water"), excluded=_list("Drinks","Transport"), highlights=_list("20+ food stalls","Local food expert","10 included tastings","Cultural stories"), schedule="Sat & Sun, 5:00 PM", available_dates=_list("2026-09-20","2026-09-27","2026-10-04","2026-10-11"), cancellation_policy="Free cancellation up to 24 hours before.", is_active=True, what_to_bring=_list("Empty stomach","Camera","Cash for extras"), instructor_guide="Nong Bai", languages="English, Thai", location_details="Starts at Tha Phae Gate, Chiang Mai Old City", safety_info="Allergies: please inform us. Vegetarian options available.", fitness_level="Beginner"),
]


RESTAURANTS = [
    dict(
        restaurant_name="Ocean Breeze Restaurant", destination="Cox's Bazar", country="Bangladesh", cuisine="Seafood",
        description="Beachfront seafood restaurant with stunning ocean views. Fresh catch of the day, grilled to perfection.",
        price_range="$$", rating=4.4, address="Kolatoli Road, Cox's Bazar",
        opening_hours="11:00 AM – 11:00 PM",
        popular_dishes=_list("Grilled Pomfret", "Seafood Platter", "Prawn Curry"),
        vegetarian_options=False, outdoor_seating=True, delivery_available=False,
        latitude=21.4270, longitude=92.0059,
        image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="The Fort Kitchen", destination="Galle", country="Sri Lanka", cuisine="Sri Lankan & Western",
        description="Fusion restaurant inside Galle Fort. Traditional recipes with modern presentation.",
        price_range="$$$", rating=4.7, address="33 Lighthouse Street, Galle Fort",
        opening_hours="12:00 PM – 10:00 PM",
        popular_dishes=_list("Lamb Curry", "Coconut Sambol", "Jaffna Crab Curry"),
        vegetarian_options=True, outdoor_seating=True, delivery_available=False,
        latitude=6.0264, longitude=80.2170,
        image="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="Himalayan Kitchen", destination="Kathmandu", country="Nepal", cuisine="Nepali & Tibetan",
        description="Authentic Nepali cuisine in a traditional Newari courtyard. Famous for momos and thali sets.",
        price_range="$", rating=4.6, address="Thamel, Kathmandu",
        opening_hours="8:00 AM – 10:00 PM",
        popular_dishes=_list("Momos", "Dal Bhat", "Thukpa"),
        vegetarian_options=True, outdoor_seating=False, delivery_available=True,
        latitude=27.7152, longitude=85.3126,
        image="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="Khao Soi Nimman", destination="Chiang Mai", country="Thailand", cuisine="Thai (Northern)",
        description="The best khao soi in Chiang Mai. Rich coconut curry noodles with crispy egg noodles on top.",
        price_range="$", rating=4.8, address="Nimmanhaemin Road, Chiang Mai",
        opening_hours="10:00 AM – 9:00 PM",
        popular_dishes=_list("Khao Soi", "Sai Oua", "Som Tum"),
        vegetarian_options=True, outdoor_seating=True, delivery_available=True,
        latitude=18.7953, longitude=98.9687,
        image="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="Darjeeling Tea Lounge", destination="Darjeeling", country="India", cuisine="Indian & Continental",
        description="Colonial-era tea lounge serving the finest Darjeeling tea alongside English breakfast and Indian curries.",
        price_range="$$", rating=4.5, address="Mall Road, Darjeeling",
        opening_hours="7:00 AM – 9:00 PM",
        popular_dishes=_list("First Flush Tea", "Chicken Tikka", "Fish and Chips"),
        vegetarian_options=True, outdoor_seating=True, delivery_available=False,
        latitude=27.0410, longitude=88.2663,
        image="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="Sunset Grill Beach Bar", destination="Cox's Bazar", country="Bangladesh", cuisine="BBQ & Seafood",
        description="Casual beachside grill where you pick your seafood and they cook it. Perfect sunset spot.",
        price_range="$", rating=4.3, address="Laboni Beach, Cox's Bazar",
        opening_hours="4:00 PM – 12:00 AM",
        popular_dishes=_list("Grilled Lobster", "BBQ Prawns", "Fish Tikka"),
        vegetarian_options=False, outdoor_seating=True, delivery_available=False,
        latitude=21.4434, longitude=92.0059,
        image="https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1476224203421-9ac39bcb3327?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="Spice Garden Restaurant", destination="Galle", country="Sri Lanka", cuisine="Sri Lankan",
        description="Family-run restaurant serving authentic home-style Sri Lankan food. Rice and curry is a must.",
        price_range="$", rating=4.6, address="Church Street, Galle",
        opening_hours="7:00 AM – 10:00 PM",
        popular_dishes=_list("Rice & Curry", "Hoppers", "Kottu Roti"),
        vegetarian_options=True, outdoor_seating=False, delivery_available=True,
        latitude=6.0300, longitude=80.2165,
        image="https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=85",
        ),
    ),
    dict(
        restaurant_name="Yangon Taste", destination="Kathmandu", country="Nepal", cuisine="Tibetan & Sherpa",
        description="Tibetan restaurant with mountain views. Warm hospitality and hearty food perfect for trekkers.",
        price_range="$", rating=4.4, address="Boudhanath, Kathmandu",
        opening_hours="8:00 AM – 9:00 PM",
        popular_dishes=_list("Thenthuk", "Shapale", "Butter Tea"),
        vegetarian_options=True, outdoor_seating=True, delivery_available=False,
        latitude=27.7215, longitude=85.3620,
        image="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=85",
        images=_imgs(
            "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=85",
        ),
    ),
]

FLIGHTS = [
    dict(airline="Biman Bangladesh Airlines", flight_number="BG 147", departure_city="Dhaka", arrival_city="Cox's Bazar", departure_airport="DAC", arrival_airport="CXB", departure_time="08:30", arrival_time="09:35", duration="1h 05m", stops="Direct", price_economy=75, price_business=180, price_first_class=350, total_seats=120, available_seats=120, cabin_class="Economy", baggage_allowance="20 kg"),
    dict(airline="Biman Bangladesh Airlines", flight_number="BG 148", departure_city="Cox's Bazar", arrival_city="Dhaka", departure_airport="CXB", arrival_airport="DAC", departure_time="16:00", arrival_time="17:05", duration="1h 05m", stops="Direct", price_economy=80, price_business=190, price_first_class=370, total_seats=120, available_seats=120, cabin_class="Economy", baggage_allowance="20 kg"),
    dict(airline="US-Bangla Airlines", flight_number="BS 305", departure_city="Dhaka", arrival_city="Cox's Bazar", departure_airport="DAC", arrival_airport="CXB", departure_time="10:15", arrival_time="11:20", duration="1h 05m", stops="Direct", price_economy=70, price_business=170, price_first_class=320, total_seats=150, available_seats=150, cabin_class="Economy", baggage_allowance="20 kg"),
    dict(airline="SriLankan Airlines", flight_number="UL 189", departure_city="Colombo", arrival_city="Galle", departure_airport="CMB", arrival_airport="CMB", departure_time="07:00", arrival_time="08:15", duration="1h 15m", stops="Direct (connecting bus)", price_economy=95, price_business=220, price_first_class=420, total_seats=180, available_seats=180, cabin_class="Economy", baggage_allowance="23 kg"),
    dict(airline="Thai Airways", flight_number="TG 103", departure_city="Bangkok", arrival_city="Chiang Mai", departure_airport="BKK", arrival_airport="CNX", departure_time="09:45", arrival_time="11:10", duration="1h 25m", stops="Direct", price_economy=65, price_business=200, price_first_class=380, total_seats=200, available_seats=200, cabin_class="Economy", baggage_allowance="25 kg"),
    dict(airline="Thai AirAsia", flight_number="FD 4521", departure_city="Bangkok", arrival_city="Chiang Mai", departure_airport="DMK", arrival_airport="CNX", departure_time="14:30", arrival_time="15:55", duration="1h 25m", stops="Direct", price_economy=40, price_business=None, price_first_class=None, total_seats=180, available_seats=180, cabin_class="Economy", baggage_allowance="15 kg"),
    dict(airline="Buddha Air", flight_number="U4 201", departure_city="Kathmandu", arrival_city="Pokhara", departure_airport="KTM", arrival_airport="PKR", departure_time="08:00", arrival_time="08:40", duration="25 min", stops="Direct", price_economy=110, price_business=None, price_first_class=None, total_seats=19, available_seats=19, cabin_class="Economy", baggage_allowance="20 kg"),
    dict(airline="Yeti Airlines", flight_number="YT 105", departure_city="Kathmandu", arrival_city="Pokhara", departure_airport="KTM", arrival_airport="PKR", departure_time="10:30", arrival_time="10:55", duration="25 min", stops="Direct", price_economy=105, price_business=None, price_first_class=None, total_seats=19, available_seats=19, cabin_class="Economy", baggage_allowance="20 kg"),
    dict(airline="IndiGo", flight_number="6E 735", departure_city="Kolkata", arrival_city="Bagdogra (Darjeeling)", departure_airport="CCU", arrival_airport="IXB", departure_time="11:20", arrival_time="12:10", duration="50 min", stops="Direct", price_economy=55, price_business=140, price_first_class=None, total_seats=180, available_seats=180, cabin_class="Economy", baggage_allowance="15 kg"),
    dict(airline="SpiceJet", flight_number="SG 871", departure_city="Delhi", arrival_city="Bagdogra (Darjeeling)", departure_airport="DEL", arrival_airport="IXB", departure_time="07:00", arrival_time="09:30", duration="2h 30m", stops="Direct", price_economy=85, price_business=None, price_first_class=None, total_seats=180, available_seats=180, cabin_class="Economy", baggage_allowance="15 kg"),
    dict(airline="AirAsia India", flight_number="I5 912", departure_city="Kolkata", arrival_city="Bagdogra (Darjeeling)", departure_airport="CCU", arrival_airport="IXB", departure_time="15:00", arrival_time="15:50", duration="50 min", stops="Direct", price_economy=50, price_business=None, price_first_class=None, total_seats=180, available_seats=180, cabin_class="Economy", baggage_allowance="15 kg"),
    dict(airline="Vistara", flight_number="UK 737", departure_city="Delhi", arrival_city="Bagdogra (Darjeeling)", departure_airport="DEL", arrival_airport="IXB", departure_time="13:15", arrival_time="15:25", duration="2h 10m", stops="Direct", price_economy=90, price_business=210, price_first_class=None, total_seats=164, available_seats=164, cabin_class="Economy", baggage_allowance="15 kg"),
]


PROMOTIONS = [
    dict(title="Summer Beach Escape", description="Save big on Cox's Bazar hotels this summer. Book now for unforgettable ocean views and golden sunsets.", destination="Cox's Bazar", original_price=650, discount_percent=20, final_price=520, promo_code="BEACH20", valid_until=datetime(2026, 9, 30, tzinfo=timezone.utc), image="https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=1200&q=85", badge="Hot Deal"),
    dict(title="Hill Trek Adventure", description="Exclusive discount on Bandarban trek packages. Includes eco-lodge, meals, and expert guide.", destination="Bandarban", original_price=420, discount_percent=17, final_price=350, promo_code="HILL17", valid_until=datetime(2026, 10, 31, tzinfo=timezone.utc), image="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85", badge="Limited Time"),
    dict(title="Galle Fort Heritage Special", description="Experience Sri Lanka's colonial charm at a special price. Includes boutique hotel, guided tours, and tuk-tuk adventures.", destination="Galle", original_price=450, discount_percent=15, final_price=380, promo_code="HERITAGE15", valid_until=datetime(2026, 11, 15, tzinfo=timezone.utc), image="https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=1200&q=85", badge="New"),
    dict(title="Nepal Valley Explorer", description="Discover ancient temples and vibrant culture in Kathmandu Valley. Special rate on 6-day cultural immersion.", destination="Kathmandu", original_price=520, discount_percent=19, final_price=420, promo_code="NEPAL19", valid_until=datetime(2026, 11, 30, tzinfo=timezone.utc), image="https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=85", badge="Popular"),
    dict(title="Chiang Mai Cooking & Culture", description="Learn Thai cooking, visit golden temples, and meet elephants. Book now and save 18% on this magical experience.", destination="Chiang Mai", original_price=380, discount_percent=18, final_price=310, promo_code="CHIANGMAI18", valid_until=datetime(2026, 10, 31, tzinfo=timezone.utc), image="https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1200&q=85", badge="Staff Pick"),
]

LOCAL_TRANSPORTS = [
    dict(transport_type="Bus", provider_name="Dhaka Cox's Bazar Express", route_name="Dhaka – Cox's Bazar AC Bus", departure_city="Dhaka", arrival_city="Cox's Bazar", departure_time="06:00", arrival_time="13:00", duration="7h", price_per_person=25, total_seats=40, available_seats=40, frequency="Daily (3 departures)", features="AC, WiFi, Reclining Seats, Restroom"),
    dict(transport_type="Bus", provider_name="Hanif Paribahan", route_name="Dhaka – Cox's Bazar Direct", departure_city="Dhaka", arrival_city="Cox's Bazar", departure_time="08:00", arrival_time="15:00", duration="7h", price_per_person=18, total_seats=45, available_seats=45, frequency="Every 2 hours", features="AC, Reclining Seats"),
    dict(transport_type="Bus", provider_name="Shyamoli Paribahan", route_name="Dhaka – Galle (via Hikkaduwa)", departure_city="Dhaka", arrival_city="Galle", departure_time="05:30", arrival_time="18:00", duration="12h 30m", price_per_person=45, total_seats=40, available_seats=40, frequency="Daily", features="AC, WiFi, Meals Included, Charging Ports"),
    dict(transport_type="Bus", provider_name="Green Line Paribahan", route_name="Kathmandu – Pokhara Express", departure_city="Kathmandu", arrival_city="Pokhara", departure_time="07:00", arrival_time="13:00", duration="6h", price_per_person=12, total_seats=35, available_seats=35, frequency="Every 3 hours", features="AC, WiFi, Mountain Views"),
    dict(transport_type="Bus", provider_name="Buddha Air Bus", route_name="Kathmandu – Chitwan Jungle Express", departure_city="Kathmandu", arrival_city="Chitwan", departure_time="08:00", arrival_time="13:30", duration="5h 30m", price_per_person=10, total_seats=40, available_seats=40, frequency="Daily", features="AC, Comfortable Seats"),
    dict(transport_type="Bus", provider_name="BRTC", route_name="Kolkata – Darjeeling Hill Bus", departure_city="Kolkata", arrival_city="Darjeeling", departure_time="05:00", arrival_time="14:00", duration="9h", price_per_person=8, total_seats=50, available_seats=50, frequency="Daily", features="Non-AC, Scenic Route"),

    dict(transport_type="Train", provider_name="Bangladesh Railway", route_name="Subarna Express – Dhaka to Chittagong", departure_city="Dhaka", arrival_city="Chittagong", departure_time="07:00", arrival_time="13:30", duration="6h 30m", price_per_person=15, total_seats=200, available_seats=200, frequency="Daily", features="AC Chair, Snack Bar, Charging Ports"),
    dict(transport_type="Train", provider_name="Bangladesh Railway", route_name="Mahanagar Express – Dhaka to Sylhet", departure_city="Dhaka", arrival_city="Sylhet", departure_time="21:30", arrival_time="05:30", duration="8h", price_per_person=12, total_seats=180, available_seats=180, frequency="Daily", features="Sleeper Class, AC Cabin, Dining Car"),
    dict(transport_type="Train", provider_name="Sri Lanka Railways", route_name="Colombo – Galle Coastal Line", departure_city="Colombo", arrival_city="Galle", departure_time="06:30", arrival_time="10:00", duration="3h 30m", price_per_person=5, total_seats=250, available_seats=250, frequency="6 daily departures", features="Scenic Coastal Views, Air-conditioned available"),
    dict(transport_type="Train", provider_name="Nepal Railways", route_name="Jaynagar – Janakpur Shuttle", departure_city="Jaynagar (India)", arrival_city="Janakpur (Nepal)", departure_time="08:00", arrival_time="11:00", duration="3h", price_per_person=3, total_seats=300, available_seats=300, frequency="Daily", features="Basic Seating"),
    dict(transport_type="Train", provider_name="Indian Railways", route_name="Kolkata – New Jalpaiguri (Darjeeling)", departure_city="Kolkata", arrival_city="New Jalpaiguri", departure_time="22:00", arrival_time="08:00", duration="10h", price_per_person=10, total_seats=300, available_seats=300, frequency="Daily", features="Sleeper, AC 2-Tier, Pantry Car"),

    dict(transport_type="Taxi", provider_name="ComfyGo Taxi", route_name="Cox's Bazar Airport Transfer", departure_city="Cox's Bazar", arrival_city="Cox's Bazar", departure_time="Any time", arrival_time="Any time", duration="20 min", price_per_person=8, total_seats=4, available_seats=4, frequency="24/7", features="AC, GPS Tracked, Air-conditioned"),
    dict(transport_type="Taxi", provider_name="PickMe", route_name="Galle City Tour", departure_city="Galle", arrival_city="Galle", departure_time="Any time", arrival_time="Any time", duration="3 hours", price_per_person=20, total_seats=4, available_seats=4, frequency="24/7", features="AC, English-speaking driver, City tour route"),
    dict(transport_type="Taxi", provider_name="Pathao", route_name="Kathmandu Airport to Thamel", departure_city="Kathmandu Airport", arrival_city="Thamel", departure_time="Any time", arrival_time="Any time", duration="30 min", price_per_person=6, total_seats=4, available_seats=4, frequency="24/7", features="AC, Metered Fare"),
    dict(transport_type="Taxi", provider_name="Chiang Mai Taxi Service", route_name="Airport to Old City Transfer", departure_city="Chiang Mai Airport", arrival_city="Old City", departure_time="Any time", arrival_time="Any time", duration="15 min", price_per_person=5, total_seats=4, available_seats=4, frequency="24/7", features="AC, Meet & Greet service"),
    dict(transport_type="Taxi", provider_name="Darjeeling Cabs", route_name="Bagdogra Airport to Darjeeling Hill", departure_city="Bagdogra", arrival_city="Darjeeling", departure_time="Any time", arrival_time="Any time", duration="3h", price_per_person=22, total_seats=4, available_seats=4, frequency="24/7", features="AC, Mountain road experienced drivers"),

    dict(transport_type="Car Rental", provider_name="Hertz Sri Lanka", route_name="Galle – Self-Drive Coastal Tour", departure_city="Galle", arrival_city="Galle", departure_time="Pick-up", arrival_time="Drop-off", duration="Full day", price_per_person=35, total_seats=5, available_seats=5, frequency="Daily rental", features="AC, GPS, Insurance included, Unlimited KM"),
    dict(transport_type="Car Rental", provider_name="Avis Bangladesh", route_name="Dhaka – Cox's Bazar Road Trip", departure_city="Dhaka", arrival_city="Cox's Bazar", departure_time="Pick-up", arrival_time="Drop-off", duration="Full day", price_per_person=40, total_seats=5, available_seats=5, frequency="Daily rental", features="AC, GPS, 24/7 Support, Insurance"),
    dict(transport_type="Car Rental", provider_name="Budget Car Rental Nepal", route_name="Kathmandu Valley – Nagarkot Excursion", departure_city="Kathmandu", arrival_city="Nagarkot", departure_time="Pick-up", arrival_time="Drop-off", duration="Full day", price_per_person=30, total_seats=5, available_seats=5, frequency="Daily rental", features="AC, GPS, Experienced mountain drivers"),
    dict(transport_type="Car Rental", provider_name="Thai Rent a Car", route_name="Chiang Mai – Doi Inthanon Day Trip", departure_city="Chiang Mai", arrival_city="Doi Inthanon", departure_time="Pick-up", arrival_time="Drop-off", duration="Full day", price_per_person=25, total_seats=5, available_seats=5, frequency="Daily rental", features="AC, GPS, Insurance, Unlimited mileage"),
    dict(transport_type="Car Rental", provider_name="Zoomcar India", route_name="Kolkata – Darjeeling Road Trip Package", departure_city="Kolkata", arrival_city="Darjeeling", departure_time="Pick-up", arrival_time="Drop-off", duration="Full day", price_per_person=30, total_seats=5, available_seats=5, frequency="Daily rental", features="AC, GPS, Hill driving insurance, 24/7 support"),
]


def seed_extended(force: bool = False):
    session = Database.session_factory()()
    try:
        existing = session.query(Room).count()
        if existing and not force:
            print(f"  ℹ  Extended tables already seeded ({existing} rooms). Use --force to re-seed.")
            return

        if force:
            print("  [WARN]  --force: clearing extended data...")
            session.query(ActivityBooking).delete(synchronize_session=False)
            session.query(PackageBooking).delete(synchronize_session=False)
            session.query(Review).delete(synchronize_session=False)
            session.query(Room).delete(synchronize_session=False)
            session.query(TourPackage).delete(synchronize_session=False)
            session.query(Activity).delete(synchronize_session=False)
            session.query(Restaurant).delete(synchronize_session=False)
            session.query(Flight).delete(synchronize_session=False)
            session.query(LocalTransport).delete(synchronize_session=False)
            session.query(Promotion).delete(synchronize_session=False)
            session.commit()

        print("\nSeeding extended ComfyGo data...\n")

        hotel_ids = [h.hotel_id for h in session.query(Hotel.hotel_id).all()]
        customer_ids = [c.customer_id for c in session.query(Customer.customer_id).all()]

        rooms_data = _gen_rooms(hotel_ids)
        for r in rooms_data:
            session.add(Room(**r))
        print(f"  [OK] Rooms -- {len(rooms_data)} created")

        package_objs = []
        for p in PACKAGES:
            obj = TourPackage(**p)
            session.add(obj)
            session.flush()
            package_objs.append(obj)
        package_ids = [p.package_id for p in package_objs]
        print(f"  [OK] Tour Packages -- {len(package_objs)} created")

        for a in ACTIVITIES:
            session.add(Activity(**a))
        print(f"  [OK] Activities -- {len(ACTIVITIES)} created")

        restaurant_objs = []
        for r in RESTAURANTS:
            obj = Restaurant(**r)
            session.add(obj)
            session.flush()
            restaurant_objs.append(obj)
        restaurant_ids = [r.restaurant_id for r in restaurant_objs]
        print(f"  [OK] Restaurants -- {len(restaurant_objs)} created")

        for f in FLIGHTS:
            session.add(Flight(**f))
        print(f"  [OK] Flights -- {len(FLIGHTS)} created")

        for p in PROMOTIONS:
            session.add(Promotion(**p))
        print(f"  [OK] Promotions -- {len(PROMOTIONS)} created")

        for t in LOCAL_TRANSPORTS:
            session.add(LocalTransport(**t))
        print(f"  [OK] Local Transport -- {len(LOCAL_TRANSPORTS)} created")

        reviews_data = _gen_reviews(hotel_ids, customer_ids, [], package_ids, restaurant_ids=restaurant_ids)
        for r in reviews_data:
            session.add(Review(**r))
        print(f"  [OK] Reviews -- {len(reviews_data)} created")

        session.commit()
        print("\n[DONE] Extended data seeded successfully!\n")

    except Exception as exc:
        session.rollback()
        print(f"\n[FAIL] Extended seed failed: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    force_flag = "--force" in sys.argv
    seed_extended(force=force_flag)
