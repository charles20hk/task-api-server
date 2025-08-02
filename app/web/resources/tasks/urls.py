"""Consolidate the tasks urls."""

from fastapi import APIRouter

from app.web.resources.tasks.api import create_task


router = APIRouter(prefix="/tasks")

router.add_api_route("/", create_task, methods=["POST"], tags=["Tasks"])
