from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
import json

from .models import College, Branch, Category, Year, Round, Cutoff, PYQ, CutoffUploadLog
from .forms import PDFUploadForm, PYQUploadForm
from .utils.pdf_parser import PDFParser, save_cutoff_data


# ============= Index/Root View =============

def index_view(request):
    """Redirect to dashboard or login"""
    if request.user.is_authenticated:
        return redirect('cutoff:dashboard')
    return redirect('cutoff:login')


# ============= Authentication Views =============

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('cutoff:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cutoff:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('cutoff:login')


# ============= Helper Functions =============

def is_staff_user(user):
    """Check if user is staff"""
    return user.is_staff and user.is_active


# ============= Dashboard View =============

@login_required(login_url='cutoff:login')
def dashboard(request):
    """Dashboard home page"""
    context = {
        'total_colleges': College.objects.count(),
        'total_branches': Branch.objects.count(),
        'total_categories': Category.objects.count(),
        'total_cutoffs': Cutoff.objects.count(),
        'total_pyqs': PYQ.objects.count(),
    }
    return render(request, 'dashboard.html', context)


# ============= PDF Upload & Processing =============

@login_required(login_url='cutoff:login')
@user_passes_test(is_staff_user)
def upload_pdf(request):
    """Admin page for uploading and processing cutoff PDFs"""
    
    context = {
        'years': Year.objects.all().order_by('-year'),
        'rounds': Round.objects.all().order_by('round_number'),
        'recent_uploads': CutoffUploadLog.objects.all()[:10]
    }

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            year_id = request.POST.get('year')
            round_id = request.POST.get('round')

            # Validate year and round
            if not year_id or not round_id:
                context['error'] = 'Please select both Year and Round'
                context['form'] = form
                return render(request, 'upload_pdf.html', context)

            try:
                year_obj = Year.objects.get(id=year_id)
                round_obj = Round.objects.get(id=round_id)
            except (Year.DoesNotExist, Round.DoesNotExist):
                context['error'] = 'Invalid Year or Round selected'
                context['form'] = form
                return render(request, 'upload_pdf.html', context)

            # Parse PDF
            parser = PDFParser(pdf_file)
            success, parse_result = parser.parse()

            if not success:
                log = CutoffUploadLog.objects.create(
                    uploaded_file=pdf_file,
                    status='failed',
                    error_message='; '.join(parse_result['errors']),
                    uploaded_by=request.user,
                    total_rows=0
                )
                context['error'] = f'PDF parsing failed: {"; ".join(parse_result["errors"])}'
                context['form'] = form
                context['recent_uploads'] = CutoffUploadLog.objects.all()[:10]
                return render(request, 'upload_pdf.html', context)

            # Save to database
            extracted_data = parse_result.get('extracted_data', [])
            colleges_found = parse_result.get('colleges_found', [])

            inserted_count, updated_count, errors = save_cutoff_data(
                extracted_data,
                year_obj,
                round_obj
            )

            # Create log entry
            status = 'success' if not errors else 'partial'
            log = CutoffUploadLog.objects.create(
                uploaded_file=pdf_file,
                status=status,
                total_rows=len(extracted_data),
                inserted_count=inserted_count,
                updated_count=updated_count,
                error_message='; '.join(errors) if errors else '',
                uploaded_by=request.user
            )

            context['success'] = True
            colleges_str = ', '.join(colleges_found) if colleges_found else 'Unknown'
            context['message'] = f'''
                PDF processed successfully!
                - Rows extracted: {len(extracted_data)}
                - New cutoffs inserted: {inserted_count}
                - Existing cutoffs updated: {updated_count}
                - Colleges found: {colleges_str}
                - Year: {year_obj.year}
                - Round: {round_obj.name}
            '''
            if errors:
                context['warnings'] = errors
            
            context['form'] = PDFUploadForm()
            context['recent_uploads'] = CutoffUploadLog.objects.all()[:10]
            return render(request, 'upload_pdf.html', context)
        else:
            context['error'] = 'Invalid form submission'
            context['form'] = form
    else:
        context['form'] = PDFUploadForm()

    return render(request, 'upload_pdf.html', context)


# ============= Cutoff Search =============

@login_required(login_url='cutoff:login')
def cutoff_search(request):
    """Cutoff search page with dynamic filters"""
    context = {
        'colleges': College.objects.all().order_by('name'),
        'categories': Category.objects.all().order_by('code'),
        'years': Year.objects.all().order_by('-year'),
        'rounds': Round.objects.all().order_by('round_number'),
    }

    # Handle search
    if request.method == 'POST' or request.GET:
        college_id = request.POST.get('college_id') or request.GET.get('college_id')
        branch_id = request.POST.get('branch_id') or request.GET.get('branch_id')
        category_id = request.POST.get('category_id') or request.GET.get('category_id')
        year_id = request.POST.get('year_id') or request.GET.get('year_id')
        round_id = request.POST.get('round_id') or request.GET.get('round_id')

        # Build filter query
        filters = {}
        if college_id:
            filters['college_id'] = college_id
        if branch_id:
            filters['branch_id'] = branch_id
        if category_id:
            filters['category_id'] = category_id
        if year_id:
            filters['year_id'] = year_id
        if round_id:
            filters['round_id'] = round_id

        if filters:
            results = Cutoff.objects.filter(**filters).select_related(
                'college', 'branch', 'category', 'year', 'round'
            )
            context['results'] = results
            context['selected_filters'] = {
                'college': college_id,
                'branch': branch_id,
                'category': category_id,
                'year': year_id,
                'round': round_id
            }

    return render(request, 'cutoff_search.html', context)


# ============= API Endpoints for Dynamic Dropdowns =============

@login_required(login_url='cutoff:login')
@require_http_methods(["GET"])
def api_get_branches(request):
    """Get branches for a specific college"""
    college_id = request.GET.get('college_id')
    
    if not college_id:
        return JsonResponse({'error': 'college_id required'}, status=400)

    branches = Branch.objects.filter(
        college_id=college_id
    ).values('id', 'name').order_by('name')
    
    return JsonResponse({'branches': list(branches)})


@login_required(login_url='cutoff:login')
@require_http_methods(["GET"])
def api_get_categories(request):
    """Get categories for selected filters"""
    college_id = request.GET.get('college_id')
    branch_id = request.GET.get('branch_id')

    query = Q()
    if college_id:
        query &= Q(cutoffs__college_id=college_id)
    if branch_id:
        query &= Q(cutoffs__branch_id=branch_id)

    categories = Category.objects.filter(query).distinct().values('id', 'code', 'description').order_by('code')
    
    return JsonResponse({'categories': list(categories)})


# ============= PYQ Management =============

@login_required(login_url='cutoff:login')
def pyq_list(request):
    """List and download PYQs"""
    year_id = request.GET.get('year_id')
    subject_query = request.GET.get('subject', '').strip()

    context = {
        'years': Year.objects.all().order_by('-year'),
        'subjects': PYQ.objects.values_list('subject', flat=True).distinct().order_by('subject'),
    }

    # Build query
    pyqs = PYQ.objects.select_related('year')

    if year_id:
        pyqs = pyqs.filter(year_id=year_id)
        context['selected_year'] = year_id

    if subject_query:
        pyqs = pyqs.filter(subject__icontains=subject_query)
        context['search_subject'] = subject_query

    context['pyqs'] = pyqs.order_by('-year', 'subject')

    return render(request, 'pyq_list.html', context)


@login_required(login_url='cutoff:login')
def pyq_download(request, pyq_id):
    """Download PYQ PDF"""
    pyq = get_object_or_404(PYQ, id=pyq_id)
    
    if pyq.pdf_file:
        return FileResponse(
            pyq.pdf_file.open('rb'),
            as_attachment=True,
            filename=f"{pyq.subject}_{pyq.year.year}.pdf"
        )
    
    return redirect('cutoff:pyq_list')


@login_required(login_url='cutoff:login')
@user_passes_test(is_staff_user)
def upload_pyq(request):
    """Admin page to upload PYQs"""
    context = {}

    if request.method == 'POST':
        form = PYQUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            context['success'] = 'PYQ uploaded successfully!'
            context['form'] = PYQUploadForm()
        else:
            context['error'] = 'Error uploading PYQ'
            context['form'] = form
    else:
        context['form'] = PYQUploadForm()

    context['pyqs'] = PYQ.objects.all().order_by('-year', 'subject')
    return render(request, 'upload_pyq.html', context)
