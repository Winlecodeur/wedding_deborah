var menu = document.querySelector('.nav-menu')
var small_menu = document.querySelector('.menu-toggle')
small_menu.onclick = function (){
    small_menu.classList.toggle('active')
    menu.classList.toggle('responsive')
}