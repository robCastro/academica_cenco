var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
      this.getElementsByClassName('accion')[0].innerHTML ='[Expandir &#9660;]';
    } else {
      content.style.display = "block";
      this.getElementsByClassName('accion')[0].innerHTML = '[Contraer &#9658;]';
    }
  });
}