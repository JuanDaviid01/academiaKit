#Oculta algunos campos para los usuarios que no sean admin
class AdminFieldsMixin:
    admin_only_fields = ("is_active", "created_at", "updated_at")

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        
        if not request:
            return fields

        is_admin = bool(getattr(request.user, "is_staff", False))
        if not is_admin:
            for name in self.admin_only_fields:
                fields.pop(name, None)
        else:
            for name in ("created_at", "updated_at"):
                if name in fields:
                    fields[name].read_only = True
        return fields
    
class UserAdminFieldsMixin(AdminFieldsMixin):
    #campos solo admin específicos para User
    admin_only_fields = AdminFieldsMixin.admin_only_fields + (
        "is_staff", "role", "is_verified", "last_login", "date_joined",
    )
