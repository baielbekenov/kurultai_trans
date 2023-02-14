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
const profile = document.querySelector('.forProfile')
const mainProfile = document.querySelector('.profile') 
const clickBurger = (e) =>
{
    menu.classList.toggle('close')
    contentMenu.classList.toggle('hide')
}
menu.onclick = (e) =>
{
    clickBurger(e)
}
const item = document.querySelectorAll('.menuActionsEb')
for (i of item) i.onclick = (e) => clickBurger(e)


