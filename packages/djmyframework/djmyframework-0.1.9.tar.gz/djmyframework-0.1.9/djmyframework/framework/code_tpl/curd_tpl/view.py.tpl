# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @Time: ${datetime}


from drf_yasg.utils import swagger_auto_schema
from framework.filters import MyFilterBackend, OrderingFilter, MyFilterSerializer
from framework.translation import _
from framework.route import Route
from framework.serializer import s,BaseModelSerializer, EditParams, IdSerializer, IdsSerializer, ParamsSerializer, PaginationSerializer
from framework.views import CurdViewSet, ListPageNumberPagination, Response,action,Request
from framework.views import render_to_response as rt
from ${app_name}.models import ${model_name}


class ${model_name}Serializer(BaseModelSerializer):
    # https://www.django-rest-framework.org/api-guide/serializers/
    # https://www.django-rest-framework.org/api-guide/relations/
% for f in model_many_to_many:
    #${f.name} = s.PrimaryKeyRelatedField(many=True,label=_("${f.verbose_name}"),queryset=${model_name}.${f.name}.field.related_model.objects.all() )
% endfor
% for f in model_foreigns:
    #${f.name} = s.RelatedField(label=_("${f.verbose_name}"),queryset=${model_name}.${f.name}.field.related_model.objects.all())
% endfor
% for f in fields:
    % if f.choices:
    ${f.name}_alias = s.CharField(source='get_${f.name}_display',required=False, read_only=True)
    % endif
% endfor

    class Meta:
        model = ${model_name}
        fields =  ${all_fields_name_list} or '__all__'
        #exclude = ['session_key']
        read_only_fields = ['create_datetime', 'update_datetime']
        #extra_kwargs = {'password': {'write_only': True}}


class List${model_name}RspSerializer(PaginationSerializer):
    results = ${model_name}Serializer(many=True)

@Route('${app_name}/${model_lower_name}')
class ${model_name}Set(CurdViewSet):
    filter_backends = (MyFilterBackend,OrderingFilter)

    serializer_class = ${model_name}Serializer
    # 可条件过滤的字段
    filter_fields =  ${list(fields_name_list)}
    # 可排序的字段
    ordering_fields = ${list(fields_name_list)}
    # 可以查询字段
    queryset_fields = ${list(fields_name_list)}

    model = ${model_name}

    def get_queryset(self):
        return ${model_name}.objects.all().prefetch_related(*${[f.name for f in model_many_to_many]}).select_related(*${[f.name for f in model_foreigns]}).only(*${model_name}Set.queryset_fields)

    @swagger_auto_schema(query_serializer=MyFilterSerializer,responses=List${model_name}RspSerializer)
    def list(self, request):
        """${model_desc} 列表"""
        return rt("${app_name}/${model_lower_name}/list.html",super().list(request))

    @swagger_auto_schema(query_serializer=EditParams, responses=${model_name}Serializer)
    def edit(self, request):
        """${model_desc} 编辑"""
        return rt("${app_name}/${model_lower_name}/edit.html",super().edit(request))

    @swagger_auto_schema(query_serializer=IdSerializer,request_body=${model_name}Serializer, responses=${model_name}Serializer)
    def save(self, request):
        """${model_desc} 保存"""
        return super().save(request)

    @swagger_auto_schema(request_body=IdsSerializer, responses=IdsSerializer)
    def delete(self, request):
        """${model_desc} 删除"""
        return super().delete(request)


    # @swagger_auto_schema(methods=['post'], request_body=${model_name}Serializer, responses=${model_name}Serializer)
    # @action(['post'])
    # def foo_action(self, request):
    #     return Response(${model_name}Serializer().data)