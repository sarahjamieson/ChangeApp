from django.db import models

from accounts.models import User


# have dates and users on all models
class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Hub(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IGCheck(BaseModel):
    done_by = models.ForeignKey(User, on_delete=models.PROTECT)
    check_profiling_or_automated_decisions = models.BooleanField()
    check_special_category_data = models.BooleanField()
    check_monitor_publically_accessible_place = models.BooleanField()
    check_innovative_technology = models.BooleanField()
    check_decision_on_service_access = models.BooleanField()
    check_large_scale_profiling = models.BooleanField()
    check_process_biometric_or_genetic_data = models.BooleanField()
    check_combine_compare_or_match_data = models.BooleanField()
    check_personal_data_without_privacy_notice = models.BooleanField()
    check_track_behaviour_or_location = models.BooleanField()
    check_process_childrens_data = models.BooleanField()
    check_risk_of_physical_harm_upon_breach = models.BooleanField()


class CEIVDCheck(BaseModel):
    done_by = models.ForeignKey(User, on_delete=models.PROTECT)
    check_required_ce_ivd = models.BooleanField()


class ChangeSuggestion(BaseModel):
    class ChangeTypes(models.TextChoices):
        ROUTINE = 'Routine'
        SERVICE_PROVISION = 'Service Provision'
        RESEARCH = 'Research'

    made_by = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=80)
    type = models.CharField(max_length=254, choices=ChangeTypes.choices)
    hub = models.ForeignKey(Hub, on_delete=models.PROTECT)
    summary = models.CharField(max_length=500)
    impact = models.CharField(max_length=500)
    strategy = models.CharField(max_length=500)

    ig_check = models.ForeignKey(IGCheck, on_delete=models.PROTECT)
    ce_ivd_check = models.ForeignKey(CEIVDCheck, on_delete=models.PROTECT)
    is_clinical_software = models.BooleanField()


class Change(BaseModel):
    class Stages(models.TextChoices):
        SUGGESTION = ('1', 'Suggestion')
        VALIDATION = ('2', 'Validation')
        VERIFICATION = ('3', 'Verification')
        FINAL_DECISION = ('4', 'Final Decision')
        IMPLEMENTED = ('5', 'Implemented')

    stage = models.CharField(max_length=254, choices=Stages.choices)
    # suggestion stage
    suggestion = models.ForeignKey(ChangeSuggestion, on_delete=models.CASCADE)
    requires_dpia = models.BooleanField(null=True)
    requires_ce_ivd = models.BooleanField(null=True)


