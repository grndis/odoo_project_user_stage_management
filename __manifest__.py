# -*- coding: utf-8 -*-
{
    "name": "Project User Stage Management",
    "version": "16.0.1.0.0",
    "category": "Project",
    "summary": "Allow Project Users to create and manage project stages",
    "description": """
Project User Stage Management
=============================

This module extends the project management functionality to allow users 
with "Project / User" role to create new project stages.

Features:
---------
* Enables "+ Stage" button in Kanban view for Project Users
* Maintains security and access control
* No core modifications - fully upgrade safe

    """,
    "author": "superuser.id",
    "website": "https://superuser.id",
    "depends": ["project"],
    "data": [
        "security/project_security.xml",
        "security/ir.model.access.csv",
        "views/project_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "project_user_stage_management/static/src/js/project_kanban_stage_button.js",
        ],
    },
    "images": ["static/description/icon.png"],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "application": False,
}
