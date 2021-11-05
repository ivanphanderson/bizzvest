const usernameField=document.querySelector("#usernameField");
const usernameFeedBack=document.querySelector(".invalid_username")
const emailField=document.querySelector("#emailField");
const emailFeedBack=document.querySelector(".invalid_email")


emailField.addEventListener("keyup", (e) => {
    const emailValue = e.target.value;

    emailField.classList.remove('is-invalid');
    emailFeedBack.style.display="none";

    if(emailValue.length > 0) {
        fetch("/start-web/validate-email", {
            body: JSON.stringify({email: emailValue}),
            method: "POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("data", data);
        if(data.email_error) {
            emailField.classList.add('is-invalid');
            emailFeedBack.style.display="block";
            emailFeedBack.innerHTML=`<p>${data.email_error}</p>`
        }
    });
}
});

usernameField.addEventListener("keyup", (e) => {
    const usernameValue = e.target.value;

    usernameField.classList.remove('is-invalid');
    usernameFeedBack.style.display="none";

    if(usernameValue.length > 0) {
        fetch("/start-web/validate-username", {
            body: JSON.stringify({username: usernameValue}),
            method: "POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("data", data);
        if(data.username_error) {
            usernameField.classList.add('is-invalid');
            usernameFeedBack.style.display="block";
            usernameFeedBack.innerHTML=`<p>${data.username_error}</p>`
        }
    });
}
});