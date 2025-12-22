from django.exceptions import ValidationError

REQUIRED_FIELDS = {
    "email" : ["to","subject"],
    "approval":["approval"], 
    "task" : ["task"],
}

def validate_step_config(step_type: str , config: dict) :
    if step_type not in REQUIRED_FIELDS:
        raise ValidationError(
            "Unsupported Step Type"
        )
    if not isinstance(config, dict) :
        raise ValidationError(
            "config must be a JSON object"
        )
    missing = []
    for field in REQUIRED_FIELDS[step_type] :
        if field not in config :
            missing.append(field)
    if missing:
        raise ValidationError(
            f"Missing config field for {step_type} , {missing}"
        )