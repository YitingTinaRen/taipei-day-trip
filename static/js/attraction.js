// Extract attraction id from current url
current_url=location.href;
attraction_id=current_url.substr(current_url.lastIndexOf('/')+1)
var images;
let slideIndex = 1;

fetch("/api/user/auth").then((response)=>{return response.json()}).then(function(auth){
    if(!auth){
        document.querySelectorAll(".RightItem2")[0].style.display='block';
        document.querySelectorAll(".RightItem2")[1].style.display='none';
    }else{
        document.querySelectorAll(".RightItem2")[0].style.display='none';
        document.querySelectorAll(".RightItem2")[1].style.display='block';
    }
})

// Next/previous controls
function plusSlides(n) {
showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
showSlides(slideIndex = n);
}

function showSlides(n) {
let i;
let slides = document.getElementsByClassName("mySlides");
let dots = document.getElementsByClassName("dot");
if (n > slides.length) {slideIndex = 1} 
if (n < 1) {slideIndex = slides.length}
for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none"; 
}
for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
}
slides[slideIndex-1].style.display = "block"; 
dots[slideIndex-1].className += " active";
}

function putInfo(data){
    let container=document.querySelector(".info");
    let description=document.createElement('div');
    let address_title=document.createElement('div');
    let address=document.createElement('div');
    let transport_title=document.createElement('div');
    let transport=document.createElement('div');

    // Set Attributes
    description.setAttribute("class","info_content");
    address.setAttribute("class","info_content");
    transport.setAttribute("class","info_content");
    address_title.setAttribute("class","info_title");
    transport_title.setAttribute("class","info_title");

    description.appendChild(document.createTextNode(data.data.description));
    address.appendChild(document.createTextNode(data.data.address));
    transport.appendChild(document.createTextNode(data.data.transport));
    address_title.appendChild(document.createTextNode("景點地址:"));
    transport_title.appendChild(document.createTextNode("交通方式:"));

    container.appendChild(description);
    container.appendChild(address_title);
    container.appendChild(address);
    container.appendChild(address);
    container.appendChild(transport_title);
    container.appendChild(transport);

}

function putProfile(data){
    let container=document.querySelector(".profile");
    let name=document.createElement("div");
    let cat_mrt=document.createElement("div");

    name.setAttribute("class","name");
    cat_mrt.setAttribute("class","profile_text");

    name.appendChild(document.createTextNode(data.data.name));
    cat_mrt.appendChild(document.createTextNode(data.data.category+" at "+data.data.mrt));

    container.appendChild(name);
    container.appendChild(cat_mrt);
    insertForm(container);

}

