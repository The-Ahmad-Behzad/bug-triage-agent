"""MongoDB connection management"""

import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

logger = logging.getLogger("bug_triage_agent")


class MongoDBConnection:
    """MongoDB connection manager"""
    
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None
    
    @classmethod
    def get_client(cls) -> MongoClient:
        """
        Get or create MongoDB client
        
        Returns:
            MongoClient instance
        
        Raises:
            ConnectionFailure: If connection cannot be established
        """
        if cls._client is None:
            mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            try:
                cls._client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=5000,  # 5 second timeout
                    connectTimeoutMS=5000
                )
                # Test connection
                cls._client.admin.command('ping')
                logger.info(f"Connected to MongoDB at {mongodb_uri}")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                raise ConnectionFailure(f"Cannot connect to MongoDB: {e}")
        
        return cls._client
    
    @classmethod
    def get_database(cls) -> Database:
        """
        Get or create database instance
        
        Returns:
            Database instance
        """
        if cls._database is None:
            client = cls.get_client()
            db_name = os.getenv("MONGODB_DB_NAME", "bug_triage_agent")
            cls._database = client[db_name]
            logger.info(f"Using database: {db_name}")
        
        return cls._database
    
    @classmethod
    def close_connection(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._database = None
            logger.info("MongoDB connection closed")


def get_mongodb_client() -> MongoClient:
    """
    Get MongoDB client instance
    
    Returns:
        MongoClient instance
    """
    return MongoDBConnection.get_client()


def get_database() -> Database:
    """
    Get database instance
    
    Returns:
        Database instance
    """
    return MongoDBConnection.get_database()



