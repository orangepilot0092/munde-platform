from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.database import get_db
from src.core.secrets import SecretsManager

router = APIRouter(prefix="/apis", tags=["API Registry & Status"])


@router.get("/status")
def get_api_integration_status(db: Session = Depends(get_db)):
    rows = db.execute(
        text("""
        SELECT api_id, name, department, auth_method, access_status, 
               auth_config_ref, application_url, notes
        FROM api_registry ORDER BY access_status, name
    """)
    ).fetchall()

    apis = []
    for r in rows:
        has_key = SecretsManager.is_configured(r.api_id) if r.auth_config_ref else True
        apis.append(
            {
                "api_id": r.api_id,
                "name": r.name,
                "department": r.department,
                "access_status": r.access_status,
                "auth_configured": has_key,
                "env_var": r.auth_config_ref,
                "application_url": r.application_url,
                "notes": r.notes,
                "integration_state": "LIVE" if has_key else "NEEDS_KEY",
            }
        )

    summary = {
        "total": len(apis),
        "live": sum(1 for a in apis if a["integration_state"] == "LIVE"),
        "needs_key": sum(1 for a in apis if a["integration_state"] == "NEEDS_KEY"),
        "missing_env_vars": SecretsManager.get_missing_apis(),
    }

    return {"summary": summary, "apis": apis}
