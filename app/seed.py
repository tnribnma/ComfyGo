import sys
from datetime import date, datetime, timezone, timedelta
from random import choice, randint, uniform

from .database import Database, get_db
from .models import (
    Admin, Employee, Hotel, Customer, Guide,
    Booking, BookingStatus, Payment, PaymentMethod, PaymentStatus,
    TouristSpot,
)
from .core.security import get_password_hash

def _pw(plain: str) -> str:
    return get_password_hash(plain)

ADMIN = dict(
    admin_name="Rafiq Hassan",
    admin_email="admin@comfygo.com",
    admin_phone="+880 1712-345678",
    admin_password=_pw("Admin123"),
)

HOTELS = [
    dict(
        hotel_name="The Ceylon House",
        hotel_address="32 Lighthouse Street, Fort Galle",
        hotel_city="Galle",
        hotel_country="Sri Lanka",
        hotel_phone="+94 91 223 4567",
        hotel_email="info@ceylonhouse.lk",
        hotel_description="A serene colonial retreat steps from the sea. This beautifully restored Dutch-era townhouse offers four airy suites overlooking the historic ramparts. Expect handloom linens, locally roasted coffee, and evenings on the rooftop terrace watching the sun melt into the Indian Ocean.",
        hotel_rating=4.9,
    ),
    dict(
        hotel_name="Fort Breeze Boutique",
        hotel_address="18 Church Street, Fort Galle",
        hotel_city="Galle",
        hotel_country="Sri Lanka",
        hotel_phone="+94 91 223 8901",
        hotel_email="stay@fortbreeze.lk",
        hotel_description="Tucked inside Galle Fort's winding lanes, this intimate five-room boutique blends whitewashed walls with antique Sri Lankan furniture. A plunge pool, open-air courtyard dining and a rooftop hammock make it hard to leave.",
        hotel_rating=4.7,
    ),

    dict(
        hotel_name="Coastline Villa",
        hotel_address="42 Marine Drive Road, Cox's Bazar",
        hotel_city="Cox's Bazar",
        hotel_country="Bangladesh",
        hotel_phone="+880 341 64567",
        hotel_email="info@coastlinevilla.com",
        hotel_description="Easy days and endless ocean at your doorstep. Perched on a gentle rise above Inani Beach, Coastline Villa offers infinity-pool views, a seafood grill restaurant and sunset yoga on the terrace. The world's longest natural sandy beach is yours to explore.",
        hotel_rating=4.7,
    ),
    dict(
        hotel_name="Tidal Inn",
        hotel_address="15 Kolatoli Road, Cox's Bazar",
        hotel_city="Cox's Bazar",
        hotel_country="Bangladesh",
        hotel_phone="+880 341 78901",
        hotel_email="reservations@tidalinn.com",
        hotel_description="A laid-back beachside inn where the sound of waves is your alarm clock. Clean rooms, a casual open-air restaurant and direct beach access make Tidal Inn a favourite with backpackers and families alike.",
        hotel_rating=4.3,
    ),
    dict(
        hotel_name="Golden Shore Resort",
        hotel_address="8 Hotel Motel Zone, Cox's Bazar",
        hotel_city="Cox's Bazar",
        hotel_country="Bangladesh",
        hotel_phone="+880 341 56789",
        hotel_email="stay@goldenshore.com.bd",
        hotel_description="A family-friendly resort in the heart of the motel zone with indoor pool, kids' playground and a beachfront seafood buffet. The sunset cruise excursion is included for guests staying three nights or more.",
        hotel_rating=4.5,
    ),

    dict(
        hotel_name="Sylvan Retreat",
        hotel_address="7 Nilgiri Road, Bandarban",
        hotel_city="Bandarban",
        hotel_country="Bangladesh",
        hotel_phone="+880 361 61234",
        hotel_email="hello@sylvanretreat.com",
        hotel_description="Wake up above the clouds in the hill country. This eco-lodge sits at 1,200 metres on the slopes of Nilgiri, offering bamboo cottages, guided tribal village walks and a farm-to-table restaurant using ingredients grown on-site.",
        hotel_rating=4.8,
    ),
    dict(
        hotel_name="Hilltop Haven Lodge",
        hotel_address="22 Thanchi Road, Bandarban",
        hotel_city="Bandarban",
        hotel_country="Bangladesh",
        hotel_phone="+880 361 65432",
        hotel_email="info@hilltophaven.com",
        hotel_description="Nestled among golden Buddha statues and pine-scented air, Hilltop Haven offers panoramic valley views from every room. Wake to birdsong, hike to Keokradong peak, and return for a traditional Marma dinner by firelight.",
        hotel_rating=4.6,
    ),

    dict(
        hotel_name="Himalayan Heritage Inn",
        hotel_address="26 Thamel Marg, Kathmandu",
        hotel_city="Kathmandu",
        hotel_country="Nepal",
        hotel_phone="+977 1 4423456",
        hotel_email="bookings@himalayanheritage.com.np",
        hotel_description="A restored Newari courtyard house in the heart of Thamel. Hand-carved wooden balconies, a meditation garden and rooftop views of Swayambhunath make this a soulful base for exploring the Valley of the Gods.",
        hotel_rating=4.8,
    ),
    dict(
        hotel_name="Buddha Garden Hotel",
        hotel_address="5 Durbar Square, Kathmandu",
        hotel_city="Kathmandu",
        hotel_country="Nepal",
        hotel_phone="+977 1 4256789",
        hotel_email="info@buddhagarden.com.np",
        hotel_description="Steps from the ancient royal palace, Buddha Garden Hotel wraps a serene inner courtyard around a 400-year-old Bodhi tree. Rooms feature handmade Nepali paper lampshades, and the rooftop terrace serves Newari platters with local craft beer.",
        hotel_rating=4.5,
    ),

    dict(
        hotel_name="Lanna Lotus Resort",
        hotel_address="108 Nimmanhaemin Soi 9, Chiang Mai",
        hotel_city="Chiang Mai",
        hotel_country="Thailand",
        hotel_phone="+66 53 894 321",
        hotel_email="reservations@lannalotus.com",
        hotel_description="A tranquil Lanna-style retreat hidden behind teak gates on lively Nimmanhaemin Road. An open-air pool, lotus pond and a cooking school where you can learn to prepare khao soi and green curry from local chefs.",
        hotel_rating=4.9,
    ),

    dict(
        hotel_name="Misty Peaks Homestay",
        hotel_address="31 Circular Road, Darjeeling",
        hotel_city="Darjeeling",
        hotel_country="India",
        hotel_phone="+91 354 225 4432",
        hotel_email="stay@mistypeak.in",
        hotel_description="A charming hillside homestay overlooking Kanchenjunga's snow-capped summit. Wake to the aroma of freshly brewed Darjeeling tea, spend your day on the heritage toy-train ride, and return for scones and jam by the fireplace.",
        hotel_rating=4.7,
    ),
]

EMPLOYEES_SEED = [
    dict(
        employee_name="Nimal Perera",
        employee_email="nimal@comfygo.com",
        employee_phone="+94 77 123 4567",
        employee_position="Front Desk Manager",
        employee_password=_pw("Employee1"),
    ),
    dict(
        employee_name="Fatima Begum",
        employee_email="fatima@comfygo.com",
        employee_phone="+880 1812 345678",
        employee_position="Operations Coordinator",
        employee_password=_pw("Employee1"),
    ),
]

CUSTOMERS = [
    dict(
        customer_name="Sarah Mitchell",
        customer_email="sarah@example.com",
        customer_phone="+1 415-555-0123",
        customer_address="San Francisco, CA, USA",
        customer_password=_pw("Password1"),
    ),
    dict(
        customer_name="Tanvir Ahmed",
        customer_email="tanvir@example.com",
        customer_phone="+880 1711-987654",
        customer_address="Dhaka, Bangladesh",
        customer_password=_pw("Password1"),
    ),
    dict(
        customer_name="Priya Sharma",
        customer_email="priya@example.com",
        customer_phone="+91 98765-43210",
        customer_address="Mumbai, India",
        customer_password=_pw("Password1"),
    ),
    dict(
        customer_name="James Walker",
        customer_email="james@example.com",
        customer_phone="+44 7700-900123",
        customer_address="London, United Kingdom",
        customer_password=_pw("Password1"),
    ),
    dict(
        customer_name="Mizuki Tanaka",
        customer_email="mizuki@example.com",
        customer_phone="+81 90-1234-5678",
        customer_address="Tokyo, Japan",
        customer_password=_pw("Password1"),
    ),
    dict(
        customer_name="Amina Rahman",
        customer_email="amina@example.com",
        customer_phone="+880 1912-345678",
        customer_address="Chittagong, Bangladesh",
        customer_password=_pw("Password1"),
    ),
    dict(
        customer_name="Demo Traveller",
        customer_email="customer@comfygo.com",
        customer_phone="+880 1555-000000",
        customer_address="ComfyGo Demo Address",
        customer_password=_pw("Password1"),
    ),
]

