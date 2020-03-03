from collections import defaultdict

from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from applications.domain import Domain, Status
from applications.models import Application, SubmissionTypes


@require_http_methods(["GET"])
def staff_applications_view(request: HttpRequest) -> HttpResponse:
    query = Application.objects.all().order_by("user__email")

    filter_by_application_status = request.GET.get("application_status")

    applications = []
    count = defaultdict(int)
    for a in query:
        application_status = Domain.get_application_status(a)
        count[application_status.value] += 1
        if filter_by_application_status is not None and application_status.name != filter_by_application_status:
            continue

        applications.append(
            {
                "ref": a,
                "status_list": [
                    application_status,
                    *[Domain.get_sub_type_status(a, sub_type) for sub_type in SubmissionTypes.all],
                ],
            }
        )

    status_enum = {s.name: {"name": s.name, "value": s.value, "count": count[s.value]} for s in Status}
    ctx = {"status_enum": status_enum, "applications": applications}

    template = loader.get_template("./staff_templates/applications.html")
    return HttpResponse(template.render(ctx, request))
