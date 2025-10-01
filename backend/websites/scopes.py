default_scopes = {
}

approvable_scopes = {
    "websites:sites:view": "View my business sites's sites",
    "websites:sites:edit": "Edit my business sites's sites",
    "websites:articles:view": "View my business's articles",
    "websites:articles:edit": "Edit my business's articles",
    # Academic module scopes
    "websites:subjects:view": "View subjects",
    "websites:subjects:edit": "Create/update/delete subjects",
    "websites:subjects:assign": "Assign teacher to subject",
    "websites:classrooms:view": "View classrooms",
    "websites:classrooms:edit": "Create/update/delete classrooms",
    "websites:classrooms:assign": "Assign teacher to classroom",
    "websites:students:view": "View student records",
    "websites:students:edit": "Create/update/delete student records",
    "websites:registrations:view": "View registrations",
    "websites:registrations:create": "Create registrations",
    "websites:registrations:delete": "Delete registrations",
    "websites:tuitions:view": "View tuition records",
    "websites:tuitions:pay": "Mark tuition as paid",
    "websites:grades:view": "View grades",
    "websites:grades:enter": "Enter/update grades",
}

scopes = {}
scopes.update(default_scopes)
scopes.update(approvable_scopes)
