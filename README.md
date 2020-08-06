# drf-test
Test task using Django REST Framework

How to run
----------
1. Make sure docker-compose is installed
3. Execute `docker-compose up` to run API

API endpoints
----------

#### POST /api/upload/
Upload an image (as base64 string) with optional annotation.

**Request**

```
{
    "image": "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
    "labels": [
        {
            "meta": {
                "confirmed": false,
                "confidence_percent": 0.99
            },
            "id": "5b0cd508-587b-493b-98ea-b08a8c31d403",
            "class_id": "tooth",
            "surface": [
                "B",
                "O",
                "L"
            ],
            "shape": {
                "endX": 983,
                "endY": 1399,
                "startY": 605,
                "startX": 44
            }
        },
        {
            "meta": {
                "confirmed": true,
                "confidence_percent": 0.99
            },
            "id": "5b0cd508-587b-493b-98ea-b08a8c31d103",
            "class_id": "tooth",
            "surface": [
                "B",
                "O",
                "L"
            ],
            "shape": {
                "endX": 983,
                "endY": 1399,
                "startY": 605,
                "startX": 44
            }
        }
    ]
}
```

**Response**

```
{
    "uuid": "adddea9f-8d0d-48f6-9e07-2b5ae9673c50"
}
``` 

#### GET /api/\<uuid:image_uuid\>/annotation/
Get image annotation. 

Optional `annotation_format` query param can be provided (possible values are `external` and `internal`). If missing, internal format will be used.

**Response**

```
{
    "labels": [
        {
            "id": "c1386742-b4de-443b-af0b-3fa6c73e698b",
            "class_id": "innovate visionary portals",
            "surface": "aaa"
        },
        {
            "id": "93bfa253-cf37-46a9-a45a-abadb50965fd",
            "class_id": "orchestrate end-to-end relationships",
            "surface": "cca"
        },
        {
            "id": "5212afb2-e9bd-4e75-803c-b1d70b12abe9",
            "class_id": "enhance open-source info-mediaries",
            "surface": "cba"
        }
    ]
}
``` 

#### PUT /api/\<uuid:image_uuid\>/annotation/
Update image annotation.

**Request**

```
{
    "labels": [
        {
            "meta": {
                "confirmed": false,
                "confidence_percent": 0.99
            },
            "id": "5b0cd508-587b-493b-98ea-b08a8c31d202",
            "class_id": "tooth",
            "surface": [
                "B",
                "O",
                "L"
            ],
            "shape": {
                "endX": 983,
                "endY": 1399,
                "startY": 605,
                "startX": 44
            }
        }
    ]
}
```

**Response**

```
{
    "labels": [
        {
            "meta": {
                "confirmed": false,
                "confidence_percent": 0.99
            },
            "id": "5b0cd508-587b-493b-98ea-b08a8c31d202",
            "class_id": "tooth",
            "surface": [
                "B",
                "O",
                "L"
            ],
            "shape": {
                "endX": 983,
                "endY": 1399,
                "startY": 605,
                "startX": 44
            }
        }
    ]
}
```

Some notes regarding design choices
----------
- Image labels are stored as flat Django model instances related to `Image`. They could be stored in JSON field of `Image` model instead, but IMHO it's easier to query and debug flat model data. Also, it should work faster.
---
- Image upload API endpoint receives JSON dict with image as base64 string and labels array. It has its downsides, as we should spend some CPU time to encode and decode image, and resulting string is larger than binary file. Nevertheless, it's a good solution, since it's easy to implement, maintain and debug.
- Another solution would be to POST form-data with image as binary file and related metadata as JSON converted to string. This would be harder to maintain and debug. For example, it's harder to understand what's going on in Chrome debug console when you're looking at JSON encoded as string compared to raw object (no formatting and syntax highlighting).
- Yet another solution would be to make two separate requests for uploading an image and sending metadata. Its downsides are spending more time and traffic to round-trips, and risk of losing data integrity (we successfully uploaded an image but got an error while sending metadata).

Libraries and tools used in project
-----------------------------------
- Django + Django REST Framework + django-extra-fields (for base64 image upload support)
- PostgreSQL
- Docker + Docker-compose
