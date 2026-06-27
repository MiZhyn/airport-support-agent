PAGES = [
    # Facilities - 两层爬取（目录页 → 详细页）
    {
        "name": "baggage",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=baggage",
        "category": "facilities",
        "scrape_type": "directory"
    },
    {
        "name": "amenities",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=amenities",
        "category": "facilities",
        "scrape_type": "directory"
    },
    {
        "name": "assistance",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=assistance",
        "category": "facilities",
        "scrape_type": "directory"
    },
    {
        "name": "facilities",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=facilities",
        "category": "facilities",
        "scrape_type": "directory"
    },
    {
        "name": "other-services",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=other-services",
        "category": "facilities",
        "scrape_type": "directory"
    },
    {
        "name": "transportation",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=transportation",
        "category": "facilities",
        "scrape_type": "directory"
    },

    # Hotels - 直接爬详细页
    {
        "name": "hotels",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory.html?category=hotels",
        "category": "hotels",
        "scrape_type": "detail"
    },
    {
        "name": "transit-hotels",
        "url": "https://www.changiairport.com/en/at-changi/facilities-and-services-directory/transit-hotels.html",
        "category": "transit-hotels",
        "scrape_type": "detail"
    },
]

BASE_URL = "https://www.changiairport.com"