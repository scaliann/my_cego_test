from django.urls import path
from .views import IndexView, FileDownloadView, BulkDownloadView, SequentialDownloadResponseView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('download/', FileDownloadView.as_view(), name='download'),
    path('bulk_download/', BulkDownloadView.as_view(), name='bulk_download'),
    path('sequential/', SequentialDownloadResponseView.as_view(), name='sequential_download'),
]
