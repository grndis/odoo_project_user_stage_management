# -*- coding: utf-8 -*-
from odoo import models, api, fields


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


class ProjectTask(models.Model):
    _inherit = "project.task"

    # Add a computed field to check if user can create stages
    can_create_stage = fields.Boolean(compute="_compute_can_create_stage")

    def _compute_can_create_stage(self):
        can_create = self.env.user.has_group(
            "project.group_project_manager"
        ) or self.env.user.has_group("project.group_project_user")
        for task in self:
            task.can_create_stage = can_create
