function pedidoPregunta(){
$.ajax({
url:"/preguntas",
type:"GET",
// data: {"value":valor},
success: function(response){;
  console.log(response)
let listBody=document.getElementById('listaPregunta');
  for(let i=0 ; i<response.length ; i++){
  listBody.innerHTML += `<li">
                    <p>${response[i]["pregunta"]}</p>
                </li>`
  }
},
error: function(error){
alert("Ups algo salió mal :/")
console.log(error);
}, }); 
}

function envioPregunta(){
  var pregunta = document.getElementById("pregunta").value;
  $.ajax({
    url:"/ingresarPreg",
    type:"POST",
    data: {pregunta: pregunta},
    success: function(response){
    if (response=="True"){
      alert("Se añadió la pregunta correctamente")
      console.log(true)
    location.reload()} else{
      alert("Algo falló y no se añadió la pregunta correctamente :(")
      console.log(false)
    }
    },
    error: function(error){
    alert("Ups algo salió mal :/")
    console.log(error);

}, });
}


function modificarPregunta(){
  var pregunta = document.getElementById("listaPregunta");
  var text = pregunta.options[pregunta.selectedIndex].text
  var modif =document.getElementById("respCorrecta").value;
  $.ajax({
    url:"/modificarPreg",
    type:"PUT",
    data: {pregunta: text, 
          respuesta: modif},
    success: function(response){
    if (response[0]=="True"){
      alert(`Se modificó la pregunta correctamente. La nueva respuesta es ${response[1]}`)
    } else{
      alert("Algo falló y no se modificó la pregunta correctamente :(")
    }
    },
    error: function(error){
    alert("Ups algo salio mal :/")
    console.log(error);

}, });
}


function eliminarPregunta(){
  var pregunta = document.getElementById("listaPregunta");
  var text = pregunta.options[pregunta.selectedIndex].text
   $.ajax({
    url:"/eliminarPreg",
    type:"DELETE",
    data: {pregunta: text},
    success: function(response){
    if (response=="True"){
      alert("Se eliminó la pregunta correctamente")
      console.log(true)
      location.reload()
    } else{
      alert("Algo falló y no se eliminó la pregunta correctamente :(")
      console.log(false)
    }
    },
    error: function(error){
    alert("Ups algo salió mal :/")
    console.log(error);

}, });
} 