function insertForm(profile){
    let container=document.createElement("form");
    container.action="#";
    container.method="post";

    let sub_container1=document.createElement("div");
    let sub_container2=document.createElement("div");
    let sub_container3=document.createElement("div");
    

    let title1=document.createElement("div");
    let title2=document.createElement("div");
    let title3=document.createElement("div");
    let title4=document.createElement("div");
    let text1=document.createElement("div");
    let text2=document.createElement("div");
    let text3=document.createElement("div");
    let text4=document.createElement("div");
    let btn=document.createElement("button");
    let input1=document.createElement("input");
    let input2=document.createElement("input");
    let input3=document.createElement("input");
    input1.style.marginLeft="5px";


    title1.setAttribute("class","form_title");
    title2.setAttribute("class","form_title");
    title3.setAttribute("class","form_title");
    title4.setAttribute("class","form_title");
    text1.setAttribute("class","profile_text");
    text2.setAttribute("class","profile_text");
    text3.setAttribute("class","profile_text");
    text4.setAttribute("class","profile_text");
    btn.setAttribute("class","btn");
    sub_container1.setAttribute("class","container");
    sub_container2.setAttribute("class","container");
    sub_container3.setAttribute("class","container");

    title1.style.marginBottom="15px";
    input1.type="date";
    input1.name="date";
    input1.placeholder="yyyy/mm/dd";
    // input1.onfocus="(this.placeholder='')";
    // input1.onchange="this.className=(this.value!=''?'has-value':'')";
    input1.required=true;
    input1.style.width="193px";
    input1.style.height="35px";
    input1.style.padding="5px 10px";
    input2.type="radio";
    input3.type="radio";
    input2.name="time";
    input2.value="上半天";
    input3.name="time";
    input3.value="下半天";
    input2.style.width="22px";
    input2.style.height="22px";
    input3.style.width="22px";
    input3.style.height="22px";
    input2.style.marginLeft="10px";
    input3.style.marginLeft="10px";
    text2.style.marginLeft="5px";

    title1.appendChild(document.createTextNode("訂購導覽行程"));
    title2.appendChild(document.createTextNode("選擇日期:"));
    title3.appendChild(document.createTextNode("選擇時間:"));
    title4.appendChild(document.createTextNode("導覽費用:"));
    text1.appendChild(document.createTextNode("以此景點為中心的一日行程，帶您探索城市角落故事"));
    text2.appendChild(document.createTextNode("新台幣2000元"));
    text3.appendChild(document.createTextNode("上半天"));
    text4.appendChild(document.createTextNode("下半天"));
    btn.appendChild(document.createTextNode("開始預約行程"));

    container.appendChild(title1);
    container.appendChild(text1);
    sub_container1.appendChild(title2);
    sub_container1.appendChild(input1);
    container.appendChild(sub_container1);
    sub_container2.appendChild(title3);
    sub_container2.appendChild(input2);
    sub_container2.appendChild(text3);
    sub_container2.appendChild(input3);
    sub_container2.appendChild(text4);
    container.appendChild(sub_container2);
    sub_container3.appendChild(title4);
    sub_container3.appendChild(text2);
    container.appendChild(sub_container3);
    container.appendChild(btn);
    profile.appendChild(container);
}

function drawSlides(images){
    imageNum=images.length;
    let container=document.querySelector(".slideshow-container");
    for(let i=0; i<imageNum;i++){

        let myslides=document.createElement('div');
        let img=document.createElement("img")
        
        myslides.setAttribute("class","mySlides fade");

        img.src=images[i];
        img.style.width= "100%" ;
        img.style.borderRadius="5px";
        img.style.height="406px";
        img.style.objectPosition="center center";
        img.style.objectFit="cover";

        myslides.appendChild(img);
        container.appendChild(myslides);
        
    }

    let dot_container=document.createElement("div");
    dot_container.setAttribute("class","dot_container");
    dot_container.style.textAlign="center";
    dot_container.style.left=540/2-(imageNum*12);
    for(let i=0; i<imageNum;i++){
        let dot=document.createElement("span");
        dot.setAttribute("class", "dot");
        dot.onclick="currentSlide("+String(i+1)+")";
        dot_container.appendChild(dot);
    }
    container.appendChild(dot_container);

    let prev=document.createElement("a");
    let next=document.createElement("a");
    let img_prev=document.createElement("img");
    let img_next=document.createElement("img");

    prev.setAttribute("class","prev");
    next.setAttribute("class","next");

    prev.setAttribute("onclick","plusSlides(-1);");
    next.setAttribute("onclick","plusSlides(1);");
    img_prev.src="/static/imgs/btn_leftArrow.png";
    img_next.src="/static/imgs/btn_rightArrow.png";

    prev.appendChild(img_prev);
    next.appendChild(img_next);
    container.appendChild(prev);
    container.appendChild(next);
}



