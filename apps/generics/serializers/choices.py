from rest_framework import serializers


class ChoiceSerializer(serializers.Serializer):
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    @classmethod
    def get_value(cls, obj) -> str:
        return str(obj.get("_choice_value"))

    @classmethod
    def get_label(cls, obj) -> str:
        return str(obj.get("_choice_label"))
