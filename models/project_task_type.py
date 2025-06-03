# -*- coding: utf-8 -*-
from odoo import models, api, fields
from lxml import etree
import json


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        """Override to enable stage creation in kanban view for Project Users."""
        res = super().get_view(view_id, view_type, **options)

        if view_type == "kanban" and self.env.user.has_group(
            "project.group_project_user"
        ):
            doc = etree.XML(res["arch"])

            # Find all kanban tags and enable group_create
            for node in doc.xpath("//kanban"):
                node.set("group_create", "true")
                node.set("quick_create", "true")
                node.set("group_delete", "false")
                node.set("groups_draggable", "true")

                # Also check if default_group_by is stage_id
                if node.get("default_group_by") == "stage_id":
                    node.set("group_create", "true")

            res["arch"] = etree.tostring(doc, encoding="unicode")

        return res

    @api.model
    def web_search_read(
        self,
        domain=None,
        specification=None,
        offset=0,
        limit=None,
        order=None,
        count_limit=None,
    ):
        """Override to ensure Project Users can read stages properly."""
        if self.env.user.has_group("project.group_project_user"):
            # Temporarily use sudo for stage-related searches
            if any("stage_id" in str(d) for d in (domain or [])):
                self = self.sudo()
        return super().web_search_read(
            domain, specification, offset, limit, order, count_limit
        )


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        """Allow Project Users to create/write stages."""
        if operation in ["create", "write"] and self.env.user.has_group(
            "project.group_project_user"
        ):
            return True
        return super().check_access_rights(operation, raise_exception)

    @api.model_create_multi
    def create(self, vals_list):
        """Allow Project Users to create stages."""
        if self.env.user.has_group("project.group_project_user") and not self.env.su:
            return super(ProjectTaskType, self.sudo()).create(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        """Allow Project Users to write stages."""
        if self.env.user.has_group("project.group_project_user") and not self.env.su:
            return super(ProjectTaskType, self.sudo()).write(vals)
        return super().write(vals)

    @api.model
    def name_create(self, name):
        """Allow Project Users to create stages via quick create."""
        if self.env.user.has_group("project.group_project_user"):
            return super(ProjectTaskType, self.sudo()).name_create(name)
        return super().name_create(name)

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        """Ensure Project Users can read stages in grouped views."""
        if self.env.user.has_group("project.group_project_user"):
            return super(ProjectTaskType, self.sudo()).read_group(
                domain, fields, groupby, offset, limit, orderby, lazy
            )
        return super().read_group(domain, fields, groupby, offset, limit, orderby, lazy)


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    @api.model
    def _postprocess_view(self, node, model, view_id, in_tree_view, model_fields):
        """Post-process views to enable stage creation for Project Users."""
        res = super()._postprocess_view(
            node, model, view_id, in_tree_view, model_fields
        )

        # Only process if it's a project.task kanban view and user is Project User
        if (
            model == "project.task"
            and node.tag == "kanban"
            and self.env.user.has_group("project.group_project_user")
        ):
            # Enable group creation
            node.set("group_create", "true")
            node.set("quick_create", "true")

        return res