GUIDES = [
    dict(
        guide_name="Nimal Perera",
        guide_email="nimal.guide@local.com",
        guide_city="Galle",
        guide_phone="+94 77 111 2233",
        guide_language="English, Sinhala",
        guide_experience=8,
    ),
    dict(
        guide_name="Ayesha Rahman",
        guide_email="ayesha.guide@local.com",
        guide_city="Cox's Bazar",
        guide_phone="+880 1812 222 333",
        guide_language="English, Bangla",
        guide_experience=6,
    ),
    dict(
        guide_name="Farhan Islam",
        guide_email="farhan.guide@local.com",
        guide_city="Bandarban",
        guide_phone="+880 1712 444 555",
        guide_language="English, Bangla, Arabic",
        guide_experience=10,
    ),
    dict(
        guide_name="Suman Tamang",
        guide_email="suman.guide@local.com",
        guide_city="Kathmandu",
        guide_phone="+977 9841 666 777",
        guide_language="English, Nepali, Hindi",
        guide_experience=7,
    ),
    dict(
        guide_name="Rina Gurung",
        guide_email="rina.guide@local.com",
        guide_city="Kathmandu",
        guide_phone="+977 9851 888 999",
        guide_language="English, Nepali",
        guide_experience=5,
    ),
    dict(
        guide_name="Kittisak Wongsa",
        guide_email="kittisak.guide@local.com",
        guide_city="Chiang Mai",
        guide_phone="+66 89 123 4567",
        guide_language="English, Thai, Mandarin",
        guide_experience=12,
    ),
    dict(
        guide_name="Bikash Rai",
        guide_email="bikash.guide@local.com",
        guide_city="Darjeeling",
        guide_phone="+91 98321 00011",
        guide_language="English, Hindi, Nepali",
        guide_experience=9,
    ),
    dict(
        guide_name="Dilani Fernando",
        guide_email="dilani.guide@local.com",
        guide_city="Galle",
        guide_phone="+94 71 333 4455",
        guide_language="English, Sinhala, Tamil",
        guide_experience=4,
    ),
]

import json as _json

def _img(url):
    return url

def _imgs(*urls):
    return _json.dumps(list(urls))

def _list(*items):
    return _json.dumps(list(items))

def _nearby(*items):
    return _json.dumps([{"name": n, "distance": d} for n, d in items])

