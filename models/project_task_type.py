# -*- coding: utf-8 -*-
from odoo import models, api


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        """Allow Project Users to create/write stages."""
        # If user has Project User group, allow create and write operations
        if operation in ["create", "write"] and self.env.user.has_group(
            "project.group_project_user"
        ):
            return True
        return super().check_access_rights(operation, raise_exception)

    @api.model_create_multi
    def create(self, vals_list):
        """Allow Project Users to create stages with elevated privileges."""
        if self.env.user.has_group("project.group_project_user") and not self.env.su:
            return super(ProjectTaskType, self.sudo()).create(vals_list)
        return super().create(vals_list)

    def write(self, vals):
        """Allow Project Users to write stages with elevated privileges."""
        if self.env.user.has_group("project.group_project_user") and not self.env.su:
            return super(ProjectTaskType, self.sudo()).write(vals)
        return super().write(vals)


class ProjectProject(models.Model):
    _inherit = "project.project"

    def _compute_task_count(self):
        """Override to ensure Project Users can see task counts."""
        if self.env.user.has_group("project.group_project_user"):
            # Use sudo to ensure access to all tasks for counting
            for project in self:
                project.task_count = (
                    self.env["project.task"]
                    .sudo()
                    .search_count([("project_id", "=", project.id)])
                )
        else:
            super()._compute_task_count()


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        """Override to ensure Project Users can group by stage."""
        # This ensures the kanban view works properly when grouped by stage
        if "stage_id" in groupby and self.env.user.has_group(
            "project.group_project_user"
        ):
            # Temporarily use sudo for the read_group operation
            self = self.sudo()
        return super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
