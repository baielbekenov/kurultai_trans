// fixed header
window.onscroll = function showHeader()
{
    const header = document.querySelector('#headerJs');
    const introH = document.getElementById('introJs').clientHeight;
    if (window.pageYOffset > introH+200) {
        header.classList.add('fixed');
    } else {
        header.classList.remove('fixed');
    }
}

// menu button
const menu = document.querySelector('#menu')
const contentMenu = document.querySelector('.burgerActive')

const clickBurger = (e) =>
{
    e.preventDefault();
    menu.classList.toggle('close')
    contentMenu.classList.toggle('hide')
}
menu.onclick = (e) =>
{
    clickBurger(e)
}
const item = document.querySelectorAll('.menuActionsEb')
for (i of item) i.onclick = (e) => clickBurger(e)

// eye

const firstEye = document.querySelector('.eyeForOld')
const secondEye = document.querySelector('.eyeForNew')
const thirdEye = document.querySelector('.eyeForPass')
const old = document.getElementById('old')
const newP = document.getElementById('new')
const pass = document.getElementById('pass')

function changeType(elem) {
    if (elem.type === "password") {
        elem.type = "text";
    } else {
        elem.type = "password";
    }
}

firstEye.onclick =(e)=>changeType(old)
secondEye.onclick =(e)=>changeType(newP)
thirdEye.onclick = (e) => changeType(pass)

// document.getElementById('resetPassword').onsubmit = (e) =>
// {
//     e.preventDefault()
//     window.location.href = "../success.html"
// }