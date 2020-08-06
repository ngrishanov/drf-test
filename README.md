# drf-test
Test task using Django REST Framework

How to run
----------
1. Make sure docker-compose is installed
3. Execute `docker-compose up` to run API

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
