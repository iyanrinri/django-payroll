from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema

class TokenAuthAutoSchema(SwaggerAutoSchema):
    def get_security(self):
        return [{"Bearer": []}]
