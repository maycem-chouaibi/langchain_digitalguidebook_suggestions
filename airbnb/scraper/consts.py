AIRBNB_URL = "https://www.airbnb.com/s/{city}/homes?checkin={checkin}&checkout={checkout}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

API_ENDPOINTS = {
    "reviews": "https://www.airbnb.com/api/v3/StaysPdpReviewsQuery", 
    "calendar": "https://www.airbnb.com/api/v3/PdpAvailabilityCalendar", 
    "info": "https://www.airbnb.com/api/v3/StaysPdpSections", 
    "lnglat": "google.internal.maps.mapsjs.v1.MapsJsInternalService/GetViewportInfo",
    "generalInfo": "https://www.airbnb.com/api/v2/get-data-layer-variables"
}

OUTPUT_DIR = "airbnb_listings"

SECTIONS_TO_EXTRACT = [
    "petsAllowed",
    "petDetails",
    "houseRulesSections",
    "safetyAndPropertiesSections",
    "guestDisclaimer",
    "structuredDisplayPrice",
    "stayListingData",
    "ogTags",
    "cancellationPolicies",
    "sbuiData",
    "sharingConfig",
    "calendarMonths",
    "reviews",
    "structuredDisplayPrice",
    "amenities",
    "listingTitle",
    "structuredDisplayPrice"

]

DELETE_SECTIONS = [
    "loggingEventData",
    "loggingData",
    "icon",
    "deleted",
    "categoryTags",
    "avgFtblLtvPerRaw",
    "isAutoTranslateOn",
    "sharingConfig",
    "minimumNumberOfLinesForTruncation",
    "recommendedNumberOfLines",
    "petSubtitleAction",
    "__typename"
]
