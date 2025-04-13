
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView
from .forms import PublicLinkForm
from .services.yandex_disk import YandexDiskService
import io
import zipfile
from django.views import View
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .services.yandex_disk import YandexDiskService
class IndexView(LoginRequiredMixin, FormView):
    template_name = "disk/index.html"
    form_class = PublicLinkForm

    def form_valid(self, form):
        public_key = form.cleaned_data["public_key"]
        file_type = form.cleaned_data.get("file_type", "all")
        service = YandexDiskService(public_key)
        try:
            file_list = service.get_file_list()
            if file_type != "all":
                file_list = [f for f in file_list if f.get("type") == file_type]
            extra_context = {"file_list": file_list, "public_key": public_key}
        except Exception as e:
            extra_context = {"error": f"Ошибка получения файлов: {str(e)}"}
        context = self.get_context_data(form=form, **extra_context)
        return self.render_to_response(context)



class FileDownloadView(View):
    def get(self, request, *args, **kwargs):
        public_key = request.GET.get("public_key")
        file_path = request.GET.get("file_path")
        if not public_key or not file_path:
            return HttpResponse("Не переданы необходимые параметры", status=400)

        service = YandexDiskService(public_key)
        try:
            file_content = service.download_file(file_path)
        except Exception as e:
            raise Http404(f"Ошибка загрузки файла: {e}")



        file_name = file_path.split("/")[-1]

        response = HttpResponse(file_content, content_type="application/octet-stream")
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response




class BulkDownloadView(LoginRequiredMixin, View):
    """
    Представление для скачивания нескольких файлов одним архивом.
    Нужно передавать список файлов (через name="files") и public_key.
    """

    def post(self, request, *args, **kwargs):
        public_key = request.POST.get("public_key", "")
        file_paths = request.POST.getlist("files")  # список выбранных файлов

        if not public_key:
            return HttpResponse("Не передан public_key", status=400)
        if not file_paths:
            return HttpResponse("Не выбрано ни одного файла для скачивания.", status=400)

        service = YandexDiskService(public_key)

        # Создаём архив в памяти
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
            for path in file_paths:
                try:
                    file_content = service.download_file(path)
                except Exception as e:
                    raise Http404(f"Ошибка загрузки файла {path}: {e}")

                filename = path.split("/")[-1] or "file"
                # Добавляем файл в архив
                zip_file.writestr(filename, file_content)

        # Подготовим ответ пользователю с архивом
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.read(), content_type="application/zip")
        response["Content-Disposition"] = 'attachment; filename="selected_files.zip"'
        return response


class SequentialDownloadView(LoginRequiredMixin, View):
    """
    Представление для скачивания файлов по очереди.
    Получаем список выбранных файлов (через POST),
    формируем список ссылок для индивидуального скачивания,
    и возвращаем HTML-страницу с JavaScript, который инициирует загрузку.
    """

    def post(self, request, *args, **kwargs):
        public_key = request.POST.get("public_key", "")
        file_paths = request.POST.getlist("files")

        if not public_key:
            return HttpResponse("Не передан public_key", status=400)
        if not file_paths:
            return HttpResponse("Не выбрано ни одного файла для скачивания.", status=400)

        # Формируем список ссылок для скачивания каждого файла
        download_links = []
        for path in file_paths:
            # Формируем ссылку, которая обращается к FileDownloadView с нужными параметрами
            link = reverse('download') + f"?public_key={public_key}&file_path={path}"
            download_links.append(link)

        context = {
            'download_links': json.dumps(download_links)
        }
        return render(request, 'disk/sequential_download.html', context)
