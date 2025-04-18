function myFunction(button) {
    const content = button.nextElementSibling;
    const isOpen = content.classList.contains("dropdown-open");

    // Fecha todos os dropdowns
    document.querySelectorAll('.dropdown-content').forEach(drop => {
        drop.classList.remove("dropdown-open");
        drop.classList.add("dropdown-close");
    });

    // Se não estava aberto, abre com transição lenta
    if (!isOpen) {
        content.classList.remove("dropdown-close");
        content.classList.add("dropdown-open");
    }
}
