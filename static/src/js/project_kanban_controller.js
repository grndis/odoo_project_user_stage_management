/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProjectTaskKanbanController } from "@project/views/project_task_kanban/project_task_kanban_controller";

patch(ProjectTaskKanbanController.prototype, {
  async onWillStart() {
    await super.onWillStart();
    if (this.props.list.isGroupedByStage) {
      // Check if user has either Project Manager or Project User group
      const hasProjectManager = await this.userService.hasGroup(
        "project.group_project_manager",
      );
      const hasProjectUser = await this.userService.hasGroup(
        "project.group_project_user",
      );

      // Allow stage creation for both groups
      this.isProjectManager = hasProjectManager || hasProjectUser;
    }
  },
});
