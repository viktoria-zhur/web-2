// static/lab7/main_db.js
function fillFilmList() {
    fetch('/lab7-db/rest-api/films/')
        .then(r => r.json())
        .then(films => {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';
            
            films.forEach(film => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td style="padding: 10px; border: 1px solid #ddd;">${film.title === film.title_ru ? '' : film.title}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">${film.title_ru}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">${film.year}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">
                        <button onclick="editFilm(${film.id})" style="padding: 5px 10px; background: #FF9800; color: white; border: none; border-radius: 3px; margin-right: 5px;">ред.</button>
                        <button onclick="deleteFilm(${film.id}, '${film.title_ru}')" style="padding: 5px 10px; background: #f44336; color: white; border: none; border-radius: 3px;">уд.</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        });
}

function addFilm() {
    const title = prompt("Оригинальное название:");
    const titleRu = prompt("Русское название:");
    const year = prompt("Год:");
    const description = prompt("Описание:");
    
    const filmData = {
        title: title || titleRu,
        title_ru: titleRu,
        year: parseInt(year),
        description: description
    };
    
    fetch('/lab7-db/rest-api/db/films/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(filmData)
    })
    .then(r => {
        if (r.ok) {
            alert('Фильм добавлен в БД!');
            fillFilmList();
        } else {
            alert('Ошибка! Проверьте данные.');
        }
    });
}

function editFilm(id) {
    const title = prompt("Новое оригинальное название:");
    const titleRu = prompt("Новое русское название:");
    const year = prompt("Новый год:");
    const description = prompt("Новое описание:");
    
    const filmData = {
        title: title || titleRu,
        title_ru: titleRu,
        year: parseInt(year),
        description: description
    };
    
    fetch(`/lab7-db/rest-api/db/films/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(filmData)
    })
    .then(r => {
        if (r.ok) {
            alert('Фильм обновлен в БД!');
            fillFilmList();
        } else {
            alert('Ошибка!');
        }
    });
}

function deleteFilm(id, title) {
    if (confirm(`Удалить "${title}" из БД?`)) {
        fetch(`/lab7-db/rest-api/db/films/${id}`, {
            method: 'DELETE'
        })
        .then(r => {
            if (r.ok) {
                alert('Фильм удален из БД!');
                fillFilmList();
            }
        });
    }
}