TOURIST_SPOTS = [
    dict(
        spot_name="Galle Fort",
        spot_city="Galle",
        spot_country="Sri Lanka",
        spot_description="A UNESCO World Heritage Site — a 16th-century Dutch colonial fortress with ramparts, cobblestone streets, boutique shops and ocean views.",
        spot_detailed_description="Galle Fort is one of the best-preserved colonial fortifications in Asia. Built by the Portuguese in 1588 and later expanded by the Dutch, it stands on a rocky promontory overlooking the Indian Ocean. Walk along the massive coral and granite ramparts at sunset as local cricketers play on the parade ground. Inside, narrow cobblestone lanes wind past converted Dutch-era buildings now home to art galleries, boutique hotels, jewellery shops selling sapphires, and laid-back cafés. The lighthouse, the oldest in Sri Lanka, stands sentinel at the southeastern corner. Every full moon, the fort comes alive with the lantern-lit Esala Perahera festival. Don't miss the Maritime Archaeology Museum housed in the old Dutch Hospital — one of the oldest buildings in the fort.",
        spot_hero_image="https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Historical",
        spot_rating=5,
        spot_best_time="November to April (dry season). The fort is magical year-round, but peak season runs December–March with clear skies and calm seas.",
        spot_duration="Half day to full day. Allow 3–4 hours to explore the ramparts and inner streets.",
        spot_budget_daily="$40–80 per day including meals, entry and a tuk-tuk ride.",
        spot_currency="Sri Lankan Rupee (LKR). 1 USD ≈ 320 LKR.",
        spot_language="Sinhala and Tamil. English widely spoken in the fort area.",
        spot_timezone="UTC+5:30 (IST).",
        spot_weather="Tropical. Hot and humid year-round (25–32°C). Monsoon rains May–September from the southwest.",
        spot_latitude=6.0271,
        spot_longitude=80.2176,
        spot_attractions=_list("Galle Lighthouse", "Dutch Reformed Church", "Maritime Museum", "Rampart sunset walk", "Old Gate", "Meeran Jumma Masjid", "National Maritime Museum", "Historical Mansion Museum"),
        spot_activities=_list("Rampart walking tour", "Cobblestone café hopping", "Sapphire & gem shopping", "Photography workshop", "Cricket watching on the parade ground", "Whale watching from nearby Mirissa", "Surfing at Unawatuna"),
        spot_nearby=_nearby(("Unawatuna Beach", "5 km"), ("Jungle Beach", "12 km"), ("Mirissa", "45 km"), ("Hikkaduwa", "18 km")),
        spot_travel_tips="Wear comfortable walking shoes — the cobblestones are uneven. Visit the ramparts at sunset for the best photos. Many shops close on Poya days (full moon holidays).", 
        spot_safety_info="Generally very safe. Watch for pickpockets in crowded market streets. Watch your step on the ramparts — they can be slippery after rain.",
        spot_transport_info="Tuk-tuks are the most convenient way to get around. Galle is 2.5 hours south of Colombo by train — the coastal railway is one of the most scenic in Asia. Rent a bicycle to explore at a relaxed pace.",
    ),
    dict(
        spot_name="Unawatuna Beach",
        spot_city="Galle",
        spot_country="Sri Lanka",
        spot_description="One of the best beaches in Sri Lanka — a crescent of golden sand framed by palm trees and coral reefs, ideal for swimming and snorkelling.",
        spot_detailed_description="Unawatuna is Sri Lanka's most famous beach, a perfect crescent of golden sand protected by a natural coral reef that creates a calm, warm lagoon ideal for swimming. Palm-fringed and backed by colourful guesthouses, seafood restaurants and beach bars, it has a laid-back tropical vibe that makes it easy to linger for days. The reef is alive with parrotfish, angelfish and sea urchins — bring a mask and snorkel. At the northern end, a small Buddha statue perched on the rocks watches over the bay. The nearby Japanese Peace Pagoda on Rumassala hill offers panoramic views and a meditative atmosphere. Just offshore, Rumassala's underwater rocks are among the best snorkelling sites on the southern coast.",
        spot_hero_image="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Beach",
        spot_rating=5,
        spot_best_time="November to April. December–February is peak season with calm seas and the best snorkelling visibility.",
        spot_duration="Full day. Many visitors stay 2–3 days to enjoy the beach at a relaxed pace.",
        spot_budget_daily="$25–60 per day. Beachside rooms from $20/night, seafood meals $5–10.",
        spot_currency="Sri Lankan Rupee (LKR).",
        spot_language="Sinhala, Tamil, English.",
        spot_timezone="UTC+5:30.",
        spot_weather="Tropical beach climate. 27–32°C year-round. Gentle ocean breeze keeps it pleasant.",
        spot_latitude=6.0172,
        spot_longitude=80.2463,
        spot_attractions=_list("Unawatuna Beach", "Japanese Peace Pagoda", "Rumassala Rock Pool", "Rumassala diving site", "Dalawella Beach (rope swing)", "Singing Fish of Koggala"),
        spot_activities=_list("Swimming in the lagoon", "Snorkelling the coral reef", "Scuba diving at Rumassala", "Beach yoga", "Seafood dining on the sand", "Kayaking", "Paddleboarding"),
        spot_nearby=_nearby(("Galle Fort", "5 km"), ("Jungle Beach", "3 km"), ("Talpe Beach", "2 km"), ("Koggala Lake", "8 km")),
        spot_travel_tips="Arrive early to get a good spot near the water. The northern end is quieter. Bring reef shoes — sea urchins are common. Many guesthouses rent snorkel gear.",
        spot_safety_info="Swim only in the lagoon — the outer reef can have strong currents. Reef shoes protect from urchins. Reef fish are not dangerous.",
        spot_transport_info="Tuk-tuk from Galle Fort costs about 300 LKR ($1). Local buses run frequently. If driving, park near the temple and walk down.",
    ),
    dict(
        spot_name="Jungle Beach",
        spot_city="Galle",
        spot_country="Sri Lanka",
        spot_description="A hidden cove accessible by a short jungle trek — crystal-clear water, quiet atmosphere, and excellent snorkelling among tropical fish.",
        spot_detailed_description="True to its name, Jungle Beach is a secluded cove hidden behind a lush coastal forest, reached by a 15-minute trek through dense tropical vegetation. Unlike busier beaches in the area, it remains relatively untouched — a local secret that rewards the adventurous. The small bay has clear turquoise water, a rocky shoreline perfect for snorkelling, and the shade of towering trees for a midday rest. Underwater, you'll find colourful coral formations, sea cucumbers, and schools of tropical fish. The trek itself is part of the adventure — you'll pass through a spice garden, spot monitor lizards, and emerge onto a deserted beach. For the best experience, bring your own snorkelling gear and snacks — there are only a couple of small stalls.",
        spot_hero_image="https://images.unsplash.com/photo-1468413253725-0d5181091126?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1468413253725-0d5181091126?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Nature",
        spot_rating=4,
        spot_best_time="November to April. Early morning or late afternoon avoids the midday heat.",
        spot_duration="Half day. 15-minute trek each way, plus 2–3 hours at the beach.",
        spot_budget_daily="$20–40. Tuk-tuk from Unawatuna is about $5. Bring your own food.",
        spot_currency="Sri Lankan Rupee (LKR).",
        spot_language="Sinhala, English.",
        spot_timezone="UTC+5:30.",
        spot_weather="Same as Unawatuna — warm and humid. The jungle trail provides shade.",
        spot_latitude=5.9897,
        spot_longitude=80.2320,
        spot_attractions=_list("Hidden cove", "Snorkelling reef", "Jungle trek trail", "Rocky beach", "Spice garden en route"),
        spot_activities=_list("Jungle trekking", "Snorkelling", "Rock jumping", "Bird watching", "Photography", "Meditation by the sea"),
        spot_nearby=_nearby(("Unawatuna Beach", "3 km"), ("Galle Fort", "10 km"), ("Talpe Beach", "2 km")),
        spot_travel_tips="Wear sturdy shoes for the jungle trail — it can be muddy after rain. Bring water, sunscreen, and snacks. Best visited in the morning when the beach is empty.",
        spot_safety_info="The trail is not maintained — be careful on steep sections. No lifeguards at the beach. Strong currents possible outside the cove.",
        spot_transport_info="Tuk-tuk from Unawatuna (about 500 LKR) to the trailhead. From the trailhead, a 15-minute walk through the forest.",
    ),

    dict(
        spot_name="Cox's Bazar Beach",
        spot_city="Cox's Bazar",
        spot_country="Bangladesh",
        spot_description="The world's longest natural sandy beach — 120 km of golden shoreline along the Bay of Bengal, perfect for sunrise walks and seafood.",
        spot_detailed_description="Cox's Bazar is officially the world's longest uninterrupted natural sandy beach, stretching an astonishing 120 km along the Bay of Bengal in southeastern Bangladesh. The golden-brown sand, backed by a continuous row of coconut palms and casuarina trees, creates a breathtaking coastal panorama. At sunrise, the entire beach glows amber and rose as fishermen cast their nets in the shallow surf. The beach is divided into several zones — Kolatoli and Sugandha are the main tourist strips with hotels, restaurants and shops, while more remote sections towards Himchari and Inani offer solitude. The beach is alive with activity: horse-drawn carriages at sunset, local cricket games, seafood stalls grilling fresh catch, and children flying kites. The Laboni Beach area is the most developed, while Humchari and Nakkhali offer quieter stretches.",
        spot_hero_image="https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Beach",
        spot_rating=5,
        spot_best_time="November to March. October–February has pleasant weather with cool breezes. Avoid April–May when temperatures soar above 35°C.",
        spot_duration="2–3 days minimum. You can walk the beach for hours and still not cover half of it.",
        spot_budget_daily="$15–40. Beachside hotels from $10/night. Street seafood $2–5 per meal.",
        spot_currency="Bangladeshi Taka (BDT). 1 USD ≈ 110 BDT.",
        spot_language="Bangla (Bengali). English understood in tourist areas.",
        spot_timezone="UTC+6 (BST).",
        spot_weather="Tropical. Hot and humid year-round. 25–35°C. Monsoon rains June–September.",
        spot_latitude=21.4272,
        spot_longitude=92.0062,
        spot_attractions=_list("Laboni Beach Point", "Himchari National Park", "Inani Beach", "Charippa Sea Beach", "Mermaid Beach", "Cox's Bazar Marine Aquarium", "Bay of Bengal sunset"),
        spot_activities=_list("Sunrise beach walk", "Horse riding", "Beach cricket", "Paragliding", "Jet skiing", "Seafood tasting", "Kite flying", "Photography"),
        spot_nearby=_nearby(("Inani Beach", "18 km"), ("Himchari National Park", "12 km"), ("Saint Martin Island", "60 km"), ("Chittagong", "150 km")),
        spot_travel_tips="Visit at sunrise for the most magical experience — the entire beach glows gold. Try the local dried fish (shutki) from the market. Negotiate horse ride prices beforehand.",
        spot_safety_info="The beach can be slippery when wet. Be cautious of tides — they rise quickly. Keep valuables in your hotel. The sea can be rough during monsoon season.",
        spot_transport_info="Direct buses from Dhaka (8–10 hours) or fly to Cox's Bazar airport. Within town, rickshaws and auto-rickshaws are the main transport. Rent a motorbike to explore the coast.",
    ),
    dict(
        spot_name="Inani Beach",
        spot_city="Cox's Bazar",
        spot_country="Bangladesh",
        spot_description="A quieter stretch south of Cox's Bazar — coral stones, clear water, and fewer crowds. Great for a peaceful day by the sea.",
        spot_detailed_description="Inani Beach is a serene escape from the bustle of central Cox's Bazar, located about 18 km south along the coastal road. Unlike the main beach, Inani is known for its unique coral formations scattered along the shoreline — smooth stones and fossilised coral create a dramatic, almost lunar landscape at low tide. The water here is cleaner and calmer, making it ideal for swimming. The beach is backed by a dense forest of casuarina and coconut trees, providing natural shade for picnics. During low tide, tide pools form among the coral rocks, home to small crabs, sea cucumbers and hermit crabs — a natural aquarium for curious explorers. There are fewer facilities here than in central Cox's Bazar, which is exactly the charm. A handful of small restaurants serve fresh grilled fish. Inani is also the starting point for boat trips to Saint Martin Island.",
        spot_hero_image="https://images.unsplash.com/photo-1471922694874-5a06df4803e4?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1471922694874-5a06df4803e4?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Beach",
        spot_rating=4,
        spot_best_time="November to March for calm seas and low tide exploration. Visit during low tide for the best coral viewing.",
        spot_duration="Half day to full day. Great as a day trip from Cox's Bazar.",
        spot_budget_daily="$10–25. Tuk-tuk from Cox's Bazar about $3–5. Bring your own snacks.",
        spot_currency="Bangladeshi Taka (BDT).",
        spot_language="Bangla. Limited English.",
        spot_timezone="UTC+6.",
        spot_weather="Tropical coastal. 24–32°C. Sea breezes keep it comfortable.",
        spot_latitude=21.2333,
        spot_longitude=92.0167,
        spot_attractions=_list("Coral formations", "Tide pools", "Saint Martin Island", "Himchari viewpoint"),
        spot_activities=_list("Tide pool exploration", "Coral rock photography", "Swimming", "Picnicking under casuarinas", "Boat trip to Saint Martin"),
        spot_nearby=_nearby(("Cox's Bazar Beach", "18 km"), ("Saint Martin Island", "45 km by boat"), ("Himchari National Park", "8 km")),
        spot_travel_tips="Check tide tables before visiting — the coral is only visible at low tide. Bring reef shoes to protect your feet from sharp coral. There are limited food options, so pack snacks.",
        spot_safety_info="Sharp coral can cut bare feet — always wear reef shoes. No lifeguards on duty. Avoid swimming at high tide when currents are stronger.",
        spot_transport_info="Auto-rickshaw from Cox's Bazar takes about 45 minutes. No public buses, so arrange transport in advance. Boats to Saint Martin leave from the jetty nearby.",
    ),
    dict(
        spot_name="Himchari National Park",
        spot_city="Cox's Bazar",
        spot_country="Bangladesh",
        spot_description="Lush tropical forest with waterfalls cascading into the ocean — hiking trails, biodiversity, and panoramic coastal views.",
        spot_detailed_description="Himchari National Park is a 17,940-hectare protected area where the Chittagong Hill Tracts meet the Bay of Bengal — a rare convergence of tropical forest and ocean. The park features dramatic waterfalls (especially spectacular during monsoon), dense evergreen and semi-evergreen forests, and a stunning coastal cliff walkway with panoramic views of the Bay. The park is home to elephants, leopards, wild boar, jungle fowl, and over 200 bird species. The main waterfall cascades from a height of 30 metres into a rocky pool surrounded by lush vegetation. A network of trails leads through the forest to secluded beaches and cliff-top viewpoints. The park also protects one of the last remaining stretches of tropical lowland rainforest in Bangladesh.",
        spot_hero_image="https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Nature",
        spot_rating=4,
        spot_best_time="October to March (dry season). Monsoon season (June–September) brings spectacular waterfalls but muddy trails.",
        spot_duration="Full day. Plan for 3–4 hours of hiking plus travel time.",
        spot_budget_daily="$15–35. Entry fee is minimal. Bring your own food.",
        spot_currency="Bangladeshi Taka (BDT).",
        spot_language="Bangla. Very limited English.",
        spot_timezone="UTC+6.",
        spot_weather="Humid subtropical. 22–30°C in the hills. Cooler than Cox's Bazar due to elevation.",
        spot_latitude=21.2750,
        spot_longitude=92.0250,
        spot_attractions=_list("Himchari Waterfall", "Coastal cliff viewpoint", "Dense forest trails", "Bird watching hides", "Coastal rock formations"),
        spot_activities=_list("Hiking", "Waterfall swimming", "Bird watching", "Nature photography", "Elephant spotting", "Forest camping"),
        spot_nearby=_nearby(("Inani Beach", "8 km"), ("Cox's Bazar Beach", "12 km"), ("Saint Martin Island", "55 km")),
        spot_travel_tips="Hire a local guide — trails are not well marked. Wear sturdy hiking boots and bring insect repellent. Start early to avoid afternoon heat and catch wildlife at dawn.",
        spot_safety_info="Leeches are common during monsoon. Wear long sleeves and apply insect repellent. Do not approach wild elephants. Carry sufficient water.",
        spot_transport_info="Arrange a jeep or auto-rickshaw from Cox's Bazar (about 45 min). Entry permits are available at the park gate. No public transport to the park.",
    ),

    dict(
        spot_name="Nilgiri Hills",
        spot_city="Bandarban",
        spot_country="Bangladesh",
        spot_description="The highest peak in Bangladesh — misty mountain vistas, tribal villages, bamboo forests, and stunning sunrise views from 1,000+ metres.",
        spot_detailed_description="Nilgiri Hills, standing at 1,052 metres, is the second-highest peak in Bangladesh and offers the most accessible mountain experience in the Chittagong Hill Tracts. The road up winds through dense bamboo forests, past terraced rice paddies and Marma tribal villages, emerging onto a grassy plateau with 360-degree views of mist-shrouded valleys. At sunrise, the sky erupts in shades of pink and gold as distant peaks emerge from a sea of clouds. The hill is home to several Marma villages — the Marma people are ethnically related to the Burmese and maintain traditional wooden stilt houses, distinct Buddhist customs and vibrant festivals. On a clear day, you can see into Myanmar. The air is cool and crisp — a stark contrast to the sweltering lowlands. Simple guesthouses and eco-lodges offer basic but clean accommodation. The night sky here, far from city lights, reveals a dense canopy of stars.",
        spot_hero_image="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Mountain",
        spot_rating=5,
        spot_best_time="October to March (dry season). December–February for the clearest sunrise views and starry nights.",
        spot_duration="2–3 days. Allow a full day for the drive up, one day for exploration, and an early morning for sunrise.",
        spot_budget_daily="$20–50. Simple guesthouses $10–15/night. Meals $3–5.",
        spot_currency="Bangladeshi Taka (BDT).",
        spot_language="Marma, Bangla. Limited English.",
        spot_timezone="UTC+6.",
        spot_weather="Cool mountain climate. 10–22°C. Foggy mornings, clear afternoons. Pack warm clothes for evenings.",
        spot_latitude=21.8250,
        spot_longitude=92.4833,
        spot_attractions=_list("Sunrise viewpoint", "Marma tribal villages", "Bamboo forest trail", "Army observation post", "Valley overlook"),
        spot_activities=_list("Sunrise watching", "Mountain trekking", "Village homestay", "Star gazing", "Photography", "Cultural exchange with Marma people"),
        spot_nearby=_nearby(("Boga Lake", "25 km"), ("Thanchi", "40 km"), ("Bandarban town", "45 km")),
        spot_travel_tips="The road is steep and winding — motion sickness tablets recommended. Bring warm layers for the evening. Sunrise is around 6 AM — be at the viewpoint by 5:30 AM. Mobile signal is weak.",
        spot_safety_info="Roads can be dangerous during monsoon. Army checkpoints are common — carry your passport. Limited medical facilities. Stick to marked trails.",
        spot_transport_info="Jeep from Bandarban town (2–3 hours, $15–20 one way). Only 4x4 vehicles can make the ascent. Arrange transport through your hotel in Bandarban.",
    ),
    dict(
        spot_name="Boga Lake",
        spot_city="Bandarban",
        spot_country="Bangladesh",
        spot_description="A mysterious natural lake at 1,200 metres — surrounded by wild hills, reflecting the sky like a mirror. Sacred to the local Tripura people.",
        spot_detailed_description="Boga Lake is one of Bangladesh's most enchanting natural wonders — a crystal-clear lake sitting at 1,200 metres in the remote hills of Bandarban. According to local legend, the lake was formed when a great fire killed a dragon, and the resulting crater filled with water. The Tripura people who live nearby consider it sacred and believe a giant snake still guards its depths. The lake's colour changes throughout the day — emerald green in the morning, deep blue at noon, and silver at sunset. Surrounded by wild hills covered in tropical forest, the reflections create a perfect mirror image that doubles the scenery. Reaching Boga Lake requires a challenging trek through indigenous villages and dense forest — there is no road, which preserves its pristine isolation. Simple bamboo huts built by the Tripura community offer overnight accommodation. The lake is best visited during dry season when the trek is passable.",
        spot_hero_image="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Nature",
        spot_rating=4,
        spot_best_time="October to March (dry season). The trek is impassable during monsoon. Early mornings offer the most magical light.",
        spot_duration="3–4 days including trek. 1 day trek each way, plus 1–2 days at the lake.",
        spot_budget_daily="$15–30. Basic bamboo hut $5–8/night. Meals $2–3.",
        spot_currency="Bangladeshi Taka (BDT).",
        spot_language="Tripura, Marma, Bangla. Very limited English.",
        spot_timezone="UTC+6.",
        spot_weather="Cool highland climate. 8–20°C. Cold nights. Fog common in mornings.",
        spot_latitude=21.7833,
        spot_longitude=92.5333,
        spot_attractions=_list("Mirror lake", "Dragon legend site", "Tripura village", "Trek through indigenous lands", "Starlit skies"),
        spot_activities=_list("Trekking", "Camping", "Photography", "Cultural immersion", "Fishing (with permission)", "Meditation by the lake"),
        spot_nearby=_nearby(("Nilgiri Hills", "25 km"), ("Bandarban town", "50 km"), ("Thanchi", "35 km")),
        spot_travel_tips="Hire a local guide — the trail is not marked. Start the trek early in the day. Bring enough food for the entire stay — there are no shops. Respect the Tripura people's sacred relationship with the lake.",
        spot_safety_info="The trek is physically demanding. River crossings can be dangerous during rain. No medical facilities nearby. Always trek with a guide. Carry a satellite phone if possible.",
        spot_transport_info="Jeep from Bandarban to Remakri (3 hours), then 4–6 hour trek through the forest. Guide and porter arrangement essential. No public transport.",
    ),
    dict(
        spot_name="Thanchi Waterfall",
        spot_city="Bandarban",
        spot_country="Bangladesh",
        spot_description="A majestic multi-tiered waterfall in the deep jungle — accessible by boat and trek, surrounded by indigenous Mro villages.",
        spot_detailed_description="Thanchi Waterfall is one of Bangladesh's most spectacular hidden treasures — a series of cascading waterfalls deep in the Chittagong Hill Tracts, accessible only by boat along the Sangu River followed by a jungle trek. The main waterfall drops 40 metres over moss-covered rocks into a pool of startlingly clear water, surrounded by ancient trees draped in ferns and orchids. The journey to Thanchi is as much the adventure as the destination — the boat ride along the Sangu River passes through towering canyon walls, past fishing villages where Mro and Tripura people live in bamboo houses. During monsoon, the falls are thunderous and powerful; during dry season, they are delicate and ethereal. The surrounding forest is home to wild elephants, hornbills, and rare orchids. The Mro people who live near the falls are known for their distinctive face tattoos and their hand-woven textiles.",
        spot_hero_image="https://images.unsplash.com/photo-1432405972618-c6b0cfba8b4b?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1432405972618-c6b0cfba8b4b?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1433086966358-54859d0ed716?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Nature",
        spot_rating=4,
        spot_best_time="October to March for safe river travel. The waterfall is most impressive during and just after monsoon (September–October).",
        spot_duration="3–4 days. Full-day boat ride, trek, and return journey.",
        spot_budget_daily="$15–30. Basic accommodation. Bring all supplies.",
        spot_currency="Bangladeshi Taka (BDT).",
        spot_language="Mro, Tripura, Bangla. English very limited.",
        spot_timezone="UTC+6.",
        spot_weather="Tropical forest climate. 20–30°C. High humidity. Rain possible any time.",
        spot_latitude=21.6500,
        spot_longitude=92.6500,
        spot_attractions=_list("Main waterfall cascade", "Sangu River canyon", "Mro tribal villages", "Wild orchid forest", "Rock pool swimming"),
        spot_activities=_list("River boat journey", "Jungle trekking", "Waterfall swimming", "Village visits", "Bird watching", "Fishing"),
        spot_nearby=_nearby(("Boga Lake", "35 km"), ("Bandarban town", "60 km"), ("Nilgiri Hills", "45 km")),
        spot_travel_tips="Book a boat from Thanchi town well in advance. Carry enough food and water for the entire journey. Respect local customs — ask before photographing villagers. A local guide is essential.",
        spot_safety_info="The river can be treacherous during monsoon. No medical facilities. Always travel with a guide. Watch for leeches on the trek. Snakes are present in the forest.",
        spot_transport_info="Jeep from Bandarban to Thanchi (3–4 hours), then motorized boat up the Sangu River (3–4 hours), followed by a 2-hour trek. Arranged through local tour operators.",
    ),

    dict(
        spot_name="Swayambhunath Stupa",
        spot_city="Kathmandu",
        spot_country="Nepal",
        spot_description="The ancient Monkey Temple — a hilltop Buddhist stupa with all-seeing eyes, panoramic valley views, and 365 steps to the top.",
        spot_detailed_description="Swayambhunath, universally known as the Monkey Temple, is one of Nepal's most sacred and ancient religious sites, perched atop a conical hill west of central Kathmandu. The complex dates back over 2,000 years and is believed to have originated from a lotus flower that bloomed in the lake that once filled the Kathmandu Valley. The main stupa features the iconic all-seeing eyes of Buddha gazing in all four directions, symbolising wisdom and compassion. A climb of 365 stone steps — shared with hundreds of mischievous monkeys — leads to the summit, where the panorama unfolds: the entire Kathmandu Valley spreads below, with the snow-capped Himalayan range forming a dramatic backdrop on clear days. The complex includes several smaller stupas, shrines, temples and a Tibetan monastery. At the base, a Hindu temple dedicated to Hariti (the goddess of smallpox) stands at the entrance. The site is a living testament to Nepal's unique blend of Buddhism and Hinduism.",
        spot_hero_image="https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Historical",
        spot_rating=5,
        spot_best_time="October to December and February to April. Clear skies offer Himalayan views. Early morning or late afternoon avoids crowds.",
        spot_duration="2–3 hours. Combine with a walking tour of old Kathmandu.",
        spot_budget_daily="$20–50 for the whole Kathmandu area. Entry fee 200 NPR ($1.50) for foreigners.",
        spot_currency="Nepalese Rupee (NPR). 1 USD ≈ 133 NPR.",
        spot_language="Nepali. English widely spoken in tourist areas.",
        spot_timezone="UTC+5:45 (Nepal Time).",
        spot_weather="Subtropical. Pleasant during dry season (10–25°C). Hazy in spring. Monsoon rains June–September.",
        spot_latitude=27.7149,
        spot_longitude=85.2906,
        spot_attractions=_list("Main stupa with Buddha eyes", "365-step stairway", "Monkey population", "Panoramic valley view", "Tibetan monastery", "Prayer wheels", "Hariti temple"),
        spot_activities=_list("Climbing the stairs", "Photography", "Sunset viewing", "Meditation", "Prayer wheel spinning", "Valley panorama viewing", "Monkey watching"),
        spot_nearby=_nearby(("Boudhanath Stupa", "3 km"), ("Thamel", "2 km"), ("Kathmandu Durbar Square", "3 km"), ("Pashupatinath Temple", "5 km")),
        spot_travel_tips="Visit at sunrise or late afternoon for the best light and fewer crowds. Watch out for monkeys — they steal sunglasses, phones and food. Wear shoes suitable for climbing stone steps. The west side offers the best sunset views.",
        spot_safety_info="Monkeys can be aggressive — do not tease them or show food. Steps can be slippery. Earthquake risk — some structures may be under restoration after the 2015 earthquake.",
        spot_transport_info="A 20-minute walk from Thamel, or take a taxi (200–300 NPR). From Boudhanath, it's a 15-minute taxi ride. No direct public bus.",
    ),
    dict(
        spot_name="Boudhanath Stupa",
        spot_city="Kathmandu",
        spot_country="Nepal",
        spot_description="One of the largest spherical stupas in the world — a spiritual hub for Tibetan Buddhists, surrounded by monasteries and prayer wheels.",
        spot_detailed_description="Boudhanath is the largest Buddhist stupa in Nepal and one of the largest in the world — a massive white dome rising 36 metres, crowned by a gilded spire with the all-seeing eyes of Buddha. It is the spiritual heart of Kathmandu's Tibetan community and one of the most mesmerising religious sites on earth. Walk clockwise around the base, spinning the prayer wheels as monks and pilgrims chant mantras. The stupa is surrounded by over 50 Tibetan monasteries, their golden roofs and colorful facades creating a vibrant spiritual enclave. Every evening at dusk, butter lamps are lit around the base, casting a warm golden glow. The rooftop cafés that ring the stupa offer arguably the best views in Kathmandu — the stupa's white dome fills the foreground while prayer flags stretch across the sky. Boudhanath was designated a UNESCO World Heritage Site in 1979 and was severely damaged in the 2015 earthquake, subsequently restored to its original glory.",
        spot_hero_image="https://images.unsplash.com/photo-1558799401-1dcba79834c0?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1558799401-1dcba79834c0?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Historical",
        spot_rating=5,
        spot_best_time="Year-round. Best at dusk when butter lamps are lit. Early morning for quiet contemplation. October–December for clear skies.",
        spot_duration="2–3 hours. Allow time to sit at a rooftop café and watch the world spin.",
        spot_budget_daily="$20–50. Entry 400 NPR ($3) for foreigners. Rooftop cafés $3–8 per meal.",
        spot_currency="Nepalese Rupee (NPR).",
        spot_language="Nepali, Tibetan. English widely spoken.",
        spot_timezone="UTC+5:45.",
        spot_weather="Subtropical valley climate. Pleasant year-round. Hazy in spring.",
        spot_latitude=27.7215,
        spot_longitude=85.3620,
        spot_attractions=_list("Main stupa dome", "Golden spire", "Prayer wheel circuit", "Tibetan monasteries", "Rooftop cafés", "Butter lamp evening", "Market streets"),
        spot_activities=_list("Kora (circumambulation)", "Prayer wheel spinning", "Rooftop café viewing", "Monastery visit", "Butter lamp lighting", "Meditation", "Tibetan thangka shopping"),
        spot_nearby=_nearby(("Swayambhunath", "3 km"), ("Thamel", "4 km"), ("Pashupatinath", "2 km")),
        spot_travel_tips="Always walk clockwise (kora) around the stupa. Visit at dusk when butter lamps are lit — it's magical. The rooftop cafés on the north side offer the best views. Buy prayer flags from local shops for good luck.",
        spot_safety_info="Pickpockets operate in crowded areas — keep valuables close. Respect religious customs — don't climb on the stupa. Photographers should ask permission before photographing monks.",
        spot_transport_info="Easily reached by taxi from Thamel (200–300 NPR). Bus route 2 from Ratna Park. Walking from Pashupatinath takes about 20 minutes.",
    ),
    dict(
        spot_name="Thamel District",
        spot_city="Kathmandu",
        spot_country="Nepal",
        spot_description="The vibrant heart of Kathmandu — narrow lanes filled with shops, cafés, live music, and the energy of travellers from around the world.",
        spot_detailed_description="Thamel is Kathmandu's beating heart — a chaotic, colourful, and utterly intoxicating neighbourhood where ancient Newari architecture meets modern traveller culture. Narrow lanes packed with shops sell everything from trekking gear and Tibetan singing bowls to hand-woven pashmina and Buddhist thangka paintings. The streets buzz 24/7 — restaurants serve cuisines from around the world, rooftop bars host live music, and cafés hum with the stories of trekkers, climbers and backpackers. It's the base camp for Himalayan adventures — every trekking agency, gear shop and guide service has a presence here. Despite its modernisation, Thamel retains its old-world charm — hidden courtyards with ancient temples, narrow alleys where motorcycles and bicycles share space with pedestrians, and the occasional cow ambling past a busy café. The acoustic energy of Thamel is legendary — you can hear Nepali folk music, Western rock, Buddhist chanting and Hindi pop all within the same block.",
        spot_hero_image="https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1558799401-1dcba79834c0?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Cultural",
        spot_rating=4,
        spot_best_time="Year-round. October–December is peak season with clear weather. Spring (March–April) is pleasant with blooming flowers.",
        spot_duration="Full day to explore. Many visitors spend several days eating, shopping and soaking in the atmosphere.",
        spot_budget_daily="$15–40. Budget guesthouses $8–15/night. Meals $2–8.",
        spot_currency="Nepalese Rupee (NPR).",
        spot_language="Nepali, English. Many shopkeepers speak Hindi and other languages.",
        spot_timezone="UTC+5:45.",
        spot_weather="Subtropical. Pleasant during dry season. Can be dusty.",
        spot_latitude=27.7150,
        spot_longitude=85.3122,
        spot_attractions=_list("Thamel Chowk", "Hidden courtyards", "Trekking gear shops", "Live music venues", "Art galleries", "Singing bowl shops", "Traditional medicine shops"),
        spot_activities=_list("Shopping for handicrafts", "Café hopping", "Live music nights", "Trekking preparation", "Cooking class", "Thangka painting workshop", "Nightlife"),
        spot_nearby=_nearby(("Kathmandu Durbar Square", "1 km"), ("Swayambhunath", "2 km"), ("Boudhanath", "4 km")),
        spot_travel_tips="Negotiate prices at shops — bargaining is expected. Walk to explore — the streets are too narrow for cars. Visit small courtyards off the main streets for hidden temples. ATMs are plentiful.",
        spot_safety_info="Pickpockets operate in crowded areas. Traffic is chaotic — watch for motorcycles. Touts can be persistent — a firm 'no thanks' works. Avoid unlicensed money changers.",
        spot_transport_info="Thamel is walkable from most central Kathmandu locations. Auto-rickshaws and taxis are available. No public buses enter Thamel. Walking is the best way to explore.",
    ),

    dict(
        spot_name="Doi Suthep Temple",
        spot_city="Chiang Mai",
        spot_country="Thailand",
        spot_description="A golden Buddhist temple perched on a mountain — 306 steps flanked by naga statues, offering sweeping views over Chiang Mai.",
        spot_detailed_description="Wat Phra That Doi Suthep is Chiang Mai's most sacred temple and one of Thailand's most spectacular religious sites, perched at 1,055 metres on Doi Suthep mountain. The legend says that a white elephant carrying a relic of the Buddha climbed the mountain, turned three times, and trumpeted — marking the spot where the temple should be built. The approach is a climb of 306 steps flanked by magnificent naga (serpent) balustrades, each step a meditation in itself. At the summit, the gleaming gold chedi (stupa) is surrounded by a courtyard ringed with bells that ring in the mountain breeze. From the terrace, the entire Chiang Mai Valley spreads below — on clear days, the view extends to the Myanmar border. The temple complex includes a sacred Bodhi tree planted from a cutting of the original tree in Bodh Gaya, India, and a meditation hall where monks offer blessings. The evening light show illuminates the gold in a way that photographs can barely capture.",
        spot_hero_image="https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Historical",
        spot_rating=5,
        spot_best_time="November to February (cool season). Year-round visits are pleasant. Early morning for fewer crowds and best light on the gold.",
        spot_duration="Half day. Allow 2–3 hours for the visit including the climb and temple exploration.",
        spot_budget_daily="$25–60. Entry 30 THB ($1). Songthaew (red truck) from old city 80–100 THB.",
        spot_currency="Thai Baht (THB). 1 USD ≈ 35 THB.",
        spot_language="Thai. English spoken at tourist sites.",
        spot_timezone="UTC+7 (ICT).",
        spot_weather="Tropical. Cool and pleasant November–February (15–28°C). Hot season March–May (up to 40°C). Rainy June–October.",
        spot_latitude=18.8049,
        spot_longitude=98.9215,
        spot_attractions=_list("Gold chedi (stupa)", "306-step naga staircase", "Valley viewpoint", "Bodhi tree", "Bell ringers courtyard", "Meditation hall", "Helicopter pad viewpoint"),
        spot_activities=_list("Climbing the 306 steps", "Gold chedi viewing", "Valley panorama", "Meditation", "Blessing from monks", "Bell ringing", "Incense offering"),
        spot_nearby=_nearby(("Chiang Mai Old City", "15 km"), ("Huay Kaew Waterfall", "8 km"), ("Elephant Nature Park", "60 km")),
        spot_travel_tips="Take the 306 steps up instead of the cable car — it's the proper way to approach the temple. Dress modestly (cover shoulders and knees). Visit early morning for the best photos. Don't miss the viewpoint at the back of the temple.",
        spot_safety_info="Dress appropriately — no shorts or sleeveless tops. Monkeys on the steps can grab items — secure belongings. The steps can be slippery when wet.",
        spot_transport_info="Songthaew (red shared taxi) from the Old City gates (80–100 THB). Private taxi 300–400 THB. Motorcycle rental is common. Many tour agencies offer half-day trips.",
    ),
    dict(
        spot_name="Night Bazaar",
        spot_city="Chiang Mai",
        spot_country="Thailand",
        spot_description="The legendary night market — hundreds of stalls selling handicrafts, street food, and live performances under the stars.",
        spot_detailed_description="The Chiang Mai Night Bazaar is Southeast Asia's most famous night market, stretching along Chang Klan Road and spilling into surrounding streets. Every evening from dusk, hundreds of vendors transform the area into a sensory feast — silk scarves billow in the breeze, silver jewellery glitters under strings of lights, and the air fills with the intoxicating mix of grilled meats, Thai curries, mango sticky rice and fresh fruit shakes. The market is actually three markets in one: the main Chang Klan Night Bazaar (daily), the Saturday Walking Street at Wua Lai (Saturdays only), and the Sunday Walking Street at Ratchadamnoen (Sundays only). Each has its own character. The main bazaar offers everything from handicrafts and clothing to Thai massage and live cultural performances. The Saturday and Sunday walking streets are more local, with food stalls, art, and live music. Bargaining is expected and part of the fun. The market is best enjoyed slowly — wander, taste, chat with vendors, and let the energy wash over you.",
        spot_hero_image="https://images.unsplash.com/photo-1504214208698-ea1916a2195a?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1504214208698-ea1916a2195a?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1528181304800-259b08848526?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Cultural",
        spot_rating=4,
        spot_best_time="Year-round. Sunday Walking Street (Ratchadamnoen Rd) is the most atmospheric. Cool season (Nov–Feb) is most pleasant.",
        spot_duration="Evening (5 PM – midnight). Sunday Walking Street is the longest, running until midnight.",
        spot_budget_daily="$10–30. Street food $1–3 per dish. Bargain hard on souvenirs.",
        spot_currency="Thai Baht (THB).",
        spot_language="Thai. English understood by most vendors.",
        spot_timezone="UTC+7.",
        spot_weather="Cool in the evening during Nov–Feb. Hot season evenings are warm but pleasant.",
        spot_latitude=18.7883,
        spot_longitude=98.9940,
        spot_attractions=_list("Chang Klan Night Bazaar", "Sunday Walking Street", "Saturday Walking Street", "Live cultural shows", "Khao Soi street stall", "Silver crafts", "Silk scarves"),
        spot_activities=_list("Shopping", "Street food tasting", "Bargaining", "Thai massage", "Live music", "Art browsing", "People watching"),
        spot_nearby=_nearby(("Chiang Mai Old City", "1 km"), ("Doi Suthep", "15 km"), ("Nimmanhaemin Road", "2 km")),
        spot_travel_tips="Sunday Walking Street is the best — it's a pedestrian-only zone. Arrive early (5 PM) before crowds build. Bring cash — most vendors don't accept cards. Walk the full length before buying — you'll find better deals further in. Try the mango sticky rice.",
        spot_safety_info="Watch for pickpockets in dense crowds. Keep bags zipped. Be cautious with hot food — stalls are crowded. Some 'handicrafts' are mass-produced — quality varies.",
        spot_transport_info="Within the Old City, walk or rent a bicycle. Songthaews (red trucks) run along main roads. Tuk-tuks available but more expensive than songthaews. Parking can be difficult on Sunday evenings.",
    ),
    dict(
        spot_name="Elephant Nature Park",
        spot_city="Chiang Mai",
        spot_country="Thailand",
        spot_description="An ethical elephant sanctuary — feed, bathe, and walk with rescued elephants in a lush riverside valley.",
        spot_detailed_description="Elephant Nature Park is the world's leading ethical elephant sanctuary, founded by the legendary Sangduen 'Lek' Chailert to rescue elephants from the tourism and logging industries. Unlike many tourist attractions that offer elephant rides, ENP is strictly no-riding — instead, visitors walk alongside, feed, and bathe these gentle giants in the Mae Taeng River. The sanctuary is home to over 40 rescued elephants, each with a story of survival from abuse. Some have blind eyes from being stabbed with bullhooks, others have damaged feet from walking on concrete. At ENP, they roam freely in the valley, socialising with other elephants, swimming in the river, and eating the 400 kg of food they consume daily. The visitor experience is deeply moving — you'll learn each elephant's story, watch them interact, and feel the emotional weight of their recovery. The park also houses rescued dogs, cats, water buffalo and other animals. The one-day visit includes lunch, transport from Chiang Mai, and a tour led by knowledgeable guides.",
        spot_hero_image="https://images.unsplash.com/photo-1564760055775-d63b17a55c44?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Nature",
        spot_rating=5,
        spot_best_time="Year-round. Best from November to February when weather is cooler. Weekday visits are less crowded.",
        spot_duration="Full day (7 AM pickup, return by 5 PM). Book well in advance — sells out weeks ahead.",
        spot_budget_daily="$75–100 including transport and lunch. Half the fee goes directly to elephant care.",
        spot_currency="Thai Baht (THB).",
        spot_language="English. Tours conducted in English by knowledgeable guides.",
        spot_timezone="UTC+7.",
        spot_weather="Valley location. 20–35°C. River bathing keeps you cool.",
        spot_latitude=19.2100,
        spot_longitude=98.9100,
        spot_attractions=_list("Elephant feeding", "River bathing", "Elephant shelter tour", "Rescue stories", "Valley walking trail", "Water buffalo encounter"),
        spot_activities=_list("Feeding elephants", "River bathing with elephants", "Walking alongside elephants", "Learning rescue stories", "Dog shelter visit", "Volunteering opportunities"),
        spot_nearby=_nearby(("Chiang Mai Old City", "60 km"), ("Doi Suthep", "55 km"), ("Chiang Rai", "180 km")),
        spot_travel_tips="Book at least 2–3 weeks in advance — the park limits visitors and sells out fast. Wear clothes you don't mind getting wet and dirty. Bring a waterproof camera/phone case. There's no WiFi — embrace the digital detox.",
        spot_safety_info="Elephants are large animals — follow guide instructions at all times. Some elephants are unpredictable. Don't approach without a guide. Wear closed-toe shoes. No single-use plastic bags (elephants may eat them).",
        spot_transport_info="Included in the tour fee — pickup from Chiang Mai hotels at 7 AM. The park is 60 km north of Chiang Mai in Mae Taeng district. The drive takes about 1.5 hours each way.",
    ),

    dict(
        spot_name="Tiger Hill Sunrise",
        spot_city="Darjeeling",
        spot_country="India",
        spot_description="Wake before dawn for a legendary sunrise over Kanchenjunga — the third-highest mountain in the world glows pink and gold.",
        spot_detailed_description="Tiger Hill is the most famous viewpoint in Darjeeling, perched at 2,590 metres on Ghoom mountain, offering an unobstructed view of the sunrise over Mount Kanchenjunga (8,586 m) — the third-highest peak in the world. On a clear morning, the experience is transcendent: the pre-dawn darkness slowly gives way to a deep indigo sky, then the first rays of sunlight strike the snow-capped summit, painting it in shades of rose, salmon, and finally brilliant gold. The transformation takes only minutes but feels eternal. On exceptionally clear days, you can even see Mount Everest in the far distance. The viewpoint is surrounded by alpine forest of rhododendrons and magnolias, which bloom spectacularly in spring. Below, the toy train tracks wind through tea plantations, and the town of Ghoom emerges from the morning mist. The experience of watching the sunrise from Tiger Hill is considered one of India's most iconic travel moments. A visit to the nearby Ghoom Monastery (Yiga Choeling), the oldest Tibetan Buddhist monastery in the area, is the perfect complement.",
        spot_hero_image="https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Mountain",
        spot_rating=5,
        spot_best_time="October to December and March to May. March–May for rhododendron season. October–November for the clearest skies. December–January for snow-capped peaks.",
        spot_duration="Half day (4 AM pickup for sunrise). Combined with Ghoom Monastery and Batasia Loop.",
        spot_budget_daily="$15–40. Jeep hire 1500–2000 INR ($20–25). Entry 30 INR.",
        spot_currency="Indian Rupee (INR). 1 USD ≈ 83 INR.",
        spot_language="Hindi, English, Nepali, Bengali.",
        spot_timezone="UTC+5:30 (IST).",
        spot_weather="Alpine. Cold at dawn (2–10°C in winter, 10–18°C in summer). Dress warmly for the sunrise.",
        spot_latitude=27.0169,
        spot_longitude=88.2636,
        spot_attractions=_list("Kanchenjunga sunrise", "Everest distant view", "Ghoom Monastery", "Batasia Loop", "Alpine forest walk", "Tea garden panorama"),
        spot_activities=_list("Sunrise watching", "Photography", "Monastery visit", "Batasia Loop war memorial", "Mountain trekking", "Bird watching"),
        spot_nearby=_nearby(("Darjeeling town", "11 km"), ("Ghoom", "4 km"), ("Batasia Loop", "5 km"), ("Tiger Hill", "11 km from town")),
        spot_travel_tips="Wake at 3:30 AM — jeep leaves at 4:00 AM sharp. The first 15 minutes of sunrise are the most spectacular. Bring warm layers — it's very cold before dawn. Book a jeep the day before. Arrive early to get a good spot.",
        spot_safety_info="The road to Tiger Hill is steep and winding — motion sickness is common. Frost on the viewing platform can be slippery. It's very dark — carry a flashlight.",
        spot_transport_info="Jeep hire from Darjeeling town (1500–2000 INR round trip, shared jeeps available). The toy train passes near but doesn't stop at Tiger Hill. Walking is possible but strenuous.",
    ),
    dict(
        spot_name="Darjeeling Himalayan Railway",
        spot_city="Darjeeling",
        spot_country="India",
        spot_description="The famous Toy Train — a UNESCO heritage narrow-gauge railway winding through tea gardens and misty hills.",
        spot_detailed_description="The Darjeeling Himalayan Railway, affectionately known as the Toy Train, is a UNESCO World Heritage Site and one of the most iconic railway experiences in the world. Built between 1879 and 1881, this narrow-gauge railway climbs 2,200 metres from New Jalpaiguri to Darjeeling, threading through tea plantations, oak forests, and misty mountain villages. The tiny blue steam locomotives — some over 100 years old — puff and chug around hairpin bends, through loops where the track crosses itself, and past stunning Himalayan panoramas. The most famous section is the Batasia Loop, a dramatic spiral where the train circles a war memorial with 360-degree views of Kanchenjunga. The journey takes about 5 hours from New Jalpaiguri to Darjeeling, but many visitors take the shorter Ghum-Darjeeling segment (about 2 hours). Sitting in the open-air balcony car, watching the tea gardens slide past while a steam engine bell rings, is pure magic. The railway is a living museum — the engines are still fired with coal, the whistle echoes through the hills, and the stationmasters wear colonial-era uniforms.",
        spot_hero_image="https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Historical",
        spot_rating=5,
        spot_best_time="Year-round. October–November for the clearest mountain views. March–May for rhododendrons. December for snow on the peaks.",
        spot_duration="2 hours for Ghum-Darjeeling segment. Full day for New Jalpaiguri to Darjeeling.",
        spot_budget_daily="$15–40. First-class seat 1500 INR ($18). Observation car 800 INR.",
        spot_currency="Indian Rupee (INR).",
        spot_language="Hindi, English, Bengali, Nepali.",
        spot_timezone="UTC+5:30.",
        spot_weather="Mountain climate. Cool year-round. Fog common, especially mornings. Bring a jacket.",
        spot_latitude=27.0400,
        spot_longitude=88.2600,
        spot_attractions=_list("Batasia Loop spiral", "Ghum station (highest point)", "Steam locomotive viewing", "Tea garden pass", "Observation car", "Colonial-era stations"),
        spot_activities=_list("Train journey", "Tea garden viewing", "Photography from observation car", "Station exploration", "Toy train museum", "Walking alongside the tracks"),
        spot_nearby=_nearby(("Darjeeling town", "3 km from Ghum"), ("Tiger Hill", "11 km"), ("Batasia Loop", "5 km")),
        spot_travel_tips="Book first-class seats well in advance — they sell out fast. The observation car with open windows gives the best experience. Sit on the right side going up for the best views. Carry snacks — the journey is long and there's no dining car.",
        spot_safety_info="Keep arms inside the train — it passes close to walls and trees. The open windows can be drafty. Motion sickness is possible on the winding track. Secure your camera strap.",
        spot_transport_info="Full journey starts from New Jalpaiguri station (4 hours from Kolkata by train). Shorter Ghum-Darjeeling segment starts from Ghum station, accessible by jeep from Darjeeling. Toy train tickets bookable online at indianrailways.gov.in.",
    ),
    dict(
        spot_name="Tea Garden Walks",
        spot_city="Darjeeling",
        spot_country="India",
        spot_description="Walk through emerald-green tea plantations — learn about the tea-making process, taste fresh Darjeeling tea, and enjoy mountain air.",
        spot_detailed_description="Darjeeling is synonymous with tea — the emerald-green plantations that blanket the Himalayan slopes produce some of the finest and most expensive tea in the world, often called the 'Champagne of teas'. Walking through these gardens is a sensory experience unlike any other: the neat rows of tea bushes stretch to the horizon, interspersed with tall shade trees and rhododendron bushes. Tea pluckers — mostly Nepali women in bright saris — move gracefully through the rows, their fingers nimbly selecting the two leaves and a bud that make the finest tea. The air smells of earth, chlorophyll and mountain mist. Many plantations offer guided walks where you learn about the tea-making process — from plucking to withering, rolling, oxidation and drying. You'll taste freshly brewed tea at different stages and learn to distinguish the first flush (spring) from the second flush (summer) and the monsoon flush. The Makaibari and Happy Valley estates are the most visitor-friendly, offering full-day experiences including walks, factory tours and tasting sessions. The colonial-era planter's bungalows serve as charming guesthouses where you can wake to mist and birdsong.",
        spot_hero_image="https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=1200&q=85",
        spot_gallery_images=_imgs(
            "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=800&q=85",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=85",
        ),
        spot_category="Nature",
        spot_rating=4,
        spot_best_time="March–May for first flush (brightest flavour). October–November for second flush (most complex). Year-round walks are pleasant.",
        spot_duration="Half day for a garden walk. Full day for factory tour + tasting + lunch.",
        spot_budget_daily="$10–30. Garden walks are often free or minimal charge. Tea tasting $5–10.",
        spot_currency="Indian Rupee (INR).",
        spot_language="English, Nepali, Hindi, Bengali.",
        spot_timezone="UTC+5:30.",
        spot_weather="Mountain climate. Cool and misty. 10–20°C. Bring a light jacket.",
        spot_latitude=27.0500,
        spot_longitude=88.2800,
        spot_attractions=_list("Makaibari Tea Estate", "Happy Valley Tea Factory", "Tea plucking experience", "Tasting sessions", "Planter's bungalows", "Tea museum"),
        spot_activities=_list("Tea garden walk", "Tea plucking", "Factory tour", "Tea tasting", "Photography", "Staying in a planter's bungalow"),
        spot_nearby=_nearby(("Darjeeling town", "5 km"), ("Tiger Hill", "15 km"), ("Batasia Loop", "3 km")),
        spot_travel_tips="Makaibari offers the best experience — book in advance. Wear comfortable walking shoes. The walks are on hilly terrain. Bring a camera — the gardens are incredibly photogenic, especially in morning mist.",
        spot_safety_info="Trails can be muddy and slippery. Leeches are common during monsoon — carry salt. Stay on designated paths. Some gardens are working farms — follow guide instructions.",
        spot_transport_info="Most tea estates are within 10 km of Darjeeling town. Hire a jeep or walk. Some estates offer pick-up services. The toy train passes through tea gardens — the Ghum-Darjeeling segment offers excellent views.",
    ),
]


