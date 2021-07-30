import aioredis
import os
from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from typing import List

host = os.environ['HOST']
user = os.environ['USER']
password = os.environ['PASSWORD']
database = os.environ['DATABASE']

engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(user, password, host, database))

app = FastAPI(
    title="Blue Sky Analytics Assignment",
    description="Blue Sky Analytics Assignment for Full Stack Developer",
    version="1.0.0",
    openapi_url="/api/v0.1.0/openapi.json",
    docs_url="/",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/countries', responses={
    200: {
        "description": "Country along with their IDs and valid years",
        "content": {
            "application/json": {
                "example": {
                    "Country Name": {
                        "id": "ID of the Country",
                        "validYears": ["List of Valid Years"]
                    }
                }
            }
        }
    }
})
@cache(expire=60, coder=JsonCoder)
async def countries():
    with engine.connect() as conn:
        query = ''' SELECT DISTINCT (detail.year), area.id, area.country from countrydata as area,  ghdata as detail
                    where detail.country = area.country
        '''
        results = conn.execute(query)
        value = {}
        for result in results:
            if result.country in value.keys():
                value[result.country]["validYears"].append(result.year)
            else:
                value[result.country] = {
                    "id": result.id,
                    "validYears": [result.year]
                }

        return value


@app.get('/country/{id}', responses={
    200: {
        "description": "Green House Emission Data Year Wise Data as per Country",
        "content": {
            "application/json": {
                "example": {
                    "id": ["ID of the Country"],
                    "country": ["Name of the Country"],
                    "Category-1": {
                        "Year-1": "value",
                        "Year-2": "value"
                    }
                }
            }
        }
    },
    404: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "Country doesn't have categorical value for specified date range"
                }
            }
        }
    },
    400: {
        "content": {
            "application/json": {
                "example": {
                    "detail": "startYear can't be greater than endYear"
                }
            }
        }
    },
})
@cache(expire=60, coder=JsonCoder)
async def data(id: int = Path(..., title="Country ID", ge=1, le=43),
               startYear: int = Query(..., title="Starting Year", ge=1990, le=2014),
               endYear: int = Query(..., title="Ending Year", ge=1990, le=2014),
               category: List[str] = Query(..., title="Gas Emitted")):
    if startYear > endYear:
        raise HTTPException(status_code=400, detail="startYear can't be greater than endYear")
    else:
        category = tuple(set(category))
        with engine.connect() as conn:
            format_strings = ','.join(['%s'] * len(category))

            query = '''
            select c.id, c.country, year, category ,value  from ghdata as g
            inner join countrydata c on g.country = c.country
            where c.id = {} and category in (%s) and year between {} and {}   
            '''.format(id, startYear, endYear)

            results = conn.execute(query % format_strings, category)
            value = dict()

            for result in results:
                if result.category in value.keys():
                    value[result.category][result.year] = result.value
                else:
                    value['id'] = result.id,
                    value['country'] = result.country,
                    value[result.category] = {
                        result.year: result.value
                    }

            if len(value) == 0:
                raise HTTPException(status_code=404,
                                    detail="Country doesn't have categorical value for specified date range")
            else:
                return value


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://{}".format(host), password=password, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
