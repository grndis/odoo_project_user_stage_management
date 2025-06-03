# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    @api.model
    def check_access_rights(self, operation, raise_exception=True):
        """Override to allow Project Users to create stages."""
        res = super().check_access_rights(operation, raise_exception=False)

        # If standard check failed and operation is create/write
        if not res and operation in ["create", "write"]:
            # Check if user has Project User group
            if self.env.user.has_group("project.group_project_user"):
                return True
            elif raise_exception:
                raise AccessError(
                    _("You don't have the required access rights to %s stages.")
                    % operation
                )

        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Allow Project Users to create stages."""
        # Temporarily elevate privileges if user is Project User
        if self.env.user.has_group("project.group_project_user"):
            self = self.sudo()
        return super().create(vals_list)

    def write(self, vals):
        """Allow Project Users to write stages."""
        # Temporarily elevate privileges if user is Project User
        if self.env.user.has_group("project.group_project_user"):
            self = self.sudo()
        return super().write(vals)
