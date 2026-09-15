"""
mongodb_lexer.py
~~~~~~~~~~~~~~~~
A custom Pygments lexer for MongoDB shell queries and aggregation pipelines.

Supports:
  - MongoDB shell commands (db.collection.find, insertOne, aggregate, etc.)
  - BSON types: ObjectId, ISODate, NumberLong, NumberDecimal, BinData, Timestamp, etc.
  - Aggregation pipeline stages ($match, $group, $project, $lookup, etc.)
  - Query operators ($eq, $gt, $in, $regex, $elemMatch, etc.)
  - Update operators ($set, $unset, $push, $pull, $inc, etc.)
  - Projection, sort, and option keywords
  - JavaScript literals: strings, numbers, booleans, null, regex
  - Comments (single-line // and multi-line /* */)
"""

import re
from pygments.lexer import RegexLexer, bygroups, words, include
from pygments.token import (
    Text, Comment, Keyword, Name, String, Number,
    Operator, Punctuation, Token, Literal
)

# ── Custom token subtypes ────────────────────────────────────────────────────
BsonType   = Token.Name.BsonType       # ObjectId, ISODate, …
Stage      = Token.Keyword.Stage       # $match, $group, …
QueryOp    = Token.Keyword.QueryOp     # $eq, $gt, $in, …
UpdateOp   = Token.Keyword.UpdateOp    # $set, $push, …
Method     = Token.Name.Method         # find, aggregate, insertOne, …
Collection = Token.Name.Collection     # db.<name>


# ── Keyword lists ─────────────────────────────────────────────────────────────

BSON_TYPES = (
    "ObjectId", "ISODate", "Date", "Timestamp",
    "NumberLong", "NumberInt", "NumberDecimal", "NumberDouble",
    "BinData", "DBRef", "MinKey", "MaxKey", "UUID",
    "HexData", "Symbol",
)

COLLECTION_METHODS = (
    # CRUD
    "find", "findOne", "findOneAndUpdate", "findOneAndReplace",
    "findOneAndDelete", "insertOne", "insertMany", "updateOne",
    "updateMany", "replaceOne", "deleteOne", "deleteMany",
    "bulkWrite", "countDocuments", "estimatedDocumentCount",
    # Aggregation
    "aggregate", "distinct", "mapReduce",
    # Index
    "createIndex", "createIndexes", "dropIndex", "dropIndexes",
    "getIndexes", "listIndexes", "reIndex",
    # Collection info
    "drop", "rename", "stats", "validate",
    # Cursor methods chained on find()
    "sort", "limit", "skip", "projection", "hint",
    "explain", "count", "toArray", "forEach", "next",
    "hasNext", "batchSize", "collation", "comment",
    # Watch / change streams
    "watch",
)

DB_METHODS = (
    "getCollection", "createCollection", "dropDatabase",
    "runCommand", "adminCommand", "getSiblingDB",
    "getCollectionNames", "listCollections", "serverStatus",
    "currentOp", "killOp", "setProfilingLevel",
    "isMaster", "hello",
)

PIPELINE_STAGES = (
    "$match", "$group", "$project", "$addFields", "$set",
    "$unset", "$lookup", "$unwind", "$sort", "$limit", "$skip",
    "$count", "$bucket", "$bucketAuto", "$facet", "$sortByCount",
    "$replaceRoot", "$replaceWith", "$merge", "$out",
    "$graphLookup", "$geoNear", "$redact", "$sample",
    "$indexStats", "$collStats", "$planCacheStats",
    "$changeStream", "$documents", "$fill", "$densify",
    "$setWindowFields", "$unionWith",
)

