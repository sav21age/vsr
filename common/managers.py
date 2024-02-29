from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity


class IsVisibleManager(models.Manager):
    def get_queryset(self):
        return super(IsVisibleManager, self).get_queryset()\
            .filter(is_visible=True)


class SearchManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            # or_lookup = (Q(name__icontains=query))
            # qs = qs.filter(or_lookup)
            # qs = qs.filter(name__search=query)

            # qs = qs.annotate(search=SearchVector("name", config="russian"),) \
            #     .filter(search=SearchQuery(query, config="russian"))

            # qs = qs.filter(search_vector=SearchQuery(query, config="russian"))
            qs_vector = qs.filter(search_vector=SearchQuery(query, config="russian"))
            
            if qs_vector:
                return qs_vector
                
            return qs.annotate(similarity=TrigramSimilarity("name", query),) \
                .filter(similarity__gt=0.2).order_by("-similarity")
            
            # qs = qs.filter(search_vector=query)

            # qs = qs.annotate(search=SearchVector("name",),) \
            #     .filter(search=SearchQuery(query))

            # qs = qs.annotate(similarity=TrigramSimilarity("name", query),) \
            # .filter(similarity__gt=0.1).order_by("-similarity")

        # return qs
