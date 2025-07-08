document.addEventListener('DOMContentLoaded', function () {
    // Open Add Modal
    document.getElementById("addApplication")?.addEventListener("click", function() {
        $('#addApplicationModal').modal('show');
    });

    // Add Application
    document.getElementById("addApplicationButton")?.addEventListener("click", function () {
        const company = document.getElementById("company").value.trim();
        const role = document.getElementById("role").value.trim();
        const category = document.getElementById("category").value.trim();
        const deadline = document.getElementById("deadline").value;
        const status = document.getElementById("status").value;
        const link = document.getElementById("link").value.trim();

        // Simple validation
        if (!company || !role || !category || !deadline || !status) {
            alert("Please fill in all required fields.");
            return;
        }

        // Disable button + show spinner
        const button = document.getElementById("addApplicationButton");
        button.disabled = true;
        button.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Adding...`;

        $.post('/add', {
            company,
            role,
            category,
            deadline,
            status,
            link
        }).done(function () {
            $('#addApplicationModal').modal('hide');
            location.reload();
        }).fail(function (xhr) {
            alert("Error: " + (xhr.responseJSON?.error || "Could not add application."));
        }).always(function () {
            button.disabled = false;
            button.innerHTML = "Add application";
        });
    });
    
    // Delete Application
    window.deleteApplication = function (element) {
        var id = element.getAttribute("value");
        $.post('/delete', { id }).done(function () {
            location.reload();
        }).fail(function () {
            alert("Failed to delete.");
        });
    };

    // Edit button
    window.openEditModal = function (element) {
        const tr = element.closest('tr');
        const id = element.getAttribute('data-id');

        document.getElementById("edit-id").value = id;
        document.getElementById("edit-company").value = tr.children[0].innerText;
        document.getElementById("edit-role").value = tr.children[1].innerText;
        document.getElementById("edit-category").value = tr.children[2].innerText;
        document.getElementById("edit-deadline").value = tr.children[3].childNodes[0].textContent.trim();
        document.getElementById("edit-status").value = tr.children[4].innerText.trim();
        document.getElementById("edit-link").value = tr.children[5].innerText.trim();

        $('#editApplicationModal').modal('show');
    };

    document.getElementById("editApplicationButton")?.addEventListener("click", function () {
        const id = document.getElementById("edit-id").value;
        const data = {
            id: id,
            company: document.getElementById("edit-company").value,
            role: document.getElementById("edit-role").value,
            category: document.getElementById("edit-category").value,
            deadline: document.getElementById("edit-deadline").value,
            status: document.getElementById("edit-status").value,
            link: document.getElementById("edit-link").value
        };

        $.post('/edit', data).done(function () {
            $('#editApplicationModal').modal('hide');
            location.reload();
        });
    });
    
    document.querySelectorAll('.badge-status').forEach(select => {
        const option = select.options[select.selectedIndex];
        const badgeClass = option.getAttribute('data-class');
        select.className += ` ${badgeClass}`;
    });

    document.getElementById("search").addEventListener("input", function () {
        const term = this.value.toLowerCase();
        document.querySelectorAll("#applicationTabel tbody tr").forEach(row => {
            row.style.display = row.innerText.toLowerCase().includes(term) ? "" : "none";
        });
    });
});






function changeStatus(select) {
    const id = select.getAttribute("data-id");
    const newStatus = select.value;
    const selectedOption = select.options[select.selectedIndex];
    const badgeClass = selectedOption.getAttribute("data-class");

    // Update style immediately
    select.className = "form-select form-select-sm badge-status " + badgeClass;

    $.post('/change-status', { id, status: newStatus })
        .done(() => console.log("Status updated"))
        .fail(() => alert("Failed to update status"));
}


$(document).ready(function () {
    const $input = $('#company');
    const $suggestions = $('#companySuggestions');

    $input.on('input', function () {
        const query = $input.val().trim();
        if (query.length < 2) return $suggestions.empty();

        $.get('/company/search', { q: query }, function (data) {
            $suggestions.empty();
            data.forEach(company => {
                const item = $('<a href="#" class="list-group-item list-group-item-action"></a>').text(company.name);
                item.on('click', function (e) {
                    e.preventDefault();
                    $input.val(company.name);
                    $suggestions.empty();
                });
                $suggestions.append(item);
            });
        });
    });

    $(document).on('click', function (e) {
        if (!$(e.target).closest('#company').length) {
            $suggestions.empty();
        }
    });
});


