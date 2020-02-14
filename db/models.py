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
    check_collect_new_info = models.BooleanField()
    check_compel_provision_of_info = models.BooleanField()
    check_disclosed_to_new_3rd_party = models.BooleanField()
    check_new_purpose = models.BooleanField()
    check_new_privacy_intrusive_technology = models.BooleanField()
    check_decisions_with_significant_impact = models.BooleanField()
    check_health_or_wellbeing_info = models.BooleanField()
    check_intrusive_contact = models.BooleanField()


class CEIVDCheck(BaseModel):
    done_by = models.ForeignKey(User, on_delete=models.PROTECT)
    check_required_ce_ivd = models.BooleanField()


class Change(BaseModel):
    class Stages(models.TextChoices):
        SUGGESTION = ('1', 'Suggestion')
        VALIDATION = ('2', 'Validation')
        VERIFICATION = ('3', 'Verification')
        FINAL_DECISION = ('4', 'Final Decision')
        IMPLEMENTED = ('5', 'Implemented')

    index = models.CharField(max_length=12)
    stage = models.CharField(max_length=254, choices=Stages.choices)

    # suggestion stage
    requires_dpia = models.BooleanField(null=True)
    requires_ce_ivd = models.BooleanField(null=True)


class ChangeSuggestionReview(BaseModel):
    class ReviewOutcomes(models.TextChoices):
        ACCEPTED = ('A', 'Accepted')
        INFO_REQUIRED = ('I', 'Additional Information Required')
        SHELVED = ('S', 'Shelved')

    change = models.OneToOneField(
        Change,
        on_delete=models.CASCADE,
        null=True
    )
    reviewers = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="suggestion_reviews"
    )
    pending = models.BooleanField()
    outcome = models.CharField(max_length=1, choices=ReviewOutcomes.choices)


class ChangeSuggestion(BaseModel):
    class ChangeTypes(models.TextChoices):
        ROUTINE = 'Routine'
        SERVICE_PROVISION = 'Service Provision'
        RESEARCH = 'Research'

    change = models.OneToOneField(Change, on_delete=models.CASCADE)

    made_by = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=80)
    change_type = models.CharField(max_length=254, choices=ChangeTypes.choices)
    hub = models.ForeignKey(Hub, on_delete=models.PROTECT)
    summary = models.CharField(max_length=500)
    impact = models.CharField(max_length=500)
    strategy = models.CharField(max_length=500)

    ig_check = models.ForeignKey(IGCheck, on_delete=models.PROTECT)
    ce_ivd_check = models.ForeignKey(CEIVDCheck, on_delete=models.PROTECT)
    is_clinical_software = models.BooleanField()

    review = models.ForeignKey(
        ChangeSuggestionReview,
        on_delete=models.SET_NULL,
        null=True
    )



