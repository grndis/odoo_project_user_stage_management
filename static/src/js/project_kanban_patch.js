/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";

patch(KanbanController.prototype, {
  setup() {
    super.setup(...arguments);
    this.user = useService("user");

    onWillStart(async () => {
      if (this.props.resModel === "project.task") {
        const hasProjectUser = await this.user.hasGroup(
          "project.group_project_user",
        );
        const hasProjectManager = await this.user.hasGroup(
          "project.group_project_manager",
        );

        if (hasProjectUser || hasProjectManager) {
          // Override the canCreateGroup getter
          Object.defineProperty(this, "canCreateGroup", {
            get() {
              if (
                this.model.groupBy &&
                this.model.groupBy.includes("stage_id")
              ) {
                return true;
              }
              return this._canCreateGroup;
            },
            set(value) {
              this._canCreateGroup = value;
            },
          });
        }
      }
    });
  },
});
