function copyEmail(id){
    // Function which copies related email by Entity's id.
    const email = document.getElementById(id).innerText;
    navigator.clipboard.writeText(email);
    alert(email + "copied.");
}
