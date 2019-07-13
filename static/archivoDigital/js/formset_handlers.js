if(document.querySelector('#id_changePass').value="change")document.querySelector('#id_changePass').value="";
document.querySelector('.field-changePass').style.visibility = 'hidden';
document.querySelector('#id_changePass').style.visibility = 'hidden';
document.querySelector('.field-password_admin').style.visibility = 'hidden';

indicador = document.querySelector('#one');

indicador.addEventListener("click",function(){
  (indicador['checked'])?((confirm("¿Esta seguro de querer cambiar la contraseña?"))?document.querySelector('#id_changePass').value="change":
    document.getElementById("one").checked=false):document.querySelector('#id_changePass').value="";
})
