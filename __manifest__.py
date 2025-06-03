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
    "website": "https://superuser.id",
    "depends": ["project"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "odoo_project_user_stage_management/static/src/js/project_kanban_controller.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}
