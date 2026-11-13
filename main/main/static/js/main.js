var redirectDialog = document.getElementById("redirectDialog");
var authButton = document.getElementById("authButton");
var cancelButton = document.getElementById("editCancel");


authButton.addEventListener('click', function onOpen(){
    redirectDialog.showModal();
})

cancelButton.addEventListener('click', function onClose(){
    redirectDialog.close();
})