from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import AddressForm
from .utils import compare_addresses
from .utils import distance as levenshtein_distance
from .utils import editops as levenshtein_editops


@require_POST
def field_update(request: HttpRequest):
    # Get the field name from the custom header
    field_name = request.headers.get("Hx-Trigger-Name").split("-")[-1]

    print(f"Field updated: {field_name}")
    print(f"Field updated: {request.POST=}")

    """Update structured fields from raw text"""
    # Determine which form was submitted
    prefix = "form1" if any(key.startswith("form1-") for key in request.POST) else "form2"
    form = AddressForm(request.POST, prefix=prefix)
    form.update_field(field_name)

    # Render the updated form
    return render(
        request,
        "address_form.html",
        {
            "form": form,
            "form_id": prefix,
        },
    )


def index(request: HttpRequest) -> HttpResponse:
    # Only process POST requests if not from HTMX
    if request.method == "POST" and not request.htmx:
        # Handle form submissions for the full page
        form1 = AddressForm(request.POST, prefix="form1")
        form2 = AddressForm(request.POST, prefix="form2")
    else:
        # Initial load or GET request
        form1 = AddressForm(prefix="form1")
        form2 = AddressForm(prefix="form2")

    # Compare addresses
    if form1.is_valid() and form2.is_valid():
        addr1 = form1.address
        addr2 = form2.address
        field_comparison = compare_addresses(addr1, addr2)

        # Get example for Levenshtein explanation
        example_text1 = addr1.raw_text or "kitten"
        example_text2 = addr2.raw_text or "sitting"
        distance, operations = (
            levenshtein_distance(example_text1, example_text2),
            levenshtein_editops(example_text1, example_text2),
        )

        return render(
            request,
            "comparison.html",
            {
                "comparison": {
                    field: field_comparison.lev_similarity for field, field_comparison in field_comparison.items()
                },
                "example_text1": example_text1,
                "example_text2": example_text2,
                "distance": distance,
                "operations": operations,
            },
        )

    # Initial render or clear form
    if request.method == "POST" and "clear_form1" in request.POST:
        form1 = AddressForm(prefix="form1")

    if request.method == "POST" and "clear_form2" in request.POST:
        form2 = AddressForm(prefix="form2")

    # Default example for Levenshtein explanation
    example_text1 = "kitten"
    example_text2 = "sitting"
    distance, operations = (
        levenshtein_distance(example_text1, example_text2),
        levenshtein_editops(example_text1, example_text2),
    )

    addr1 = form1.address
    addr2 = form2.address
    field_comparison = compare_addresses(addr1, addr2)

    return render(
        request,
        "index.html",
        {
            "form1": form1,
            "form2": form2,
            "form_compare": form1,
            "example_text1": example_text1,
            "example_text2": example_text2,
            "distance": distance,
            "operations": operations,
        },
    )


def clear_form(request: HttpRequest, form_id: str) -> HttpResponse:
    """Clear a specific form"""
    if form_id == "form1":
        form = AddressForm(prefix="form1")
    else:
        form = AddressForm(prefix="form2")

    return render(
        request,
        "address_form.html",
        {
            "form": form,
            "form_id": form_id,
        },
    )