QUERY_OPERATORS = (
    # Comparison
    "$eq", "$ne", "$gt", "$gte", "$lt", "$lte", "$in", "$nin",
    # Logical
    "$and", "$or", "$nor", "$not",
    # Element
    "$exists", "$type",
    # Evaluation
    "$regex", "$options", "$expr", "$jsonSchema",
    "$mod", "$text", "$where",
    # Array
    "$all", "$elemMatch", "$size",
    # Bitwise
    "$bitsAllClear", "$bitsAllSet", "$bitsAnyClear", "$bitsAnySet",
    # Geospatial
    "$geoWithin", "$geoIntersects", "$near", "$nearSphere",
    "$geometry", "$box", "$polygon", "$center", "$centerSphere",
    "$maxDistance", "$minDistance",
    # Projection
    "$meta", "$slice", "$elemMatch",
    # Aggregation expressions (commonly used in queries too)
    "$cond", "$ifNull", "$switch", "$mergeObjects",
    "$concatArrays", "$filter", "$map", "$reduce",
    "$first", "$last", "$push", "$addToSet",
    "$sum", "$avg", "$min", "$max", "$stdDevPop", "$stdDevSamp",
    "$arrayElemAt", "$arrayToObject", "$objectToArray",
    "$split", "$substr", "$toLower", "$toUpper", "$concat",
    "$dateToString", "$dateToParts", "$dateFromParts",
    "$dateFromString", "$toDate", "$year", "$month", "$week",
    "$dayOfMonth", "$dayOfWeek", "$dayOfYear", "$hour",
    "$minute", "$second", "$millisecond",
    "$toString", "$toInt", "$toLong", "$toDouble", "$toDecimal",
    "$toBool", "$type", "$isNumber", "$isArray",
    "$convert", "$abs", "$ceil", "$floor", "$round", "$trunc",
    "$multiply", "$divide", "$add", "$subtract",
    "$mod", "$pow", "$sqrt", "$log", "$log10", "$ln", "$exp",
    "$literal", "$let", "$function", "$accumulator",
    "$zip", "$range", "$reverseArray", "$size",
    "$indexOfArray", "$indexOfBytes", "$indexOfCP",
    "$regexFind", "$regexFindAll", "$regexMatch",
    "$trim", "$ltrim", "$rtrim", "$strLenBytes", "$strLenCP",
    "$substrBytes", "$substrCP",
    "$getField", "$setField", "$unsetField",
    "$rank", "$denseRank", "$documentNumber",
    "$locf", "$linearFill",
)

UPDATE_OPERATORS = (
    # Field
    "$set", "$unset", "$rename", "$setOnInsert",
    "$currentDate",
    # Numeric
    "$inc", "$mul", "$min", "$max",
    # Array
    "$addToSet", "$pop", "$pull", "$pullAll",
    "$push", "$each", "$position", "$slice", "$sort",
    "$bit",
)

OPTION_KEYWORDS = (
    "upsert", "multi", "writeConcern", "collation", "arrayFilters",
    "bypassDocumentValidation", "returnDocument", "returnNewDocument",
    "projection", "sort", "hint", "comment", "maxTimeMS",
    "readConcern", "readPreference", "session", "let",
)


