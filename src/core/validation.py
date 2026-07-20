from pydantic import BaseModel, ValidationError
from typing import Any, Optional


class ValidationResult(BaseModel):
    is_valid: bool
    score: float  # 1.0 to 5.0
    report: dict


class ValidationEngine:
    @staticmethod
    def validate_data(
        data: Any, schema: Optional[type[BaseModel]] = None
    ) -> ValidationResult:
        # Skip validation if no schema is provided or data is not a tabular list (e.g. nested JSON)
        if schema is None or not isinstance(data, list):
            return ValidationResult(
                is_valid=True,
                score=5.0,
                report={
                    "message": "Schema validation skipped (no schema or not a tabular list)"
                },
            )

        errors = []
        valid_count = 0
        total_count = len(data)

        for item in data:
            try:
                schema(**item)
                valid_count += 1
            except ValidationError as e:
                errors.append({"item": item, "errors": e.errors()})

        score = (valid_count / total_count) * 5.0 if total_count > 0 else 0.0
        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            score=round(score, 2),
            report={
                "total_records": total_count,
                "valid_records": valid_count,
                "invalid_records": len(errors),
                "error_samples": errors[:5],  # Keep first 5 errors for the report
            },
        )
