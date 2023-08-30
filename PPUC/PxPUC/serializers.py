from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import *
import os, re
import logging

logger = logging.getLogger(__name__)


class LocationSerializer(serializers.ModelSerializer):
    hasTxt = serializers.SerializerMethodField()
    hasPdf = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ("id", "name", "state", "hasTxt", "hasPdf")

    def __init__(self, *args, **kwargs):
        super(LocationSerializer, self).__init__(*args, **kwargs)

        # TODO: make this less hacky for other possible serializer use cases
        # only include sentences if preloaded for performance
        if len(args) > 0 and isinstance(args[0], QuerySet) and len(args[0]) > 0:
            obj = args[0][0]
            if hasattr(obj, "_prefetched_objects_cache"):
                is_preloaded = (
                    obj._prefetched_objects_cache.get(
                        obj.sentences.field.related_query_name()
                    )
                    is not None
                )
                if is_preloaded:
                    self.fields["sentences"] = serializers.SerializerMethodField()
                    self.fields["rank"] = serializers.SerializerMethodField()

    def get_sentences(self, obj):
        return SentenceSerializer(obj.sentences, many=True).data

    def get_rank(self, obj):
        return obj.rank

    def get_hasTxt(self, obj):
        # check filesystem
        return os.path.exists(
            "%s/PxPUC/static/app/contracts_txt/%s.txt" % (os.getcwd(), obj.name)
        )

    def get_hasPdf(self, obj):
        # check filesystem
        return os.path.exists(
            "%s/PxPUC/static/app/contracts_pdf/%s.pdf" % (os.getcwd(), obj.name)
        )


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name")

    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

        # TODO: make this less hacky for other possible serializer use cases
        # only include questions if preloaded for performance
        if len(args) > 0 and len(args[0]) > 0:
            obj = args[0][0]
            if hasattr(obj, "_prefetched_objects_cache"):
                is_preloaded = (
                    obj._prefetched_objects_cache.get(obj.questions.prefetch_cache_name)
                    is not None
                )
                if is_preloaded:
                    self.fields["questions"] = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.category

    def get_questions(self, obj):
        return QuestionSerializer(obj.questions, many=True).data


class QuestionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ("id", "question", "answer")

    def get_question(self, obj):
        return obj.q

    def get_answer(self, obj):
        return obj.a


class ProblematicSentenceSerializer(serializers.ModelSerializer):
    limitOversight = serializers.SerializerMethodField()
    cityPayMisconduct = serializers.SerializerMethodField()
    eraseMisconduct = serializers.SerializerMethodField()
    disqualifyComplaint = serializers.SerializerMethodField()
    restrictInterrogation = serializers.SerializerMethodField()
    unfairInformation = serializers.SerializerMethodField()

    class Meta:
        model = Problematic_Sentence
        fields = (
            "text",
            "impact",
            "limitOversight",
            "cityPayMisconduct",
            "eraseMisconduct",
            "disqualifyComplaint",
            "restrictInterrogation",
            "unfairInformation",
        )

    def get_limitOversight(self, obj):
        return obj.limit_oversight

    def get_cityPayMisconduct(self, obj):
        return obj.city_pay_for_misconduct

    def get_eraseMisconduct(self, obj):
        return obj.erase_misconduct

    def get_disqualifyComplaint(self, obj):
        return obj.disqualify_complaints

    def get_restrictInterrogation(self, obj):
        return obj.restrict_interrogation

    def get_unfairInformation(self, obj):
        return obj.unfair_information


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ("id", "text")


class ContractSerializer(serializers.ModelSerializer):
    parsed = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ("id", "text", "parsed")

    def get_parsed(self, obj):
        return obj.is_parsed


class GlossaryTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = ("id", "term", "definition")


class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = {"id", "query", "timestamp", "results"}


# Added by SU23 Internship
# Converting new Django models created in models.py by SP23 Capstone team
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ("id", "keyword", "example")


class ProvisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provision
        fields = ("id", "number", "category", "explanation")
        print("In serial")
        logger.info(fields)


class MasterContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterContract
        fields = ("id", "department", "startYear", "endYear", "bargAgent")


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            "id",
            "deptName",
            "webLink",
            "fullOfficers2019",
            "partOfficers2019",
            "hasBill",
        )


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = (
            "id",
            "municID",
            "municipality",
            "department",
            "totPop2010",
            "nonWhitePop2010",
            "sqMiArea",
            "acreArea",
            "region",
            "COG",
            "school",
            "sfGlobalID",
            "sfSHAPEleng",
            "sfSHAPEarea",
        )
