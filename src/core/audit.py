from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.core.logging_config import get_logger

logger = get_logger(__name__)


async def log_audit_event(
    db: AsyncSession,
    user_id: Optional[str],
    action: str,
    resource: str,
    ip_address: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
):
    """Asynchronously log an audit event to the database."""
    try:
        query = text("""
            INSERT INTO audit_logs (user_id, action, resource, ip_address, details, timestamp)
            VALUES (:user_id, :action, :resource, :ip_address, :details, NOW())
        """)

        await db.execute(
            query,
            {
                "user_id": user_id,
                "action": action,
                "resource": resource,
                "ip_address": ip_address,
                "details": details,
            },
        )
        await db.commit()
        logger.info(f"AUDIT: {action} on {resource} by {user_id}")
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")
        # Don't fail the request if audit logging fails
