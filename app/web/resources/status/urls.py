"""Consolidate the status urls."""

from fastapi import APIRouter

from app.web.resources.status.api import get_status


router = APIRouter(prefix="/status")

router.add_api_route("/", get_status, methods=["GET"], tags=["Status"])
