"""The main urls module. Import all the routes here."""

from app.web.resources.status.urls import router as status_router
from app.web.resources.tasks.urls import router as tasks_router


all_routers = [status_router, tasks_router]
