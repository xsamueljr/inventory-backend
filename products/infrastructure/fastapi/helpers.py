from auth.domain.logged_user_info import LoggedUserInfo


from fastapi import HTTPException


def resolve_local_location_id(
    user: LoggedUserInfo,
    location_id: int | None,
    mode: str = "read",
) -> int:
    if user.is_admin:
        return location_id if location_id is not None else user.location_id

    if mode == "create":
        return user.location_id

    if location_id is None:
        return user.location_id

    if location_id != user.location_id:
        raise HTTPException(status_code=403, detail="Forbidden location")

    return user.location_id