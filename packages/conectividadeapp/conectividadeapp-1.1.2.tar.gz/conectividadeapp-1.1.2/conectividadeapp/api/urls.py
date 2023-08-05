from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.APIRootView = views.ConectividadeappRootView

router.register('actor-list', views.ActorViewSet, basename=views.ActorViewSet.name)
router.register('actorcategory-list', views.ActorCategoryViewSet)
router.register('activity-list', views.ActivityViewSet)

app_name = 'conectividadeapp-api'

urlpatterns = router.urls
