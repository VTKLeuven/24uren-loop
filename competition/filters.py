from rest_framework.compat import coreapi, coreschema
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from rest_framework.filters import BaseFilterBackend


class LimitFilter(BaseFilterBackend):
    limit_param = 'limit'
    limit_title = _('Limit')
    limit_description = _('The limiting of the queryset results')

    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get(self.limit_param, None)

        if limit:
            try:
                limit = int(limit)
                if limit < 0:
                    raise ValueError()
                return queryset[:limit]
            except ValueError:
                raise ValidationError({'limit': 'The limit should be a non-negative integer'})
        return queryset


    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.limit_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.limit_title),
                    description=force_str(self.limit_description)
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.limit_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.limit_description),
                'schema': {
                    'type': 'string',
                },
            },
        ]


class OffsetFilter(BaseFilterBackend):
    offset_param = 'offset'
    offset_title = _('Offset')
    offset_description = _('The Offset of the queryset results')

    def filter_queryset(self, request, queryset, view):
        offset = request.query_params.get(self.offset_param, None)

        if offset:
            try:
                offset = int(offset)
                if offset < 0:
                    raise ValueError()
                return queryset[offset:]
            except ValueError:
                raise ValidationError({'offset': 'The offset should be a non-negative integer'})
        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.offset_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.offset_title),
                    description=force_str(self.offset_description)
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.offset_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.offset_description),
                'schema': {
                    'type': 'string',
                },
            },
        ]
