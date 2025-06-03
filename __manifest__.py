# -*- coding: utf-8 -*-
{
    "name": "Project User Stage Access",
    "version": "18.0.1.0.0",
    "category": "Project",
    "summary": "Allow Project Users to create new project stages",
    "description": """
        This module allows users in the "Project / Users" group 
        to create new stages in the project Kanban view.
    """,
    "author": "superuser.id",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
        "views/web_assets.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "project_user_stage_access/static/src/js/kanban_controller.js",
            "project_user_stage_access/static/src/xml/kanban_controller.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