def _random_booking(hotel_idx: int, cust_idx: int, guide_idx=None):
    """Generate one booking + matching payment dict."""
    check_in = date(2026, randint(3, 10), randint(1, 28))
    nights = randint(2, 7)
    check_out = check_in + timedelta(days=nights)
    guests = randint(1, 4)
    rate = randint(95, 320)
    total = round(rate * nights * (1 + 0.1 * guests), 2)

    statuses = list(BookingStatus)
    status = choice(statuses)

    booking = dict(
        booking_date=check_in - timedelta(days=randint(3, 30)),
        check_in_date=check_in,
        check_out_date=check_out,
        number_of_guests=guests,
        booking_status=status,
        total_amount=total,
        customer_id=cust_idx,
        hotel_id=hotel_idx,
        guide_id=guide_idx,
    )

    methods = list(PaymentMethod)
    pay_status = (
        PaymentStatus.SUCCESS
        if status in (BookingStatus.CONFIRMED, BookingStatus.COMPLETED)
        else PaymentStatus.FAILED
        if status == BookingStatus.CANCELLED
        else choice([PaymentStatus.PENDING, PaymentStatus.SUCCESS])
    )

    payment = dict(
        payment_amount=total,
        payment_method=choice(methods),
        payment_status=pay_status,
        transaction_id=f"TXN-{hotel_idx:02d}{cust_idx:02d}-{randint(100000, 999999)}",
        payment_date=datetime.now(timezone.utc) - timedelta(days=randint(0, 60)),
        booking_id=0, 
    )
    return booking, payment


