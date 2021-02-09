const textArea = document.getElementById("textInput");
const imageView = document.getElementById("imageView");

function click() {
    let text = textArea.value;
    fetch('/analyze', {
        // Specify the method
        method: 'POST',
        // A JSON payload
        // redirect: 'follow',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'text': text})
    }).then(function (response) { 
         // At this point, Flask has printed our JSON
        return response.blob();
    }).then(function (text) {
        // Should be 'OK' if everything was successful
        // console.log(text);
        var encodedResponse = btoa(text);
        imageView.src = URL.createObjectURL(text);
    });
}
const button2 = document.getElementById("submitBtn");
button2.addEventListener("click", click, false);