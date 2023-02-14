const disc = document.querySelector('.mobDiscus')
const discBtn = document.querySelector('.discusH3')
const newsBtn = document.querySelector('.newsH3')
const newses = document.querySelectorAll('.news')

discBtn.onclick = () =>
{
    for (let news of newses) news.style.display = 'none'
    disc.style.display = 'flex'
    discBtn.classList.add('active')
    newsBtn.classList.remove('active')
}
newsBtn.onclick = () =>
{
    for (let news of newses) news.style.display = 'block'
    disc.style.display = 'none'
    newsBtn.classList.add('active')
    discBtn.classList.remove('active')
}


// popapp
const openModal = (elem) =>
{
    elem.classList.add('show')
    elem.classList.remove('hide')
    document.body.style.overflow = 'hidden'
}
const closeModal = (elem) =>
{
    elem.classList.add('hide');
    elem.classList.remove('show')
    document.body.style.overflow = ''
}

const popapp = document.querySelector('.settingPop')
const modal = document.querySelector('.modal')
const popBtn = document.querySelector('.popBtn')
popBtn.onclick = () => openModal(popapp)

popapp.addEventListener('click', (e) =>
{
    if (!modal.contains(e.target) && popapp.classList.contains('show')) 
    closeModal(popapp)
})