def seed(force: bool = False):
    session = Database.session_factory()()

    try:
        existing = session.query(Admin).count()
        if existing and not force:
            print(f"  ℹ  Database already has {existing} admin(s). Skipping (use --force to re-seed).")
            return

        if force:
            print("  [WARN]  --force: clearing existing data...")
            session.query(TouristSpot).delete(synchronize_session=False)
            session.query(Payment).delete(synchronize_session=False)
            session.query(Booking).delete(synchronize_session=False)
            session.query(Employee).delete(synchronize_session=False)
            session.query(Guide).delete(synchronize_session=False)
            session.query(Customer).delete(synchronize_session=False)
            session.query(Hotel).delete(synchronize_session=False)
            session.query(Admin).delete(synchronize_session=False)
            session.commit()

        print("Seeding ComfyGo database...\n")

        admin = Admin(**ADMIN)
        session.add(admin)
        session.flush()
        print(f"  [OK] Admin  -- {admin.admin_email}")

        hotel_objs = []
        for h in HOTELS:
            obj = Hotel(**h)
            session.add(obj)
            session.flush()
            hotel_objs.append(obj)
        print(f"  [OK] Hotels -- {len(hotel_objs)} created")

        for i, emp in enumerate(EMPLOYEES_SEED):
            emp["hotel_id"] = hotel_objs[i % len(hotel_objs)].hotel_id
            emp["admin_id"] = admin.admin_id
            session.add(Employee(**emp))
        print(f"  [OK] Employees -- {len(EMPLOYEES_SEED)} created")

        cust_objs = []
        for c in CUSTOMERS:
            obj = Customer(**c)
            session.add(obj)
            session.flush()
            cust_objs.append(obj)
        print(f"  [OK] Customers -- {len(cust_objs)} created")

        guide_objs = []
        for g in GUIDES:
            obj = Guide(**g)
            session.add(obj)
            session.flush()
            guide_objs.append(obj)
        print(f"  [OK] Guides -- {len(guide_objs)} created")

        for ts in TOURIST_SPOTS:
            session.add(TouristSpot(**ts))
        print(f"  [OK] Tourist Spots -- {len(TOURIST_SPOTS)} created")

        booking_pairs = [
            (0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, None),
            (4, 4, 3), (5, 5, 4), (6, 0, 5), (7, 1, 6),
            (8, 2, 7), (9, 3, 0), (10, 4, 1), (0, 5, 2),
        ]

        booking_objs = []
        for hotel_idx, cust_idx, guide_idx in booking_pairs:
            hotel_id = hotel_objs[hotel_idx].hotel_id
            cust_id = cust_objs[cust_idx].customer_id
            guide_id = guide_objs[guide_idx].guide_id if guide_idx is not None else None
            bk, pay = _random_booking(hotel_id, cust_id, guide_id)
            bk_obj = Booking(**bk)
            session.add(bk_obj)
            session.flush()
            pay["booking_id"] = bk_obj.booking_id
            session.add(Payment(**pay))
            booking_objs.append(bk_obj)
        print(f"  [OK] Bookings -- {len(booking_objs)} created")
        print(f"  [OK] Payments -- {len(booking_objs)} created")

        session.commit()
        print("\n[DONE] Database seeded successfully!\n")
        print("  Login credentials:")
        print("  Admin:  admin@comfygo.com     / Admin123  ")
        print("  Demo:   customer@comfygo.com  / Password1  ")

    except Exception as exc:
        session.rollback()
        print(f"\n[FAIL] Seed failed: {exc}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    force_flag = "--force" in sys.argv
    seed(force=force_flag)
