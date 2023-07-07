from django.shortcuts import render
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter

def reorder_pdf(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'reorder':
            pdf_file = request.FILES['pdf_file']
            reorder_pages = request.POST.get('reorder_pages')
            keep_pages = request.POST.get('keep_pages')
            
            reordered_pdf = combine_and_reorder_pages(pdf_file, reorder_pages, keep_pages)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reordered.pdf"'
            reordered_pdf.write(response)

            return response

    return render(request, 'pdfreorder/reorder_pdf.html')

def process_page_numbers(page_numbers, total_pages):
    processed_numbers = []
    if page_numbers:
        ranges = page_numbers.split(",")
        for page_range in ranges:
            if '-' in page_range:
                start, end = map(int, page_range.split("-"))
                start = max(start, 1)
                end = min(end, total_pages)
                processed_numbers.extend(range(start, end + 1))
            else:
                number = int(page_range.strip())
                if 1 <= number <= total_pages:
                    processed_numbers.append(number)
    return processed_numbers

def combine_and_reorder_pages(pdf_file, reorder_pages, keep_pages):
    pdf = PdfReader(pdf_file)
    total_pages = len(pdf.pages)

    reorder_pages = process_page_numbers(reorder_pages, total_pages)
    keep_pages = process_page_numbers(keep_pages, total_pages)

    reordered_pdf = PdfWriter()

    for page_number in reorder_pages:
        if page_number <= total_pages:
            page = pdf.pages[page_number - 1]  # Subtract 1 to match 0-based indexing
            reordered_pdf.add_page(page)

    for page_number in keep_pages:
        if page_number <= total_pages:
            page = pdf.pages[page_number - 1]  # Subtract 1 to match 0-based indexing
            reordered_pdf.add_page(page)

    return reordered_pdf