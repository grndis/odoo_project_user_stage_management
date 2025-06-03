/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { useService } from "@web/core/utils/hooks";

// Patch the KanbanController to allow Project Users to create stages
patch(KanbanController.prototype, {
  setup() {
    super.setup();
    this.user = useService("user");

    // Override the canCreate property for project kanban views
    const originalCanCreate = this.canCreate;

    this.canCreate = async () => {
      // Check if this is a project task view grouped by stage
      if (
        this.model.resModel === "project.task" &&
        this.model.groupBy &&
        this.model.groupBy.includes("stage_id")
      ) {
        // Check if user has either Project Manager or Project User group
        const hasProjectManager = await this.user.hasGroup(
          "project.group_project_manager",
        );
        const hasProjectUser = await this.user.hasGroup(
          "project.group_project_user",
        );

        return hasProjectManager || hasProjectUser;
      }

      // For other views, use the original logic
      return originalCanCreate;
    };
  },
});
