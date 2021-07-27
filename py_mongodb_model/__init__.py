import pymongo
import os
from bson.objectid import ObjectId
import datetime

# from dotenv import load_dotenv
# from pathlib import Path
# env_path = Path('../') / '.env'
# load_dotenv(dotenv_path=env_path)
MONGODB_SRV = os.getenv("MONGODB_SRV")


class mongodb:
    def __init__(self, db_name=None, col_name=None, srv_link=None):
        if srv_link:
            db_link = srv_link
        else:
            db_link = MONGODB_SRV
        self.mongo = pymongo.MongoClient(
            db_link, maxPoolSize=50, connect=False)
        # main_db = self.mongo.database
        # print(main_db)
        if db_name and col_name:
            self.config(db_name, col_name)

    def config(self, db_name=None, col_name=None):
        if db_name:
            self.db = pymongo.database.Database(self.mongo, db_name)
        if col_name:
            self.col = pymongo.collection.Collection(self.db, col_name)

    def create(self, data={}, identifier=None):
        data["_created"] = datetime.datetime.utcnow()
        data["_updated"] = datetime.datetime.utcnow()
        record = self.col.insert_one(data)
        id = record.inserted_id
        if not identifier:
            identifier = "mdb_id"
        self.update(query=data, data={"%s" % identifier: id})
        return id

    def createIndex(self, query):
        docs = self.col.create_index(query)
        return docs

    def read(self, id):
        query = {"_id": ObjectId(id)}
        return self.col.find_one(query)

    def query(self, query={}, filter={}):
        docs = self.col.find(query, filter)
        return docs

    def query_one(self, query={}, filter={}):
        docs = self.col.find_one(query, filter)
        return docs

    def search(self, search_query=""):
        return self.col.find({"$text": {"$search": search_query}})

    def delete(self, query={}):
        return self.col.delete_one(query)

    def delete_many(self, query={}):
        return self.col.delete_many(query)

    def update(self, query={}, data={}):
        data["_updated"] = datetime.datetime.utcnow()
        return self.col.update_one(query, {"$set": data})

    def update_many(self, query={}, data={}):
        # data["_updated"] = datetime.datetime.utcnow()
        return self.col.update_many(query, data)

    def push(self, query={}, data={}):
        return self.col.update(query, {"$push": data})

    def pull(self, query={}, data={}):
        return self.col.update(
            query,
            {"$pull": data},
            # {"multi": True}
        )

    def paginate(
        self,
        query={},
        sort={"mdb_id": -1},
        page=1,
        limit=10,
        offset=0,
        search_query=None,
        projections={},
        int_keys=None,
        concat_keys=None,
    ):
        agg_array = []

        if search_query:
            print(search_query)
            print(query)
            # query['$text'] = {'$search': search_query}
            text_search = {"$match": {"$text": {"$search": search_query}}}
            agg_array.append(text_search)

        # print(sort)
        agg_array.append({"$match": query})
        agg_array.append({"$sort": sort})
        # agg_array = [
        #     {'$match': query},
        #     {'$sort': sort}
        # ]
        if int_keys:
            agg_array.insert(
                1,
                {
                    "$addFields": {
                        "%s"
                        % int_keys: {
                            "$cond": {
                                "if": {"$eq": ["$%s" % int_keys, ""]},
                                "then": 0,
                                "else": {"$toDouble": "$%s" % int_keys},
                            }
                        }
                    }
                },
            )
        if concat_keys:
            agg_array.insert(
                1,
                {
                    "$addFields": {
                        "%s"
                        % concat_keys: {"$concat": ["$first_name", " ", "$last_name"]}
                    }
                },
            )
        if projections:
            print("projections")
            print(projections)
            projections["customer"] = {
                "$concat": ["$billing.first_name", " ", "$billing.last_name"]
            }
            projections["item_count"] = {"$sum": "$line_items.quantity"}
            agg_array.insert(1, {"$project": projections})

        agg_array.append(
            {
                "$facet": {
                    # "metadata": [
                    #     {'$count': "total_items"},
                    #     {'$addFields': {
                    #         'current_page': page,
                    #         'offset': offset,
                    #         'limit': limit
                    #     }}
                    # ],
                    "items": [{"$skip": offset}, {"$limit": limit}]
                }
            }
        )
        print(agg_array)
        return self.col.aggregate(agg_array, allowDiskUse=True)

    def aggregate(self, agg_array):
        return self.col.aggregate(agg_array, allowDiskUse=True)


# mdb = mongodb()
# mdb.config("CRM", "USERS")


# def test_write():
#     user_1 = {
#         "name": "jane doe",
#         "eid": 18651,
#         "email": "janedoe@email.com"
#     }
#     result = mdb.create(user_1)
#     print(result)


# def test_query():
#     query = {"email": "janedoe@email.com"}
#     result = mdb.query(query)
#     for item in result:
#         print(item)
#         print(item["_id"])


# def test_update():
#     query = {"email": "janedoe@email.com"}
#     data = {"new_field": "test_value"}
#     response = mdb.update(query, data)
#     print(response)


# def test_delete():
#     query = {"email": "janedoe@email.com"}
#     # query={}
#     result = mdb.delete(query)
#     print(result)

# def test_get_by_id():
#     result = mdb.read("5dc39de9d014f687fe1e19f9")
#     print(result)

# test_write()
# test_update()
# test_query()
# test_delete()
# test_get_by_id()
