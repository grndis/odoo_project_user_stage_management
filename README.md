# Project User Stage Management

## Overview

This module extends Odoo's project management functionality to allow users with the "Project / User" role to create and manage project stages directly from the Kanban view.

## Features

- Enables the "+ Stage" button in project Kanban view for Project Users
- Maintains proper security and access control
- Adds menu item for stage management
- No core modifications - fully upgrade safe

## Installation

1. Copy the `project_user_stage_management` folder to your Odoo addons directory
2. Update the app list: Settings → Apps → Update Apps List
3. Search for "Project User Stage Management"
4. Click Install

## Configuration

No additional configuration required. The module works immediately after installation.

## Usage

After installation:

1. Users with "Project / User" role will see the "+ Stage" button in project Kanban views
2. They can create new stages for projects they have access to
3. A new menu item "Stages" appears under Project → Configuration for easy stage management

## Technical Details

- Compatible with Odoo 16.0
- Uses JavaScript patching to extend the Kanban renderer
- Implements proper security rules and access controls
- No Python model extensions required

## Support

For issues or questions, please contact: support@yourcompany.com

## License

LGPL-3
