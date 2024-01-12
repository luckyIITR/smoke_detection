// script.js
document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const offset = 20;
            const scrollDuration = 1000; // Set your desired duration in milliseconds

            document.getElementById(targetId).scrollIntoView({
                behavior: 'smooth',
                block: 'start',
                inline: 'nearest',
                offsetTop: offset * -1,
                scrollDuration: scrollDuration,
            });
        });
    });
});
