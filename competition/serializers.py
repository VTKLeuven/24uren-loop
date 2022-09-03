from rest_framework import serializers
import django.contrib.auth.models as authmodels

from .models import *


class ModelExtraFieldSerializer(serializers.ModelSerializer):
  def __init__(self, *args, **kwargs):
    self.__extra_fields__ = kwargs.pop('extra_fields', {})
    self.__rm_fields__ = kwargs.pop('rm_fields', {})
    super().__init__(*args, **kwargs)

  def get_fields(self):
    fields = super().get_fields()
    fields.update(self.__extra_fields__)
    return fields


class AuthGroupSerializer(ModelExtraFieldSerializer):
  class Meta:
    model = authmodels.Group
    fields = ['name']


class UserSerializer(ModelExtraFieldSerializer):

  def to_representation(self, instance):
    self.fields['groups'] = AuthGroupSerializer(many=True, read_only=True)
    return super().to_representation(instance)

  class Meta:
    model = authmodels.User
    fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'groups']


class RunnerSerializer(ModelExtraFieldSerializer):

  class Meta:
    model = Runner
    fields = '__all__'


class QueueTicketSerializer(ModelExtraFieldSerializer):
  def to_representation(self, instance):
    self.fields['runner'] = RunnerSerializer(read_only=True)
    return super().to_representation(instance)

  class Meta:
    model = QueueTicket
    fields = '__all__'


class LapSerializer(ModelExtraFieldSerializer):
  class Meta:
    model = Lap
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    rm_fields = kwargs.get('rm_fields', set())
    self.rm_runner = 'runner' in rm_fields
    if self.rm_runner:
      rm_fields.discard('runner')
    super().__init__(*args, **kwargs)

  def to_representation(self, instance):
    if self.rm_runner:
      self.fields.pop('runner', None)
    else:
      self.fields['runner'] = RunnerSerializer(read_only=True)
    return super(LapSerializer, self).to_representation(instance)


class UniversitySerializer(ModelExtraFieldSerializer):
  class Meta:
    model = University
    fields = '__all__'


class GroupSerializer(ModelExtraFieldSerializer):
  class Meta:
    model = Group
    fields = '__all__'


class HappyHourSerializer(ModelExtraFieldSerializer):
  class Meta:
    model = HappyHour
    fields = '__all__'


class ShiftSerializer(ModelExtraFieldSerializer):
  class Meta:
    model = Shift
    fields = '__all__'

class CounterSerializer(ModelExtraFieldSerializer):
  class Meta:
    model = Counter
    fields = '__all__'

