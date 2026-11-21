var editDialog = document.getElementById("editWindow");
var editButton = document.getElementById("editButton");
var cancelButton = document.getElementById("editCancel");


editButton.addEventListener('click', function onOpen(){
    editDialog.showModal();
})

cancelButton.addEventListener('click', function onClose(){
    editDialog.close();
})

//Написал ИИ
document.addEventListener("DOMContentLoaded", () => {
    const detailsEmail = document.getElementById("detailsEmail");
    if (!detailsEmail) return; // Защита на случай, если скрипт загружен на другой странице

    const emailForm = detailsEmail.querySelector("form");
    const dialog = document.getElementById("codeEmailWindow");
    const codeForm = dialog.querySelector("form");
    const cancelBtn = document.getElementById("editCodeCancel");

    // 1. Отправка нового email -> открытие модального окна
    emailForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const response = await fetch(emailForm.action, {
            method: "POST",
            body: new FormData(emailForm),
        });
        const data = await response.json();

        if (response.ok && data.status === "code_sent") {
            dialog.showModal(); 
        } else {
            alert(data.error || "Ошибка при отправке кода");
        }
    });

    // 2. Отправка кода из модального окна -> обновление почты
    codeForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const response = await fetch(codeForm.action, {
            method: "POST",
            body: new FormData(codeForm),
        });
        const data = await response.json();

        if (response.ok && data.status === "ok") {
            dialog.close();
            alert("Почта успешно обновлена!");
            window.location.reload();
        } else {
            alert(data.error || "Неверный код");
        }
    });

    // 3. Закрытие окна по кнопке "Отменить"
    cancelBtn.addEventListener("click", () => {
        codeForm.reset();
        dialog.close();
    });
});
