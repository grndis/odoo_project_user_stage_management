/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(KanbanController.prototype, {
  setup() {
    super.setup();
    this.user = useService("user");
    this.checkStageAccess();
  },

  async checkStageAccess() {
    // For project task kanban views
    if (this.props.resModel === "project.task") {
      const hasProjectUser = await this.user.hasGroup(
        "project.group_project_user",
      );
      const hasProjectManager = await this.user.hasGroup(
        "project.group_project_manager",
      );

      if (hasProjectUser || hasProjectManager) {
        // Force enable the create button for stages
        this.canQuickCreate = true;
        this.canCreateGroup = true;
      }
    }
  },

  get canCreateGroup() {
    // Check if this is project task and user has permission
    if (
      this.props.resModel === "project.task" &&
      this.model.groupByField &&
      this.model.groupByField.name === "stage_id"
    ) {
      return this._canCreateGroup;
    }
    return super.canCreateGroup;
  },

  set canCreateGroup(value) {
    this._canCreateGroup = value;
  },
});
