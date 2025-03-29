window.addEventListener('scroll', function() {
    const containers = [
        document.getElementById('welcome'),
        document.getElementById('img-1'),
        document.getElementById('img-2'),
        document.getElementById('form'),
        document.getElementById('msg')
    ];
    const windowHeight = window.innerHeight
    const scrollPosition = window.scrollY
    containers.forEach(container => {
        const divs = container.querySelectorAll('.item')
        divs.forEach(div => {
            const divTop = div.getBoundingClientRect().top + scrollPosition
            const divBottom = divTop + div.offsetHeight
            const start = scrollPosition
            const end = scrollPosition + windowHeight
            if (divBottom>start && divTop < end){
                div.classList.add('visible')
            } else {
                div.classList.remove('visible')
            }
        })
    })
})


// Sélectionner le pop-up
const popup = document.getElementById('popup');

// Afficher le pop-up
function showPopup() {
  popup.classList.add('show'); // Ajouter la classe "show"
  setTimeout(() => {
    popup.classList.remove('show'); // Masquer après 3 secondes
  }, 2000); // 3000 ms = 3 secondes
}

// Appeler la fonction pour afficher le pop-up
showPopup();