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
        
        Note: For serverless environments, connection is lazy and errors are handled gracefully
        """
        if cls._client is None:
            mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            try:
                # For serverless, use shorter timeouts
                cls._client = MongoClient(
                    mongodb_uri,
                    serverSelectionTimeoutMS=3000,  # 3 second timeout for serverless
                    connectTimeoutMS=3000,
                    # Use connection pooling for serverless
                    maxPoolSize=10,
                    minPoolSize=0
                )
                # Try to test connection, but don't fail if it doesn't work immediately
                # Connection will be established on first actual operation
                try:
                    cls._client.admin.command('ping')
                    logger.info(f"Connected to MongoDB at {mongodb_uri}")
                except Exception as ping_error:
                    # Log but don't raise - connection will be established on first use
                    logger.warning(f"MongoDB ping failed (will retry on use): {ping_error}")
            except Exception as e:
                logger.error(f"Failed to create MongoDB client: {e}")
                # Re-raise only if it's a critical error
                raise ConnectionFailure(f"Cannot create MongoDB client: {e}")
        
        return cls._client
    
    @classmethod
    def get_database(cls) -> Database:
        """
        Get or create database instance
        
        Returns:
            Database instance
        
        Note: Database connection is lazy - actual connection happens on first operation
        """
        if cls._database is None:
            try:
                client = cls.get_client()
                db_name = os.getenv("MONGODB_DB_NAME", "bug_triage_agent")
                cls._database = client[db_name]
                logger.info(f"Using database: {db_name}")
            except Exception as e:
                logger.error(f"Failed to get database: {e}")
                # Still create database reference - connection will be attempted on first use
                # This prevents crashes in serverless environments
                if cls._client is None:
                    # If client creation failed, create a minimal client
                    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
                    cls._client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=3000, connectTimeoutMS=3000)
                cls._database = cls._client[os.getenv("MONGODB_DB_NAME", "bug_triage_agent")]
        
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



