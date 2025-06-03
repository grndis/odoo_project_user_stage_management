/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProjectKanbanRenderer } from "@project/views/project_kanban/project_kanban_renderer";

/**
 * Patch the ProjectKanbanRenderer to allow Project Users to see the "+ Stage" button
 */
patch(ProjectKanbanRenderer.prototype, {
  /**
   * Override onWillStart to check for both Project Manager and Project User groups
   */
  async onWillStart() {
    // Call parent method
    await super.onWillStart(...arguments);

    // Check if view is grouped by stage
    if (this.props.list.isGroupedByStage) {
      // Check for either Project Manager OR Project User group
      const [hasProjectManager, hasProjectUser] = await Promise.all([
        this.userService.hasGroup("project.group_project_manager"),
        this.userService.hasGroup("project.group_project_user"),
      ]);

      // Allow stage creation for both groups
      this.isProjectManager = hasProjectManager || hasProjectUser;
    }
  },
});

/**
 * Additional patch for task kanban view if needed
 */
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";

patch(KanbanRenderer.prototype, {
  /**
   * Ensure the add column button is visible for project users in task kanban
   */
  get canCreateGroup() {
    // Get the original value
    const originalCanCreate = super.canCreateGroup;

    // If we're in a project context and user has project user rights
    if (
      this.props.list.model.modelName === "project.task" &&
      this.props.list.isGroupedByStage
    ) {
      return true;
    }

    return originalCanCreate;
  },
});