// Request attracton info from api
// url="http://52.37.59.29:3000/api/attraction/"+attraction_id;
// url="http://127.0.0.1:3000/api/attraction/"+attraction_id;
fetch("/api/attraction/"+attraction_id).then(function(res){
    return res.json();
}).then(function(data){
    // console.log(data.data);
    putInfo(data);
    
    images=data.data.images;
    drawSlides(images);
    showSlides(slideIndex);
    putProfile(data);

    // make footer to be at the bottom of the content
    if((document.querySelector(".MainBackground").scrollHeight+document.querySelector(".MainBackground").offsetTop+104)<=window.innerHeight){
        // console.log("in if")
        let distance2bottom=window.innerHeight-document.querySelector(".topnavground").scrollHeight-document.querySelector(".MainBackground").scrollHeight-104;
        document.querySelector(".mainframe").style.paddingBottom=distance2bottom.toString()+"px";
    }
    footer=document.querySelector(".footer");
    footer.style.visibility="visible";
});

// Get the Login/signup form
var LoginForm = document.getElementById('id01');

// When the user clicks anywhere outside of the LoginForm, close it
window.onclick = function(event) {
    if (event.target == LoginForm) {
        LoginForm.style.display = "none";
    }
}


function register(){
    uname=document.getElementsByName("uname")[0].value;
    email=document.getElementsByName("email")[1].value;
    psw=document.getElementsByName("psw")[1].value;
    data={"name":uname, "email":email, "password":psw};
    console.log(data);

    fetch("/api/user",
        {
            method:"POST",
            headers:{
                'Content-Type':'application/json',
            },
            body:JSON.stringify(data),
        }
    ).then(function(res){
        return res.json();
    }).then(function(result){
        console.log(result);
        if(result['ok']){
            success_text="註冊成功!";
            if(document.querySelectorAll("#id02 .LoginForm-content .form_text").length==1){
                referenceNode=document.querySelector("#id02 .LoginForm-content .form_text");
                parentNode=document.querySelector("#id02 .LoginForm-content .container");
                newNode=document.createElement("div");
                newNode.setAttribute("class","form_text");
                newNode.appendChild(document.createTextNode(success_text));
                parentNode.insertBefore(newNode,referenceNode);
            }else{
                document.querySelectorAll("#id02 .LoginForm-content .form_text")[0].textContent=success_text;
            }
        }
        if(result['error']){
            if(document.querySelectorAll("#id02 .LoginForm-content .form_text").length==1){
                referenceNode=document.querySelector("#id02 .LoginForm-content .form_text");
                parentNode=document.querySelector("#id02 .LoginForm-content .container");
                newNode=document.createElement("div");
                newNode.setAttribute("class","form_text");
                newNode.appendChild(document.createTextNode(result["message"]));
                parentNode.insertBefore(newNode,referenceNode);
            }else{
                document.querySelectorAll("#id02 .LoginForm-content .form_text")[0].textContent=result["message"];
            }
        }
    });
}

function login(){
    email=document.getElementsByName("email")[0].value;
    psw=document.getElementsByName("psw")[0].value;
    data={"email":email, "password":psw};

    fetch("/api/user/auth",
        {
            method:"PUT",
            headers:{
                'Content-Type':'application/json',
            },
            body:JSON.stringify(data),
        }
    ).then(function(res){
        return res.json();
    }).then(function(result){
        console.log(result);
        if(result['ok']){
            window.location.reload();
        }
        else if(result['error']){
            console.log(result);
            if(document.querySelectorAll("#id01 .LoginForm-content .form_text").length ==1){
                referenceNode=document.querySelector("#id01 .LoginForm-content .form_text");
                parentNode=document.querySelector("#id01 .LoginForm-content .container");
                newNode=document.createElement("div");
                newNode.setAttribute("class","form_text");
                newNode.appendChild(document.createTextNode(result["message"]));
                parentNode.insertBefore(newNode,referenceNode);
            }else{
                document.querySelectorAll("#id01 .LoginForm-content .form_text")[0].textContent=result["message"];
            }
        }
    });
}

function logout(){
    fetch("/api/user/auth",
        {
            method:"DELETE",
        }
    ).then(function(res){
        return res.json();
    }).then(function(result){
        console.log(result);
        if(result){
            window.location.reload();
        }
    });
}