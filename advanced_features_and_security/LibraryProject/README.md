# Managing Permissions and Groups in Django

## Custom Permissions
Custom permissions were added to the Book model:

- can_view
- can_create
- can_edit
- can_delete

These permissions control access to viewing, creating, editing,
and deleting book instances.

## Groups Configuration
The following groups can be created and managed using Django Admin:

- Admins: can_view, can_create, can_edit, can_delete
- Editors: can_view, can_create, can_edit
- Viewers: can_view

## Permission Enforcement in Views
Django's @permission_required decorator is used in views to
restrict access based on assigned permissions.

## Testing
Different users were assigned to different groups to verify
that permissions are enforced correctly.
