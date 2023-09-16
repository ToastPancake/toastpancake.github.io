const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");
const scanButton = document.getElementById("scan");
var imgLink = "";



inputFile.addEventListener("change", uploadImage);

function uploadImage(){
  imgLink = URL.createObjectURL(inputFile.files[0]);
  imageView.style.backgroundImage = `url(${imgLink})`;
  imageView.textContent = "";
  imageView.style.border = 0;
}

dropArea.addEventListener("dragover", function(e){
  e.preventDefault();
});
dropArea.addEventListener("drop", function(e){
  e.preventDefault();
  inputFile.files = e.dataTransfer.files;
  uploadImage();
});

scanButton.addEventListener("click", function(e){
  document.getElementById("out1").innerHTML = imgLink;
  document.getElementById("out2").innerHTML = blobToImage(imgLink);
  document.location.href = "http://127.0.0.1:5000/scan?value="+blobToImage(imgLink);
  $.ajax(
    {
      type:'POST',
      contentType:'application/json;charset-utf-08',
      dataType:'json',
      url:'http://127.0.0.1:5000/scan?value='+blobToImage(imgLink),
      success:function (data) {
          var reply=data.reply;
          if (reply=="success")
          {
            return;
          }
          else
          {
            alert("some error ocured in session agent")
          }
        }
    }
  );
});

let blobToImage=(binaryUrl) => {
  var canvas = document.createElement("canvas")
  var img=document.createElement('img');
  img.src=binaryUrl;
  var context = canvas.getContext("2d")
  context.drawImage(img, 0, 0);
  return canvas.toDataURL();
}

