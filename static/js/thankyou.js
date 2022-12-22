const queryString= window.location.search;
console.log(queryString)
const urlParams=new URLSearchParams(queryString);
const number=urlParams.get('number');
console.log(number)

text = document.createElement("span");
text.innerHTML = `訂單完成，訂單編號: `+ number;
console.log(text);
frame = document.querySelector(".frame");
frame.appendChild(text);
frame.style.height='200px';

showFooter()
footer = document.querySelector(".footer");
footer_box = document.querySelector(".footer_box");
footer.style.height = "100%";
footer.style.alignItems = "flex-start";
footer_box.style.marginTop = "45px";