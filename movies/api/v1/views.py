from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView

from movies.models import Filmwork, PersonRole


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        role_enums = [
            ("actors", PersonRole.ACTOR),
            ("directors", PersonRole.DIRECTOR),
            ("writers", PersonRole.WRITER),
        ]
        annotate_args = {"genres": ArrayAgg("genres__name", distinct=True)}
        annotate_args.update(
            {
                role: ArrayAgg(
                    "persons__full_name",
                    filter=Q(personfilmwork__role=role_enum),
                    distinct=True,
                )
                for role, role_enum in role_enums
            }
        )

        filmworks = (
            Filmwork.objects.select_related("genres", "persons")
            .all()
            .values()
            .annotate(**annotate_args)
            .order_by("id")
        )
        return filmworks

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by
        )
        context = {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        return kwargs["object"]
