from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Drug
from .forms import DrugForm, ShelfLifeFormSet
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


# Create - створення нового запису
@login_required
@csrf_protect
def create_drug(request):
    if request.method == 'POST':
        drug_form = DrugForm(request.POST)
        shelf_life_formset = ShelfLifeFormSet(request.POST)

        if drug_form.is_valid() and shelf_life_formset.is_valid():
            drug = drug_form.save()
            shelf_life_formset.instance = drug
            shelf_life_formset.save()
            messages.success(request, "Drug successfully added.")
            return redirect('get_drugs')
        else:
            messages.error(request, "Please correct the errors below.")
            print(drug_form.errors)  # Log form errors for debugging

    else:
        drug_form = DrugForm()
        shelf_life_formset = ShelfLifeFormSet()

    return render(request, 'drugs/drug_form.html', {
        'drug_form': drug_form,
        'shelf_life_formset': shelf_life_formset
    })


# Read - отримання списку або конкретного запису
def get_drugs(request):
    # Отримання параметрів з URL
    page_number = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')

    # Базовий QuerySet
    drugs = Drug.objects.all()

    # Фільтрація за пошуковим запитом
    if search_query:
        drugs = drugs.filter(
            Q(trade_name__icontains=search_query) |
            Q(international_name__icontains=search_query) |
            Q(form__icontains=search_query) |
            Q(composition__icontains=search_query)
        ).distinct()

    # Пагінація
    paginator = Paginator(drugs, 10)  # 10 препаратів на сторінку
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        return JsonResponse({'error': 'Invalid page number'}, status=400)

    # Контекст для шаблону
    context = {
        'drugs': page_obj,
        'search_query': search_query,
        'page_obj': page_obj,
    }

    return render(request, 'drugs/drug_list.html', context)


def get_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    return render(request, 'drugs/drug_detail.html', {'drug': drug})


# Update - оновлення існуючого запису
@login_required
@permission_required('drugs.change_drug', raise_exception=True)
@csrf_protect
def update_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == 'POST':
        # Створіть форму для препарату та shelf life
        drug_form = DrugForm(request.POST, instance=drug)
        shelf_life_formset = ShelfLifeFormSet(request.POST, instance=drug)

        if drug_form.is_valid() and shelf_life_formset.is_valid():
            try:
                drug_form.save()
                shelf_life_formset.save()
                # Повідомлення про успішне оновлення
                messages.success(request, f"Препарат '{drug.trade_name}' успішно оновлено.")
                return redirect('get_drugs')  # Переконайтесь, що цей URL правильний
            except Exception as e:
                messages.error(request, f"Помилка при оновленні препарату: {str(e)}")
                print(f"Error: {str(e)}")  # Додати для дебагу
        else:
            messages.error(request, "Форма містить помилки.")
            print(drug_form.errors)  # Додати для дебагу
    else:
        # Якщо не POST запит, просто створюємо форми
        drug_form = DrugForm(instance=drug)
        shelf_life_formset = ShelfLifeFormSet(instance=drug)

    return render(request, 'drugs/drug_form.html', {
        'drug_form': drug_form,
        'shelf_life_formset': shelf_life_formset,
        'drug': drug,  # Передаємо drug в контекст шаблону
    })


# Delete - видалення запису
@login_required
@permission_required('drugs.delete_drug', raise_exception=True)
@csrf_exempt
def delete_drug(request, drug_id):
    if request.method == 'POST':
        try:
            # Отримати об'єкт для видалення
            drug = get_object_or_404(Drug, id=drug_id)
            drug.delete()

            # Додати повідомлення
            messages.success(request, f"Препарат '{drug.trade_name}' успішно видалено.")

            # Повернути користувача на попередню сторінку
            return redirect(request.META.get('HTTP_REFERER', 'get_drugs'))
        except Exception as e:
            messages.error(request, f"Помилка при видаленні препарату: {e}")
            return redirect(request.META.get('HTTP_REFERER', 'get_drugs'))
    messages.error(request, 'Неправильний метод запиту.')
    return redirect(request.META.get('HTTP_REFERER', 'get_drugs'))


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
