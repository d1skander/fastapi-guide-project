var editDialog = document.getElementById("editWindow");
var editButton = document.getElementById("editButton");
var cancelButton = document.getElementById("editCancel");


editButton.addEventListener('click', function onOpen(){
    editDialog.showModal();
})

cancelButton.addEventListener('click', function onClose(){
    editDialog.close();
})