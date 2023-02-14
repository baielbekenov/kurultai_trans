const form = document.querySelector('.voteForm')
const rezalts = document.querySelector('.rezalts')
// form.onsubmit = (e) => {
//     e.preventDefault()
//     e.target.style.display = 'none';
//     rezalts.classList.toggle('rezaltsHide')
// }

const down = document.querySelector('.chatDown')
window.onload = () =>
{
    console.log('niz')
    scrollTo(down)
}
window.scrollTo(0, document.body.scrollHeight)