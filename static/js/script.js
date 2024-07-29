document.addEventListener("DOMContentLoaded", function () {
  var test = document.getElementById("test");

  var text =
    "Welcome to Stellar Classification, your interactive gateway to exploring the fascinating world of astronomical data. This web application is designed to provide comprehensive insights into the Sloan Digital Sky Survey (SDSS) dataset, making it an invaluable tool for students, new researchers, and astronomy enthusiasts alike.";
  var result = "";

  for (let i = 0; i < text.length; i++) {
    setTimeout(function () {
      result += text[i];
      test.innerHTML = result;
    }, 40 * i);
  }
});
