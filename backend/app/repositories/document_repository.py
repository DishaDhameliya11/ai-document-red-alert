from datetime import datetime, timezone
from bson import ObjectId
from bson.errors import InvalidId
from app.db.mongodb import get_database

COLLECTION_NAME = "documents"


async def save_document_analysis(analysis_data: dict) -> str:
    database = get_database()
    collection = database[COLLECTION_NAME]

    document_to_save = {
        **analysis_data,
        "created_at": datetime.now(timezone.utc),
    }

    result = await collection.insert_one(document_to_save)

    return str(result.inserted_id)

async def get_document_history(user_id: str, limit: int = 20) -> list[dict]:
    database = get_database()
    collection = database[COLLECTION_NAME]

    cursor = (
        collection.find({"uploaded_by": user_id})
        .sort("created_at", -1)
        .limit(limit)
    )

    documents = []

    async for document in cursor:
        document["document_id"] = str(document["_id"])
        document.pop("_id", None)

        if "created_at" in document:
            document["created_at"] = document["created_at"].isoformat()

        documents.append(document)

    return documents

async def get_document_by_id(document_id: str) -> dict | None:
    database = get_database()
    collection = database[COLLECTION_NAME]

    try:
        object_id = ObjectId(document_id)
    except InvalidId:
        return None

    document = await collection.find_one({"_id": object_id})

    if not document:
        return None

    document["document_id"] = str(document["_id"])
    document.pop("_id", None)

    if "created_at" in document:
        document["created_at"] = document["created_at"].isoformat()

    return document

async def get_all_documents(limit: int = 50) -> list[dict]:
    database = get_database()
    collection = database[COLLECTION_NAME]

    cursor = collection.find().sort("created_at", -1).limit(limit)

    documents = []

    async for document in cursor:
        document["document_id"] = str(document["_id"])
        document.pop("_id", None)

        if "created_at" in document:
            document["created_at"] = document["created_at"].isoformat()

        documents.append(document)

    return documents