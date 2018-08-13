var cerrar = document.getElementsByClassName("btnCerrar");
var i;

for (i = 0; i < cerrar.length; i++) {
    cerrar[i].onclick = function(){
        var div = this.parentElement;
        div.style.opacity = "0";
        setTimeout(function(){ div.style.display = "none"; }, 300);
    }
}