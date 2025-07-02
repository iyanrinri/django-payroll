from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.permissions import AllowAny


class TokenAuthAutoSchema(SwaggerAutoSchema):
    def get_security(self):
        if hasattr(self.view, 'permission_classes'):
            if AllowAny in self.view.permission_classes:
                return []
        return [{"Bearer": []}]
