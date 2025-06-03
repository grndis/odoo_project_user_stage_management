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
        "views/project_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