class MongoDBLexer(RegexLexer):
    """Lexer for MongoDB shell syntax (queries, aggregations, BSON)."""

    name = "MongoDB"
    aliases = ["mongodb", "mongo"]
    filenames = ["*.mongodb", "*.mongo"]
    mimetypes = ["text/x-mongodb"]

    flags = re.DOTALL | re.MULTILINE

    # Build word-boundary patterns from lists
    _bson       = words(BSON_TYPES,         prefix=r"\b", suffix=r"\b")
    _col_method = words(COLLECTION_METHODS, prefix=r"\b", suffix=r"\b")
    _db_method  = words(DB_METHODS,         prefix=r"\b", suffix=r"\b")
    _stage      = words(PIPELINE_STAGES,    prefix=r'"', suffix=r'"')   # usually quoted
    _stage_uq   = words(PIPELINE_STAGES,    prefix=r"",  suffix=r"")    # unquoted
    _query_op   = words(QUERY_OPERATORS,    prefix=r'"', suffix=r'"')
    _query_uq   = words(QUERY_OPERATORS,    prefix=r"",  suffix=r"")
    _update_op  = words(UPDATE_OPERATORS,   prefix=r'"', suffix=r'"')
    _update_uq  = words(UPDATE_OPERATORS,   prefix=r"",  suffix=r"")
    _opts       = words(OPTION_KEYWORDS,    prefix=r"\b", suffix=r"\b")

    tokens = {
        "root": [
            # ── Whitespace ──────────────────────────────────────────────────
            (r"\s+", Text),

            # ── Comments ────────────────────────────────────────────────────
            (r"//.*?$",       Comment.Single),
            (r"/\*.*?\*/",    Comment.Multiline),

            # ── db.collectionName.method(...) ───────────────────────────────
            (
                r"\b(db)(\.)([A-Za-z_$][A-Za-z0-9_$]*)(\.)(" +
                "|".join(COLLECTION_METHODS) + r")\b",
                bygroups(
                    Keyword.Declaration,   # db
                    Punctuation,           # .
                    Collection,            # collectionName
                    Punctuation,           # .
                    Method,                # find / aggregate / …
                ),
            ),
            # ── db.method(...) (without collection) ─────────────────────────
            (
                r"\b(db)(\.)(" + "|".join(DB_METHODS) + r")\b",
                bygroups(Keyword.Declaration, Punctuation, Method),
            ),
            # ── db keyword alone ────────────────────────────────────────────
            (r"\bdb\b", Keyword.Declaration),

            # ── BSON constructor calls ───────────────────────────────────────
            (_bson, BsonType),

            # ── Pipeline stages (quoted, e.g. "$match") ─────────────────────
            (_stage, Stage),
            # ── Query operators (quoted, e.g. "$eq") ────────────────────────
            (r'"(?:' + "|".join(re.escape(op) for op in UPDATE_OPERATORS) + r')"', UpdateOp),
            (_query_op, QueryOp),

            # ── Option keywords (unquoted) ───────────────────────────────────
            (_opts, Name.Attribute),

            # ── JavaScript keywords / literals ───────────────────────────────
            (words(("true", "false", "null", "undefined",
                    "new", "var", "let", "const",
                    "function", "return", "if", "else",
                    "for", "while", "do", "in", "of"),
                   prefix=r"\b", suffix=r"\b"), Keyword),

            # ── Strings ──────────────────────────────────────────────────────
            (r'"', String.Double, "string_double"),
            (r"'", String.Single, "string_single"),

            # ── Template literals ────────────────────────────────────────────
            (r"`[^`]*`", String.Backtick),

            # ── Regex literals (JS /pattern/flags) ──────────────────────────
            (r"/(?:[^/\\\n]|\\.)+/[gimsuy]*", String.Regex),

            # ── Numbers ──────────────────────────────────────────────────────
            (r"0[xX][0-9a-fA-F]+", Number.Hex),
            (r"-?\d+\.\d*(?:[eE][+-]?\d+)?", Number.Float),
            (r"-?\d+(?:[eE][+-]?\d+)?",      Number.Integer),

            # ── Operators ────────────────────────────────────────────────────
            (r"[=!<>]=?|&&|\|\||[+\-*/%]", Operator),

            # ── Punctuation ──────────────────────────────────────────────────
            (r"[{}\[\](),.:;]", Punctuation),

            # ── Unquoted $-operators (fallback) ─────────────────────────────
            # Handles $op appearing without surrounding quotes in JS contexts
            (r"\$[A-Za-z]+", Name.Variable),

            # ── Identifiers ──────────────────────────────────────────────────
            (r"[A-Za-z_$][A-Za-z0-9_$]*", Name),
        ],

        # ── String states ────────────────────────────────────────────────────
        "string_double": [
            # Pipeline / query / update operators inside strings
            (r'(?:' + "|".join(re.escape(s) for s in PIPELINE_STAGES)  + r')(?=")', Stage),
            (r'(?:' + "|".join(re.escape(s) for s in UPDATE_OPERATORS) + r')(?=")', UpdateOp),
            (r'(?:' + "|".join(re.escape(s) for s in QUERY_OPERATORS)  + r')(?=")', QueryOp),
            (r'\\.',          String.Escape),
            (r'[^\\"$]+',     String.Double),
            (r'\$',           String.Double),   # literal $ inside string
            (r'"',            String.Double, "#pop"),
        ],
        "string_single": [
            (r"\\.",          String.Escape),
            (r"[^\\']+",      String.Single),
            (r"'",            String.Single, "#pop"),
        ],
    }