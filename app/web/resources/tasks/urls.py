"""Consolidate the tasks urls."""

from fastapi import APIRouter

from app.web.resources.tasks.api import create_task, get_task_by_id, query


router = APIRouter(prefix="/tasks")

router.add_api_route("/", create_task, methods=["POST"], tags=["Tasks"])
router.add_api_route("/", query, methods=["GET"], tags=["Tasks"])
router.add_api_route("/{id}", get_task_by_id, methods=["GET"], tags=["Tasks"])
