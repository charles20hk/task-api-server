"""The main urls module. Import all the routes here."""

from app.web.resources.status.urls import router as status_router


all_routers = [status_router]
