from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, ProductIngredientViewSet, ProductViewSet

router = DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("product-ingredients", ProductIngredientViewSet, basename="product-ingredient")
router.register("", ProductViewSet, basename="product")

urlpatterns = router.urls
