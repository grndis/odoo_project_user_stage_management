# -*- coding: utf-8 -*-
from odoo import models, api, fields
from lxml import etree


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
            kanban_nodes = doc.xpath("//kanban")

            for node in kanban_nodes:
                # Enable group_create
                node.set("group_create", "1")
                node.set("quick_create", "1")

            res["arch"] = etree.tostring(doc, encoding="unicode")

        return res
